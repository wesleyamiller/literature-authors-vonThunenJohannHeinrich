# Project Charter: Johann Heinrich von Thünen Author-Corpus Acquisition

## Project Subject
Johann Heinrich von Thünen (1783–1850)

## Objective
Build a complete, auditable, machine-readable corpus of the writings of Johann Heinrich von Thünen.

## Scope Flags

```yaml
project_subject: johann_heinrich_von_thuenen
active_scope: works_by
include_published_works: true
include_periodical_writings: true
include_archival_manuscripts: true
include_letters_authored_by_thuenen: true
include_posthumous_primary_texts: true
include_translations: true
include_abridgments: true
include_excerpts_only_if_attributable: true
include_collected_works_editions: true
include_works_about: false
include_influence_graph: false
require_authority_cluster_before_mass_harvest: true
require_work_expression_manifestation_model: true
prefer_public_domain_digital_copies: true
require_local_copy_if_lawful: true
extract_text_for_all_acquired_text_bearing_artifacts: true
capture_archive_finding_aids: true
allow_secondary_metadata_for_gap_detection: true
```

## Identity Model
person -> work -> expression -> manifestation -> holding/artifact

## Status Ladders
- Authority: candidate -> authority_record_verified -> variants_harvested -> authority_cluster_locked
- Work: candidate -> seeded -> metadata_verified -> canonicalized -> expression_backbone_built -> work_complete -> work_locked
- Expression: candidate -> verified -> manifestation_discovered -> best_manifestation_selected -> acquired_or_located -> qa_checked -> expression_locked
- Manifestation: discovered -> located -> access_state_assigned -> acquired -> checksum_verified -> text_extracted -> qa_checked -> locked
- Archive unit: discovered -> findingaid_verified -> linked_to_work -> digitized_or_noted -> locked

## Full-Text Tiers
- FT-7: Structured scholarly text (TEI/XML/ALTO)
- FT-6: High-quality diplomatic or normalized text
- FT-5: Born-digital PDF or high-quality OCR package
- FT-4: OCR-backed scan with acceptable extraction
- FT-3: Image scan with recoverable text via OCR
- FT-2: Facsimile only
- FT-1: Metadata / finding-aid only
- FT-0: Unresolved

## Metadata Tiers
- MD-5: Authority-backed archival/national-library record with stable identifiers
- MD-4: Strong catalog or archive finding-aid record
- MD-3: Scholarly bibliography or edited collected-works metadata
- MD-2: Secondary catalog or scan metadata
- MD-1: Citation mention only
- MD-0: Unresolved

## Relation Types
is_part_of, is_translation_of, is_abridgment_of, is_transcription_of, is_reprint_of, is_posthumous_edition_of, is_held_at, was_edited_by, future_about_relation, future_influence_relation

## Authorship Status Taxonomy
confirmed, attributed, suspected, to_be_verified, editorial_reconstruction, dictated, disputed

## Editorial Intervention Status Taxonomy
none, light_editing, heavy_editing, posthumous_compilation, editorial_reconstruction, transcription_only, unknown

## Canonical Filename Pattern
thuenen_{workid}_{expressionid}_{manifestationid}_{year}_{shorttitle}_{routetype}.{ext}

## Charter Locked
2026-03-12
