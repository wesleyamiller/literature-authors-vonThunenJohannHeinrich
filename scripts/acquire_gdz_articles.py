"""Download article page ranges from GDZ Goettingen IIIF manifests.

Maps printed page numbers to scan numbers via canvas labels,
downloads only the relevant page images, and combines into per-article PDFs.

Usage:
    python scripts/acquire_gdz_articles.py --batch scripts/gdz_batch.json [--resume]
"""

import argparse
import hashlib
import json
import logging
import re
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

GDZ_MANIFEST_BASE = "https://manifests.sub.uni-goettingen.de/iiif/presentation"
USER_AGENT = "Wesley Miller millerwe@usc.edu - academic corpus project"
RETRY_MAX = 3
RETRY_DELAY = 5

# Cache manifests so we don't re-fetch for articles in the same band
_manifest_cache: dict[str, dict] = {}


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"acquire_gdz_{ts}.log"
    logger = logging.getLogger("gdz_acquire")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def fetch_manifest(ppn: str, logger: logging.Logger) -> dict:
    if ppn in _manifest_cache:
        return _manifest_cache[ppn]
    url = f"{GDZ_MANIFEST_BASE}/{ppn}/manifest"
    logger.info("Fetching manifest: %s", url)
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp:
        manifest = json.loads(resp.read())
    _manifest_cache[ppn] = manifest
    return manifest


def build_page_label_map(manifest: dict) -> dict[str, list[int]]:
    """Map canvas labels (printed page numbers) to lists of 1-based scan indices.

    Some bands contain two sub-volumes with overlapping page numbers,
    so a label like '1' can appear at multiple scan positions.
    """
    label_to_scans: dict[str, list[int]] = {}
    canvases = manifest["sequences"][0]["canvases"]
    for i, canvas in enumerate(canvases):
        label = canvas.get("label", "").strip()
        clean = re.sub(r"[\[\]]", "", label).strip()
        if clean:
            label_to_scans.setdefault(clean, []).append(i + 1)
    return label_to_scans


def find_scan_range(label_map: dict[str, list[int]], page_start: int, page_end: int,
                    total_canvases: int, logger: logging.Logger) -> tuple[int, int]:
    """Convert printed page range to scan range using label map.

    When a page label appears multiple times (two sub-volumes in one band),
    pick the pair where scan_start < scan_end and the gap is consistent
    with the page count.
    """
    starts = label_map.get(str(page_start), [])
    ends = label_map.get(str(page_end), [])

    # Try nearby pages if exact match not found
    if not starts:
        for delta in range(1, 5):
            nearby = label_map.get(str(page_start - delta), [])
            if nearby:
                starts = [s + delta for s in nearby]
                logger.warning("  Page %d not found, estimated from page %d",
                               page_start, page_start - delta)
                break
    if not ends:
        for delta in range(1, 5):
            nearby = label_map.get(str(page_end + delta), [])
            if nearby:
                ends = [s - delta for s in nearby]
                logger.warning("  Page %d not found, estimated from page %d",
                               page_end, page_end + delta)
                break

    # Fall back to offset estimation
    if not starts or not ends:
        offset = _estimate_offset(label_map)
        if not starts:
            starts = [page_start + offset]
            logger.warning("  Page %d not in labels, offset %d -> scan %d",
                           page_start, offset, starts[0])
        if not ends:
            ends = [page_end + offset]
            logger.warning("  Page %d not in labels, offset %d -> scan %d",
                           page_end, offset, ends[0])

    # Pick the best (start, end) pair
    expected_span = page_end - page_start
    best_pair = None
    best_score = float("inf")
    for s in starts:
        for e in ends:
            if e >= s:
                span = e - s
                score = abs(span - expected_span)
                if score < best_score:
                    best_score = score
                    best_pair = (s, e)

    if best_pair is None:
        # Fall back to first occurrence
        best_pair = (starts[0], ends[0] if ends[0] >= starts[0] else ends[-1])

    scan_start, scan_end = best_pair
    scan_start = max(1, min(scan_start, total_canvases))
    scan_end = max(1, min(scan_end, total_canvases))

    return scan_start, scan_end


def _estimate_offset(label_map: dict[str, list[int]]) -> int:
    """Estimate the offset between page numbers and scan numbers."""
    offsets = []
    for label, scans in label_map.items():
        try:
            page_num = int(label)
            offsets.append(scans[0] - page_num)  # use first occurrence
        except ValueError:
            continue
    if offsets:
        offsets.sort()
        return offsets[len(offsets) // 2]
    return 10


def get_image_url(canvas: dict) -> str | None:
    images = canvas.get("images", [])
    if not images:
        return None
    resource = images[0].get("resource", {})
    service = resource.get("service", {})
    base_id = service.get("@id", "")
    if base_id:
        return f"{base_id}/full/full/0/default.jpg"
    url = resource.get("@id", "")
    return url if url else None


def download_page(url: str, dest: Path, logger: logging.Logger) -> bool:
    for attempt in range(1, RETRY_MAX + 1):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=60) as resp:
                data = resp.read()
            dest.write_bytes(data)
            return True
        except (HTTPError, URLError, TimeoutError) as e:
            logger.warning("  Attempt %d failed: %s", attempt, e)
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


def acquire_article(item: dict, logger: logging.Logger, resume: bool = False) -> Path | None:
    ppn = item["ppn"]
    output_name = item["output"]
    page_start = item["page_start"]
    page_end = item["page_end"]
    mid = item.get("manifestation_id", "")
    wid = item.get("work_id", "")

    output_path = FACSIMILES / output_name
    if output_path.exists() and output_path.stat().st_size > 5000:
        logger.info("Already exists: %s (%d bytes), skipping", output_name, output_path.stat().st_size)
        return output_path

    logger.info("=== %s / %s: %s pp. %d-%d ===", mid, wid, ppn, page_start, page_end)

    manifest = fetch_manifest(ppn, logger)
    canvases = manifest["sequences"][0]["canvases"]
    total_canvases = len(canvases)
    logger.info("  Total canvases in band: %d", total_canvases)

    label_map = build_page_label_map(manifest)
    scan_start, scan_end = find_scan_range(label_map, page_start, page_end,
                                            total_canvases, logger)
    logger.info("  Pages %d-%d -> Scans %d-%d (%d pages)",
                page_start, page_end, scan_start, scan_end, scan_end - scan_start + 1)

    # Temp directory
    safe_name = output_name.replace(".pdf", "")
    page_dir = ACQUISITIONS / "tmp_pages" / safe_name
    page_dir.mkdir(parents=True, exist_ok=True)

    ckpt_path = CHECKPOINT_DIR / f"gdz_{safe_name}.json"
    ckpt = load_checkpoint(ckpt_path) if resume else {"completed_pages": [], "total_pages": 0}

    total = scan_end - scan_start + 1
    ckpt["total_pages"] = total
    completed = set(ckpt["completed_pages"])

    for scan_idx in range(scan_start, scan_end + 1):
        page_num = scan_idx - scan_start + 1
        page_file = page_dir / f"page_{page_num:05d}.jpg"

        if page_num in completed and page_file.exists():
            continue

        canvas = canvases[scan_idx - 1]  # 0-based index
        url = get_image_url(canvas)
        if not url:
            logger.warning("  No image URL for scan %d", scan_idx)
            continue

        ok = download_page(url, page_file, logger)
        if ok:
            completed.add(page_num)
            if page_num % 10 == 0:
                logger.info("  Downloaded %d / %d pages", page_num, total)
                ckpt["completed_pages"] = sorted(completed)
                save_checkpoint(ckpt_path, ckpt)
            time.sleep(0.3)
        else:
            logger.error("  FAILED scan %d after %d retries", scan_idx, RETRY_MAX)

    ckpt["completed_pages"] = sorted(completed)
    save_checkpoint(ckpt_path, ckpt)
    logger.info("  Downloaded %d / %d pages", len(completed), total)

    # Combine into PDF
    page_files = sorted(page_dir.glob("page_*.jpg"))
    if not page_files:
        logger.error("  No page images, cannot create PDF")
        return None

    FACSIMILES.mkdir(parents=True, exist_ok=True)
    layout = img2pdf.get_fixed_dpi_layout_fun((300, 300))
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in page_files], layout_fun=layout))

    size_kb = output_path.stat().st_size / 1024
    sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    logger.info("  PDF: %s (%.0f KB, SHA-256: %s)", output_name, size_kb, sha)

    # Cleanup
    for p in page_files:
        p.unlink()
    try:
        page_dir.rmdir()
    except OSError:
        pass
    if ckpt_path.exists():
        ckpt_path.unlink()

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Download GDZ article page ranges")
    parser.add_argument("--batch", required=True, help="JSON batch file")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    batch = json.loads(Path(args.batch).read_text(encoding="utf-8"))
    logger = setup_logging()

    logger.info("Starting GDZ article download: %d items", len(batch))
    results = {"success": 0, "skipped": 0, "failed": 0}

    for item in batch:
        try:
            path = acquire_article(item, logger, args.resume)
            if path:
                results["success"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            logger.error("Error processing %s: %s", item.get("output", "?"), e)
            results["failed"] += 1

    logger.info("Done: %d success, %d failed", results["success"], results["failed"])


if __name__ == "__main__":
    main()
