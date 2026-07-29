#!/usr/bin/env python3
"""Validate exact/near duplicate groups in the committed visual inventory."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "audit" / "all_source_visuals.json"


def hamming(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def main() -> None:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = payload["visuals"]
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        if record["duplicate_group"]:
            groups[record["duplicate_group"]].append(record)
    issues: list[str] = []
    for group_id, members in groups.items():
        preferred = {
            member["preferred_source"]
            for member in members
            if re.fullmatch(r"[A-Z]+-[0-9a-f]{12}", str(member.get("preferred_source", "")))
        }
        if preferred and len(preferred) != 1:
            issues.append(f"{group_id}: expected one preferred source, got {sorted(preferred)}")
        if group_id.startswith("EXACT-"):
            hashes = {
                member["file_hash_sha256"]
                for member in members
                if re.fullmatch(r"[0-9a-f]{64}", str(member.get("file_hash_sha256", "")))
            }
            if hashes and len(hashes) != 1:
                issues.append(f"{group_id}: exact group contains {len(hashes)} SHA-256 values")
        if group_id.startswith("NEAR-"):
            phashes = [
                member["perceptual_hash"]
                for member in members
                if re.fullmatch(r"[0-9a-fA-F]+", str(member.get("perceptual_hash", "")))
            ]
            if phashes and min(hamming(phashes[0], value) for value in phashes[1:] or phashes) > 8:
                issues.append(f"{group_id}: near group lacks a close perceptual match")
    if issues:
        print("VISUAL DUPLICATE VALIDATION FAILED")
        print("\n".join(f"- {issue}" for issue in issues[:100]))
        sys.exit(1)
    print(f"PASS visual duplicates: {len(groups)} groups across {len(records)} records")


if __name__ == "__main__":
    main()
