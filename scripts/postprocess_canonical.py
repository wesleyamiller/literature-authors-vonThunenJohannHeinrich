"""Post-process canonical text files to fix systematic Tesseract Fraktur OCR errors.

Applies the following corrections to FT-3 canonical files in data/canonical/:
1. ch/ck ligature restoration: < → ch, > → ck (only in word context)
2. Page-number header bleed removal: lone 1-4 digit lines from journal headers
3. Library stamp removal: BSB barcode/stamp patterns
4. Short fragment line removal: lines under 4 chars that are scan bleed-through

Does NOT modify:
- W001 (FT-7 DTA text, already gold standard)
- YAML frontmatter headers
- Lines containing actual mathematical operators (standalone <, >, =>, etc.)

Usage:
    python -m scripts.postprocess_canonical [--dry-run] [--force]

    --dry-run   Show what would be changed without modifying files
    --force     Overwrite even if already post-processed
"""

import argparse
import hashlib
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CANONICAL_DIR = BASE_DIR / "data" / "canonical"
LOG_DIR = BASE_DIR / "logs"

# Files to skip (FT-7 or non-Fraktur sources)
SKIP_WORK_IDS = {"W001"}

# BSB library stamp patterns
BSB_STAMP_RE = re.compile(
    r"^(<?\d{10,}|Bayer\.\s*Staatsbibliothek|Ministerialforst|Bücherei|"
    r"Bayerische\s+Staats|BIBLIOTHEK)$",
    re.IGNORECASE,
)

# Page number header bleed: lone 1-4 digit number on a line
PAGE_NUM_BLEED_RE = re.compile(r"^\d{1,4}\s*$")

# Fragment line: very short non-blank line (scan bleed-through artifacts)
FRAGMENT_MAX_CHARS = 3

# Fraktur ligature patterns — only substitute when inside a word
# Letter class for German/Fraktur (includes long-s ſ and umlauts)
_L = r"A-Za-z\u00e4\u00f6\u00fc\u00c4\u00d6\u00dc\u00df\u017f"

# Step 1: <h → ch (consume the redundant h; e.g. dur<h → durch, not durchh)
ANGLE_LEFT_H = re.compile(rf"(?<=[{_L}])<h")
# Step 2: remaining < → ch when adjacent to a letter
ANGLE_LEFT_IN_WORD = re.compile(rf"(?<=[{_L}])<|<(?=[{_L}])")
# > → ck when adjacent to a letter
ANGLE_RIGHT_IN_WORD = re.compile(rf"(?<=[{_L}])>|>(?=[{_L}])")


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"postprocess_canonical_{ts}.log"
    logger = logging.getLogger("postprocess")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def extract_work_id(filename: str) -> str:
    """Extract work ID (e.g. 'W001') from canonical filename."""
    return filename.split("_")[0]


def is_page_marker(line: str) -> bool:
    """Check if line is a --- Page N --- marker."""
    return line.startswith("--- Page ") and line.rstrip().endswith(" ---")


def is_separator(line: str) -> bool:
    """Check if line is a multi-part separator (===...)."""
    stripped = line.strip()
    return len(stripped) > 10 and all(c == "=" for c in stripped)


def process_line(line: str, stats: dict) -> str | None:
    """Process a single line. Returns processed line or None to remove it."""
    stripped = line.rstrip()

    # Preserve page markers and separators
    if is_page_marker(stripped) or is_separator(stripped):
        return line

    # Remove BSB library stamps
    if BSB_STAMP_RE.match(stripped):
        stats["stamps_removed"] += 1
        return None

    # Remove page number header bleed (but not in tables — check context)
    if PAGE_NUM_BLEED_RE.match(stripped):
        stats["page_nums_removed"] += 1
        return None

    # Remove very short fragment lines (bleed-through)
    if 0 < len(stripped) <= FRAGMENT_MAX_CHARS and not stripped.isdigit():
        # Don't remove if it looks like a Roman numeral or meaningful abbreviation
        if not re.match(r"^[IVXLCivxlc]+\.?$", stripped):
            stats["fragments_removed"] += 1
            return None

    # ch/ck ligature restoration
    new_line = line
    # < → ch: first handle <h → ch (avoid durchh), then remaining < → ch
    ch_h_count = len(ANGLE_LEFT_H.findall(new_line))
    new_line = ANGLE_LEFT_H.sub("ch", new_line)
    ch_count = len(ANGLE_LEFT_IN_WORD.findall(new_line))
    new_line = ANGLE_LEFT_IN_WORD.sub("ch", new_line)
    stats["ch_restored"] += ch_h_count + ch_count

    # > → ck (in word context)
    ck_count = len(ANGLE_RIGHT_IN_WORD.findall(new_line))
    new_line = ANGLE_RIGHT_IN_WORD.sub("ck", new_line)
    stats["ck_restored"] += ck_count

    return new_line


def process_file(path: Path, dry_run: bool, logger: logging.Logger) -> dict:
    """Process a single canonical file. Returns stats dict."""
    work_id = extract_work_id(path.name)
    stats = {
        "work_id": work_id,
        "ch_restored": 0,
        "ck_restored": 0,
        "stamps_removed": 0,
        "page_nums_removed": 0,
        "fragments_removed": 0,
        "lines_in": 0,
        "lines_out": 0,
        "modified": False,
    }

    if work_id in SKIP_WORK_IDS:
        logger.info(f"{work_id}: skipped (FT-7, no processing needed)")
        return stats

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Split into frontmatter and body
    fm_end = -1
    fm_count = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            fm_count += 1
            if fm_count == 2:
                fm_end = i
                break

    if fm_end < 0:
        logger.warning(f"{work_id}: no YAML frontmatter found, skipping")
        return stats

    frontmatter = lines[: fm_end + 1]
    body = lines[fm_end + 1 :]
    stats["lines_in"] = len(body)

    # Process body lines
    processed = []
    for line in body:
        result = process_line(line, stats)
        if result is not None:
            processed.append(result)

    stats["lines_out"] = len(processed)
    total_changes = (
        stats["ch_restored"]
        + stats["ck_restored"]
        + stats["stamps_removed"]
        + stats["page_nums_removed"]
        + stats["fragments_removed"]
    )

    if total_changes > 0:
        stats["modified"] = True
        # Add post-processing note to frontmatter
        # Insert before closing ---
        pp_note = f'postprocessed: "ch/ck ligature restoration, stamp/fragment removal"'
        if not any("postprocessed:" in fl for fl in frontmatter):
            frontmatter.insert(fm_end, pp_note)

        if not dry_run:
            new_content = "\n".join(frontmatter + processed)
            path.write_text(new_content, encoding="utf-8")

        logger.info(
            f"{work_id}: {stats['ch_restored']} ch, {stats['ck_restored']} ck restored; "
            f"{stats['stamps_removed']} stamps, {stats['page_nums_removed']} page nums, "
            f"{stats['fragments_removed']} fragments removed"
            f"{' (dry-run)' if dry_run else ''}"
        )
    else:
        logger.info(f"{work_id}: no changes needed")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Post-process canonical text files")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--force", action="store_true", help="Re-process already processed files")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info(f"Starting post-processing {'(dry-run)' if args.dry_run else ''}")

    files = sorted(CANONICAL_DIR.glob("W*.txt"))
    all_stats = []
    totals = {
        "files_processed": 0,
        "files_modified": 0,
        "total_ch": 0,
        "total_ck": 0,
        "total_stamps": 0,
        "total_page_nums": 0,
        "total_fragments": 0,
    }

    for fp in files:
        # Check if already post-processed (unless --force)
        if not args.force:
            content = fp.read_text(encoding="utf-8")
            if "postprocessed:" in content.split("---")[1] if content.count("---") >= 2 else "":
                logger.info(f"{extract_work_id(fp.name)}: already post-processed, skipping (use --force)")
                continue

        stats = process_file(fp, args.dry_run, logger)
        all_stats.append(stats)
        totals["files_processed"] += 1
        if stats["modified"]:
            totals["files_modified"] += 1
        totals["total_ch"] += stats["ch_restored"]
        totals["total_ck"] += stats["ck_restored"]
        totals["total_stamps"] += stats["stamps_removed"]
        totals["total_page_nums"] += stats["page_nums_removed"]
        totals["total_fragments"] += stats["fragments_removed"]

    logger.info(
        f"\nSummary: {totals['files_processed']} files processed, "
        f"{totals['files_modified']} modified. "
        f"Restored: {totals['total_ch']} ch + {totals['total_ck']} ck. "
        f"Removed: {totals['total_stamps']} stamps, {totals['total_page_nums']} page nums, "
        f"{totals['total_fragments']} fragments."
    )


if __name__ == "__main__":
    main()
