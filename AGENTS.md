
# AI Agent Playbook for the Johann Heinrich von Thünen Author-Corpus Acquisition Project
## Authority cluster -> canonical work registry -> expression / manifestation graph -> auditable machine-readable corpus -> future intellectual genealogy

## Document Purpose

This playbook governs AI-agent work for building a complete, auditable, machine-readable corpus of the writings of **Johann Heinrich von Thünen**. The immediate objective is **works by Thünen**. Works **about** Thünen and works **influenced by** Thünen are architecturally anticipated but are **not** part of the active acquisition scope unless explicitly switched on later.

This is **not** a journal-corpus problem and **not** a paper-series problem. The control plane is author-centric. The correct backbone is:

**person authority cluster -> canonical work registry -> expression registry -> manifestation registry -> holdings / routes / files -> future relation graph**

The objective is not narrative synthesis. The objective is exhaustive discovery, verified identity, bibliographic accuracy, best-available lawful full text, archive-aware provenance, and an explicit record of what is complete, incomplete, ambiguous, blocked, posthumous, translated, abridged, or uncertain.

This playbook is optimized specifically for **Johann Heinrich von Thünen** while reusing the strongest techniques from the uploaded literature-database instruction sets: architecture lock, explicit status ladders, route-state honesty, checkpoint reporting, exception logs, provenance discipline, extraction triage, and auditable completeness tests.

## Primary Objective

Obtain every in-scope **writing by Johann Heinrich von Thünen** in the best available lawful machine-readable form while preserving:

- identity-level accuracy,
- work-level completeness,
- expression-level completeness,
- manifestation-level provenance,
- bibliographic accuracy,
- archive linkage,
- reproducibility,
- and explicit accounting of gaps, blocks, duplicates, and authorship uncertainty.

## Default Scope

### Active scope now
**Works by Johann Heinrich von Thünen**, including published and unpublished authored writings, subject to the inclusion rules below.

### Deferred scope, architecturally prepared but OFF by default
- works **about** Thünen
- works **influenced by** Thünen
- reception, citation, translation, commentary, and genealogy networks beyond direct authorship

## Success Condition

The project is successful only when, for every in-scope Thünen writing:

- the author identity is reconciled against authority records,
- the writing is represented by one canonical **work** record,
- all known relevant **expressions** of that work are tracked,
- all known relevant **manifestations** are attached to the correct expression,
- each manifestation has a route history and access state,
- the best lawful full-text artifact is identified,
- acquired artifacts have checksums and provenance,
- manuscripts and archival units are linked where relevant,
- duplicates and variants are reconciled,
- posthumous and editorial interventions are made explicit,
- and unresolved cases remain visible in exceptions rather than disappearing.

Do not call the corpus “complete” unless the authority cluster, work registry, expression registry, manifestation registry, route registry, full-text manifest, and exceptions log reconcile.

---

# PART I: NON-NEGOTIABLE RULES

## 1. Truthfulness

1. Do not fabricate authorship, work existence, edition existence, translations, manuscript status, archive holdings, metadata, downloads, or text extraction.
2. Do not say a writing has been acquired unless a local artifact, extracted text artifact, or explicitly documented blocked state exists.
3. Do not say a work is complete unless its known expressions and major manifestations have been checked against authoritative sources.
4. Do not say a manifestation is the “original” unless edition and publication history support that claim.
5. If authorship is suspected but not confirmed, mark it `suspected` or `to_be_verified`.
6. If a text survives only through later edition, excerpt, reprint, transcription, or archival description, preserve that fact explicitly.

## 2. Route-State Honesty

Distinguish at minimum:

- `authority_record_verified`
- `work_seeded`
- `work_verified`
- `expression_verified`
- `manifestation_located`
- `holding_verified`
- `archive_findingaid_only`
- `metadata_only`
- `machine_readable_available`
- `facsimile_only`
- `held_not_digitized`
- `digitization_known_unretrieved`
- `rights_restricted`
- `browser_gated`
- `license_blocked`
- `downloaded`
- `text_extracted`
- `qa_checked`
- `verified_complete`
- `exception_open`

A failed title search is not evidence that the work does not exist. Exhaust authority-first, bibliography-first, catalog-first, and archive-first routes before calling a work missing.

## 3. Licensing and Ethics

- Respect publisher, archive, repository, and institutional access rules.
- Do not exfiltrate credentials.
- Do not paste long copyrighted text into notes or manifests.
- If lawful institutional access exists, it may be used only through compliant means.
- Preserve metadata and locators even when the file itself cannot lawfully be redistributed.
- Prefer open and public-domain routes before restricted routes.
- Stop immediately if challenge pages, anti-bot interstitials, or terms-violating barriers appear.

## 4. Exhaustiveness Over Convenience

The goal is not “major Thünen texts.” The goal is the **universe of Thünen’s writings** within the active scope. Well-known books do not substitute for short essays, periodical pieces, letters, memoranda, manuscript fragments, prefaces, or posthumously edited material.

## 5. Canonical Identity Rule

For this project, the canonical identity is not a journal article and not a bare catalog record. The canonical identity stack is:

1. **person**
2. **work**
3. **expression**
4. **manifestation**
5. **holding / artifact**

This distinction is mandatory.

- A **work** is the abstract intellectual item.
- An **expression** is a specific language / redaction / part / translation / abridgment / transcription / posthumous editorial realization of that work.
- A **manifestation** is a concrete publication or archival embodiment (edition, printing, journal appearance, manuscript unit, scan package, PDF, XML, etc.).
- A **holding / artifact** is a specific library, archive, or digital file instance.

Do not flatten these layers into a single bibliographic row.

---

# PART II: SCOPE, INCLUSION, AND CONFIGURATION

## 6. Active Scope Definition: “Works by Thünen”

Treat as in scope, unless explicitly excluded, any writing authored by Johann Heinrich von Thünen, including where applicable:

- standalone books
- multi-part books
- individual parts or sections of larger works when separately issued
- essays
- journal or society articles
- reports
- pamphlets
- memoranda
- lectures or lecture texts if written by him
- letters authored by him
- notebooks
- manuscript drafts
- short printed notices or replies clearly authored by him
- prefaces, appendices, supplements, and fragments if attributable to him
- posthumously published Thünen writings, provided the posthumous editorial status is recorded
- collected letters or collected writings editions containing primary authored text

## 7. Default Exclusions for the Active Scope

Exclude by default unless needed for evidence, linkage, or future extension:

- biographies of Thünen
- commentary on Thünen
- later textbooks summarizing Thünen
- works merely named after him
- institutional publications of the Johann Heinrich von Thünen-Institut unrelated to his authorship
- reception literature
- papers influenced by him but not authored by him
- portraits, medals, exhibitions, and monuments unless they contain authored text by him

## 8. Borderline Cases

Do not silently drop borderline cases. Keep them with explicit classification if there is uncertainty around:

- dictated text
- heavily edited posthumous text
- collected fragments
- excerpts attributed to him by later editors
- notes embedded in biographies
- reported speeches
- editorial reconstructions
- marginalia or annotations
- letters only known through printed transcription

Use `authorship_status` and `editorial_intervention_status` fields rather than binary inclusion guesses.

## 9. Recommended Project Flags

At project start, explicitly set:

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

Do not leave these implicit.

## 10. Completeness Units

Completeness is assessed at six nested levels:

1. authority cluster
2. work
3. expression
4. manifestation
5. holding / artifact
6. corpus

No higher-level unit is complete if any lower-level unit remains unresolved.

---

# PART III: THÜNEN-SPECIFIC MODEL OF THE CORPUS

## 11. Authority-Cluster-First Control Plane

Johann Heinrich von Thünen appears under many name variants across catalogs, archives, and languages. Therefore the project must begin with an **authority cluster**, not free-text title harvesting.

The authority cluster must include, at minimum:

- preferred authorized form
- known German abbreviated forms
- ASCII / transliterated forms
- foreign-language name variants
- persistent identifiers
- linked archive and bibliography systems

## 12. Required Person Authorities

Create one canonical `person_id` for Thünen and reconcile, at minimum, these identifiers where available:

- GND
- VIAF
- WorldCat / OCLC-linked identity evidence
- relevant archive authority entries
- optional convenience identifiers (Wikidata, LoC, ISNI) if useful but not as sole source of truth

## 13. Major-Work Decomposition Rule

Thünen’s corpus includes a major multi-part work, **Der isolierte Staat**, that unfolded across multiple dates, parts, editions, translations, and posthumous publications. Therefore:

- treat **Der isolierte Staat** as a **work group**, not a single flat book row
- create child work / expression structure for its parts where necessary
- record first edition, revised editions, posthumous sections, collected reprints, translations, abridgments, and critical editions separately
- do not collapse “the work” and “one edition of the work” into a single identity

## 14. Periodical-Writing Rule

Thünen published significant shorter writings in periodical or society venues in addition to his better-known book-form work. Therefore:

- book-only searching is prohibited
- periodical and society-annals searching is required
- every discovered shorter piece gets its own canonical work record unless evidence shows it is merely a reprint, excerpt, or duplicate manifestation

## 15. Archival-Writing Rule

The project must distinguish between:

- **published writings**
- **archival unpublished writings**
- **published texts derived from archival materials**

Do not collapse manuscript units and printed editions into a single bibliographic object. Link them through explicit relations.

## 16. Posthumous-Editing Rule

Some Thünen materials were published after his death or under editorial mediation. Therefore:

- preserve editor names
- preserve publication date distinct from authorship date
- record whether the text is autograph, copy, transcription, edition, or reconstruction
- never silently attribute editorial framing to Thünen

## 17. Translation and Abridgment Rule

Translations, abridgments, and selected-text editions are important for discoverability and later influence mapping, but they are not equivalent to original-language expressions.

Therefore:

- link translations to source expressions
- mark abridgments explicitly
- preserve translator / editor metadata
- do not let an English abridgment stand in for the full German text

## 18. Future Genealogy Extension

Although the active scope is limited to works by Thünen, the system of record must be future-ready for two later expansions:

- **works about Thünen**
- **works influenced by Thünen**

Therefore create graph-ready relation tables now, even if they remain sparse during phase one.

---

# PART IV: MACHINE-READABILITY AND METADATA HIERARCHIES

## 19. Preferred Full-Text Ranking

Always prefer the highest available lawful tier.

### FT-7: Structured scholarly text
Examples: TEI / XML / authoritative encoded transcription / ALTO with strong structure.

### FT-6: High-quality diplomatic or normalized text
Authoritative HTML transcription, repository text, or other structured text with reliable segmentation and metadata.

### FT-5: Born-digital PDF or high-quality OCR package
Strong text layer, usable page anchors, minimal corruption.

### FT-4: OCR-backed scan with acceptable extraction
Usable for indexing and parsing after cleanup, but not trusted blindly for exact quotation.

### FT-3: Image scan with recoverable text via OCR
Facsimile exists; machine readability requires local extraction.

### FT-2: Facsimile only
Scan or image exists, but no reliable text yet.

### FT-1: Metadata / finding-aid only
The writing is verified, but no full text has yet been acquired.

### FT-0: Unresolved
Existence or route remains insufficiently verified.

## 20. Metadata-Plane Ranking

Track metadata quality separately.

### MD-5: Authority-backed archival or national-library record with stable identifiers
### MD-4: Strong catalog or archive finding-aid record with publication / holding detail
### MD-3: Scholarly bibliography or edited collected-works metadata
### MD-2: Secondary catalog or scan metadata
### MD-1: Citation mention only
### MD-0: Unresolved

## 21. Selection Rule

For each writing, retain:

- the best available machine-readable artifact,
- the best available facsimile artifact if distinct,
- the best available metadata source set,
- and the route history explaining why the chosen artifact is canonical.

If a lower-tier artifact is selected while a higher-tier route exists, explain why.

## 22. Text Reliability Rule

Machine-readable does not mean correct. Nineteenth-century German materials frequently contain:

- Fraktur OCR errors
- long-s / ligature confusion
- umlaut normalization problems
- title-line corruption
- broken footnotes
- bad page joins
- pagination drift
- editorial matter mixed into body text
- tables and formula damage

Use extracted text for search, indexing, and parsing. Use the facsimile or manuscript image for page-truth and exact quotation verification.

---

# PART V: REQUIRED SYSTEM OF RECORD

## 23. Canonical Files

Maintain these as system-of-record artifacts:

- `project/charter.md`
- `project/source_protocol.md`
- `project/acquisition_protocol.md`
- `notes/state_pack.md`
- `data/persons/person_authorities.csv`
- `data/persons/name_variants.csv`
- `data/works/works.csv`
- `data/works/work_groups.csv`
- `data/expressions/expressions.csv`
- `data/manifestations/manifestations.csv`
- `data/holdings/holdings.csv`
- `data/archives/archive_units.csv`
- `data/routes/routes.csv`
- `data/acquisitions/fulltext_manifest.csv`
- `data/relations/relation_edges.csv`
- `data/acquisitions/exceptions.csv`
- `data/acquisitions/duplicate_resolution.csv`
- `data/acquisitions/authorship_conflicts.csv`
- `outputs/reports/`

## 24. Minimum Schema: `person_authorities.csv`

Required fields:

- `person_id`
- `preferred_name`
- `birth_year`
- `death_year`
- `gnd_id`
- `viaf_id`
- `wikidata_id`
- `loc_id`
- `primary_authority_source`
- `authority_status`
- `notes`

## 25. Minimum Schema: `name_variants.csv`

Required fields:

- `variant_id`
- `person_id`
- `name_raw`
- `name_normalized`
- `script`
- `language`
- `variant_type`
- `source`
- `search_priority`
- `notes`

## 26. Minimum Schema: `work_groups.csv`

Use for grouped multi-part works and major corpora.

Required fields:

- `work_group_id`
- `person_id`
- `group_title`
- `group_title_normalized`
- `group_type`
- `date_span_raw`
- `date_span_normalized`
- `is_primary_cluster`
- `notes`

## 27. Minimum Schema: `works.csv`

Required fields:

- `work_id`
- `work_group_id`
- `person_id`
- `canonical_title`
- `canonical_title_normalized`
- `work_type`
- `original_language`
- `authorship_status`
- `editorial_intervention_status`
- `composition_date_raw`
- `composition_date_normalized`
- `first_publication_date_raw`
- `first_publication_date_normalized`
- `is_posthumous`
- `parent_work_id`
- `work_status`
- `best_expression_id`
- `metadata_confidence`
- `notes`

## 28. Minimum Schema: `expressions.csv`

Required fields:

- `expression_id`
- `work_id`
- `expression_title`
- `language`
- `expression_type`
- `completeness`
- `translator`
- `editor`
- `expression_date_raw`
- `expression_date_normalized`
- `source_expression_id`
- `is_abridged`
- `is_translation`
- `is_transcription`
- `is_posthumous_expression`
- `expression_status`
- `best_manifestation_id`
- `notes`

## 29. Minimum Schema: `manifestations.csv`

Required fields:

- `manifestation_id`
- `expression_id`
- `manifestation_title`
- `publication_type`
- `edition_statement`
- `place`
- `publisher`
- `printer`
- `container_title`
- `container_volume`
- `container_issue`
- `page_start`
- `page_end`
- `page_label_raw`
- `publication_year`
- `publication_date_raw`
- `publication_date_normalized`
- `oclc_id`
- `dnb_id`
- `doi`
- `isbn_or_other_id`
- `manifestation_status`
- `best_route_id`
- `canonical_facsimile_route_id`
- `notes`

## 30. Minimum Schema: `holdings.csv`

Required fields:

- `holding_id`
- `manifestation_id`
- `repository`
- `repository_type`
- `shelfmark_or_call_number`
- `holding_url`
- `country`
- `digitization_state`
- `access_state`
- `copy_notes`

## 31. Minimum Schema: `archive_units.csv`

Required fields:

- `archive_unit_id`
- `person_id`
- `work_id`
- `expression_id`
- `repository`
- `fonds_or_collection`
- `series`
- `container`
- `shelfmark`
- `finding_aid_url`
- `digitized_state`
- `access_state`
- `archive_unit_status`
- `notes`

## 32. Minimum Schema: `routes.csv`

Required fields:

- `route_id`
- `manifestation_id`
- `archive_unit_id`
- `platform`
- `url_or_locator`
- `route_type`
- `access_state`
- `fulltext_tier`
- `metadata_tier`
- `file_format`
- `license_state`
- `retrieved_at`
- `checksum`
- `local_path`
- `extraction_path`
- `route_quality_notes`

## 33. Minimum Schema: `fulltext_manifest.csv`

Required fields:

- `manifestation_id`
- `canonical_text_path`
- `canonical_facsimile_path`
- `canonical_structured_path`
- `text_format`
- `text_extraction_method`
- `text_quality_score`
- `heading_quality_score`
- `footnote_quality_score`
- `table_quality_score`
- `equation_quality_score`
- `page_anchor_quality`
- `checksum`
- `last_verified_at`

## 34. Minimum Schema: `relation_edges.csv`

Required fields:

- `edge_id`
- `source_node_type`
- `source_node_id`
- `relation_type`
- `target_node_type`
- `target_node_id`
- `edge_scope`
- `confidence`
- `evidence_source`
- `notes`

Examples of relation types:

- `is_part_of`
- `is_translation_of`
- `is_abridgment_of`
- `is_transcription_of`
- `is_reprint_of`
- `is_posthumous_edition_of`
- `is_held_at`
- `was_edited_by`
- `future_about_relation`
- `future_influence_relation`

## 35. Minimum Schema: `exceptions.csv`

Required fields:

- `exception_id`
- `person_id`
- `work_id`
- `expression_id`
- `manifestation_id`
- `archive_unit_id`
- `exception_class`
- `severity`
- `opened_at`
- `current_status`
- `safest_interpretation`
- `next_recovery_step`
- `owner`
- `notes`

---

# PART VI: STATUS LADDERS

## 36. Authority-Cluster Status Ladder

Use:

`candidate -> authority_record_verified -> variants_harvested -> authority_cluster_locked`

## 37. Work-Level Status Ladder

Use:

`candidate -> seeded -> metadata_verified -> canonicalized -> expression_backbone_built -> work_complete -> work_locked`

## 38. Expression-Level Status Ladder

Use:

`candidate -> verified -> manifestation_discovered -> best_manifestation_selected -> acquired_or_located -> qa_checked -> expression_locked`

## 39. Manifestation-Level Status Ladder

Use:

`discovered -> located -> access_state_assigned -> acquired -> checksum_verified -> text_extracted -> qa_checked -> locked`

## 40. Archive-Unit Status Ladder

Use:

`discovered -> findingaid_verified -> linked_to_work -> digitized_or_noted -> locked`

## 41. Lock Rule

Do not mark a work `work_complete` unless:

- the authority cluster is stable,
- the work is clearly distinct from nearby variants,
- key expressions are recorded,
- key manifestations are recorded,
- a lawful best-route decision exists for the best available manifestation,
- archival linkage has been checked where relevant,
- and duplicates / authorship conflicts are resolved or explicitly deferred.

---

# PART VII: SOURCE STRATEGY

## 42. Primary Source Classes

Use source classes in this order.

### A. Person authority sources
Use for identity backbone and alias expansion.

Examples:
- Deutsche Biographie
- GND / DNB-linked authority data
- VIAF
- Kalliope authority entry

### B. Seed bibliography sources
Use for initial work discovery and gap detection.

Examples:
- works list in major biographical reference entries
- early scholarly biographies containing bibliographies
- collected letters or collected works tables of contents
- modern critical editions introducing prior publication history

### C. National and union catalogs
Use for manifestation discovery and holding verification.

Examples:
- DNB
- WorldCat / OCLC
- KVK and major German union catalogs
- BSB / GBV / SWB / OBV / CERL and similar systems

### D. Digital libraries and repositories
Use for full-text acquisition where lawful.

Examples:
- Internet Archive
- Google Books
- HathiTrust
- Biodiversity Heritage Library
- Deutsche Digitale Bibliothek
- Deutsches Textarchiv
- Gallica
- institutional repositories
- library scan platforms

### E. Archive finding-aid systems
Use for manuscripts, letters, and estate material.

Examples:
- Kalliope
- Archivportal-D
- university archives
- regional state archives
- archive catalogs of Hohenheim, Rostock, Oldenburg, and other relevant repositories

### F. Secondary scholarly literature
Use only for reconciliation, chronology, and gap detection, not as sole proof of a manifestation’s existence where stronger sources should exist.

## 43. Source Priority Rule

Unless a documented exception applies, use source priority in this order:

1. authority record
2. bibliography / works list
3. national or archive catalog
4. specific holding record
5. digitized artifact
6. secondary scholarly bibliography
7. tertiary web mention

Do not let a tertiary source override an authority-backed bibliographic record without logging the conflict.

## 44. Search Strategy Rule

Searching must proceed in this order:

1. person authority expansion
2. seed bibliography expansion
3. exact-title and variant-title manifestation search
4. archive and holding verification
5. digital surrogate discovery
6. local acquisition and extraction

Do not begin with free-text web search alone.

## 45. Alias Expansion Rule

Every title and authorship search must use a maintained alias set including, at minimum:

- `Johann Heinrich von Thünen`
- `Johann Heinrich v. Thünen`
- `Johann H. von Thünen`
- `Joh. Heinr. von Thünen`
- `J. H. von Thünen`
- `J.H. von Thünen`
- `Thuenen, Johann Heinrich von`
- other archive and transliterated forms discovered in authority records

## 46. Periodical Container Rule

For early shorter writings, search both by title and by known container titles. Periodical discovery should include year, volume, and page span where possible. Do not rely on author-title search alone.

## 47. Public-Domain First Rule

For nineteenth-century Thünen materials, search public-domain digital libraries before restricted sources. Many relevant manifestations are likely out of copyright and may exist as scans, OCR text, or full-text downloads.

---

# PART VIII: WORKFLOW

## 48. Phase 1: Architecture Lock

Before mass acquisition:

1. freeze schemas,
2. freeze status taxonomies,
3. freeze naming conventions,
4. freeze relation types,
5. define text-quality scoring,
6. define authorship / editorial intervention taxonomy,
7. define completeness tests.

Do not begin large-scale harvesting before this lock.

## 49. Phase 2: Authority Cluster

Build the authority cluster first.

Required procedure:

1. create canonical person record,
2. ingest all known name variants,
3. reconcile core identifiers,
4. record source systems that mention the person,
5. lock the authority cluster only after search alias coverage is acceptable.

## 50. Phase 3: Seed Bibliography

Build the initial candidate work list before manifestation hunting.

Required procedure:

1. ingest works lists from biographical and authority sources,
2. ingest bibliographies from early biographies and modern editions,
3. normalize titles cautiously,
4. split grouped listings into candidate work units,
5. mark grouped / multipart works explicitly,
6. do not reconcile silent duplicates yet.

## 51. Phase 4: Canonical Work Registry

For each candidate writing:

1. decide whether it is a distinct work,
2. assign work type,
3. assign parent work group where relevant,
4. record original language,
5. record likely composition and first-publication dates,
6. classify authorship certainty,
7. create one canonical work row.

## 52. Phase 5: Expression Registry

For each work:

1. identify original-language expression(s),
2. identify revised expressions,
3. identify translated expressions,
4. identify abridgments,
5. identify transcriptions and modern edited realizations,
6. record posthumous expression status,
7. link expression-to-expression relations explicitly.

## 53. Phase 6: Manifestation Discovery

For each expression:

1. locate first or earliest known manifestation,
2. locate revised or reissued manifestations,
3. locate collected-works manifestations,
4. locate digital surrogates,
5. locate archive holdings for manuscript embodiments if relevant,
6. assign access state and metadata tier.

## 54. Phase 7: Acquisition and Preservation

For each lawful artifact:

- download or store the permitted file / locator,
- compute checksum,
- preserve original filename,
- create deterministic canonical filename,
- store facsimile and extracted text separately,
- never overwrite raw files,
- preserve container metadata and source URL / locator.

## 55. Phase 8: Text Extraction

For each acquired text-bearing artifact:

1. detect whether structured text already exists,
2. if so, preserve it before doing new extraction,
3. classify born-digital vs OCR-derived vs image-only,
4. extract text using the lightest sufficient method,
5. preserve page segmentation,
6. preserve page-to-text mapping,
7. score quality rather than assuming success.

## 56. Phase 9: Archival Pass

After the published-manifestation backbone is stable:

1. search archive finding aids for manuscripts, letters, and estate materials,
2. attach archive units to work / expression records,
3. distinguish autograph from copy / transcript / later edition,
4. log repositories and shelfmarks,
5. note digitization state,
6. create exceptions for inaccessible but verified material.

## 57. Phase 10: Metadata Reconciliation

Reconcile, at minimum:

- title variants
- spelling modernization variants
- Fraktur-to-modern transliteration differences
- author abbreviations
- place and publisher variants
- part / section structure
- posthumous vs lifetime publication status
- container titles
- page ranges
- library identifiers
- archive shelfmarks
- duplicate scan routes

When conflicts remain, keep them visible.

## 58. Phase 11: QA and Completeness Audit

Run these tests repeatedly:

- every work is attached to the canonical person record,
- every expression belongs to a canonical work,
- every manifestation belongs to a canonical expression,
- every manifestation has route history,
- every acquired artifact has checksum,
- every text extraction has a quality score,
- every archive unit is linked or intentionally deferred,
- every grouped work has its parts resolved or explicitly flagged,
- every `work_complete` item has no unexplained expression gap.

## 59. Phase 12: Corpus Lock

Only after QA passes:

- lock completed work clusters,
- freeze snapshots,
- generate interval reports,
- leave unresolved cases in exceptions,
- and never hide gaps by omission.

---

# PART IX: ACQUISITION ORDER RULES

## 60. Required Acquisition Sequence

Unless a documented exception applies, use this order:

1. authority verification
2. seed bibliography build
3. canonical work registry
4. expression registry
5. manifestation discovery
6. holding / archive verification
7. lawful acquisition
8. extraction
9. QA and completeness audit
10. manual rescue only for unresolved cases

## 61. Preferred Operational Strategy

Use a pilot, then scale.

Recommended pilot blocks:

- the major **Der isolierte Staat** work group
- a small set of shorter early periodical writings
- one posthumous expression / edition case
- one archival / letter case

The pilot must validate:

- authority clustering,
- work-expression-manifestation modeling,
- part decomposition,
- public-domain acquisition,
- archive linkage,
- and completeness auditing.

Only then scale.

## 62. Batch Dimensions

Suggested batching dimensions:

- by work group
- by decade
- by publication type
- by language
- by archive vs print status
- by extraction difficulty

Do not redesign the schema after large-scale acquisition unless absolutely necessary.

## 63. Script-First Rule

For repetitive work, prefer scripts over manual browsing.

Scripts should:

- have narrow purpose,
- log inputs and outputs,
- be resumable,
- emit replayable manifests,
- avoid hard-coded credentials,
- record partial success explicitly,
- and preserve source-specific raw data when useful.

## 64. Parallelization Rule

Parallelization is allowed only after identity logic is stable.

When processing many manifestations:

- split work into non-overlapping work or manifestation ranges,
- give each stream its own checkpoint file,
- use append mode for shared CSV outputs,
- write headers conditionally,
- flush rows incrementally,
- and keep polite request pacing.

Do not parallelize fuzzy identity resolution prematurely.

## 65. Storage Rule

Separate:

- raw facsimiles,
- structured text,
- OCR text,
- metadata tables,
- archive metadata,
- QA outputs,
- and reports.

Do not mix raw acquisition artifacts with curated derivatives.

---

# PART X: DEDUPLICATION AND CANONICALIZATION

## 66. Duplicate Types

Handle explicitly:

- same work under multiple titles
- same expression across multiple catalogs
- same manifestation across multiple repositories
- same scan mirrored on multiple platforms
- same text as original and reprint
- same text as manuscript and later edited edition
- same item embedded in collected works and also issued separately
- same title referring to different part numbers or dates
- same translation appearing under multiple catalog titles

## 67. Canonical Record Rule

Each distinct writing gets one canonical work record. Additional expressions and manifestations attach to it rather than spawning new work identities.

## 68. Earliest-Manifestation Rule

The earliest discoverable manifestation is important but is not automatically the canonical usable text. The corpus should preserve:

- earliest known manifestation
- best machine-readable manifestation
- best facsimile manifestation

These may differ.

## 69. Posthumous-Manifestation Rule

A posthumous manifestation is not a duplicate nuisance. It may be the first or only manifestation of a work or part of a work. Preserve that role explicitly.

## 70. Canonical Filename Policy

Use a deterministic filename pattern, for example:

`thuenen_{workid}_{expressionid}_{manifestationid}_{year}_{shorttitle}_{routetype}.{ext}`

Examples:

- `thuenen_w0001_e0001_m0001_1826_der-isolirte-staat_part1_archive-pdf.pdf`
- `thuenen_w0001_e0004_m0012_1966_isolated-state_english-abridgment_pdf.pdf`
- `thuenen_w0047_e0047_m0103_1868_forscherleben_bibliography_scan.pdf`

Preserve original filenames in metadata.

---

# PART XI: EXTRACTION AND TEXT QA

## 71. Extraction Defaults

Use the best existing structured text before inventing new extraction work.

Recommended priority:

1. authoritative structured text
2. reliable repository text
3. OCR text already bundled with high-quality public-domain scans
4. local native extraction from born-digital PDF
5. OCR from image scans
6. manual transcription only when justified and logged

## 72. Fraktur and Historical German Rule

For nineteenth-century German materials:

- preserve original orthography in raw text artifacts
- allow normalized derivatives only as separate files
- do not overwrite diplomatic text with normalized text
- store transliteration / normalization provenance

## 73. Text QA Fields

For each text artifact, score:

- character integrity
- heading integrity
- paragraph integrity
- footnote integrity
- table integrity
- formula integrity
- page-anchor integrity
- orthographic fidelity
- editorial contamination risk

## 74. Facsimile Priority Rule

If machine-readable text is poor but facsimile is good, keep both and downgrade the text-quality score rather than pretending the text is reliable.

## 75. Page-Truth Rule

Whenever exact quotations, dating, typography, or page-cited interpretation matters, use the facsimile or manuscript image as ground truth.

---

# PART XII: THÜNEN-SPECIFIC EDGE CASES

## 76. Der isolierte Staat Must Be Handled as a Cluster

Do not treat all references to **Der isolierte Staat** as the same bibliographic object. Distinguish, as needed:

- part 1
- later revised part 1
- part 2 sections
- part 3
- collected reissues
- editorial reprints
- translations
- abridgments
- modern scholarly editions

## 77. Short Agricultural and Economic Pieces

Early shorter writings in agricultural and economic venues are part of the corpus and must not be eclipsed by the famous major work.

## 78. Letters as Writings

Letters authored by Thünen are in scope, but must be tracked carefully:

- autograph letter
- copy
- printed letter
- excerpt in secondary source
- collected correspondence edition

Do not collapse these.

## 79. Manuscripts Known Only via Finding Aids

A manuscript can be in-scope even if only a finding aid is currently available. Record it as `archive_findingaid_only` or `metadata_only`, not as missing.

## 80. Works Embedded in Biographies or Editions

Biographies and edited collections sometimes reproduce primary Thünen text. Record the reproduced text as primary-source evidence only if the reproduced writing can be isolated and attributed clearly. Otherwise log it as evidence, not as a separate manifestation.

## 81. Language Variants

Preserve German original forms and exact historic spellings. Record English and other translations as linked expressions, not normalized replacements.

---

# PART XIII: EXCEPTIONS AND MANUAL REVIEW

## 82. Exceptions Requiring Human Review

Escalate when you encounter:

- uncertain authorship
- uncertain work boundaries
- unclear part / section structure
- posthumous editorial ambiguity
- archive holdings without clear item-level description
- title collisions
- conflicting dates across catalogs
- conflicting identifiers across authority systems
- duplicate candidates that cannot be reconciled automatically
- poor OCR on important texts
- partial scans
- letters known only through later quotation
- manifestations that appear to be excerpts rather than full texts

## 83. Exception Handling Rule

Every exception must produce:

- a record in `exceptions.csv`,
- a short explanation,
- the current safest interpretation,
- the next best recovery step,
- and an owner.

No silent failures.

---

# PART XIV: AGENT ROLES

## 84. Recommended Workstream Roles

### Corpus Architect
Owns schemas, naming, status ladders, relation types, and completeness logic.

### Authority Registrar
Builds and locks the person authority cluster and alias set.

### Work Registrar
Builds and reconciles the canonical work registry.

### Expression Registrar
Handles translations, abridgments, posthumous expressions, and part structure.

### Manifestation Finder
Discovers editions, printings, scans, and digital surrogates.

### Archive Liaison
Finds and links manuscripts, letters, and estate units across repositories.

### Acquisition Lead
Downloads artifacts, computes checksums, and preserves provenance.

### Text Extraction Lead
Runs extraction pipelines and scores quality.

### Metadata QA Lead
Resolves title, date, authorship, edition, and identifier conflicts.

### Completeness Auditor
Owns gap reports, coverage summaries, and final reconciliation.

### Provenance Lead
Maintains state pack, manifests, and reproducible run logs.

---

# PART XV: REQUIRED OUTPUT AT EACH CHECKPOINT

## 85. Checkpoint Report Format

At the end of each meaningful work session, report:

1. authority records touched
2. works added or merged
3. expressions added
4. manifestations added
5. archive units linked
6. artifacts acquired
7. texts upgraded to better full-text tiers
8. unresolved exceptions opened or closed
9. exact files updated
10. what is now safe to rely on
11. next highest-value action

## 86. State Pack Requirements

Maintain `notes/state_pack.md` with:

- current scope flags
- authority-cluster status
- completed work groups
- unresolved work groups
- counts by work type
- counts by expression type
- counts by full-text tier
- counts by access state
- counts by archive linkage state
- top blockers
- active scripts / manifests
- next exact steps

---

# PART XVI: WHAT THE AGENT MUST NEVER DO

## 87. Prohibited Shortcuts

Do not:

- start with random title scraping before authority lock
- flatten work, expression, and manifestation into one row
- treat a translation as the original text
- treat an abridgment as equivalent to the full work
- silently merge part-level records
- overwrite raw files
- infer nonexistence from a failed digitized search
- let a famous work stand in for the whole corpus
- let later commentary count as primary text
- declare completion while archive-only and metadata-only cases remain unreviewed

---

# PART XVII: INITIAL EXECUTION ORDER

## 88. First Actions

When the agent starts, it must do the following in order:

1. create or verify the project directory and schemas,
2. lock project flags,
3. build the authority cluster,
4. ingest name variants and identifiers,
5. build the seed bibliography,
6. create the canonical work registry,
7. choose a pilot set,
8. build the expression and manifestation registries for that pilot,
9. acquire lawful artifacts,
10. extract text and score quality,
11. run QA and authorship / duplication audit,
12. refine the pipeline,
13. then scale to the full corpus.

## 89. North-Star Principle

Optimize for a corpus another serious scholar or engineer could audit, extend, and trust.

---

# PART XVIII: THÜNEN-SPECIFIC OPERATIONAL LESSONS

## 90. Authority Records Are Not Optional

Thünen appears under many abbreviated, transliterated, and foreign-language name forms. Authority-first discovery is therefore mandatory, not optional.

## 91. The Famous Work Is a Trap if Treated Flatly

The **Der isolierte Staat** tradition spans multiple dates, parts, translations, abridgments, and posthumous editions. A flat book model will corrupt the corpus.

## 92. Shorter Writings Matter

Biographical and bibliographic sources indicate that Thünen’s output was not limited to book-form work. Shorter writings in agricultural and economic venues must be included deliberately.

## 93. Archive Distribution Must Be Expected

Relevant Thünen materials are distributed across multiple archives and repositories. A complete corpus cannot rely on one library catalog or one scan platform.

## 94. Public-Domain Digital Surrogates Are Strategic

Important Thünen texts and key early biography / bibliography materials are available as public-domain scans with downloadable OCR or full-text derivatives. These should be harvested early because they accelerate both discovery and text extraction.

## 95. Separate Primary Corpus from Future Genealogy

The end goal may be a universal genealogy of writings and influence, but phase one must stay strict: **works by Thünen first**. Mixing primary corpus and reception corpus too early will contaminate completeness logic.

---

# PART XIX: SOURCE NOTES FOR THE PROJECT OWNER

The following facts materially shape this playbook:

1. **Authority and alias complexity.** Deutsche Biographie and Kalliope list numerous name variants for Thünen and identify core authority records including **GND 118622366** and **VIAF 94496**. This is why the workflow begins with an authority cluster rather than free-text harvesting.
2. **Multipart / posthumous work structure.** Deutsche Biographie’s works list shows that **Der isolierte Staat** spans multiple parts and dates: part 1 in **1826**, a second edition in **1842**, part 2 in **1850** and **1863**, and part 3 in **1863**, with later collected reprints and translations. This is why the work-expression-manifestation model is mandatory.
3. **Shorter writings beyond the major book.** The same Deutsche Biographie works list includes shorter items such as writings from **1817**, **1821**, **1831**, and **1834** in the *Neue Annalen der Mecklenburgischen Landwirthschafts-Gesellschaft*. This is why book-only acquisition is prohibited.
4. **Distributed archival holdings.** Deutsche Biographie notes Thünen-related archival holdings in the **University Archives of Hohenheim**, the **University Archives of Rostock**, and the **Lower Saxony State Archives / Oldenburg**; Kalliope also lists holdings and other mentions under the Thünen authority entry. This is why archive linkage is a first-class requirement.
5. **Seed bibliography source.** The digitized biography **Johann Heinrich von Thünen; ein Forscherleben** (Schumacher-Zarchlin, 1868) states that it contains a bibliography of Thünen’s published books and essays. This makes it a high-value seed source for the initial work registry.
6. **Public-domain digital surrogates exist.** Internet Archive provides downloadable scans and OCR-derived assets for important Thünen materials, including the **1910** collected printing of *Der isolierte Staat*, which makes public-domain route discovery strategically valuable early in the workflow.
7. **Translations and abridgments must be modeled explicitly.** WorldCat records an English **1966** edition, *Isolated state; an English edition of Der isolierte Staat*, described as **abridged and translated from the 2d German edition**. This is why translations and abridgments must be represented as separate expressions, not merged into the original.

---

# PART XX: FUTURE EXTENSIONS (OFF BY DEFAULT)

## 96. Works About Thünen

When later enabled, add a parallel scope:

- biographies
- commemorative volumes
- histories of economic thought sections on Thünen
- journal articles interpreting Thünen
- dissertations on Thünen
- editions with extensive scholarly commentary

Track these in parallel tables or with `edge_scope = about_thuenen`. Do not merge them into the primary corpus.

## 97. Works Influenced by Thünen

When later enabled, add influence edges such as:

- cites Thünen
- explicitly builds on Thünen
- translates Thünen into new disciplinary language
- critiques Thünen
- applies Thünen’s ring model
- extends Thünen’s rent or location theory

Influence is a graph problem, not a primary-corpus problem. Do not activate it until the primary corpus is stable.

## 98. Genealogy Rule

The eventual “genealogy” should be built on top of the clean primary corpus. The graph must be layered:

- **primary text layer**: works by Thünen
- **reception layer**: works about Thünen
- **influence layer**: works shaped by Thünen

This sequence is mandatory for interpretability and auditability.

---

# Final Instruction

If forced to choose between a corpus that is broad but blurry and a corpus that is slower but structurally correct, choose the structurally correct corpus every time.
