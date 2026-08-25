# BlackIndex Investigation Scoring System

## Purpose

BlackIndex evaluates controversial historical records without treating either government records, official investigations, journalistic accounts, witness statements, or oppositional/conspiracy claims as automatically trustworthy.

The scoring system describes the **current state of the record**. It does not render a final verdict about what ultimately happened.

> **BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations. Conclusions remain provisional and may remain unresolved indefinitely.**

Every investigation uses independent diagnostics:

1. **Plausibility** — Did an actor have motive, capability, and opportunity?
2. **Evidence Density** — How much relevant, direct, diverse, and independently grounded material has been collected?
3. **Obstruction / Anomaly** — How compromised, contradictory, evasive, or unusual is the surviving record?
4. **Archive Confidence** — How complete and reconstructable does the accessible record appear?
5. **Source Confidence** — How independently usable is a particular assertion/source?
6. **State of Record** — How mature is the investigation corpus?

None of these equals `therefore X happened`.

---

# 1. Plausibility Score

**Maximum: 15**

| Factor | Score | Question |
|---|---:|---|
| Motive | 0–5 | Was there a meaningful reason, incentive, or potential benefit? |
| Capability | 0–5 | Did the actor have relevant resources, authority, access, knowledge, or technical ability? |
| Opportunity | 0–5 | Could the actor realistically have acted at the relevant time/place? |

### Descriptive bands

- **0–4:** Low plausibility conditions
- **5–8:** Some plausibility conditions present
- **9–11:** Substantial plausibility conditions present
- **12–13:** Strong plausibility conditions present
- **14–15:** Exceptional motive/capability/opportunity alignment

**Critical rule:** Motive + capability + opportunity establish practical possibility only. They do not establish involvement.

---

# 2. Evidence Density Score

**Maximum: 30**

Score each category from **0–5**.

| Factor | Measures |
|---|---|
| Direct Documentary Material | Orders, communications, logs, reports, recordings, contemporaneous records |
| Independent Corroboration | Genuinely separate source chains supporting the same assertion |
| Physical / Technical Material | Forensics, technical records, physical evidence, telemetry, signals, metadata |
| Witness Material | Firsthand testimony, interviews, depositions, contemporaneous accounts |
| Financial / Logistical Material | Money, travel, personnel, equipment, communications, administrative records |
| Timeline / Causal Fit | How well collected material maps onto the relevant chronology |

### Source-independence rule

Three reports are not three corroborating sources if all three derive from the same informant, document, analyst, press account, or institutional summary.

Where possible record the underlying source dependency graph.

### Conflicting evidence

Do **not** force contradictions into a single net score.

Preserve supporting material under `corroboration` and inconsistent material under `conflicts`. Evidence Density is a measure of how much quality material has been collected, not which side wins.

### Descriptive bands

- **0–4:** Sparse record
- **5–11:** Limited relevant material
- **12–19:** Meaningful record
- **20–25:** Dense multi-source record
- **26–30:** Exceptionally dense record

These bands do not mean unsupported/confirmed.

---

# 3. Obstruction / Anomaly Score

**Maximum: 20**

| Factor | Score | Examples |
|---|---:|---|
| Record Irregularities | 0–5 | Missing files, destroyed material, missing attachments, unexplained gaps, version conflicts |
| Contradictory Accounts | 0–5 | Changed testimony, conflicting agency accounts, internal/public discrepancies |
| Evasion / Non-Cooperation | 0–5 | Avoided questions, delayed compliance, withheld records, incomplete responses |
| Misleading / Concealment Behavior | 0–5 | Demonstrably false statements, selective disclosure, unusual secrecy, mischaracterization |

### Descriptive bands

- **0–3:** Few notable anomalies recorded
- **4–7:** Notable anomalies
- **8–12:** Significant anomaly load
- **13–16:** Severe record-integrity concerns
- **17–20:** Exceptional anomaly/obstruction load

### Critical rule

**Evidence of concealment is evidence of concealment.**

It is not automatically proof of the underlying allegation.

Likewise, a missing or destroyed record may materially reduce archive confidence without establishing what the missing record contained.

---

# 4. Archive Confidence

**0–5**

Measures how complete, traceable, and reconstructable the accessible archive appears.

| Score | Meaning |
|---:|---|
| 5 | Extensive, intact, version-traceable archive with strong provenance |
| 4 | Good record with limited gaps |
| 3 | Meaningful gaps or inaccessible portions |
| 2 | Major missing/classified/destroyed material |
| 1 | Severely compromised surviving record |
| 0 | Archive effectively unavailable or non-reconstructable |

Low archive confidence limits the weight of both positive and negative findings.

---

# 5. Source Confidence

Source Confidence belongs to **individual assertions/sources**, not an entire investigation.

Evaluate where information permits:

- firsthand vs hearsay
- contemporaneous vs retrospective
- independent vs derivative
- access to underlying facts
- incentives/conflicts
- internal consistency
- external corroboration
- provenance / chain of custody
- document integrity

A source can be strong on one assertion and weak on another.

---

# 6. Inference Dependency

Every pivotal analytical assertion should identify how much inferential distance separates it from source material.

| Code | Meaning |
|---|---|
| `D0` | Directly stated or directly observable in the record |
| `D1` | One modest inference required |
| `D2` | Multiple linked inferences required |
| `D3` | Depends on unresolved assumptions |
| `D4` | Highly assumption-dependent / speculative |

A high inference dependency is not forbidden. It simply must remain visible.

---

# 7. State of Record

BlackIndex no longer uses `A — Confirmed`, `B — Strongly Supported`, `C — Plausible`, `D — Weak`, `E — Unsupported`, or similar classes as final historical judgments.

Use maturity codes instead:

| Code | State of Record |
|---|---|
| `R0` | Minimal material collected |
| `R1` | Preliminary record |
| `R2` | Multiple relevant sources |
| `R3` | Substantial corroborating and conflicting material |
| `R4` | Extensive multi-source record |
| `R5` | Mature record; major accessible sources reviewed |

`R5` does **not** mean the investigation is solved. It means the accessible evidence universe has been substantially mapped.

Legacy A/B/C/D/E/X labels in older extraction files are historical scoring snapshots only. They are not permanent BlackIndex conclusions and should be migrated during substantive re-review.

---

# 8. Investigator / Report Reliability Diagnostics

A negative or positive investigative conclusion is another attributed assertion in the corpus.

For a material investigation/report, capture these dimensions from **0–5** where possible:

- **Investigator Independence**
- **Access to Evidence**
- **Method Transparency**
- **Reproducibility**
- **Conflict Exposure**

A low score does not mean investigators lied. It means BlackIndex has limited independent grounds to rely on the conclusion.

---

# 9. Negative Findings

Store negative findings without converting them into factual absence.

For example:

`FBI investigators reported finding no evidence of X.`

is valid attribution.

`There is no evidence of X.`

is not equivalent unless the broader record actually supports that stronger claim.

For every material negative finding capture:

- Who made the finding
- Who employed/controlled the investigator
- Potential conflicts/institutional interests
- Scope of investigation
- Authority/access
- Records reviewed
- Records unavailable/excluded/not sought/destroyed
- Duration/resources
- Interviews conducted
- Important omitted witnesses where known
- Survival of investigative workpapers
- Competing investigations/results
- Reproducibility
- Exact wording

Preserve wording distinctions such as:

- `no evidence found`
- `no credible evidence`
- `unable to substantiate`
- `insufficient evidence`
- `no evidence within records reviewed`

---

# 10. Required Investigation Card

Every BlackIndex investigation should record:

**Research question / hypothesis:**
What exactly is being tested or mapped?

**State of Record:** `R0–R5`

**Plausibility:** `__/15`
- Motive:
- Capability:
- Opportunity:

**Evidence Density:** `__/30`

**Obstruction / Anomaly:** `__/20`

**Archive Confidence:** `__/5`

### Corroborating material
List important supporting material and source independence.

### Conflicting material
List important inconsistent or qualifying evidence without forcing a winner.

### Critical missing evidence
What unavailable material could materially change understanding?

### Alternative explanations
Strongest reasonable competing/mundane explanations for anomalies.

### Unresolved questions
Specific records, versions, testimony, technical evidence, or provenance needed next.

### Anomaly log
Record:
- missing/destroyed records
- missing attachments
- timeline inconsistencies
- changed testimony
- agency disagreements
- unusual classification/withholding chronology
- delayed disclosure
- refusals/evasive answers
- public/internal discrepancies
- procedural deviations
- later releases inconsistent with earlier descriptions
- version conflicts

---

# Core BlackIndex Rule

Separate and preserve:

**Source assertion → Document content → Corroboration → Conflicts → Gaps → Inference → Unresolved questions**

Never convert:

**Could have + benefited + behaved strangely**

into:

**Therefore did it.**

Likewise, never convert:

**An investigation reported no evidence**

into:

**Therefore no evidence exists.**

And never convert:

**No surviving document says it happened**

into:

**Therefore it did not happen.**

BlackIndex should preserve enough provenance and uncertainty that conflicting statements can coexist until the record itself supports stronger treatment — which may never occur.
