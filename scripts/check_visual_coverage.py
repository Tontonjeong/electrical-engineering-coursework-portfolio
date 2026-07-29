#!/usr/bin/env python3
"""Fail when required engineering visual categories lack published evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "audit" / "visual_coverage_manifest.json"
REPOSITORIES = {
    "coursework": ROOT,
    "ppg": ROOT.parent / "ppg-hrv",
    "radar": ROOT.parent / "fmcw-radar",
}


def main() -> None:
    if not MANIFEST.exists():
        print(f"VISUAL COVERAGE FAILED\n- missing {MANIFEST.relative_to(ROOT)}")
        sys.exit(1)
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    issues: list[str] = []
    checked = 0
    for project, categories in payload["projects"].items():
        for category, entry in categories.items():
            checked += 1
            repository = entry.get("repository", "coursework")
            repo_root = REPOSITORIES.get(repository)
            if repo_root is None:
                issues.append(f"{project}/{category}: unknown repository={repository}")
                continue
            paths = [repo_root / path for path in entry.get("public_paths", [])]
            if entry.get("status") != "Published":
                issues.append(f"{project}/{category}: status={entry.get('status')}")
            if not paths:
                issues.append(f"{project}/{category}: no public_paths")
            for path in paths:
                if not path.exists() or path.stat().st_size == 0:
                    issues.append(f"{project}/{category}: missing/empty {repository}:{path}")
            if not entry.get("evidence_status") or not entry.get("caption_ko") or not entry.get("alt_en"):
                issues.append(f"{project}/{category}: provenance/caption/alt incomplete")
    if issues:
        print("VISUAL COVERAGE FAILED")
        print("\n".join(f"- {issue}" for issue in issues))
        sys.exit(1)
    print(f"PASS visual coverage: {checked} required evidence categories")


if __name__ == "__main__":
    main()
