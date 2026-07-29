#!/usr/bin/env python3
"""Validate public image files, references, captions, and inventory linkage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "audit"
TEXT_SUFFIXES = {".md", ".html"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".svg"}


def main() -> None:
    issues: list[str] = []
    referenced: set[Path] = set()
    markdown = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    html = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
    alt_html = re.compile(r"\balt=[\"']([^\"']*)[\"']", re.I)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for alt, target in markdown.findall(text):
            if not alt.strip():
                issues.append(f"{path.relative_to(ROOT)}: empty Markdown image alt")
            parsed = urlparse(target)
            if parsed.scheme in {"http", "https", "data"}:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            referenced.add(resolved)
            if not resolved.exists():
                issues.append(f"{path.relative_to(ROOT)}: missing image {target}")
        for tag in html.findall(text):
            parsed = urlparse(tag)
            if parsed.scheme in {"http", "https", "data"}:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            referenced.add(resolved)
            if not resolved.exists():
                issues.append(f"{path.relative_to(ROOT)}: missing image {tag}")
        for match in re.finditer(r"<img\b[^>]*>", text, re.I):
            alt_match = alt_html.search(match.group())
            if not alt_match or not alt_match.group(1).strip():
                # Decorative card images with explicit empty alt are allowed.
                if 'alt=""' not in match.group():
                    issues.append(f"{path.relative_to(ROOT)}: HTML image lacks meaningful alt")
    public_images = [
        path for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES and ".git" not in path.parts
    ]
    for path in public_images:
        if path.stat().st_size == 0:
            issues.append(f"{path.relative_to(ROOT)}: zero-byte image")
        if path.stat().st_size > 8 * 1024**2:
            issues.append(f"{path.relative_to(ROOT)}: image exceeds 8 MiB")
        if path.suffix.lower() != ".svg":
            try:
                with Image.open(path) as image:
                    if image.width == 0 or image.height == 0:
                        issues.append(f"{path.relative_to(ROOT)}: invalid dimensions")
            except Exception as exc:
                issues.append(f"{path.relative_to(ROOT)}: unreadable image ({exc})")
    payload = json.loads((AUDIT / "all_source_visuals.json").read_text(encoding="utf-8"))
    for record in payload["visuals"]:
        if record["publication_status"] == "Published" and not record["public_locations"]:
            issues.append(f"{record['asset_id']}: Published without public location")
        if record["publication_status"] == "Selected for Publication" and not record["caption_ko"]:
            issues.append(f"{record['asset_id']}: Selected without caption")
        if record["publication_status"] == "Selected for Publication" and not record["alt_en"]:
            issues.append(f"{record['asset_id']}: Selected without alt text")
    if issues:
        print("VISUAL REFERENCE VALIDATION FAILED")
        print("\n".join(f"- {issue}" for issue in issues[:200]))
        sys.exit(1)
    print(f"PASS visual references: {len(public_images)} public images, captions/alt/provenance")


if __name__ == "__main__":
    main()
