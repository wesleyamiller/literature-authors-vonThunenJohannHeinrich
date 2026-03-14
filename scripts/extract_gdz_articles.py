"""Extract text from GDZ article PDFs using Tesseract Fraktur.

Reads the gdz_batch.json and gdz_batch_supplement.json files,
finds the corresponding PDFs in facsimiles/, and runs Tesseract on each.

Usage:
    python scripts/extract_gdz_articles.py [--resume]
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
SCRIPTS = PROJECT_ROOT / "scripts"
LOG_DIR = PROJECT_ROOT / "logs"

# Import the Tesseract extraction function
sys.path.insert(0, str(PROJECT_ROOT))
from scripts.extract_text_tesseract import extract_one, setup_logging


def main():
    parser = argparse.ArgumentParser(description="Extract text from GDZ article PDFs")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = setup_logging("gdz_articles")

    # Load both batch files
    items = []
    for batch_file in ["gdz_batch.json", "gdz_batch_supplement.json"]:
        path = SCRIPTS / batch_file
        if path.exists():
            batch = json.loads(path.read_text(encoding="utf-8"))
            items.extend(batch)

    logger.info("Total GDZ articles: %d", len(items))

    results = {"success": 0, "skipped": 0, "failed": 0}

    for item in items:
        pdf_name = item["output"]
        mid = item.get("manifestation_id", "unknown")
        wid = item.get("work_id", "unknown")
        input_path = FACSIMILES / pdf_name
        output_name = pdf_name.replace(".pdf", "_tesseract-fraktur.txt")
        output_path = EXTRACTED / output_name

        if not input_path.exists():
            logger.warning("PDF not found: %s (skipping)", pdf_name)
            results["skipped"] += 1
            continue

        if output_path.exists() and output_path.stat().st_size > 50:
            logger.info("Already extracted: %s (%d bytes)", output_name,
                         output_path.stat().st_size)
            results["skipped"] += 1
            continue

        logger.info("=== %s / %s: %s ===", mid, wid, pdf_name)
        ok = extract_one(input_path, output_path, "Fraktur", logger, args.resume)
        if ok:
            results["success"] += 1
        else:
            results["failed"] += 1

    logger.info("Done: %d extracted, %d skipped, %d failed",
                 results["success"], results["skipped"], results["failed"])


if __name__ == "__main__":
    main()
