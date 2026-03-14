# State Pack: Johann Heinrich von Thuenen Corpus Project

**Last updated:** 2026-03-13 (session 5, continued)

## Current Scope Flags
- active_scope: works_by
- include_works_about: false
- include_influence_graph: false

## Authority-Cluster Status
- **Status:** variants_harvested (ready for authority_cluster_locked)
- **Person ID:** P001
- **GND:** 118622366 | **VIAF:** 94496 | **Wikidata:** Q76787 | **LoC:** n85127362 | **ISNI:** 0000000112036754
- **Name variants ingested:** 14

## Registry Counts
| Entity | Count |
|--------|-------|
| Works | 37 |
| Expressions | 43 |
| Manifestations | 44 (40 located, 4 discovered) |
| Routes | 39 |
| Relation edges | 38 |
| Archive units | 8 |
| Acquired artifacts | 82 files (~896MB) |
| Works with text | 33/37 (89%) |

## Manifestation Routing: 91% Complete
**Located (40):** All Der isolirte Staat editions (1826-1910), all 27 Neue Annalen articles, both Doberan conference papers, both French translations, English translation.

**Still discovered (4):**
- M006: 1875 3rd ed placeholder (already covered by M014/M015 vols)
- M017: Landw. Calender 1818 (W012, obscure periodical)
- M039: Schweriner Anzeblatt (W034, newspaper)
- M042: Landw. Annalen patriot. Vereins 1846 (W037)

## Acquired Artifacts

**Major book facsimiles (10 PDFs, ~540MB):**
- 1842 2nd ed Part 1 (Google Books, 22MB)
- 1850 Part 2.1 (BSB/IIIF, 302pp, 113MB)
- 1863 Part 2.2 (BSB/IIIF, 470pp, 159MB)
- 1863 Part 3 (BSB/IIIF, 160pp, 51MB)
- 1875 3rd ed Vol 1+3 (IA, 30MB)
- 1910 Waentig (IA, 28MB)
- 1851 Laverriere French (Gallica/IIIF, 372pp, 105MB)
- Neue Annalen Vol 17/1 + 18/1 (IA, 29MB)

**GDZ article facsimiles (26 PDFs, ~350MB):**
- 22 articles from main GDZ batch (Bands 1,4,6,8,10,16,17,18,19,21,23,24,25,26,28)
- 4 articles from supplement batch (Bands 17,18 — former IA-only articles)
- Downloaded via IIIF with printed-page-to-scan mapping

**Structured text (3 files, 12MB):** DTA TEI XML + txt + TCF (1826 Part 1)
**OCR text (6 files, 4MB):** IA ABBYY djvu.txt for Waentig, 1875 vols, Forscherleben, NA vols

**Extracted text (33 files, ~3.8MB):**
- 1842 2nd ed embedded GBooks OCR (1.1MB, FT-4)
- 1875 Vol 3 docling (219KB, FT-3)
- 1863 Part 3 Tesseract Fraktur (206KB, FT-3)
- 1850 Part 2.1 Tesseract Fraktur (453KB, FT-3)
- 1863 Part 2.2 Tesseract Fraktur (646KB, FT-3)
- 1851 French Tesseract fra (588KB, FT-3)
- 26 GDZ Neue Annalen articles Tesseract Fraktur (760KB total, FT-3)
- 1 superseded docling extraction (Part 3, FT-1)

## Scripts
- `scripts/acquire_iiif_pdf.py` — downloads page images from IIIF manifests (BSB, Gallica, GDZ) and combines into PDF
- `scripts/acquire_gdz_articles.py` — downloads article page ranges from GDZ with printed-page-to-scan mapping
- `scripts/extract_text_docling.py` — extracts text from PDFs using docling (good for IA embedded OCR, crashes >50MB)
- `scripts/extract_text_tesseract.py` — page-by-page Tesseract OCR with checkpoint/resume (~10 pages/min)
- `scripts/extract_gdz_articles.py` — batch Tesseract extraction for all GDZ article PDFs
- `scripts/build_canonical.py` — assembles per-work canonical text files from best sources into `data/canonical/`

## Text Extraction Status
| Source | Method | Quality | Status |
|--------|--------|---------|--------|
| DTA 1826 Part 1 (M009) | DTA structured | FT-7 (0.95) | Complete |
| 1910 Waentig (M007) | IA ABBYY OCR | FT-4 (0.85) | Complete |
| 1842 2nd ed (M002) | GBooks embedded | FT-4 (0.75) | Complete |
| 1863 Part 3 (M005) | Tesseract Fraktur | FT-3 (0.70) | Complete |
| 1850 Part 2.1 (M003) | Tesseract Fraktur | FT-3 (0.70) | Complete |
| 1863 Part 2.2 (M004) | Tesseract Fraktur | FT-3 (0.70) | Complete |
| 1851 French (M044) | Tesseract fra | FT-3 (0.70) | Complete |
| 1875 Vol 3 (M015) | Docling from IA | FT-3 (0.55) | Complete |
| GDZ Neue Annalen (26 articles) | Tesseract Fraktur | FT-3 (0.65) | Complete |

## OCR Pipeline Findings
- **Tesseract Fraktur** (best_tessdata model): Excellent on BSB and GDZ IIIF scans at 2x render. FT-3. ~10 pages/min.
- **Docling RapidOCR:** Unusable on Fraktur (FT-0/FT-1). Only works on IA PDFs with embedded ABBYY text.
- **Google Books embedded OCR:** Good for Fraktur (FT-4). Direct extraction via pypdfium2.
- **IA ABBYY OCR:** Good for Antiqua (FT-4), very poor for Fraktur (FT-0/FT-1).
- **GDZ IIIF manifest base URL:** `https://manifests.sub.uni-goettingen.de/iiif/presentation/{PPN}/manifest`

## Text Source Priority
See `data/acquisitions/text_source_priority.csv` for per-work mapping.
- W001 (Part 1): DTA TEI (FT-7) — definitive
- W001 (Part 1, 2nd ed): 1842 GBooks embedded OCR (FT-4)
- W002-W004 (Parts 2-3): 1910 Waentig OCR (FT-4) + BSB Tesseract Fraktur (FT-3)
- W006-W033 (Neue Annalen): All 28 articles extracted from GDZ via Tesseract Fraktur (FT-3)
- W010 (fragment): Absorbed into 1850 Part 2.1 (M003)
- W035-W036 (Doberan): BSB bsb10228360 Tesseract Fraktur (FT-3)

## Remaining FT-0 Works (4 of 37)
| Work | Reason | Possible Action |
|------|--------|-----------------|
| W005 | 1803 essay. No digitized source | Rare. May not exist digitally |
| W012 | Landw. Calender 1818 | Rare periodical. M017 discovered but unlocated |
| W034 | Schweriner Anzeblatt | Newspaper. M039 discovered but unlocated |
| W037 | Landw. Annalen 1846 | Rare. M042 discovered but unlocated |

## Key Finding: BSB Has Doberan Series
BSB has the full "Amtlicher Bericht" series as bsb10228356-bsb10228369 (volumes 1-14, 1837-1851). The Doberan 1841 volume is bsb10228360. This bypassed the Google Books CAPTCHA problem.

## Canonical Text Files
- **Location:** `data/canonical/` (32 files, 2.7MB total)
- **Script:** `scripts/build_canonical.py` (rerunnable with `--force`)
- **Coverage:** 32/37 works (W010 absorbed into W002; 4 works at FT-0)
- **Format:** YAML frontmatter (provenance, tier, source) + full text
- W001: DTA plain text (FT-7) — gold standard
- W002-W004: BSB Tesseract Fraktur (FT-3) per-work files
- W006-W033: GDZ Tesseract Fraktur (FT-3)
- W035-W036: BSB Tesseract Fraktur (FT-3)
- W031: Multi-part concatenation from 3 GDZ band extractions

## Quality Review Findings
- **W001 (FT-7):** 5/5 — gold-standard DTA transcription, near-perfect
- **FT-3 files (BSB/GDZ Tesseract):** 3-4/5 — readable with systematic issues:
  - `ch`/`ck` → `<`/`>` substitution (Tesseract Fraktur ligature confusion) — universal, machine-correctable
  - Long-s (ſ) correctly preserved throughout
  - Page-number header bleed in GDZ files (lone page numbers as lines)
  - Fragment/bleed-through lines: 0.9-3.9% of non-blank lines
  - Library stamps on BSB files (first few pages)
  - Tabular data significantly garbled (W031 experimental tables)
  - Conference context contamination in W035 (preceding agenda items)
- **Best FT-3:** W028 (4/5) — clean GDZ scan, sparse artifacts
- **Weakest FT-3:** W031 (3/5) — experimental tables degraded, highest garble rate

## Next Steps
1. **Search for 3 remaining unrouted** manifestations (M017, M039, M042)
2. **Post-processing** — consider regex cleanup of `<`/`>` → `ch`/`ck` substitution across FT-3 files
3. **Authority cluster lock** — finalize person authority with all 14 name variants
