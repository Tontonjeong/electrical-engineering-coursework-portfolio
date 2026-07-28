#!/usr/bin/env python3
"""Static SVG safety audit for viewport, text size, and obvious out-of-bounds placement."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG_ROOT = ROOT / "docs" / "assets"
NUMBER = re.compile(r"[-+]?(?:\d*\.)?\d+(?:[eE][-+]?\d+)?")


def number(value: str | None) -> float | None:
    if not value:
        return None
    match = NUMBER.search(value)
    return float(match.group()) if match else None


def audit(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{path.relative_to(ROOT)}: invalid XML ({exc})"]
    viewbox = [float(item) for item in (root.get("viewBox") or "").split()]
    width, height = number(root.get("width")), number(root.get("height"))
    if len(viewbox) != 4:
        issues.append(f"{path.relative_to(ROOT)}: missing/invalid viewBox")
        return issues
    x0, y0, vw, vh = viewbox
    if vw <= 0 or vh <= 0:
        issues.append(f"{path.relative_to(ROOT)}: non-positive viewBox")
    if width is None or height is None:
        issues.append(f"{path.relative_to(ROOT)}: explicit width/height required")
    elif abs(width / height - vw / vh) > 0.02:
        issues.append(f"{path.relative_to(ROOT)}: width/height ratio differs from viewBox")
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag == "foreignObject":
            issues.append(f"{path.relative_to(ROOT)}: foreignObject is not portable")
        if tag == "text":
            size = number(elem.get("font-size"))
            style = elem.get("style", "")
            if size is None:
                match = re.search(r"font-size\s*:\s*([0-9.]+)", style)
                size = float(match.group(1)) if match else None
            if size is not None and size < 14:
                issues.append(f"{path.relative_to(ROOT)}: text below 14px ({size:g})")
            x, y = number(elem.get("x")), number(elem.get("y"))
            if x is not None and not x0 - 5 <= x <= x0 + vw + 5:
                issues.append(f"{path.relative_to(ROOT)}: text x={x:g} outside viewBox")
            if y is not None and not y0 - 5 <= y <= y0 + vh + 5:
                issues.append(f"{path.relative_to(ROOT)}: text y={y:g} outside viewBox")
    return issues


def main() -> None:
    svgs = sorted(SVG_ROOT.rglob("*.svg"))
    issues = [issue for path in svgs for issue in audit(path)]
    if issues:
        print("SVG VALIDATION FAILED")
        print("\n".join(f"- {item}" for item in issues))
        sys.exit(1)
    print(f"PASS SVG validation: {len(svgs)} files, viewBox/size/text checks")


if __name__ == "__main__":
    main()
