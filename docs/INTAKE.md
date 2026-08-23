# BlackIndex Intake Workflow

## Purpose
The intake engine converts a source file into an auditable BlackIndex record without placing the raw corpus in Git.

## Canonical local root

```text
/srv/NXDrive/BlackIndex/
```

The repository may be cloned into the same root or a nearby working directory, but raw source files remain local and excluded from Git.

## Local layout

```text
/srv/NXDrive/BlackIndex/
├── source-vault/raw/      # immutable source files
├── normalized/text/       # extracted text derivatives
├── local/index/           # local search/index artifacts
├── local/cache/           # temporary work products
├── local/logs/            # intake/audit logs
├── metadata/              # one JSON record per document
└── extractions/           # one structured research record per document
```

## Initialize

```bash
python3 tools/blackindex.py init
```

Use another root when testing:

```bash
python3 tools/blackindex.py --root /tmp/blackindex-test init
```

## Intake one document

```bash
python3 tools/blackindex.py intake ~/Downloads/report.pdf \
  --source CIA \
  --collection "Family Jewels" \
  --year 1973 \
  --title "CIA Activities Memorandum" \
  --call-id CALL-003 \
  --url "https://www.cia.gov/readingroom/..." \
  --tags "oversight,internal-audit,governance"
```

The command will:

1. SHA-256 hash the supplied file.
2. Check existing metadata for the same hash.
3. Refuse duplicate intake if the exact file is already recorded.
4. Generate a stable Doc ID.
5. Copy the original into the local source vault.
6. Mark the raw copy read-only (`0444`).
7. Create provenance metadata JSON.
8. Create a linked extraction stub.
9. Append an intake event to the local JSONL audit log.

## Doc ID format

```text
<SOURCE>-<YEAR>-<COLLECTION-SLUG>-<SEQUENCE>
```

Example:

```text
CIA-1973-family-jewels-001
```

The Doc ID is an internal BlackIndex identifier. It does not replace archive identifiers, document numbers, NARA record-group references, CIA FOIA identifiers, or other native identifiers. Record those native identifiers in metadata as the schema evolves.

## Duplicate handling

BlackIndex currently treats an identical SHA-256 checksum as a duplicate and exits without copying the file.

This distinguishes:
- same bytes / same document artifact → duplicate;
- revised scan, OCR derivative, or differently packaged release → different artifact, potentially same underlying record.

Future releases should add a `record_family_id` to connect multiple artifacts representing the same underlying historical document.

## Verification

Re-hash every locally stored raw file and compare it against intake metadata:

```bash
python3 tools/blackindex.py verify
```

A hash mismatch is a high-priority integrity failure and should be investigated before using that document in research.

## Extraction promotion rule

An intake record starts as `evidence_status: unreviewed`.

Do not promote claims into BlackIndex patterns, controls, detections, training, or playbooks until the extraction separates:

- direct evidence;
- corroboration;
- inference;
- unknown/redacted material;
- plausible alternative explanations.

## Planned next intake features

- Native archive/document identifiers
- PDF text extraction (`pdftotext` when installed)
- OCR fallback only when necessary
- URL downloader with provenance capture
- Archive landing-page snapshot metadata
- Manifest/index generation
- Record-family linking
- Collection-level batch intake
- Full-text search
- Optional semantic retrieval layer
