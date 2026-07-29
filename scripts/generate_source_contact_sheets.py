#!/usr/bin/env python3
"""Render review contact sheets for every non-duplicate source PNG."""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "source"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\malgun.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(open(args.inventory, encoding="utf-8-sig")))
    root = Path(args.source_root).resolve()
    top = next(root.iterdir())
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[str] = set()
    for row in rows:
        if row["publication_decision"] == "DUPLICATE" or row["sha256"] in seen:
            continue
        seen.add(row["sha256"])
        parts = Path(row["relative_path"]).parts
        directories = parts[:-1]
        subgroup = (
            str(Path(*directories[:2]))
            if directories
            else "root"
        )
        groups[f"{row['subject']}__{subgroup}"].append(row)

    tile_w, tile_h = 320, 236
    columns = 5
    per_page = 50
    produced = 0
    for group, records in sorted(groups.items()):
        for page_index in range(0, len(records), per_page):
            page = records[page_index : page_index + per_page]
            page_no = page_index // per_page + 1
            rows_count = math.ceil(len(page) / columns)
            sheet = Image.new("RGB", (columns * tile_w, 60 + rows_count * tile_h), "#07111f")
            draw = ImageDraw.Draw(sheet)
            draw.text(
                (18, 16),
                f"{group} · page {page_no}/{math.ceil(len(records)/per_page)} · {len(page)} files",
                fill="#f8fafc",
                font=font(20),
            )
            for index, record in enumerate(page):
                row_index, column_index = divmod(index, columns)
                x = column_index * tile_w
                y = 60 + row_index * tile_h
                draw.rectangle((x, y, x + tile_w - 2, y + tile_h - 2), fill="#f8fafc")
                source = top / record["subject"] / record["relative_path"]
                try:
                    with Image.open(source) as image:
                        preview = ImageOps.exif_transpose(image).convert("RGB")
                        preview.thumbnail((tile_w - 14, tile_h - 62), Image.Resampling.LANCZOS)
                        px = x + (tile_w - preview.width) // 2
                        py = y + 5 + (tile_h - 62 - preview.height) // 2
                        sheet.paste(preview, (px, py))
                except Exception:
                    draw.text((x + 15, y + 65), "UNREADABLE", fill="#b91c1c", font=font(18))
                label = Path(record["relative_path"]).name
                if len(label) > 43:
                    label = label[:40] + "…"
                draw.rectangle((x, y + tile_h - 54, x + tile_w - 2, y + tile_h - 2), fill="#0f172a")
                draw.text((x + 7, y + tile_h - 49), label, fill="#f8fafc", font=font(11))
                draw.text(
                    (x + 7, y + tile_h - 29),
                    f"{record['source_id']} · {record['width']}×{record['height']} · {record['publication_decision']}",
                    fill="#67e8f9",
                    font=font(9),
                )
            target = output / f"{slug(group)}-{page_no:02d}.jpg"
            sheet.save(target, quality=88, optimize=True, progressive=True)
            produced += 1
    print(f"CONTACT_SHEETS_PASS files={produced} visuals={len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
