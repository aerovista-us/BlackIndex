# BlackIndex Infrastructure Upgrade — 2026-08-25

## Scope

This upgrade preserves BlackIndex's original mission and analytical capabilities while making the evidence-map model executable.

Implemented:

1. Record Integrity objects
2. MISSING_EVIDENCE objects
3. version-family comparison
4. source-dependency graph edges
5. public-vs-internal statement comparison objects
6. negative-finding / investigator-review objects
7. neutral extraction template generation in the one-shot ingestion path
8. self-contained local HTML dashboard with search and text/review rendering

## Durable vs local data

Durable Git-backed research objects live under `objects/`.

Raw PDFs, normalized text, local indexes, and the generated dashboard remain under ignored local paths. The HTML dashboard may embed normalized text excerpts and therefore must not be committed.

## Evidence-map CLI

```bash
python3 tools/evidence_map.py --help
```

### Bootstrap existing corpus

```bash
./tools/upgrade-evidence-map.sh
```

This creates missing Record Integrity sidecars for all ingested documents, migrates only auto-generated legacy TODO stubs to the neutral review template, rebuilds the object index, builds the local dashboard, and runs the normal hash verifier.

### Record Integrity

```bash
python3 tools/evidence_map.py integrity DOC_ID \
  --completeness 3 \
  --redaction-concern 7 \
  --archive-confidence 2 \
  --known-destruction yes
```

Unset fields remain `null`/`unknown`; the system does not manufacture scores.

### Missing evidence

```bash
python3 tools/evidence_map.py missing-evidence DOC_ID \
  --summary "Attachment C is referenced but absent from the released packet" \
  --referenced-by "page 14" \
  --alternative-explanation "routine archival loss" \
  --recovery-path "search later release/version family"
```

### Version families and comparison

```bash
python3 tools/evidence_map.py version-family FAMILY_ID DOC_A DOC_B
python3 tools/evidence_map.py compare-versions DOC_A DOC_B --family-id FAMILY_ID
```

The comparison records textual differences and a similarity ratio. It does not decide the significance of those differences.

### Source dependency

```bash
python3 tools/evidence_map.py source-dependency \
  --assertion-id ASSERTION_ID \
  --source-id REPORT_B \
  --depends-on INFORMANT_A \
  --independence dependent
```

### Public/internal comparison

```bash
python3 tools/evidence_map.py statement-compare \
  --topic "program scope" \
  --public-source "public statement" \
  --public-statement "..." \
  --internal-source "DOC_ID p. 12" \
  --internal-content "..." \
  --relationship in-tension
```

Relationship values remain revisable record descriptors.

### Investigator / negative finding

```bash
python3 tools/evidence_map.py investigator-review \
  --report-or-finding "Investigation X" \
  --investigator "Agency unit" \
  --exact-wording "unable to substantiate" \
  --scope "records and interviews described in report"
```

A negative finding remains an attributed investigator statement, not a BlackIndex fact about the underlying allegation.

## Neutral review generation

`tools/ingest-url.sh` now runs `tools/generate-review-template.py` after intake. Existing substantive reviews are preserved. Only an absent extraction or a recognizable auto-generated TODO stub is generated/migrated.

Standard order:

`CLAIM → DOCUMENT CONTENT → SOURCE ATTRIBUTION → CORROBORATION → CONFLICTS → GAPS → ALTERNATIVE EXPLANATIONS → UNRESOLVED QUESTIONS → SOURCE`

## Local HTML dashboard

Build only:

```bash
python3 tools/evidence_map.py dashboard
```

Output:

`local/dashboard/blackindex-dashboard.html`

The file is self-contained: metadata, review text, Record Integrity values, and bounded normalized-text chunks are embedded at build time. Search therefore works even when the file is opened directly without a backend.

Serve only over the machine's Tailscale IPv4 address:

```bash
./tools/serve-dashboard.sh
```

Default port: `8787`.

The server exposes only `local/dashboard/`, not the raw vault or repository root.

## Current baseline

Immediately before this infrastructure upgrade, NXCore reported:

```json
{
  "checked": 12,
  "failures": [],
  "ok": true
}
```

That is the pre-upgrade integrity checkpoint. Running `tools/upgrade-evidence-map.sh` should leave the raw/normalized verification result unchanged because the upgrade adds research sidecars and local derived indexes rather than modifying corpus bytes.
