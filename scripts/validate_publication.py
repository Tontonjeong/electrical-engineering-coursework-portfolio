#!/usr/bin/env python3
"""Audit privacy, publication boundaries, relative links, assets, and manifest paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".md",
    ".html",
    ".css",
    ".js",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".py",
    ".cpp",
    ".vhd",
    ".txt",
}
WITHHELD_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".pwb",
    ".aux",
    ".sim",
    ".slx",
    ".mdl",
    ".xlsx",
    ".xls",
}
SKIP_PARTS = {".git", "__pycache__", "build", "dist"}


def text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in SKIP_PARTS for part in path.parts)
    ]


def privacy_scan(files: list[Path]) -> list[str]:
    # Patterns are assembled so the scanner source does not contain private literals.
    student_identifier = "3221" + "1479"
    windows_home = "C:" + "\\\\" + "Users" + "\\\\"
    notion_workspace = "app" + "." + "notion" + "." + "com"
    patterns = {
        "student identifier": re.compile(re.escape(student_identifier), re.I),
        "Windows home path": re.compile(re.escape(windows_home), re.I),
        "macOS/Linux home path": re.compile(r"/(?:Users|home)/[^/\s]+/", re.I),
        "private Notion workspace URL": re.compile(re.escape(notion_workspace), re.I),
    }
    issues: list[str] = []
    for path in files:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in patterns.items():
            if pattern.search(content):
                issues.append(f"{path.relative_to(ROOT)}: {label}")
    return issues


def withheld_file_scan() -> list[str]:
    return [
        f"{path.relative_to(ROOT)}: withheld extension"
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in WITHHELD_SUFFIXES
        and not any(part in SKIP_PARTS for part in path.parts)
    ]


def relative_link_scan(files: list[Path]) -> list[str]:
    issues: list[str] = []
    markdown_link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    html_link = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.I)
    for path in files:
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for raw in markdown_link.findall(content) + html_link.findall(content):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlparse(target)
            if (
                not target
                or target.startswith(("#", "mailto:", "data:"))
                or parsed.scheme in {"http", "https"}
            ):
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.exists():
                issues.append(
                    f"{path.relative_to(ROOT)}: missing relative target {target}"
                )
    return issues


def manifest_scan() -> list[str]:
    manifest = ROOT / "portfolio-manifest.yaml"
    content = manifest.read_text(encoding="utf-8")
    paths = re.findall(r"^\s+path:\s+(.+?)\s*$", content, flags=re.M)
    return [f"manifest missing path: {item}" for item in paths if not (ROOT / item).is_dir()]


def required_output_scan() -> list[str]:
    required = [
        "README.md",
        "README.en.md",
        "docs/index.html",
        "docs/en/index.html",
        "docs/assets/asset_manifest.yaml",
        "docs/assets/hero/coursework_portfolio_hero.webp",
        "docs/tools/transformer-case-calculator/index.html",
        "docs/tools/motor-pi-calculator/index.html",
        "docs/tools/transmission-line-calculator/index.html",
    ]
    course_ids = [
        "controller-logic",
        "electrical-machines",
        "power-systems",
        "motor-control",
        "rf-microwave",
        "sensor-applications",
    ]
    for course_id in course_ids:
        required.extend(
            [
                f"docs/courses/{course_id}/index.html",
                f"docs/en/courses/{course_id}/index.html",
            ]
        )
    issues = [f"required output missing: {item}" for item in required if not (ROOT / item).is_file()]
    top_lines = len((ROOT / "README.md").read_text(encoding="utf-8").splitlines())
    if not 250 <= top_lines <= 450:
        issues.append(f"README.md line target missed: {top_lines} (expected 250–450)")
    detail_paths = re.findall(
        r"^\s+path:\s+(.+?)\s*$",
        (ROOT / "portfolio-manifest.yaml").read_text(encoding="utf-8"),
        flags=re.M,
    )
    for item in detail_paths:
        readme = ROOT / item / "README.md"
        if readme.exists():
            count = len(readme.read_text(encoding="utf-8").splitlines())
            if not 120 <= count <= 300:
                issues.append(
                    f"{readme.relative_to(ROOT)} line target missed: {count} (expected 120–300)"
                )
    return issues


def main() -> None:
    files = text_files()
    issues = (
        privacy_scan(files)
        + withheld_file_scan()
        + relative_link_scan(files)
        + manifest_scan()
        + required_output_scan()
    )
    if issues:
        print("PUBLICATION VALIDATION FAILED")
        for issue in issues:
            print(f"- {issue}")
        sys.exit(1)
    print(
        "PASS publication validation: "
        f"{len(files)} text files, privacy, extensions, links, assets, manifest"
    )


if __name__ == "__main__":
    main()
