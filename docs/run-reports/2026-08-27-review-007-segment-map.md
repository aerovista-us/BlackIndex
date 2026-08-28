# BlackIndex Controlled Review Run — Review 007 Segment Map

- **Completed UTC:** `2026-08-28T00:50:47+00:00`
- **Verifier:** `36` checked / `0` failures
- **EO 14040 target families:** `2`
- **EO 14040 candidate positions:** `4`
- **Positions mapped to heuristic segments:** `2`
- **Positions without heuristic segment match:** `2`
- **Physical-page claims made:** `false`
- **Boundary claims made:** `false`
- **Record promotions:** `none`
- **Evidence-state mutations:** `none`

> This report maps normalized-text recovery positions to existing heuristic segmentation candidates. It does not establish record boundaries or physical PDF pages.

## Segment mapping

### Caysan Bin Don / Isamu Dyson interview source versions

- Parent: `FBI-2022-eo14040-2-c-001`
  - Parent SHA-256: `c7960258fa7feff92d3386da7eb7b6cb0effa457780fd756cbf43ee5fc6985b6`
  - Normalized text page: `60`
  - Physical page: `UNVERIFIED`
  - Matching segments: `1`
  - Segment: `CAND-0005`
    - Heuristic range: `58–63`
    - Record type guess: `possible_fbi_record`
    - Priority band: `P0`
    - Priority score: `28`
    - P0 review packet present: `True`
    - Existing promotion state: `review_required`
    - Boundary verified: `false`
    - Physical page verified: `false`

- Parent: `FBI-2022-eo14040-2-c-001`
  - Parent SHA-256: `c7960258fa7feff92d3386da7eb7b6cb0effa457780fd756cbf43ee5fc6985b6`
  - Normalized text page: `118`
  - Physical page: `UNVERIFIED`
  - Matching segments: `1`
  - Segment: `CAND-0013`
    - Heuristic range: `116–122`
    - Record type guess: `possible_fbi_record`
    - Priority band: `P0`
    - Priority score: `30`
    - P0 review packet present: `True`
    - Existing promotion state: `review_required`
    - Boundary verified: `false`
    - Physical page verified: `false`

### Qualid Moncef Benomrane FBI interviews — 2002

- Parent: `FBI-2021-eo14040-2-b-i-001`
  - Parent SHA-256: `288067203d5d22736a09f064020c529e06cc79db60b49fd7c665c032e44f3e00`
  - Normalized text page: `173`
  - Physical page: `UNVERIFIED`
  - Matching segments: `0`

- Parent: `FBI-2021-eo14040-2-b-i-001`
  - Parent SHA-256: `288067203d5d22736a09f064020c529e06cc79db60b49fd7c665c032e44f3e00`
  - Normalized text page: `175`
  - Physical page: `UNVERIFIED`
  - Matching segments: `0`

## Interpretation guard

A segment match means the recovered text-page position falls inside an existing heuristic candidate range. It does not prove that the named source is the candidate's complete record, that the candidate boundary is correct, or that the text-page number equals the physical PDF page. Review the original parent PDF before promotion.
