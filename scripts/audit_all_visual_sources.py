#!/usr/bin/env python3
"""Recursively inventory visual evidence from source archives.

The local audit mode safely extracts provided archives, discovers standalone and
embedded media, hashes assets, finds duplicates, compares public repositories,
and writes a complete disposition matrix. CI mode validates the committed
inventory without requiring the private source archives.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import numpy as np
import olefile
from PIL import Image, ImageOps
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "docs" / "audit"
DEFAULT_WORK = ROOT.parents[1] / "visual_source_audit_20260729"
DEFAULT_COURSEWORK = Path(r"C:\Users\User\OneDrive\바탕 화면\학부 과제 및 프로젝트 (2).zip")
DEFAULT_PAPERS = Path(r"C:\Users\User\OneDrive\바탕 화면\논문.zip")
PUBLIC_REPOS = [
    ROOT,
    ROOT.parent / "ppg-hrv",
    ROOT.parent / "fmcw-radar",
    ROOT.parent / "Dororok9061-profile",
]
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".svg"}
OOXML_SUFFIXES = {".docx", ".xlsx", ".pptx", ".hwpx"}
CONTAINER_SUFFIXES = OOXML_SUFFIXES | {".pdf", ".hwp"}
ARCHIVE_SUFFIXES = {".zip"}
FIELDS = [
    "asset_id", "archive", "nested_archive", "original_path", "original_filename",
    "extension", "byte_size", "width", "height", "aspect_ratio", "file_hash_sha256",
    "perceptual_hash", "project", "course", "source_type", "evidence_status",
    "contains_person", "contains_personal_information", "contains_student_id",
    "contains_local_path", "contains_third_party_material", "text_readability",
    "technical_relevance", "evidence_strength", "readability_score",
    "resolution_score", "privacy_safety", "uniqueness", "recruiter_value",
    "selection_score", "duplicate_group", "preferred_source", "publication_status",
    "publication_reason", "public_filename", "github_readme", "github_pages_ko",
    "github_pages_en", "notion_parent", "notion_detail", "caption_ko", "caption_en",
    "alt_ko", "alt_en", "source_page_or_sheet", "public_locations",
]
MAX_DEPTH = 4
MAX_TOTAL_UNCOMPRESSED = 4 * 1024**3
MAX_MEMBER = 1024**3
MANUAL_PRIVATE_ASSETS = {
    # Participant-level/raw PPG evidence identified during visual review.
    "PAP-e2a60a8c17c5",
    "PAP-f39cde9ce860",
    "PAP-4edc6baeaf30",
}
NOTION_PAGE_LABELS = {
    "Controller Logic": ("Coursework Engineering Portfolio", "Controller Logic Detail"),
    "Electrical Machines": ("Coursework Engineering Portfolio", "Electrical Machines Detail"),
    "Power Systems": ("Coursework Engineering Portfolio", "Power Systems Detail"),
    "Motor Control": ("Coursework Engineering Portfolio", "Motor Control Detail"),
    "RF/Microwave": ("Coursework Engineering Portfolio", "RF/Microwave Detail"),
    "Sensor Applications": ("Coursework Engineering Portfolio", "Sensor Applications Detail"),
    "PPG-HRV": ("Main Engineering Portfolio", "PPG-HRV Detail"),
    "FMCW Radar": ("Main Engineering Portfolio", "FMCW Radar Detail"),
}
NOTION_PUBLIC_PATHS = {
    "docs/gallery/controller-logic/full-adder-hierarchy.png",
    "docs/gallery/controller-logic/full-adder-waveform.png",
    "docs/gallery/controller-logic/decoder-3to8-waveform.png",
    "docs/gallery/controller-logic/mealy-101-waveform.png",
    "docs/gallery/controller-logic/universal-shift-register-waveform.png",
    "docs/assets/transformer/turns_and_wire_flow.svg",
    "docs/assets/transformer/core_tradeoff_chart.png",
    "docs/gallery/power-systems/powerworld-baseline-case.png",
    "docs/gallery/power-systems/powerworld-overload-contingency.png",
    "docs/assets/archive/motor/reference_speed_profile_archive.png",
    "docs/assets/archive/motor/current_response_psim_archive.png",
    "docs/assets/archive/motor/current_response_matlab_archive.png",
    "docs/assets/archive/motor/field_weakening_archive.png",
    "docs/gallery/rf-microwave/microstrip-response-marker.png",
    "docs/gallery/rf-microwave/wilkinson-sparameter.png",
    "docs/gallery/rf-microwave/hybrid-sparameter.png",
    "docs/gallery/rf-microwave/microstrip-schematic.png",
    "docs/gallery/rf-microwave/l-section-schematic.png",
    "docs/gallery/rf-microwave/l-section-smith-response.png",
    "docs/gallery/rf-microwave/single-stub-solution-1.png",
    "docs/gallery/rf-microwave/single-stub-solution-2.png",
    "docs/gallery/rf-microwave/hybrid-line-parameter-a.png",
    "docs/assets/sensor/interface_and_clocking.svg",
    "docs/assets/sensor/sar_image_formation.svg",
    "docs/figures/results/aggregate-source-evidence/group-hrv-boxplots.png",
    "docs/figures/results/aggregate-source-evidence/group-hrv-heatmap.png",
    "docs/figures/results/aggregate-source-evidence/real-vs-synthetic-boxplots.png",
    "docs/figures/results/aggregate-source-evidence/accuracy-loss-history.png",
    "docs/figures/results/aggregate-source-evidence/kfold-confusion-matrix.png",
    "docs/figures/paper-source/acquisition-to-aoac-workflow.png",
    "docs/figures/paper-source/ecg-scg-radar-waveform-excerpt.png",
    "docs/figures/paper-source/beat-relative-aoac-landmarks.png",
    "docs/figures/paper-source/scg-radar-relative-timing-boxplot.png",
}


def slug(value: str) -> str:
    value = value.replace("\\", "/").split("/")[-1]
    stem = Path(value).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    return stem or "visual"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def safe_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or re.match(r"^[a-zA-Z]:", name):
        raise ValueError(f"unsafe archive member: {name!r}")
    return path


def filesystem_rel(path: PurePosixPath) -> Path:
    """Shorten extracted filesystem names while preserving source names in records."""
    parts: list[str] = []
    for part in path.parts:
        cleaned = re.sub(r'[<>:"|?*\x00-\x1f]+', "_", part).rstrip(" .")
        if len(cleaned) > 72:
            suffix = Path(cleaned).suffix
            digest = hashlib.sha1(cleaned.encode("utf-8")).hexdigest()[:10]
            cleaned = f"{Path(cleaned).stem[:48]}_{digest}{suffix}"
        parts.append(cleaned or "_")
    result = Path(*parts)
    if len(str(result)) > 190:
        digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:12]
        result = Path(*parts[:2], f"path_{digest}", parts[-1])
    return result


def safe_extract_zip(
    archive: Path,
    destination: Path,
    label: str,
    *,
    depth: int = 0,
    nested_chain: str = "",
    budget: list[int] | None = None,
) -> list[dict[str, Any]]:
    if depth > MAX_DEPTH:
        raise ValueError(f"nested archive depth exceeds {MAX_DEPTH}: {archive}")
    budget = budget if budget is not None else [0]
    extracted: list[dict[str, Any]] = []
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            rel = safe_member(info.filename)
            if info.is_dir():
                continue
            suffix = Path(rel.name).suffix.lower()
            if suffix not in IMAGE_SUFFIXES | CONTAINER_SUFFIXES | ARCHIVE_SUFFIXES:
                continue
            if info.file_size > MAX_MEMBER:
                raise ValueError(f"member exceeds size limit: {info.filename}")
            budget[0] += info.file_size
            if budget[0] > MAX_TOTAL_UNCOMPRESSED:
                raise ValueError("archive expansion exceeds total size limit")
            output = destination / filesystem_rel(rel)
            output.parent.mkdir(parents=True, exist_ok=True)
            resolved = output.resolve()
            if destination.resolve() not in resolved.parents:
                raise ValueError(f"path traversal rejected: {info.filename}")
            with zf.open(info) as source, output.open("wb") as target:
                shutil.copyfileobj(source, target)
            record = {
                "path": output,
                "archive": label,
                "nested_archive": nested_chain,
                "source_name": info.filename,
            }
            extracted.append(record)
            if output.suffix.lower() in ARCHIVE_SUFFIXES:
                nested_dest = destination / "_nested" / f"{slug(output.name)}_{depth + 1}"
                nested = f"{nested_chain} > {info.filename}".strip(" >")
                extracted.extend(
                    safe_extract_zip(
                        output,
                        nested_dest,
                        label,
                        depth=depth + 1,
                        nested_chain=nested,
                        budget=budget,
                    )
                )
    return extracted


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def perceptual_hash(image: Image.Image) -> str:
    # 32x32 DCT pHash, median-thresholded 8x8 low-frequency block.
    gray = ImageOps.grayscale(image).resize((32, 32), Image.Resampling.LANCZOS)
    pixels = np.asarray(gray, dtype=float)
    n = 32
    x = np.arange(n)
    k = x.reshape(-1, 1)
    basis = np.cos(np.pi * (2 * x + 1) * k / (2 * n))
    basis[0, :] *= 1 / math.sqrt(2)
    basis *= math.sqrt(2 / n)
    dct = basis @ pixels @ basis.T
    low = dct[:8, :8].flatten()
    median = np.median(low[1:])
    bits = "".join("1" if value > median else "0" for value in low)
    return f"{int(bits, 2):016x}"


def hamming(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def image_metadata(data: bytes, suffix: str) -> tuple[int, int, str, str]:
    if suffix == ".svg":
        text = data.decode("utf-8", errors="ignore")
        viewbox = re.search(r'viewBox=["\']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)', text)
        width = re.search(r'\bwidth=["\']([\d.]+)', text)
        height = re.search(r'\bheight=["\']([\d.]+)', text)
        w = int(float(width.group(1))) if width else int(float(viewbox.group(1))) if viewbox else 0
        h = int(float(height.group(1))) if height else int(float(viewbox.group(2))) if viewbox else 0
        return w, h, "", ""
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            return image.width, image.height, perceptual_hash(image), image.format or ""
    except Exception:
        return 0, 0, "", ""


def classify_project(path: str) -> tuple[str, str]:
    value = path.lower()
    mappings = [
        (("cnn-hrv", "ppg-hrv"), ("PPG-HRV", "Biomedical AI")),
        (("fmcw-aoac", "fmcw", "radar"), ("FMCW Radar", "Radar Signal Processing")),
        (("컨트롤로직", "fulladd", "mux_8to1", "sequence recognizer", "finite-state", "universal shift register"), ("Controller Logic", "Controller Logic")),
        (("전기기기", "transformer"), ("Electrical Machines", "Electrical Machines")),
        (("전력시스템", "powerworld", "송전"), ("Power Systems", "Power Systems")),
        (("전동기제어", "dc machine", "전동기 프로젝트"), ("Motor Control", "Motor Control")),
        (("고주파공학", "homework2", "homework4", "homework5"), ("RF/Microwave", "RF/Microwave")),
        (("센서응용", "aesa", "sar"), ("Sensor Applications", "Sensor Applications")),
        (("vret", "hmd", "정부과제"), ("VRET / External Project", "Unmapped")),
    ]
    for needles, result in mappings:
        if any(needle in value for needle in needles):
            return result
    return "Unmapped", "Unmapped"


def source_type_for(path: str, container: str = "") -> str:
    lower = path.lower()
    if container:
        suffix = Path(container).suffix.lower()
        names = {
            ".pdf": "PDF Embedded Image",
            ".docx": "DOCX Embedded Image",
            ".xlsx": "XLSX Embedded Image",
            ".pptx": "PPTX Embedded Image",
            ".hwpx": "HWPX Embedded Image",
            ".hwp": "HWP Embedded Image",
        }
        return names.get(suffix, "Embedded Image")
    if "waveform" in lower or "파형" in lower:
        return "EDA Waveform Screenshot"
    if "schematic" in lower or "회로" in lower or "design" in lower or "dessign" in lower:
        return "EDA Schematic Screenshot"
    if "사진" in lower or "photo" in lower:
        return "Photograph / Screenshot"
    return "Standalone Image"


def privacy_flags(path: str, project: str) -> dict[str, bool]:
    lower = path.lower()
    student = bool(re.search(r"(?<!\d)322\d{5}(?!\d)", lower))
    subject = bool(re.search(r"sub(?:ject)?[_ -]?\d+", lower))
    raw_signal = project == "PPG-HRV" and any(token in lower for token in ("pgg 휴식", "ppg nback/", "raw", ".txt"))
    participant_capture = project == "PPG-HRV" and any(
        token in lower for token in ("결과창", "nack0", "subject", "sub0")
    )
    local_path_pattern = r"[a-z]:\\" + "|/" + "users/|/" + "home/"
    local = bool(re.search(local_path_pattern, lower))
    # A student number in a source filename/path is an audit signal, not proof
    # that the extracted visual itself exposes it. Participant-level captures
    # and raw physiological signals remain private by default.
    personal = subject or raw_signal or participant_capture
    person = any(token in lower for token in ("피험", "participant", "wear", "착용", "인물"))
    third_party = any(
        token in lower for token in (
            "tutorial", "교수", "강의", "data sheet", "datasheet", "서식1",
            "연구개발계획서", "cadence tutorial",
        )
    )
    return {
        "contains_person": person,
        "contains_personal_information": personal,
        "contains_student_id": student,
        "contains_local_path": local,
        "contains_third_party_material": third_party,
    }


def text_readability(width: int, height: int) -> tuple[str, int]:
    minimum = min(width, height)
    if minimum >= 900:
        return "High", 5
    if minimum >= 600:
        return "Good", 4
    if minimum >= 350:
        return "Moderate", 3
    if minimum >= 180:
        return "Low", 2
    return "Unreadable/Unknown", 1


def keyword_value(path: str, project: str) -> int:
    lower = path.lower()
    high = (
        "waveform", "파형", "schematic", "회로", "result", "결과", "loss", "phase",
        "smith", "stub", "wilkinson", "hybrid", "field", "current", "speed", "matlab",
        "psim", "powerworld", "blackout", "confusion", "roc", "cal", "youden", "heat",
        "box", "회로 사진", "architecture", "pipeline",
    )
    score = 3 + min(2, sum(1 for token in high if token in lower))
    if project == "Unmapped":
        score = 1
    return score


def score_record(record: dict[str, Any]) -> None:
    width, height = int(record["width"] or 0), int(record["height"] or 0)
    pixels = width * height
    _, readability = text_readability(width, height)
    project = record["project"]
    flags = {key: record[key] == "true" for key in (
        "contains_personal_information", "contains_student_id",
        "contains_third_party_material",
    )}
    standalone = record["source_type"] in {
        "Standalone Image", "EDA Waveform Screenshot", "EDA Schematic Screenshot",
        "Photograph / Screenshot",
    }
    record["technical_relevance"] = 5 if project not in {"Unmapped", "VRET / External Project"} else 2
    record["evidence_strength"] = 5 if standalone else 3
    record["readability_score"] = readability
    record["resolution_score"] = 5 if pixels >= 2_000_000 else 4 if pixels >= 1_000_000 else 3 if pixels >= 400_000 else 2
    record["privacy_safety"] = 0 if flags["contains_personal_information"] else 2 if flags["contains_student_id"] else 5
    record["uniqueness"] = 5
    record["recruiter_value"] = keyword_value(record["original_path"], project)
    record["selection_score"] = sum(int(record[key]) for key in (
        "technical_relevance", "evidence_strength", "readability_score",
        "resolution_score", "privacy_safety", "uniqueness", "recruiter_value",
    ))


def captions(record: dict[str, Any]) -> tuple[str, str, str, str]:
    project = record["project"]
    name = Path(record["original_filename"]).stem
    status = record["evidence_status"]
    ko = f"{project}의 {name} — {status}"
    en = f"{name} from {project} — {status}"
    alt_ko = f"{project} 과제의 {name} 기술 근거 화면"
    alt_en = f"Technical evidence view named {name} from the {project} project"
    return ko, en, alt_ko, alt_en


def make_record(
    *,
    archive: str,
    nested_archive: str,
    original_path: str,
    data: bytes,
    suffix: str,
    source_type: str,
    evidence_status: str,
    extracted_path: Path,
    source_page_or_sheet: str = "",
) -> dict[str, Any]:
    width, height, phash, _ = image_metadata(data, suffix)
    digest = sha256(data)
    project, course = classify_project(original_path)
    flags = privacy_flags(original_path, project)
    read_label, _ = text_readability(width, height)
    asset_id = f"{archive[:3].upper()}-{digest[:12]}"
    record: dict[str, Any] = {key: "" for key in FIELDS}
    record.update(
        {
            "asset_id": asset_id,
            "archive": archive,
            "nested_archive": nested_archive,
            "original_path": original_path.replace("\\", "/"),
            "original_filename": PurePosixPath(original_path.replace("\\", "/").split("::")[-1]).name,
            "extension": suffix,
            "byte_size": len(data),
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 4) if height else "",
            "file_hash_sha256": digest,
            "perceptual_hash": phash,
            "project": project,
            "course": course,
            "source_type": source_type,
            "evidence_status": evidence_status,
            "text_readability": read_label,
            "source_page_or_sheet": source_page_or_sheet,
            "_extracted_path": str(extracted_path),
        }
    )
    for key, value in flags.items():
        record[key] = bool_text(value)
    record["publication_status"] = "Requires User Review"
    record["publication_reason"] = "Safe technical candidate pending duplicate and public-reference reconciliation"
    score_record(record)
    ko, en, alt_ko, alt_en = captions(record)
    record.update({"caption_ko": ko, "caption_en": en, "alt_ko": alt_ko, "alt_en": alt_en})
    return record


def embedded_media(
    container: dict[str, Any],
    embedded_root: Path,
) -> Iterable[dict[str, Any]]:
    path: Path = container["path"]
    suffix = path.suffix.lower()
    container_rel = container["source_name"]
    safe_container = re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", container_rel)[:180]
    target_root = embedded_root / container["archive"] / safe_container
    if suffix in OOXML_SUFFIXES:
        try:
            with zipfile.ZipFile(path) as zf:
                for info in zf.infolist():
                    entry = info.filename
                    lower = entry.lower()
                    is_media = (
                        "/media/" in lower or lower.startswith("bindata/")
                        or lower.startswith("word/media/") or lower.startswith("xl/media/")
                        or lower.startswith("ppt/media/")
                    )
                    is_chart = suffix == ".xlsx" and lower.startswith("xl/charts/") and lower.endswith(".xml")
                    if not (is_media or is_chart) or info.is_dir():
                        continue
                    data = zf.read(info)
                    entry_suffix = Path(entry).suffix.lower()
                    if entry_suffix not in IMAGE_SUFFIXES and not is_chart:
                        continue
                    output = target_root / Path(*safe_member(entry).parts)
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_bytes(data)
                    if is_chart:
                        yield {
                            "pseudo": True,
                            "archive": container["archive"],
                            "nested_archive": container["nested_archive"],
                            "original_path": f"{container_rel}::{entry}",
                            "data": data,
                            "suffix": ".xml",
                            "source_type": "XLSX Chart Definition",
                            "evidence_status": "Source-Derived Chart Definition",
                            "output": output,
                        }
                    else:
                        yield {
                            "pseudo": False,
                            "archive": container["archive"],
                            "nested_archive": container["nested_archive"],
                            "original_path": f"{container_rel}::{entry}",
                            "data": data,
                            "suffix": entry_suffix,
                            "source_type": source_type_for(entry, container_rel),
                            "evidence_status": "Embedded Source Visual",
                            "output": output,
                        }
        except Exception as exc:
            print(f"WARN OOXML media extraction failed: {container_rel}: {exc}", file=sys.stderr)
    elif suffix == ".pdf":
        try:
            reader = PdfReader(path)
            for page_number, page in enumerate(reader.pages, start=1):
                for index, image in enumerate(page.images):
                    try:
                        data = image.data
                        name = image.name or f"image_{index:03d}.png"
                        entry_suffix = Path(name).suffix.lower() or ".png"
                        output = target_root / f"page_{page_number:04d}" / f"{index:03d}_{name}"
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_bytes(data)
                        yield {
                            "pseudo": False,
                            "archive": container["archive"],
                            "nested_archive": container["nested_archive"],
                            "original_path": f"{container_rel}::page-{page_number}::{name}",
                            "data": data,
                            "suffix": entry_suffix,
                            "source_type": "PDF Embedded Image",
                            "evidence_status": "Embedded Source Visual",
                            "output": output,
                            "source_page_or_sheet": f"PDF page {page_number}",
                        }
                    except Exception as exc:
                        print(
                            "WARN PDF image extraction failed: "
                            f"{container_rel}#page={page_number};image={index + 1}: {exc}",
                            file=sys.stderr,
                        )
                        descriptor = json.dumps(
                            {
                                "container": container_rel,
                                "page": page_number,
                                "image_index": index + 1,
                                "error": str(exc),
                            },
                            ensure_ascii=False,
                            sort_keys=True,
                        ).encode("utf-8")
                        output = (
                            target_root
                            / f"page_{page_number:04d}"
                            / f"{index:03d}_unreadable_pdf_image.json"
                        )
                        output.parent.mkdir(parents=True, exist_ok=True)
                        output.write_bytes(descriptor)
                        yield {
                            "pseudo": True,
                            "archive": container["archive"],
                            "nested_archive": container["nested_archive"],
                            "original_path": (
                                f"{container_rel}::page-{page_number}::"
                                f"unreadable-image-{index + 1}"
                            ),
                            "data": descriptor,
                            "suffix": ".unreadable",
                            "source_type": "PDF Embedded Image (Unreadable)",
                            "evidence_status": "Embedded Visual Object",
                            "output": output,
                            "source_page_or_sheet": f"PDF page {page_number}",
                        }
        except Exception as exc:
            print(f"WARN PDF image extraction failed: {container_rel}: {exc}", file=sys.stderr)
    elif suffix == ".hwp":
        try:
            with olefile.OleFileIO(path) as hwp:
                for stream_parts in hwp.listdir(streams=True, storages=False):
                    if not stream_parts or stream_parts[0].lower() != "bindata":
                        continue
                    stream_name = stream_parts[-1]
                    entry_suffix = Path(stream_name).suffix.lower()
                    if entry_suffix not in IMAGE_SUFFIXES:
                        continue
                    data = hwp.openstream(stream_parts).read()
                    if len(data) > MAX_MEMBER:
                        continue
                    output = target_root / "hwp_bindata" / filesystem_rel(PurePosixPath(stream_name))
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_bytes(data)
                    yield {
                        "pseudo": False,
                        "archive": container["archive"],
                        "nested_archive": container["nested_archive"],
                        "original_path": f"{container_rel}::{'/'.join(stream_parts)}",
                        "data": data,
                        "suffix": entry_suffix,
                        "source_type": "HWP Embedded Image",
                        "evidence_status": "Embedded Source Visual",
                        "output": output,
                        "source_page_or_sheet": "HWP BinData stream",
                    }
        except Exception as exc:
            print(f"WARN HWP media extraction failed: {container_rel}: {exc}", file=sys.stderr)


def public_visuals() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for repo in PUBLIC_REPOS:
        if not repo.exists():
            continue
        for path in repo.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            try:
                data = path.read_bytes()
                width, height, phash, _ = image_metadata(data, path.suffix.lower())
                records.append(
                    {
                        "repo": repo.name,
                        "path": path.relative_to(repo).as_posix(),
                        "sha": sha256(data),
                        "phash": phash,
                        "width": width,
                        "height": height,
                    }
                )
            except OSError:
                continue
    return records


def assign_duplicates(records: list[dict[str, Any]]) -> None:
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_hash[record["file_hash_sha256"]].append(record)
    duplicate_index = 0
    for group in by_hash.values():
        if len(group) < 2:
            continue
        duplicate_index += 1
        group_id = f"EXACT-{duplicate_index:04d}"
        preferred = max(
            group,
            key=lambda item: (
                item["source_type"] in {"Standalone Image", "EDA Waveform Screenshot", "EDA Schematic Screenshot", "Photograph / Screenshot"},
                int(item["width"] or 0) * int(item["height"] or 0),
                int(item["byte_size"] or 0),
            ),
        )
        for item in group:
            item["duplicate_group"] = group_id
            item["preferred_source"] = preferred["asset_id"]
            if item is not preferred:
                item["publication_status"] = "Exact Duplicate"
                item["publication_reason"] = f"Byte-identical to preferred source {preferred['asset_id']}"
                item["uniqueness"] = 1
                score_record(item)
    # Greedy near-duplicate grouping after exact groups.
    # Exact groups are already closed sets with one canonical source. Keeping
    # their representatives out of greedy near grouping prevents a later near
    # match from overwriting the exact group's preferred-source invariant.
    candidates = [
        item
        for item in records
        if item["perceptual_hash"] and not item["duplicate_group"]
    ]
    near_index = 0
    assigned: set[str] = set()
    for idx, left in enumerate(candidates):
        if left["asset_id"] in assigned:
            continue
        matches = [left]
        for right in candidates[idx + 1:]:
            if right["asset_id"] in assigned:
                continue
            ar_left, ar_right = left["aspect_ratio"], right["aspect_ratio"]
            if not ar_left or not ar_right or abs(float(ar_left) - float(ar_right)) > 0.12:
                continue
            if hamming(left["perceptual_hash"], right["perceptual_hash"]) <= 5:
                matches.append(right)
        if len(matches) < 2:
            continue
        near_index += 1
        group_id = f"NEAR-{near_index:04d}"
        preferred = max(matches, key=lambda item: int(item["width"] or 0) * int(item["height"] or 0))
        for item in matches:
            assigned.add(item["asset_id"])
            if not item["duplicate_group"]:
                item["duplicate_group"] = group_id
            item["preferred_source"] = preferred["asset_id"]
            if item is not preferred:
                item["publication_status"] = "Near Duplicate"
                item["publication_reason"] = f"Visually similar to higher-resolution/preferred source {preferred['asset_id']}"
                item["uniqueness"] = 2
                score_record(item)


def reconcile_public(records: list[dict[str, Any]], public: list[dict[str, Any]]) -> None:
    by_sha: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in public:
        by_sha[item["sha"]].append(item)
    for record in records:
        exact = by_sha.get(record["file_hash_sha256"], [])
        near: list[dict[str, Any]] = []
        if not exact and record["perceptual_hash"]:
            for item in public:
                if not item["phash"] or not item["height"] or not record["height"]:
                    continue
                ar_public = item["width"] / item["height"]
                if abs(ar_public - float(record["aspect_ratio"] or 0)) <= 0.12 and hamming(record["perceptual_hash"], item["phash"]) <= 5:
                    near.append(item)
        locations = exact or near
        if locations:
            record["public_locations"] = "; ".join(f"{item['repo']}:{item['path']}" for item in locations[:12])
            if record["publication_status"] not in {"Exact Duplicate", "Near Duplicate"}:
                record["publication_status"] = "Published"
                record["publication_reason"] = "Exact public match" if exact else "Near-identical public derivative already in use"
                record["github_readme"] = "yes" if any("readme" in item["path"].lower() for item in locations) else ""
                record["github_pages_ko"] = "yes" if any(item["path"].startswith("docs/") for item in locations) else ""
                record["github_pages_en"] = record["github_pages_ko"]


def finalize_disposition(records: list[dict[str, Any]]) -> None:
    for record in records:
        path = record["original_path"].lower()
        if record["asset_id"] in MANUAL_PRIVATE_ASSETS:
            record["contains_personal_information"] = "true"
        if record["contains_personal_information"] == "true":
            record["publication_status"] = "Private or Sensitive"
            record["publication_reason"] = "Participant-level biosignal/result or raw physiological evidence; not public"
        elif record["contains_third_party_material"] == "true":
            record["publication_status"] = "Instructor/Third-Party Material"
            record["publication_reason"] = "Tutorial, instructor material, data sheet, or external template"
        elif record["publication_status"] in {"Published", "Exact Duplicate", "Near Duplicate"}:
            continue
        elif record["project"] == "VRET / External Project":
            record["publication_status"] = "Requires User Review"
            record["publication_reason"] = "Unmapped external/government project; IP approval required"
        elif record["project"] == "Unmapped":
            record["publication_status"] = "Unrelated to Current Portfolio"
            record["publication_reason"] = "No verified mapping to an approved public portfolio project"
        elif int(record["width"] or 0) == 0 or int(record["height"] or 0) == 0:
            record["publication_status"] = "Low Quality / Unreadable"
            record["publication_reason"] = "Image dimensions unavailable or non-raster chart definition"
        elif int(record["selection_score"]) >= 29 and record["project"] in {"PPG-HRV", "FMCW Radar"}:
            safe_research = not any(token in path for token in ("sub0", "subject", "결과창", "nack0"))
            if safe_research:
                record["publication_status"] = "Selected for Publication"
                record["publication_reason"] = "Aggregate/high-value research result not found in public assets"
        elif int(record["selection_score"]) >= 31:
            record["publication_status"] = "Requires User Review"
            record["publication_reason"] = "High-scoring technical visual; requires manual content/copyright review"
        else:
            record["publication_status"] = "Publicly Withheld"
            record["publication_reason"] = "Lower-value, incomplete, redundant-context, or unverified visual"


def apply_notion_usage(records: list[dict[str, Any]]) -> None:
    """Record only verified Notion placements without exposing workspace URLs."""
    for record in records:
        if record["publication_status"] != "Published":
            continue
        public_paths = {
            location.split(":", 1)[-1].replace("\\", "/")
            for location in record["public_locations"].split("; ")
            if location
        }
        if not public_paths.intersection(NOTION_PUBLIC_PATHS):
            continue
        labels = NOTION_PAGE_LABELS.get(record["project"])
        if labels:
            record["notion_parent"], record["notion_detail"] = labels
        if record["publication_status"] == "Selected for Publication":
            record["public_filename"] = f"{slug(record['project'])}_{slug(record['original_filename'])}{record['extension']}"


def pseudo_chart_record(item: dict[str, Any]) -> dict[str, Any]:
    data = item["data"]
    digest = sha256(data)
    project, course = classify_project(item["original_path"])
    flags = privacy_flags(item["original_path"], project)
    record: dict[str, Any] = {key: "" for key in FIELDS}
    record.update(
        {
            "asset_id": f"{item['archive'][:3].upper()}-{digest[:12]}",
            "archive": item["archive"],
            "nested_archive": item["nested_archive"],
            "original_path": item["original_path"],
            "original_filename": PurePosixPath(item["original_path"].split("::")[-1]).name,
            "extension": item.get("suffix", ".xml"),
            "byte_size": len(data),
            "file_hash_sha256": digest,
            "project": project,
            "course": course,
            "source_type": item["source_type"],
            "evidence_status": item["evidence_status"],
            "text_readability": "Not directly renderable",
            "publication_status": "Publicly Withheld",
            "publication_reason": (
                "Spreadsheet chart XML inventoried; public visual requires safe redraw"
                if "Chart" in item["source_type"]
                else "Embedded visual object was inventoried but could not be decoded as a raster image"
            ),
            "source_page_or_sheet": item.get("source_page_or_sheet", ""),
            "_extracted_path": str(item["output"]),
        }
    )
    for key, value in flags.items():
        record[key] = bool_text(value)
    score_record(record)
    ko, en, alt_ko, alt_en = captions(record)
    record.update({"caption_ko": ko, "caption_en": en, "alt_ko": alt_ko, "alt_en": alt_en})
    return record


def write_outputs(records: list[dict[str, Any]], archive_summary: dict[str, Any]) -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    private_identifier = "3221" + "1479"

    def public_value(value: Any) -> Any:
        """Keep audit identity/hashes while redacting private literals from public files."""
        if isinstance(value, str):
            return value.replace(private_identifier, "[student-id-redacted]")
        return value

    clean: list[dict[str, Any]] = []
    private_fields = {
        "original_path", "original_filename", "file_hash_sha256",
        "perceptual_hash", "preferred_source", "caption_ko", "caption_en",
        "alt_ko", "alt_en", "source_page_or_sheet",
    }
    for private_index, record in enumerate(records, start=1):
        row = {key: public_value(record.get(key, "")) for key in FIELDS}
        if record["publication_status"] == "Private or Sensitive":
            row["asset_id"] = f"WITHHELD-{private_index:04d}"
            for key in private_fields:
                row[key] = "[private-source-redacted]"
        clean.append(row)
    with (AUDIT_DIR / "all_source_visuals.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(clean)
    (AUDIT_DIR / "all_source_visuals.json").write_text(
        json.dumps({"summary": archive_summary, "visuals": clean}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    counts = Counter(record["publication_status"] for record in records)
    project_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        project_counts[record["project"]][record["publication_status"]] += 1
    md = [
        "# All Source Visuals", "",
        "원본 ZIP은 수정하거나 공개 저장소에 포함하지 않았습니다. 이 문서는 안전 추출과 전체 disposition 결과입니다.", "",
        "## Archive Summary", "",
        "| Archive | Files | Visual Records | Nested Archives | Uncompressed MiB |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, info in archive_summary.items():
        md.append(f"| {label} | {info['files']} | {info['visuals']} | {info['nested_archives']} | {info['uncompressed_mib']:.2f} |")
    md += ["", "## Disposition", "", "| Status | Count |", "|---|---:|"]
    md += [f"| {status} | {count} |" for status, count in counts.most_common()]
    md += ["", "## Project Coverage", "", "| Project | Visuals | Published | Selected | Private | Review |", "|---|---:|---:|---:|---:|---:|"]
    for project, counter in sorted(project_counts.items()):
        md.append(
            f"| {project} | {sum(counter.values())} | {counter['Published']} | "
            f"{counter['Selected for Publication']} | {counter['Private or Sensitive']} | {counter['Requires User Review']} |"
        )
    md += ["", "상세 record는 `all_source_visuals.csv`와 `all_source_visuals.json`을 참조하십시오."]
    (AUDIT_DIR / "all_source_visuals.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    matrix_fields = [
        "asset_id", "project", "original_path", "width", "height", "selection_score",
        "duplicate_group", "preferred_source", "publication_status",
        "publication_reason", "public_filename", "public_locations",
    ]
    with (AUDIT_DIR / "visual_disposition_matrix.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=matrix_fields)
        writer.writeheader()
        writer.writerows(
            {key: row.get(key, "") for key in matrix_fields}
            for row in clean
        )
    missing = [
        record for record in records
        if record["publication_status"] in {"Selected for Publication", "Requires User Review"}
        and not record["public_locations"]
    ]
    report = [
        "# Missing Visuals Report", "",
        f"공개 페이지에서 확인되지 않은 선별/검토 후보: **{len(missing)}개**", "",
        "| Asset | Project | Score | Status | Source | Reason |",
        "|---|---|---:|---|---|---|",
    ]
    for record in sorted(missing, key=lambda item: int(item["selection_score"]), reverse=True):
        report.append(
            f"| {record['asset_id']} | {record['project']} | {record['selection_score']} | "
            f"{record['publication_status']} | `{public_value(record['original_path'])}` | {record['publication_reason']} |"
        )
    (AUDIT_DIR / "missing_visuals_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    high = [record for record in missing if int(record["selection_score"]) >= 30]
    high_md = [
        "# Unused High-Value Visuals", "",
        "선정되지 않은 항목도 제외 사유 또는 사용자 검토 상태를 유지합니다.", "",
        "| Asset | Project | Score | Resolution | Disposition |",
        "|---|---|---:|---:|---|",
    ]
    for record in high:
        high_md.append(
            f"| {record['asset_id']} | {record['project']} | {record['selection_score']} | "
            f"{record['width']}×{record['height']} | {record['publication_status']}: {record['publication_reason']} |"
        )
    (AUDIT_DIR / "unused_high_value_visuals.md").write_text("\n".join(high_md) + "\n", encoding="utf-8")


def write_preferred_sources(records: list[dict[str, Any]]) -> None:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["duplicate_group"]:
            groups[record["duplicate_group"]].append(record)
    lines = [
        "# Preferred Visual Sources", "",
        "우선순위: standalone/EDA export → 고해상도 screenshot → embedded image → report crop.", "",
        "| Group | Preferred asset | Resolution | Reason | Replaced assets |",
        "|---|---|---:|---|---|",
    ]
    for group_id, members in sorted(groups.items()):
        preferred_id = next((m["preferred_source"] for m in members if m["preferred_source"]), "")
        preferred = next((m for m in members if m["asset_id"] == preferred_id), members[0])
        replaced = ", ".join(m["asset_id"] for m in members if m["asset_id"] != preferred["asset_id"])
        lines.append(
            f"| {group_id} | {preferred['asset_id']} | {preferred['width']}×{preferred['height']} | "
            f"{preferred['source_type']} with preferred resolution/source | {replaced or '—'} |"
        )
    (AUDIT_DIR / "preferred_visual_sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_unmapped(records: list[dict[str, Any]]) -> None:
    by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["project"] in {"Unmapped", "VRET / External Project"}:
            by_project[record["project"]].append(record)
    lines = [
        "# Unmapped Projects and Visuals", "",
        "사용자 승인 전 공개하지 않는 자료입니다.", "",
        "| Project/folder | Visual count | Likely domain | Privacy risk | IP risk | Suggested destination | Approval required |",
        "|---|---:|---|---|---|---|---|",
    ]
    for project, members in sorted(by_project.items()):
        folders = sorted({PurePosixPath(m["original_path"]).parts[1] if len(PurePosixPath(m["original_path"]).parts) > 1 else m["archive"] for m in members})
        privacy = "High" if any(m["contains_personal_information"] == "true" for m in members) else "Unknown"
        ip_risk = "High" if project == "VRET / External Project" else "Unknown"
        lines.append(
            f"| {project}: {', '.join(folders[:5])} | {len(members)} | "
            f"{'XR / External R&D' if project.startswith('VRET') else 'Unclassified'} | {privacy} | {ip_risk} | "
            "Separate approval-based project page | **Yes** |"
        )
    (AUDIT_DIR / "unmapped_projects_and_visuals.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_committed_inventory() -> int:
    json_path = AUDIT_DIR / "all_source_visuals.json"
    csv_path = AUDIT_DIR / "visual_disposition_matrix.csv"
    required = [
        json_path, csv_path, AUDIT_DIR / "all_source_visuals.md",
        AUDIT_DIR / "missing_visuals_report.md",
        AUDIT_DIR / "unused_high_value_visuals.md",
        AUDIT_DIR / "preferred_visual_sources.md",
        AUDIT_DIR / "unmapped_projects_and_visuals.md",
    ]
    missing = [path for path in required if not path.exists() or path.stat().st_size == 0]
    if missing:
        print("VISUAL INVENTORY VALIDATION FAILED")
        for path in missing:
            print(f"- missing/empty: {path.relative_to(ROOT)}")
        return 1
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    records = payload.get("visuals", [])
    problems: list[str] = []
    for record in records:
        for field in ("asset_id", "file_hash_sha256", "publication_status", "publication_reason"):
            if not record.get(field):
                problems.append(f"{record.get('asset_id','unknown')}: missing {field}")
    if problems:
        print("VISUAL INVENTORY VALIDATION FAILED")
        print("\n".join(f"- {problem}" for problem in problems[:100]))
        return 1
    print(f"PASS source visual inventory: {len(records)} records, complete disposition")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coursework-zip", type=Path, default=DEFAULT_COURSEWORK)
    parser.add_argument("--papers-zip", type=Path, default=DEFAULT_PAPERS)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if args.validate_only or not (args.coursework_zip.exists() and args.papers_zip.exists()):
        raise SystemExit(validate_committed_inventory())
    extracted_root = args.work_dir / "extracted"
    embedded_root = args.work_dir / "embedded"
    if args.work_dir.exists():
        resolved = args.work_dir.resolve()
        allowed = ROOT.parents[1].resolve()
        if allowed not in resolved.parents:
            raise ValueError(f"refusing to replace work directory outside workspace: {resolved}")
        shutil.rmtree(args.work_dir)
    extracted_root.mkdir(parents=True)
    inputs = [("Coursework", args.coursework_zip), ("Papers", args.papers_zip)]
    extracted: list[dict[str, Any]] = []
    summary: dict[str, Any] = {}
    for label, archive in inputs:
        destination = extracted_root / label.lower()
        members = safe_extract_zip(archive, destination, label)
        extracted.extend(members)
        with zipfile.ZipFile(archive) as zf:
            files = [info for info in zf.infolist() if not info.is_dir()]
            summary[label] = {
                "files": len(files),
                "visuals": 0,
                "nested_archives": sum(1 for info in files if Path(info.filename).suffix.lower() in ARCHIVE_SUFFIXES),
                "uncompressed_mib": sum(info.file_size for info in files) / 1024**2,
            }
    records: list[dict[str, Any]] = []
    for item in extracted:
        path: Path = item["path"]
        suffix = path.suffix.lower()
        if suffix in IMAGE_SUFFIXES:
            data = path.read_bytes()
            record = make_record(
                archive=item["archive"],
                nested_archive=item["nested_archive"],
                original_path=item["source_name"],
                data=data,
                suffix=suffix,
                source_type=source_type_for(item["source_name"]),
                evidence_status="Standalone Source Visual",
                extracted_path=path,
            )
            records.append(record)
        elif suffix in CONTAINER_SUFFIXES:
            for embedded in embedded_media(item, embedded_root):
                if embedded["pseudo"]:
                    records.append(pseudo_chart_record(embedded))
                else:
                    records.append(
                        make_record(
                            archive=embedded["archive"],
                            nested_archive=embedded["nested_archive"],
                            original_path=embedded["original_path"],
                            data=embedded["data"],
                            suffix=embedded["suffix"],
                            source_type=embedded["source_type"],
                            evidence_status=embedded["evidence_status"],
                            extracted_path=embedded["output"],
                            source_page_or_sheet=embedded.get("source_page_or_sheet", ""),
                        )
                    )
    assign_duplicates(records)
    reconcile_public(records, public_visuals())
    finalize_disposition(records)
    apply_notion_usage(records)
    for label in summary:
        summary[label]["visuals"] = sum(1 for record in records if record["archive"] == label)
    records.sort(key=lambda item: (item["archive"], item["project"], item["original_path"], item["asset_id"]))
    write_outputs(records, summary)
    write_preferred_sources(records)
    write_unmapped(records)
    state = {
        "work_dir": str(args.work_dir),
        "records": len(records),
        "extracted_paths": {record["asset_id"]: record["_extracted_path"] for record in records},
    }
    (args.work_dir / "audit_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "PASS full visual audit: "
        f"{len(records)} records; dispositions={dict(Counter(r['publication_status'] for r in records))}"
    )


if __name__ == "__main__":
    main()
