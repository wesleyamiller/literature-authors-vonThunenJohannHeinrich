"""Download page images from IIIF manifests and combine into PDF.

Supports BSB/MDZ and GDZ Goettingen IIIF endpoints.
Implements checkpoint/resume per CLAUDE.md §1.

Usage:
    python -m scripts.acquire_iiif_pdf --manifest-url URL --output PATH [--resume]
    python -m scripts.acquire_iiif_pdf --batch scripts/bsb_batch.json [--resume]
"""

import argparse
import hashlib
import json
import logging
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import img2pdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ACQUISITIONS = PROJECT_ROOT / "data" / "acquisitions"
FACSIMILES = ACQUISITIONS / "facsimiles"
CHECKPOINT_DIR = PROJECT_ROOT / "progress" / "checkpoints"
LOG_DIR = PROJECT_ROOT / "logs"

USER_AGENT = "Wesley Miller millerwe@usc.edu - academic corpus project"
IIIF_IMAGE_WIDTH = 0  # 0 = full resolution
RETRY_MAX = 3
RETRY_DELAY = 5  # seconds


def setup_logging(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"acquire_iiif_{name}_{ts}.log"
    logger = logging.getLogger(f"iiif_{name}")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def fetch_manifest(manifest_url: str) -> dict:
    req = Request(manifest_url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def get_canvas_image_urls(manifest: dict, width: int = IIIF_IMAGE_WIDTH) -> list[str]:
    """Extract ordered image URLs from IIIF v2 manifest."""
    urls = []
    sequences = manifest.get("sequences", [])
    if not sequences:
        raise ValueError("No sequences in manifest")
    canvases = sequences[0].get("canvases", [])
    for canvas in canvases:
        images = canvas.get("images", [])
        if not images:
            continue
        resource = images[0].get("resource", {})
        service = resource.get("service", {})
        base_id = service.get("@id", "")
        if base_id:
            # IIIF Image API: {base}/{region}/{size}/{rotation}/{quality}.{format}
            if width > 0:
                url = f"{base_id}/full/{width},/0/default.jpg"
            else:
                url = f"{base_id}/full/full/0/default.jpg"
            urls.append(url)
        else:
            # Fallback: use resource @id directly
            url = resource.get("@id", "")
            if url:
                urls.append(url)
    return urls


def download_page(url: str, dest: Path, logger: logging.Logger) -> bool:
    for attempt in range(1, RETRY_MAX + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=60) as resp:
                data = resp.read()
            dest.write_bytes(data)
            return True
        except (HTTPError, URLError, TimeoutError) as e:
            logger.warning("  Attempt %d failed for %s: %s", attempt, url, e)
            if attempt < RETRY_MAX:
                time.sleep(RETRY_DELAY * attempt)
    return False


def load_checkpoint(ckpt_path: Path) -> dict:
    if ckpt_path.exists():
        return json.loads(ckpt_path.read_text(encoding="utf-8"))
    return {"completed_pages": [], "total_pages": 0}


def save_checkpoint(ckpt_path: Path, state: dict):
    ckpt_path.parent.mkdir(parents=True, exist_ok=True)
    ckpt_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def acquire_one(manifest_url: str, output_name: str, resume: bool,
                logger: logging.Logger, page_start: int = 0, page_end: int = 0) -> Path | None:
    """Download pages from a IIIF manifest and combine into PDF.

    If page_start and page_end are set, only download that range (1-indexed).
    """
    output_path = FACSIMILES / output_name
    if output_path.exists() and output_path.stat().st_size > 10000:
        logger.info("Output already exists: %s (%d bytes), skipping",
                     output_path.name, output_path.stat().st_size)
        return output_path

    # Temp directory for page images
    safe_name = output_name.replace(".pdf", "")
    page_dir = ACQUISITIONS / "tmp_pages" / safe_name
    page_dir.mkdir(parents=True, exist_ok=True)

    ckpt_path = CHECKPOINT_DIR / f"iiif_{safe_name}.json"
    ckpt = load_checkpoint(ckpt_path) if resume else {"completed_pages": [], "total_pages": 0}

    logger.info("Fetching manifest: %s", manifest_url)
    manifest = fetch_manifest(manifest_url)
    title = manifest.get("label", "unknown")
    logger.info("Manifest title: %s", title)

    all_image_urls = get_canvas_image_urls(manifest)
    total_in_manifest = len(all_image_urls)
    logger.info("Total pages in manifest: %d", total_in_manifest)

    # Apply page range filter if specified
    if page_start > 0 and page_end > 0:
        image_urls = all_image_urls[page_start - 1:page_end]
        logger.info("Page range: %d-%d (%d pages)", page_start, page_end, len(image_urls))
    else:
        image_urls = all_image_urls

    total = len(image_urls)
    ckpt["total_pages"] = total

    completed = set(ckpt["completed_pages"])
    logger.info("Already completed: %d pages", len(completed))

    for i, url in enumerate(image_urls):
        page_num = i + 1
        page_file = page_dir / f"page_{page_num:05d}.jpg"

        if page_num in completed and page_file.exists():
            continue

        ok = download_page(url, page_file, logger)
        if ok:
            completed.add(page_num)
            if page_num % 25 == 0:
                logger.info("  Downloaded %d / %d pages", page_num, total)
                ckpt["completed_pages"] = sorted(completed)
                save_checkpoint(ckpt_path, ckpt)
            # Small delay to be polite
            time.sleep(0.3)
        else:
            logger.error("  FAILED page %d after %d retries", page_num, RETRY_MAX)

    ckpt["completed_pages"] = sorted(completed)
    save_checkpoint(ckpt_path, ckpt)
    logger.info("Downloaded %d / %d pages", len(completed), total)

    # Combine into PDF
    page_files = sorted(page_dir.glob("page_*.jpg"))
    if not page_files:
        logger.error("No page images found, cannot create PDF")
        return None

    logger.info("Combining %d pages into PDF: %s", len(page_files), output_path.name)
    FACSIMILES.mkdir(parents=True, exist_ok=True)
    # Set DPI to 300 so pages have sensible physical dimensions for OCR
    # (IIIF JPEGs lack DPI metadata; img2pdf defaults to 96 -> oversized pages)
    layout = img2pdf.get_fixed_dpi_layout_fun((300, 300))
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in page_files], layout_fun=layout))

    size_mb = output_path.stat().st_size / (1024 * 1024)
    sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    logger.info("PDF created: %s (%.1f MB, SHA-256: %s)", output_path.name, size_mb, sha)

    # Cleanup page images
    for p in page_files:
        p.unlink()
    try:
        page_dir.rmdir()
    except OSError:
        pass

    # Cleanup checkpoint
    if ckpt_path.exists():
        ckpt_path.unlink()

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Download IIIF manifest pages and combine into PDF")
    parser.add_argument("--manifest-url", help="Single IIIF manifest URL")
    parser.add_argument("--output", help="Output PDF filename (in facsimiles/)")
    parser.add_argument("--page-start", type=int, default=0, help="First page to download (1-indexed)")
    parser.add_argument("--page-end", type=int, default=0, help="Last page to download (inclusive)")
    parser.add_argument("--batch", help="JSON batch file with list of {manifest_url, output}")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    if args.batch:
        batch = json.loads(Path(args.batch).read_text(encoding="utf-8"))
        for item in batch:
            logger = setup_logging(item["output"].replace(".pdf", ""))
            ps = item.get("page_start", 0)
            pe = item.get("page_end", 0)
            acquire_one(item["manifest_url"], item["output"], args.resume, logger, ps, pe)
    elif args.manifest_url and args.output:
        logger = setup_logging(args.output.replace(".pdf", ""))
        acquire_one(args.manifest_url, args.output, args.resume, logger,
                     args.page_start, args.page_end)
    else:
        parser.error("Provide either --batch or both --manifest-url and --output")


if __name__ == "__main__":
    main()
