"""Extract text from PDF facsimiles using docling.

Produces markdown output with structure preservation (headings, tables, footnotes).
Implements checkpoint/resume per CLAUDE.md section 1.

Usage:
    python scripts/extract_text_docling.py --input PATH --output PATH
    python scripts/extract_text_docling.py --batch scripts/extraction_batch.json [--resume]
    python scripts/extract_text_docling.py --all [--resume]
"""

import argparse
import hashlib
import json
import logging
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ACQUISITIONS = PROJECT_ROOT / "data" / "acquisitions"
FACSIMILES = ACQUISITIONS / "facsimiles"
EXTRACTED = ACQUISITIONS / "extracted"
CHECKPOINT_DIR = PROJECT_ROOT / "progress" / "checkpoints"
LOG_DIR = PROJECT_ROOT / "logs"
MANIFEST_PATH = ACQUISITIONS / "fulltext_manifest.csv"


def setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"extract_docling_{name}_{ts}.log"
    logger = logging.getLogger(f"docling_{name}")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def extract_one(input_path: Path, output_path: Path, logger: logging.Logger) -> bool:
    """Extract text from a single PDF using docling."""
    if output_path.exists() and output_path.stat().st_size > 100:
        logger.info("Output already exists: %s (%d bytes), skipping",
                     output_path.name, output_path.stat().st_size)
        return True

    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        return False

    size_mb = input_path.stat().st_size / (1024 * 1024)
    logger.info("Extracting: %s (%.1f MB)", input_path.name, size_mb)

    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()

        t0 = time.time()
        result = converter.convert(str(input_path))
        elapsed = time.time() - t0

        # Export as markdown (preserves structure)
        md_text = result.document.export_to_markdown()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md_text, encoding="utf-8")

        out_size = output_path.stat().st_size
        sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
        logger.info("Extracted: %s -> %s (%.1f KB, %.0fs, SHA-256: %s)",
                     input_path.name, output_path.name,
                     out_size / 1024, elapsed, sha)
        return True

    except Exception as e:
        logger.error("Extraction failed for %s: %s", input_path.name, e)
        return False


def get_pending_extractions() -> list[dict]:
    """Read fulltext_manifest.csv and return items with pending_extraction status."""
    items = []
    if not MANIFEST_PATH.exists():
        return items

    import csv
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("text_extraction_method") == "pending_extraction":
                pdf_path = row.get("canonical_facsimile_path", "")
                if pdf_path:
                    manifest_id = row.get("manifestation_id", "unknown")
                    input_path = ACQUISITIONS / pdf_path
                    stem = Path(pdf_path).stem
                    output_path = EXTRACTED / f"{stem}_docling.md"
                    items.append({
                        "manifestation_id": manifest_id,
                        "input": str(input_path),
                        "output": str(output_path),
                    })
    return items


def load_checkpoint(ckpt_path: Path) -> dict:
    if ckpt_path.exists():
        return json.loads(ckpt_path.read_text(encoding="utf-8"))
    return {"completed": [], "failed": []}


def save_checkpoint(ckpt_path: Path, state: dict):
    ckpt_path.parent.mkdir(parents=True, exist_ok=True)
    ckpt_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDFs using docling")
    parser.add_argument("--input", help="Single input PDF path")
    parser.add_argument("--output", help="Single output markdown path")
    parser.add_argument("--batch", help="JSON batch file")
    parser.add_argument("--all", action="store_true", help="Process all pending_extraction items from manifest")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    if args.input and args.output:
        logger = setup_logging(Path(args.input).stem)
        extract_one(Path(args.input), Path(args.output), logger)

    elif args.batch:
        batch = json.loads(Path(args.batch).read_text(encoding="utf-8"))
        ckpt_path = CHECKPOINT_DIR / "extraction_batch.json"
        ckpt = load_checkpoint(ckpt_path) if args.resume else {"completed": [], "failed": []}
        completed_set = set(ckpt["completed"])

        for item in batch:
            name = Path(item["input"]).stem
            if name in completed_set:
                print(f"Skipping (already done): {name}")
                continue

            logger = setup_logging(name)
            ok = extract_one(Path(item["input"]), Path(item["output"]), logger)
            if ok:
                ckpt["completed"].append(name)
            else:
                ckpt["failed"].append(name)
            save_checkpoint(ckpt_path, ckpt)

    elif args.all:
        items = get_pending_extractions()
        if not items:
            print("No pending extractions found in manifest.")
            return

        ckpt_path = CHECKPOINT_DIR / "extraction_all.json"
        ckpt = load_checkpoint(ckpt_path) if args.resume else {"completed": [], "failed": []}
        completed_set = set(ckpt["completed"])

        print(f"Found {len(items)} pending extractions, {len(completed_set)} already completed")

        for item in items:
            mid = item["manifestation_id"]
            if mid in completed_set:
                print(f"Skipping {mid} (already done)")
                continue

            logger = setup_logging(mid)
            ok = extract_one(Path(item["input"]), Path(item["output"]), logger)
            if ok:
                ckpt["completed"].append(mid)
            else:
                ckpt["failed"].append(mid)
            save_checkpoint(ckpt_path, ckpt)

        print(f"\nDone: {len(ckpt['completed'])} completed, {len(ckpt['failed'])} failed")
    else:
        parser.error("Provide --input/--output, --batch, or --all")


if __name__ == "__main__":
    main()
