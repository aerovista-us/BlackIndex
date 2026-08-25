# Phase 2 Cross-Document Synthesis 003

## Sources now in the comparison frame

Previously reviewed:
1. `SENATE-1976-church-committee-001` — Church Committee Book II
2. `JCS-1962-operation-northwoods-001` — Operation Northwoods planning memorandum
3. `FBI-1969-cointelpro-new-left-001` — COINTELPRO New Left, Alexandria
4. `CIA-1973-family-jewels-001` — CIA Family Jewels

Next-set reviewed records:
5. `NSA-1995-venona-001` — *The Venona Story* program/release guide
6. `NARA-1969-pentagon-papers-001` — Pentagon Papers index / corpus map
7. `NSC-1986-iran-contra-001` — Diversion Memo
8. `NSC-1985-iran-contra-001` — Fallback Plan, original and altered versions

## Method

BlackIndex compares mechanisms, not sensational similarities. Proposal, approval, execution, outcome, translation, attribution, and later retrospective interpretation remain separate states. Indexes and official histories can establish provenance and methodology but do not substitute for underlying primary records where a narrower factual claim requires them.

## Existing promoted patterns after expansion

### `BI-PAT-001` — Purpose drift / objective-first justification

Still high confidence. Church Committee, COINTELPRO, Northwoods, and Family Jewels remain the principal supporting records. Iran-Contra adds another secondary-purpose example, but this pattern does not need additional promotion weight to remain established.

### `BI-PAT-002` — Collection/resource-to-consequence chain

Confidence increases. The Diversion Memo extends the pattern beyond information: resources generated within one covert-policy channel are explicitly allocated toward another consequential program. This suggests the reusable pattern should be phrased broadly enough to cover information, money, authorities, access, infrastructure, or logistics that move from collection/origin into downstream action.

### `BI-PAT-003` — Fragmented oversight / incomplete-chain review

Confidence increases. The Iran-Contra records show how different operational/funding channels and highly restricted document systems can prevent a reviewer from seeing the full chain. VENONA adds the inverse lesson: a final attribution can hide a long analytic chain if source recovery, translation, alias resolution, and collateral investigation are not visible together.

## Strong candidates

### `PAT-CAND-004` — Internal awareness without timely accountability

Family Jewels remains the strongest direct case. Iran-Contra record alteration/destruction context is directionally consistent but is not the same mechanism. **Do not promote yet.**

### `PAT-CAND-005` — Analytic reconstruction provenance

VENONA shows a multi-stage evidentiary process:

intercept → cryptanalytic recovery → translation → covername handling → collateral investigation → identity attribution.

The final label can look much more certain than the underlying partial/reconstructed evidence unless every stage retains its uncertainty and provenance.

**Status:** strong candidate; validate with primary VENONA translations and another reconstruction-heavy corpus.

### `PAT-CAND-006` — Cross-program resource diversion

The Diversion Memo directly documents residual funds from one operational channel being allocated to another program. This is a distinct control failure from ordinary secondary use because the transfer occurs through money/logistics rather than only information.

**Status:** candidate; corroborate with additional Iran-Contra financial/oversight records before promotion.

### `PAT-CAND-007` — Record substitution under controlled custody

The Fallback Plan packet preserves original and altered versions of a sensitive System IV record. The case demonstrates that deletion controls alone are insufficient: if authenticity is not cryptographically or procedurally pinned, a controlled record can be returned in modified form.

**Status:** strong candidate; seek a second independent historical record-integrity case before promotion.

## Pentagon Papers disposition

The Pentagon Papers index is intentionally **no-promotion**. Its value is corpus navigation and version provenance. NARA's complete release gives BlackIndex a high-confidence map for later substantive selection, but headings such as "Public Statements" and "Internal Documents" cannot themselves establish deception, motive, or decision divergence.

The next Pentagon Papers sprint should ingest targeted paired volumes/passages capable of testing a specific hypothesis, preferably:

1. a public-justification volume;
2. the corresponding internal-document volume for the same administration/timeframe;
3. a decision-history volume covering a defined escalation/withdrawal decision.

## New cross-source control implications

1. **Purpose binding must cover resources, not only data.** Funds, access, infrastructure, accounts, credits, and intermediaries should inherit originating restrictions unless explicitly reauthorized.
2. **Evidence lineage must preserve transformations.** A final attribution should link back through translation/recovery/enrichment steps with confidence at each stage.
3. **Controlled repositories need content identity.** Checkout logs without hashes/version immutability protect custody but not authenticity.
4. **Version differences are evidence.** Original/altered, redacted/unredacted, and early/later analytic versions should be stored as related immutable objects, never merged destructively.
5. **Indexes are not evidence substitutes.** Corpus maps can guide selection but cannot satisfy primary-source requirements for substantive claims.

## New candidate detections

- Same controlled document ID returns with a different hash and no authorized revision event.
- Document template/letterhead version is newer than the claimed creation date.
- Identity attribution changes but underlying alias/source record and change rationale are absent.
- Partial/recovered qualifier disappears in downstream reporting.
- Residual funds or assets from Program A appear in Program B without a separate authority/approval edge.
- Evidence claim cites only an index/landing page despite the underlying primary volume being available.

## Evidence-discipline reminders strengthened by this set

### Translation is not identity

VENONA makes this explicit. Recovering text, translating it, and identifying the person behind a covername are different evidentiary acts.

### Proposal is not execution

The Diversion Memo and Fallback Plan contain proposed future actions alongside descriptions of prior events. Each action needs its own state.

### Alteration proves alteration, not every surrounding allegation

The original/altered Fallback Plan pair is powerful evidence of record manipulation. It does not automatically prove every broader Iran-Contra claim.

### Completeness statements are version-specific

NARA describes its 2011 Pentagon Papers release as complete and unredacted relative to earlier versions. BlackIndex should pin citations to that release rather than treating all editions as interchangeable.

## Promotion decisions

- `BI-PAT-001`: remain promoted — High confidence
- `BI-PAT-002`: remain promoted — High confidence; broaden language to include resource conversion
- `BI-PAT-003`: remain promoted — High confidence
- `PAT-CAND-004`: hold
- `PAT-CAND-005`: hold pending primary translations + second corpus
- `PAT-CAND-006`: hold pending additional Iran-Contra financial records
- `PAT-CAND-007`: hold pending second independent tamper/substitution case

## Next targets after local batch verification

1. VENONA: 3–5 primary translations chosen for different recovery/identity states.
2. Pentagon Papers: targeted paired public/internal volumes, not bulk download of all 7,000 pages.
3. Iran-Contra: one official oversight/investigative report plus one financial/accounting record to test `PAT-CAND-006` and the record-integrity chain.

## Review disposition

The next-set documents materially improve BlackIndex's methodology: VENONA strengthens evidence-lineage rules; Iran-Contra adds cross-program resource and record-integrity controls; the Pentagon index prevents indiscriminate corpus ingestion. Local NXCore acquisition/hashes remain the final provenance gate for these four records.