# CIA Family Jewels — source note

## Status

**Phase 2 target; provenance verified, local intake pending.**

BlackIndex should not mark this source as ingested or reviewed until the canonical CIA artifact has been successfully acquired on NXCore, hashed, normalized, and verified.

## Canonical context

CIA historical material states that on 26 June 2007 the Agency released an approximately 700-page collection known as the **Family Jewels**. The collection was compiled in 1973 after Director of Central Intelligence James Schlesinger directed employees to report activities they believed might be inconsistent with the Agency's charter. William Colby subsequently delivered the material to Congress.

Canonical CIA context page:
- https://www.cia.gov/resources/csi/studies-in-intelligence/volume-51-no-3/dcis-colby-and-helms-reflections-on-the-cias-time-of-troubles/

CIA Reading Room collection landing page:
- https://www.cia.gov/readingroom/collection/family-jewels

Candidate CIA artifact URL:
- https://www.cia.gov/readingroom/docs/family%20jewels%5B15132295%5D.pdf

## Retrieval caveat

The legacy CIA Reading Room endpoints may redirect or behave differently for automated clients. During the 2026-08 Phase 2 sprint, automated retrieval encountered a redirect loop while CIA's current contextual page remained available. This is an archive-delivery issue, not evidence that the collection is unavailable.

`tools/ingest-url.sh` has been hardened to use a browser-compatible user agent, compression, cookies, a PDF-friendly Accept header, and the supplied `--landing-url` as the HTTP Referer.

Do **not** substitute a third-party mirror as the canonical artifact unless the CIA-hosted copy cannot be acquired after reasonable attempts. A mirror may be used only as corroborating/fallback material with provenance recorded separately.

## Recommended one-shot intake

```bash
./tools/ingest-url.sh \
  "https://www.cia.gov/readingroom/docs/family%20jewels%5B15132295%5D.pdf" \
  --source CIA \
  --collection "Family Jewels" \
  --year 1973 \
  --title "Family Jewels" \
  --landing-url "https://www.cia.gov/readingroom/collection/family-jewels" \
  --call-id CALL-003 \
  --tags "family-jewels,cia,oversight,domestic-activities,assassination-planning,mail-opening,surveillance" \
  --redaction-note "Review redactions, withheld identities, missing attachments, and context gaps before promotion" \
  --publish
```

## Review priorities

The first review pass should separate:
1. activities directly described in the compilation;
2. proposals/planning from executed operations;
3. domestic activity from foreign intelligence activity;
4. contemporaneous Agency characterization from later Church/Rockefeller/Pike findings;
5. redactions, withheld identities, missing attachments, and ambiguous references;
6. evidence of authorization, knowledge, termination, or post-hoc corrective action.

Cross-document questions:
- Does the compilation independently corroborate purpose drift / collection-to-action amplification seen in Church Committee and COINTELPRO?
- Does it show oversight fragmentation or delayed senior awareness?
- Do any entries show outcome-first justification, controlled attribution, or pretext construction comparable to Northwoods, or is that mechanism absent?
- Which apparent abuses were already terminated/corrected by 1973, and which were continuing?

## Promotion gate

No Family Jewels item should be promoted to a reusable BlackIndex pattern solely because it is sensational. Each candidate must preserve the difference between what the 1973 compilation directly records, what later inquiries corroborate, and what remains inference or unresolved due to redaction/context gaps.
