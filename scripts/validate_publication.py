#!/usr/bin/env python3
"""Audit privacy, publication boundaries, relative links, assets, and manifest paths."""

from __future__ import annotations

import csv
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


def style_language_scan(files: list[Path]) -> list[str]:
    banned = re.compile(
        r"이 저장소의 핵심|이번 재구성본|전체 흐름을 이해|유기적으로 연결|"
        r"직관적으로|체계적으로|성공적으로|효과적으로|실무 수준|"
        r"포트폴리오의 강점|정체성이 일관되게|단순한 과제가 아니라|"
        r"의미 있는 결과|향후 확장 가능성|evidence-first portfolio|"
        r"recruiter snapshot",
        re.I,
    )
    excluded = ROOT / "docs" / "audit" / "ai_style_language_audit.md"
    issues: list[str] = []
    for path in files:
        if path == excluded or path.suffix.lower() not in {".md", ".html"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for match in banned.finditer(content):
            line = content.count("\n", 0, match.start()) + 1
            issues.append(
                f"{path.relative_to(ROOT)}:{line}: promotional/meta language: {match.group(0)}"
            )
    return issues


def audit_resolution_scan() -> list[str]:
    audit = ROOT / "docs" / "audit" / "text_as_image_violations.csv"
    if not audit.is_file():
        return ["required output missing: docs/audit/text_as_image_violations.csv"]
    allowed = {"RESOLVED", "ALLOWED_PROGRAM_UI", "ALLOWED_WORKBOOK_EVIDENCE"}
    issues: list[str] = []
    with audit.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            status = row.get("replacement_status", "")
            if status not in allowed:
                issues.append(
                    "text-as-image unresolved: "
                    f"{row.get('platform')}/{row.get('page')}/{row.get('section')}={status}"
                )
    return issues


def figure_manifest_scan() -> list[str]:
    manifest = ROOT / "docs" / "figure-manifest" / "figure_manifest.csv"
    if not manifest.is_file():
        return ["required output missing: docs/figure-manifest/figure_manifest.csv"]
    required_fields = {
        "figure_id",
        "project",
        "figure_title",
        "figure_type",
        "source_files",
        "source_pages",
        "original_screenshot_count",
        "rerun_screenshot_count",
        "generated_element_count",
        "contains_body_text",
        "crop_status",
        "public_redaction",
        "github_readme_location",
        "github_pages_location",
        "notion_location",
        "svg_path",
        "png_path",
        "validation_status",
        "notes",
    }
    required_projects = {
        "Controller Logic",
        "Electrical Machines",
        "Power Systems",
        "Motor Control",
        "RF/Microwave",
        "Sensor Applications",
    }
    issues: list[str] = []
    projects: set[str] = set()
    with manifest.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        for field in sorted(required_fields - fields):
            issues.append(f"figure manifest missing field: {field}")
        for row_number, row in enumerate(reader, start=2):
            figure_id = row.get("figure_id", f"row {row_number}")
            projects.add(row.get("project", ""))
            if row.get("contains_body_text", "").lower() != "false":
                issues.append(f"{figure_id}: contains_body_text must be false")
            if row.get("validation_status") != "PASS":
                issues.append(f"{figure_id}: validation_status must be PASS")
            for path_field in ("svg_path", "png_path"):
                asset = row.get(path_field, "").strip()
                if asset and not (ROOT / asset).is_file():
                    issues.append(f"{figure_id}: missing {path_field} {asset}")
    for project in sorted(required_projects - projects):
        issues.append(f"figure manifest missing project: {project}")
    return issues


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
        "docs/audit/ai_style_language_audit.md",
        "docs/audit/text_as_image_violations.csv",
        "docs/figure-manifest/figure_manifest.csv",
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
    top_content = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in (
        "## 증거 상태",
        "## 과목별 산출물",
        "## 재현과 검증",
        "## 검증 매트릭스",
        "## 공개 범위와 기여도",
    ):
        if heading not in top_content:
            issues.append(f"README.md missing required section: {heading}")
    detail_paths = re.findall(
        r"^\s+path:\s+(.+?)\s*$",
        (ROOT / "portfolio-manifest.yaml").read_text(encoding="utf-8"),
        flags=re.M,
    )
    for item in detail_paths:
        readme = ROOT / item / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            headings = re.findall(r"^##\s+.+$", content, flags=re.M)
            if len(headings) < 5:
                issues.append(f"{readme.relative_to(ROOT)}: fewer than five technical sections")
            if not re.search(r"!\[[^\]]+\]\([^)]+\)", content):
                issues.append(f"{readme.relative_to(ROOT)}: no technical figure")
            if "|---" not in content:
                issues.append(f"{readme.relative_to(ROOT)}: no native Markdown table")
            if not re.search(r"\d", content):
                issues.append(f"{readme.relative_to(ROOT)}: no quantitative value")
            if not any(term in content for term in ("범위", "한계", "경계")):
                issues.append(f"{readme.relative_to(ROOT)}: no verification boundary")
    return issues


def main() -> None:
    files = text_files()
    issues = (
        privacy_scan(files)
        + withheld_file_scan()
        + style_language_scan(files)
        + audit_resolution_scan()
        + figure_manifest_scan()
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
