"""Extract text from PDF facsimiles using Tesseract OCR.

Optimized for Fraktur text. Renders pages from PDF at 2x scale,
runs Tesseract with the Fraktur model, and combines output.
Implements checkpoint/resume per CLAUDE.md section 1.

Usage:
    python scripts/extract_text_tesseract.py --input PATH --output PATH [-l Fraktur]
    python scripts/extract_text_tesseract.py --all [--resume]
"""

import argparse
import hashlib
import json
import logging
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ACQUISITIONS = PROJECT_ROOT / "data" / "acquisitions"
FACSIMILES = ACQUISITIONS / "facsimiles"
EXTRACTED = ACQUISITIONS / "extracted"
CHECKPOINT_DIR = PROJECT_ROOT / "progress" / "checkpoints"
LOG_DIR = PROJECT_ROOT / "logs"
TESSDATA_DIR = PROJECT_ROOT / "tools" / "tessdata"
TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
MANIFEST_PATH = ACQUISITIONS / "fulltext_manifest.csv"

DEFAULT_LANG = "Fraktur"
RENDER_SCALE = 2  # render pages at 2x for OCR


def setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"extract_tesseract_{name}_{ts}.log"
    logger = logging.getLogger(f"tess_{name}")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def ocr_page(image_path: Path, lang: str) -> str:
    """Run Tesseract on a single page image."""
    out_base = image_path.with_suffix("")
    env = {"TESSDATA_PREFIX": str(TESSDATA_DIR)}
    result = subprocess.run(
        [TESSERACT_EXE, str(image_path), str(out_base), "-l", lang],
        capture_output=True, text=True, env={**dict(__import__("os").environ), **env},
        timeout=120,
    )
    out_file = Path(str(out_base) + ".txt")
    if out_file.exists():
        text = out_file.read_text(encoding="utf-8")
        out_file.unlink()
        return text
    return ""


def extract_one(input_path: Path, output_path: Path, lang: str,
                logger: logging.Logger, resume: bool = False) -> bool:
    """Extract text from a PDF using Tesseract page-by-page."""
    if output_path.exists() and output_path.stat().st_size > 100:
        logger.info("Output exists: %s (%d bytes), skipping", output_path.name,
                     output_path.stat().st_size)
        return True

    if not input_path.exists():
        logger.error("Input not found: %s", input_path)
        return False

    from pypdfium2 import PdfDocument

    size_mb = input_path.stat().st_size / (1024 * 1024)
    logger.info("Extracting: %s (%.1f MB, lang=%s)", input_path.name, size_mb, lang)

    doc = PdfDocument(str(input_path))
    total = len(doc)
    logger.info("Total pages: %d", total)

    safe_name = output_path.stem
    ckpt_path = CHECKPOINT_DIR / f"tess_{safe_name}.json"
    ckpt = {"completed": {}, "failed": []}
    if resume and ckpt_path.exists():
        ckpt = json.loads(ckpt_path.read_text(encoding="utf-8"))
        logger.info("Resuming: %d pages already done", len(ckpt["completed"]))

    pages_text = {}
    t0 = time.time()

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(total):
            page_num = i + 1
            page_key = str(page_num)

            if page_key in ckpt["completed"]:
                pages_text[page_num] = ckpt["completed"][page_key]
                continue

            try:
                page = doc[i]
                bitmap = page.render(scale=RENDER_SCALE)
                pil_image = bitmap.to_pil()
                img_path = Path(tmpdir) / f"page_{page_num:05d}.png"
                pil_image.save(str(img_path))

                text = ocr_page(img_path, lang)
                pages_text[page_num] = text.strip()
                ckpt["completed"][page_key] = text.strip()

                img_path.unlink(missing_ok=True)

                if page_num % 25 == 0:
                    elapsed = time.time() - t0
                    rate = page_num / elapsed * 60
                    logger.info("  Page %d/%d (%.0f pages/min)", page_num, total, rate)
                    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
                    ckpt_path.write_text(json.dumps(ckpt), encoding="utf-8")

            except Exception as e:
                logger.warning("  Page %d failed: %s", page_num, e)
                ckpt["failed"].append(page_num)
                pages_text[page_num] = ""

    # Combine all pages
    parts = []
    for pn in sorted(pages_text.keys()):
        text = pages_text[pn]
        if text:
            parts.append(f"--- Page {pn} ---\n{text}")

    full_text = "\n\n".join(parts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_text, encoding="utf-8")

    elapsed = time.time() - t0
    sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    logger.info("Done: %s (%.1f KB, %d pages, %.0fs, SHA-256: %s)",
                 output_path.name, output_path.stat().st_size / 1024,
                 len(pages_text), elapsed, sha)

    # Cleanup checkpoint
    if ckpt_path.exists():
        ckpt_path.unlink()

    return True


def get_fraktur_extractions() -> list[dict]:
    """Get items from manifest that need Fraktur OCR."""
    items = []
    if not MANIFEST_PATH.exists():
        return items
    import csv
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            method = row.get("text_extraction_method", "")
            if "fraktur" in method.lower():
                pdf = row.get("canonical_facsimile_path", "")
                if pdf:
                    mid = row.get("manifestation_id", "unknown")
                    stem = Path(pdf).stem
                    items.append({
                        "manifestation_id": mid,
                        "input": str(ACQUISITIONS / pdf),
                        "output": str(EXTRACTED / f"{stem}_tesseract-fraktur.txt"),
                        "lang": "Fraktur",
                    })
    return items


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDFs using Tesseract")
    parser.add_argument("--input", help="Input PDF path")
    parser.add_argument("--output", help="Output text path")
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG, help="Tesseract language model")
    parser.add_argument("--all", action="store_true", help="Process all fraktur_ocr items from manifest")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    if args.input and args.output:
        logger = setup_logging(Path(args.input).stem)
        extract_one(Path(args.input), Path(args.output), args.lang, logger, args.resume)
    elif args.all:
        items = get_fraktur_extractions()
        if not items:
            print("No Fraktur extraction items found in manifest.")
            return
        for item in items:
            logger = setup_logging(item["manifestation_id"])
            extract_one(Path(item["input"]), Path(item["output"]),
                         item.get("lang", DEFAULT_LANG), logger, args.resume)
    else:
        parser.error("Provide --input/--output or --all")


if __name__ == "__main__":
    main()
