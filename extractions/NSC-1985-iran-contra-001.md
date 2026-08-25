# Fallback Plan for the Nicaraguan Resistance — original and altered versions

- **Doc ID:** `NSC-1985-iran-contra-001`
- **Call ID:** `CALL-005`
- **Native ID:** NSC System IV 400246
- **Source:** National Security Council record / National Security Archive publication
- **Document date:** 1985-03-16
- **Evidence status:** reviewed
- **Landing page:** https://nsarchive.gwu.edu/document/22305-04-nsc-memorandum-oliver-l-north-robert
- **Artifact:** https://nsarchive.gwu.edu/sites/default/files/documents/3224973/04-NSC-Memorandum-from-Oliver-L-North-to-Robert.pdf
- **SHA-256:** populated by local BlackIndex intake metadata after canonical acquisition

## Evidence established by the document

1. The original memorandum presents a fallback option for sustaining the Nicaraguan resistance if Congress remains unwilling to authorize U.S. government funding for military or paramilitary operations.
2. The plan describes a public fundraising mechanism for humanitarian support while separately relying on existing foreign donors for arms and munitions.
3. The packet preserves both an original version and an altered version of the memorandum.
4. The National Security Archive's document history states that North later rewrote a small number of sensitive System IV records and returned altered versions to the controlled file system rather than simply destroying them.
5. The Archive states that investigators detected the alteration partly through anachronistic letterhead, providing a concrete record-integrity indicator independent of the altered text's substantive content.

## Corroboration

The National Security Archive identifies the packet as an example of an original and altered System IV document and explains the controlled sign-out/file environment that made simple destruction more difficult.

## Inferences

1. **Controlled repositories can shift tampering from deletion to substitution.** Strong custody rules reduce one failure mode but can create incentives for version replacement if authenticity/version checks are weak.
2. **Metadata can expose content tampering.** Letterhead, template version, timestamps, routing marks, numbering, and custody logs can contradict a forged or back-dated document even when the prose is plausible.
3. **A preserved original/altered pair is stronger evidence of record manipulation than a missing record alone because the competing versions can be directly compared.**

## Mechanisms / patterns

### PAT-CAND-007 — Record substitution under controlled custody

When deletion is constrained by a controlled repository, an actor may attempt to alter history by replacing an authentic record with a modified version that retains enough identifiers to pass as the original.

**Signals:**
- document template or letterhead postdates the stated document date;
- same control number appears with materially different text;
- custody log shows checkout/return around a later alteration period;
- file metadata conflicts with purported creation date;
- reconstructed version lacks markings present on authenticated copies.

**Promotion:** strong candidate. This packet directly demonstrates the mechanism, but BlackIndex should seek a second independent record-integrity case before promoting it as a reusable historical pattern.

### Reinforces `BI-PAT-003` — Fragmented oversight / incomplete-chain review

A reviewer who sees only the substituted copy can reach a different conclusion from a reviewer who has access to the custody history and original version.

## Failure modes

- Repository tracks check-out/check-in but not cryptographic content identity.
- Version replacement overwrites the prior artifact instead of preserving append-only history.
- Review relies on document text but ignores template/metadata/custody anomalies.
- Sensitive-record audit is scoped to missing files and misses altered files.

## Operational analogs

- Regulated records overwritten after approval while retaining the same document ID.
- Git history rewritten or force-pushed to remove an earlier version.
- Case notes edited after an incident without immutable revision history.
- Signed reports regenerated from a newer template while back-dated to an earlier approval.

## Candidate controls

1. **Immutable object hashing:** content hash recorded when a controlled document enters custody and rechecked on return/access.
2. **Append-only version history:** edits create new versions; prior bytes remain recoverable.
3. **Template/version validation:** generated documents record template ID/version and creation environment.
4. **Custody-event correlation:** edits after checkout trigger comparison against the last authenticated hash.
5. **Independent original escrow:** high-risk records have an independently held reference copy or digest.

## Candidate detections

- Same control number with different cryptographic hashes.
- Document creation metadata or letterhead version newer than the stated date.
- Significant textual changes after a sensitive-record checkout event.
- Returned file differs from last authenticated version without an authorized revision record.

## Redaction / archive analysis

This packet's highest evidentiary value comes from **version comparison**, not from redaction speculation. Any blacked-out names should be scored separately from the authenticated-vs-altered comparison.

- **Archive Confidence:** 5/5 for the existence of competing versions in this published packet.
- **Record anomaly:** severe for authenticity/version integrity.
- **Redaction concern:** variable; not the primary issue.

## Investigation scoring

**Hypothesis:** A sensitive NSC System IV document was later altered/substituted, and the surviving packet preserves evidence of the original and altered versions.

- **Plausibility:** 15/15
- **Evidence:** 28/30
- **Obstruction / Anomaly:** 18/20 for the record-integrity hypothesis
- **Archive Confidence:** 5/5 for this packet
- **Assessment:** A — Confirmed as to the existence of original/altered versions and strong evidence of deliberate record manipulation

## Watch-outs / alternative explanations

- The existence of an altered record proves a record-integrity problem; it does not by itself prove every broader allegation about Iran-Contra.
- National Security Archive narrative about motive and discovery is later archival/investigative context and should remain distinct from text on the 1985 memorandum itself.
- Changes between versions should be quoted and scored individually before inferring why each passage was changed.

## Review disposition

**Reviewed.** High-value record-integrity case. `PAT-CAND-007` retained pending cross-source corroboration; controls for immutable hashing and append-only version history are immediately useful operational analogs.