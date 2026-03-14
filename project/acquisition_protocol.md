# Acquisition Protocol

## Acquisition Sequence
1. Authority verification
2. Seed bibliography build
3. Canonical work registry
4. Expression registry
5. Manifestation discovery
6. Holding / archive verification
7. Lawful acquisition
8. Text extraction
9. QA and completeness audit
10. Manual rescue for unresolved cases

## Pilot Set
- Der isolierte Staat work group (major multi-part work)
- A small set of shorter early periodical writings
- One posthumous expression/edition case
- One archival/letter case

## Public-Domain First Rule
For 19th-century Thuenen materials, search public-domain digital libraries before restricted sources.

## Storage Separation
- Raw facsimiles: data/acquisitions/facsimiles/
- Structured text: data/acquisitions/structured/
- OCR text: data/acquisitions/ocr/
- Metadata tables: data/
- Archive metadata: data/archives/
- QA outputs: outputs/reports/
- Reports: outputs/reports/

## Filename Convention
thuenen_{workid}_{expressionid}_{manifestationid}_{year}_{shorttitle}_{routetype}.{ext}

## Checksum Policy
SHA-256 for all acquired artifacts.

## Extraction Priority
1. Authoritative structured text
2. Reliable repository text
3. OCR text bundled with high-quality public-domain scans
4. Local native extraction from born-digital PDF
5. OCR from image scans
6. Manual transcription (logged, justified)
