"""Build canonical per-work text files from best available sources.

For each work in the corpus, copies the best available text extraction
into data/canonical/ with a YAML frontmatter header documenting provenance.

Usage:
    python -m scripts.build_canonical [--force]

The --force flag overwrites existing canonical files. Without it, only
missing files are created.

Source selection logic:
- W001 (Part 1): DTA plain text (FT-7) — definitive scholarly edition
- W002-W004 (Parts 2-3): BSB Tesseract Fraktur (FT-3) per-work files
  (Waentig 1910 is FT-4 but covers all parts in one unsplittable file)
- W006-W033 (Neue Annalen): GDZ Tesseract Fraktur (FT-3)
- W035-W036 (Doberan): BSB Tesseract Fraktur (FT-3)
- W010 (fragment): Absorbed into Part 2.1 (M003)
- W031 (multi-part): Concatenated from 3 GDZ band extractions
"""

import argparse
import csv
import hashlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ACQ_DIR = BASE_DIR / "data" / "acquisitions"
CANONICAL_DIR = BASE_DIR / "data" / "canonical"
WORKS_CSV = BASE_DIR / "data" / "works" / "works.csv"
PRIORITY_CSV = ACQ_DIR / "text_source_priority.csv"
MANIFEST_CSV = ACQ_DIR / "fulltext_manifest.csv"

LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"build_canonical_{ts}.log"
    logger = logging.getLogger("build_canonical")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def load_works(path: Path) -> dict:
    """Load works.csv into dict keyed by work_id."""
    works = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            works[row["work_id"]] = row
    return works


def load_priority(path: Path) -> dict:
    """Load text_source_priority.csv into dict keyed by work_id."""
    priority = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            priority[row["work_id"]] = row
    return priority


def load_manifest(path: Path) -> dict:
    """Load fulltext_manifest.csv into dict keyed by manifestation_id."""
    manifest = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            manifest[row["manifestation_id"]] = row
    return manifest


# Maps work_id -> source file path(s) relative to ACQ_DIR.
# Most works use a single file from best_text_source in priority CSV.
# Special cases are handled explicitly.
SPECIAL_SOURCES: dict[str, list[str]] = {
    # W001: DTA plain text (FT-7)
    "W001": ["structured/thuenen_w001_e001_m009_1826_der-isolirte-staat_part1_dta-txt.txt"],
    # W002-W004: Use per-work BSB Tesseract files (FT-3), not unsplittable Waentig
    "W002": ["extracted/thuenen_w002_e003_m003_1850_part2-1_bsb_tesseract-fraktur.txt"],
    "W003": ["extracted/thuenen_w003_e004_m004_1863_part2-2_bsb_tesseract-fraktur.txt"],
    "W004": ["extracted/thuenen_w004_e005_m005_1863_part3_bsb_tesseract-fraktur.txt"],
    # W010: Absorbed into Part 2.1 — no separate canonical file
    "W010": [],
    # W031: Multi-part across 3 GDZ bands — concatenate
    "W031": [
        "extracted/neue-annalen_band25_M036a_pp202-212_tesseract-fraktur.txt",
        "extracted/neue-annalen_band25_M036b_pp588-592_tesseract-fraktur.txt",
        "extracted/neue-annalen_band26_M036c_pp665-668_tesseract-fraktur.txt",
    ],
}

# Manifestation ID to file path lookup from fulltext_manifest.csv
def resolve_source_path(work_id: str, priority: dict, manifest: dict) -> list[Path]:
    """Resolve the source file path(s) for a work."""
    if work_id in SPECIAL_SOURCES:
        paths = SPECIAL_SOURCES[work_id]
        if not paths:
            return []
        return [ACQ_DIR / p for p in paths]

    prow = priority.get(work_id)
    if not prow:
        return []

    best_src = prow.get("best_text_source", "")
    if best_src == "none" or not best_src:
        return []

    # Extract manifestation ID from "M0xx (description)" format
    mid = best_src.split("(")[0].strip().split()[-1] if best_src else ""
    if not mid.startswith("M"):
        # Try just the first token
        mid = best_src.split()[0]

    mrow = manifest.get(mid)
    if not mrow:
        return []

    text_path = mrow.get("canonical_text_path", "")
    if not text_path:
        return []

    return [ACQ_DIR / text_path]


def slugify(title: str) -> str:
    """Create a filesystem-safe slug from a title."""
    import re
    slug = title.lower()
    # Replace umlauts
    for old, new in [("ae", "ae"), ("oe", "oe"), ("ue", "ue"),
                     ("\u00e4", "ae"), ("\u00f6", "oe"), ("\u00fc", "ue"),
                     ("\u00df", "ss")]:
        slug = slug.replace(old, new)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    # Truncate to reasonable length
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
    return slug


def build_frontmatter(work_id: str, work: dict, priority_row: dict,
                      source_paths: list[Path], text_tier: str) -> str:
    """Build YAML frontmatter for a canonical text file."""
    title = work.get("canonical_title", "")
    title_norm = work.get("canonical_title_normalized", "")
    pub_date = work.get("first_publication_date_normalized", "")
    work_type = work.get("work_type", "")
    lang = work.get("original_language", "de")
    best_src = priority_row.get("best_text_source", "")
    alt_src = priority_row.get("alternative_source", "")
    notes = priority_row.get("notes", "")

    source_files = "; ".join(p.name for p in source_paths)

    lines = [
        "---",
        f"work_id: {work_id}",
        f'title: "{title}"',
        f'title_normalized: "{title_norm}"',
        f"publication_date: {pub_date}",
        f"work_type: {work_type}",
        f"language: {lang}",
        f"text_tier: {text_tier}",
        f'source: "{best_src}"',
        f"source_files: \"{source_files}\"",
    ]
    if alt_src:
        lines.append(f'alternative_source: "{alt_src}"')
    if notes:
        lines.append(f'notes: "{notes}"')
    lines.append(f"assembled: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build canonical per-work text files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("Starting canonical text assembly")

    works = load_works(WORKS_CSV)
    priority = load_priority(PRIORITY_CSV)
    manifest = load_manifest(MANIFEST_CSV)

    CANONICAL_DIR.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped_ft0 = 0
    skipped_exists = 0
    skipped_special = 0
    errors = 0

    for work_id in sorted(works.keys()):
        work = works[work_id]
        prow = priority.get(work_id)
        if not prow:
            logger.warning(f"{work_id}: not in text_source_priority.csv, skipping")
            errors += 1
            continue

        tier = prow.get("best_text_tier", "FT-0")
        if tier == "FT-0":
            logger.info(f"{work_id}: FT-0, no text available")
            skipped_ft0 += 1
            continue

        source_paths = resolve_source_path(work_id, priority, manifest)
        if not source_paths:
            if work_id == "W010":
                logger.info(f"{work_id}: absorbed into W002 (Part 2.1), no separate canonical file")
                skipped_special += 1
                continue
            logger.warning(f"{work_id}: could not resolve source path")
            errors += 1
            continue

        # Check all source files exist
        missing = [p for p in source_paths if not p.exists()]
        if missing:
            logger.error(f"{work_id}: source file(s) not found: {missing}")
            errors += 1
            continue

        title_norm = work.get("canonical_title_normalized", work_id)
        slug = slugify(title_norm)
        out_name = f"{work_id}_{slug}.txt"
        out_path = CANONICAL_DIR / out_name

        if out_path.exists() and not args.force:
            logger.info(f"{work_id}: {out_name} already exists, skipping (use --force)")
            skipped_exists += 1
            continue

        # For W002-W004, override the best_text_source display to show BSB
        display_prow = dict(prow)
        if work_id in ("W002", "W003", "W004"):
            display_prow["best_text_source"] = prow.get("alternative_source", prow["best_text_source"])
            display_prow["notes"] = (
                f"Canonical uses per-work BSB Tesseract file (FT-3). "
                f"Waentig 1910 (M007, FT-4) covers all parts but cannot be split per-work. "
                f"Original: {prow.get('notes', '')}"
            )
            tier = "FT-3"

        frontmatter = build_frontmatter(work_id, work, display_prow, source_paths, tier)

        # Read and concatenate source texts
        text_parts = []
        for sp in source_paths:
            content = sp.read_text(encoding="utf-8")
            text_parts.append(content)

        if len(text_parts) > 1:
            full_text = ("\n\n" + "=" * 72 + "\n\n").join(text_parts)
        else:
            full_text = text_parts[0]

        # Write canonical file
        out_path.write_text(frontmatter + "\n" + full_text, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        sha256 = hashlib.sha256(out_path.read_bytes()).hexdigest()[:16]
        logger.info(f"{work_id}: created {out_name} ({size_kb:.1f}KB, sha256={sha256})")
        created += 1

    logger.info(
        f"Done: {created} created, {skipped_exists} already existed, "
        f"{skipped_ft0} FT-0 (no text), {skipped_special} special, {errors} errors"
    )


if __name__ == "__main__":
    main()
