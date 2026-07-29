#!/usr/bin/env python3
"""Generate privacy-safe contact sheets from the visual inventory."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "audit"
OUTPUT = AUDIT / "contact_sheets"
DEFAULT_STATE = ROOT.parents[1] / "visual_source_audit_20260729" / "audit_state.json"
SHEET_NAMES = {
    "Controller Logic": "controller_logic_all_sources.jpg",
    "Electrical Machines": "electrical_machines_all_sources.jpg",
    "Power Systems": "power_systems_all_sources.jpg",
    "Motor Control": "motor_control_all_sources.jpg",
    "RF/Microwave": "rf_microwave_all_sources.jpg",
    "Sensor Applications": "sensor_applications_all_sources.jpg",
    "PPG-HRV": "ppg_hrv_all_sources.jpg",
    "FMCW Radar": "fmcw_paper_all_sources.jpg",
}
PRIVATE = {"Private or Sensitive", "Instructor/Third-Party Material"}


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\malgun.ttf"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def tile(record: dict, path: Path | None, size: tuple[int, int]) -> Image.Image:
    width, height = size
    private = record["publication_status"] in PRIVATE
    canvas = Image.new("RGB", size, "#18253a" if private else "#f4f7fb")
    draw = ImageDraw.Draw(canvas)
    visual_h = height - 36
    if private:
        draw.rectangle((4, 4, width - 4, visual_h - 4), fill="#3a2330")
        draw.text((width // 2, visual_h // 2), "WITHHELD", anchor="mm", fill="#ffb4c7", font=font(12))
    elif path and path.exists():
        try:
            with Image.open(path) as source:
                frame = ImageOps.exif_transpose(source).convert("RGB")
                frame.thumbnail((width - 8, visual_h - 8), Image.Resampling.LANCZOS)
                x = (width - frame.width) // 2
                y = (visual_h - frame.height) // 2
                canvas.paste(frame, (x, y))
        except Exception:
            draw.text((width // 2, visual_h // 2), "UNREADABLE", anchor="mm", fill="#7d2434", font=font(11))
    else:
        draw.text((width // 2, visual_h // 2), "NO PREVIEW", anchor="mm", fill="#5c6b81", font=font(11))
    label = f"{record['asset_id'][:16]}  {record['width']}x{record['height']}"
    status = record["publication_status"].replace("Selected for Publication", "SELECTED")
    draw.rectangle((0, visual_h, width, height), fill="#07101d")
    draw.text((5, visual_h + 3), label, fill="#f2f6ff", font=font(9))
    draw.text((5, visual_h + 17), status[:30], fill="#4de4ff", font=font(8))
    return canvas


def build(records: list[dict], paths: dict[str, str], output: Path) -> None:
    columns = 8
    tile_size = (180, 142)
    title_h = 54
    rows = math.ceil(len(records) / columns)
    sheet = Image.new("RGB", (columns * tile_size[0], title_h + rows * tile_size[1]), "#07101d")
    draw = ImageDraw.Draw(sheet)
    title = f"{records[0]['project']} — {len(records)} source visuals"
    draw.text((18, 15), title, fill="#f2f6ff", font=font(20))
    for index, record in enumerate(records):
        row, col = divmod(index, columns)
        extracted = paths.get(record["asset_id"], "")
        preview = tile(record, Path(extracted) if extracted else None, tile_size)
        sheet.paste(preview, (col * tile_size[0], title_h + row * tile_size[1]))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, "JPEG", quality=86, optimize=True, progressive=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args()
    inventory = json.loads((AUDIT / "all_source_visuals.json").read_text(encoding="utf-8"))["visuals"]
    state = json.loads(args.state.read_text(encoding="utf-8"))
    paths = state["extracted_paths"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for project, filename in SHEET_NAMES.items():
        records = [record for record in inventory if record["project"] == project]
        if records:
            build(records, paths, OUTPUT / filename)
    excluded = [
        record for record in inventory
        if record["publication_status"] in PRIVATE or record["contains_personal_information"] == "true"
    ]
    if excluded:
        # Raw private imagery is never pasted; tile() emits only WITHHELD placeholders.
        build(excluded, paths, OUTPUT / "excluded_private_assets.jpg")
    print(f"PASS contact sheets: {len(list(OUTPUT.glob('*.jpg')))} files")


if __name__ == "__main__":
    main()
