# Johann Heinrich von Thuenen: Complete Works Corpus

A machine-readable corpus of the writings of **Johann Heinrich von Thuenen** (1783-1850), the German economist and agriculturalist best known for *Der isolirte Staat* and the von Thuenen model of land use.

## Corpus Coverage

| Category | Count |
|----------|-------|
| Works identified | 37 |
| Works with machine-readable text | 33 (89%) |
| Canonical text files | 32 |
| Fulltext quality: FT-7 (scholarly TEI) | 1 |
| Fulltext quality: FT-3+ (OCR) | 32 |
| Remaining undigitized | 4 |

### Works Included

- **Der isolirte Staat** Parts 1-3 (1826-1863) -- the complete *Isolated State*, including posthumous parts
- **28 periodical articles** from *Neue Annalen der Mecklenburgischen Landwirthschafts-Gesellschaft* (1814-1844)
- **2 conference papers** from the Doberan 1841 agricultural congress
- **1 book fragment** on wage determination (1848)
- **Translations**: French (Laverriere 1851), English (Hall 1966)

### Works Not Yet Digitized (4)

| Work | Source | Reason |
|------|--------|--------|
| W005 | 1803 essay (Grossen-Flottbeck) | No known digital copy |
| W012 | Landw. Calender 1818 | Rare periodical |
| W034 | Schweriner Anzeblatt ~1841 | Newspaper |
| W037 | Landw. Annalen 1846 | Rare periodical |

## Directory Structure

```
data/
  canonical/           # 32 per-work text files with YAML provenance headers (2.7MB)
  works/               # Work registry (works.csv, work_groups.csv)
  expressions/         # Expression registry (expressions.csv)
  manifestations/      # Manifestation registry (manifestations.csv)
  persons/             # Authority cluster (person_authorities.csv, name_variants.csv)
  relations/           # FRBR relation edges (relation_edges.csv)
  routes/              # Acquisition routes to digital sources (routes.csv)
  holdings/            # Physical holding locations (holdings.csv)
  archives/            # Archive finding-aid records (archive_units.csv)
  acquisitions/
    facsimiles/        # PDF facsimiles from BSB, GDZ, Gallica, IA, GBooks (~912MB)
    extracted/         # Raw OCR/text extractions (~4MB)
    structured/        # DTA TEI XML, plain text, TCF for Part 1 (~12MB)
    ocr/               # IA ABBYY OCR files (~4MB)
    fulltext_manifest.csv       # Per-manifestation extraction metadata
    text_source_priority.csv    # Per-work best-source mapping

project/
  charter.md           # Project scope, identity model, status ladders
  source_protocol.md   # Source identification and routing rules
  acquisition_protocol.md  # Acquisition and extraction rules

scripts/               # Acquisition and extraction pipeline (see below)
notes/
  state_pack.md        # Detailed session state and progress tracking
```

## Identity Model

The corpus uses a FRBR-inspired identity model:

**Person** -> **Work** -> **Expression** -> **Manifestation** -> **Holding/Artifact**

- **Person**: Authority cluster with GND, VIAF, Wikidata, LoC, ISNI identifiers and 14 name variants
- **Work**: An abstract intellectual creation (e.g., *Der isolirte Staat* Part 1)
- **Expression**: A specific realization (e.g., 1826 first edition text, 1842 second edition text, 1910 Waentig edition)
- **Manifestation**: A physical embodiment (e.g., the BSB digitization of the 1850 Rostock printing)

## Text Quality Tiers

| Tier | Description | Count |
|------|-------------|-------|
| FT-7 | Structured scholarly text (TEI XML) | 1 (Part 1 via DTA) |
| FT-4 | OCR with acceptable quality | 3 (Waentig 1910, 1842 2nd ed, GBooks) |
| FT-3 | Recoverable text via Tesseract OCR | 29 (BSB/GDZ Fraktur OCR) |
| FT-0 | No digital text available | 4 |

### Known OCR Artifacts in FT-3 Files

Tesseract Fraktur OCR produces readable text with these systematic issues:
- `ch`/`ck` ligature misread as `<` or `>` (e.g., `ni<t` for `nicht`)
- Page-number header bleed (lone numbers from journal headers)
- Fragment lines from scan bleed-through (0.9-3.9% of lines)
- Library stamps on BSB files (first few pages)

The long-s character (ſ) is correctly preserved throughout.

## Digital Sources

Facsimiles and texts were acquired from:

- **[Deutsches Textarchiv (DTA)](https://www.deutschestextarchiv.de/)** -- TEI XML for 1826 Part 1 (gold standard)
- **[Bayerische Staatsbibliothek (BSB/MDZ)](https://www.digitale-sammlungen.de/)** -- IIIF facsimiles of Parts 2-3 and Doberan proceedings
- **[GDZ Goettingen](https://gdz.sub.uni-goettingen.de/)** -- IIIF facsimiles of all Neue Annalen articles
- **[Internet Archive](https://archive.org/)** -- 1910 Waentig edition, 1875 3rd edition
- **[Gallica (BnF)](https://gallica.bnf.fr/)** -- 1851 French translation (Laverriere)
- **[Google Books](https://books.google.com/)** -- 1842 2nd edition Part 1

## Scripts

| Script | Purpose |
|--------|---------|
| `acquire_iiif_pdf.py` | Download page images from IIIF manifests (BSB, Gallica, GDZ) and combine into PDF |
| `acquire_gdz_articles.py` | Download article page ranges from GDZ with printed-page-to-scan mapping |
| `extract_text_tesseract.py` | Page-by-page Tesseract Fraktur OCR with checkpoint/resume |
| `extract_text_docling.py` | Text extraction via docling (for IA PDFs with embedded OCR) |
| `extract_gdz_articles.py` | Batch Tesseract extraction for all GDZ article PDFs |
| `build_canonical.py` | Assemble per-work canonical text files from best sources |

### Dependencies

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) with `tessdata_best` Fraktur model
- `pypdfium2`, `img2pdf`, `requests`, `Pillow`
- Optional: `docling` (for embedded OCR extraction)

## Using the Canonical Texts

Each file in `data/canonical/` contains a YAML frontmatter header followed by the full text:

```yaml
---
work_id: W001
title: "Der isolirte Staat in Beziehung auf Landwirthschaft und Nationaloekonomie. Erster Theil"
publication_date: 1826
text_tier: FT-7
source: "M009 (DTA 1826 TEI)"
---

[full text follows]
```

To rebuild canonical files from source extractions:

```bash
python -m scripts.build_canonical          # create missing files only
python -m scripts.build_canonical --force  # overwrite all
```

## Authority Identifiers

| Authority | ID |
|-----------|----|
| GND | [118622366](https://d-nb.info/gnd/118622366) |
| VIAF | [94496](https://viaf.org/viaf/94496) |
| Wikidata | [Q76787](https://www.wikidata.org/wiki/Q76787) |
| Library of Congress | [n85127362](https://id.loc.gov/authorities/names/n85127362) |
| ISNI | 0000000112036754 |

## License

The source texts are in the public domain (pre-1900 publications). The corpus metadata, scripts, and registry files are provided as-is for research purposes.
