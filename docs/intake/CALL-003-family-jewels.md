# CALL-003 — CIA Family Jewels intake

## Canonical context

CIA describes the `Family Jewels` as a roughly 700-page collection compiled in 1973 after DCI James Schlesinger asked Agency employees to report activities they thought might be inconsistent with the Agency's charter. CIA publicly released the collection on 26 June 2007.

- **Collection landing:** https://www.cia.gov/readingroom/collection/family-jewels
- **Direct CIA artifact:** https://www.cia.gov/readingroom/docs/family%20jewels%5B15132295%5D.pdf
- **Call ID:** `CALL-003`

## NXCore one-shot

```bash
cd /srv/Collab/mini.shops/blackindex

git pull --ff-only

./tools/ingest-url.sh \
  "https://www.cia.gov/readingroom/docs/family%20jewels%5B15132295%5D.pdf" \
  --source CIA \
  --collection "Family Jewels" \
  --year 1973 \
  --title "Family Jewels — Activities Potentially Inconsistent with the CIA Charter" \
  --landing-url "https://www.cia.gov/readingroom/collection/family-jewels" \
  --call-id CALL-003 \
  --tags "family-jewels,cia,oversight,domestic-activities,internal-review,declassified" \
  --classification-note "CIA internal compilation prepared in 1973; publicly released in 2007" \
  --redaction-note "Score redactions by location, likely information type, and potential perception impact; do not treat redaction itself as evidence of wrongdoing" \
  --publish
```

## Expected behavior

1. Download official CIA artifact.
2. Reject non-PDF response.
3. Preserve immutable raw artifact locally.
4. SHA-256 raw file.
5. Normalize through `pdftotext` if usable.
6. Build metadata + extraction stub.
7. Rebuild manifest.
8. Verify raw/normalized hashes.
9. Publish durable metadata/extraction record only; raw and normalized corpus remain local.

## Review focus

Family Jewels should be reviewed as an **internal inventory**, not as a single operational program. Segment findings by activity and office where possible. Preserve whether each item is a report, recollection, allegation, confirmed activity, legal concern, or later characterization.

Priority comparison questions:

- Does the collection independently support `BI-PAT-001` purpose drift / objective-first justification?
- Does it support `BI-PAT-002` collection-to-consequence chains?
- Does it support `BI-PAT-003` fragmented oversight / incomplete-chain review?
- Are new mechanisms present that should become `BI-PAT-004` or `BI-PAT-005`?
- Where do redactions or missing context materially affect interpretation?

## Guardrails

- `Family Jewels` is not proof that every described activity was illegal; Schlesinger's request covered activities that employees thought might be inconsistent with the Agency charter.
- Separate what the 1973 record directly states from later CIA, congressional, journalistic, or scholarly characterization.
- Do not collapse planning, allegation, acknowledgment, authorization, execution, and outcome into one state.
