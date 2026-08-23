# BlackIndex Redaction Analysis Framework

Redactions are tracked separately from the three primary investigation scores.

A redaction is **not evidence of wrongdoing by itself**. It may protect intelligence sources, methods, privacy, foreign-government information, legal privilege, or ongoing investigations.

What matters is **where the redaction appears, what information is likely withheld, and whether its absence prevents a materially different interpretation of the event.**

---

# Redaction Impact Score

**0–15**

| Factor | Score | Measures |
|---|---:|---|
| **Placement Significance** | 0–5 | How important is the location of the redaction? |
| **Likely Information Type** | 0–5 | What category of information appears to be withheld? |
| **Interpretive Impact** | 0–5 | Could disclosure substantially change the understanding of the event? |

---

## 1. Placement Significance

### 0
Administrative or obviously irrelevant material.

### 1
Names/contact details with little effect on substance.

### 2
Supporting detail or secondary context.

### 3
Redaction occurs inside an important factual passage.

### 4
Redaction obscures actor, action, motive, source, target, or decision.

### 5
Redaction appears at a critical causal point where the missing information could materially determine what happened.

Examples:

- Immediately after **“authorized by”**
- Before or after **“was instructed to”**
- Missing recipient of an operational order
- Missing source for a major intelligence claim
- Missing explanation for why an investigation was stopped
- Missing names during discussion of responsibility

---

# 2. Likely Information Type

Tag each redaction where possible:

- `PERSON`
- `AGENCY`
- `INTELLIGENCE_SOURCE`
- `INTELLIGENCE_METHOD`
- `FOREIGN_GOVERNMENT`
- `LOCATION`
- `OPERATION_NAME`
- `TARGET`
- `FINANCIAL`
- `LEGAL`
- `INVESTIGATIVE`
- `COMMUNICATION`
- `DECISION_MAKER`
- `OPERATIONAL_DETAIL`
- `ASSESSMENT`
- `UNKNOWN`

Also record the stated exemption or justification when available.

Examples:

- National security
- Sources and methods
- Privacy
- Law-enforcement sensitivity
- Foreign-government information
- Grand-jury secrecy
- Ongoing investigation
- Statutory withholding

---

# 3. Interpretive Impact

### 0
Disclosure would almost certainly not affect interpretation.

### 1
Minor contextual value.

### 2
Could improve understanding but probably not alter conclusions.

### 3
Could materially strengthen or weaken an existing interpretation.

### 4
Could identify responsibility, motive, foreknowledge, source credibility, or operational involvement.

### 5
Could potentially reverse or substantially alter the accepted understanding of the event.

---

# Redaction Concern Class

### R0 — Routine
Little apparent investigative significance.

### R1 — Relevant
Potentially useful contextual information.

### R2 — Material
Missing information affects an important factual question.

### R3 — Critical
Redaction prevents evaluation of a central actor, action, decision, or claim.

### R4 — High-Impact Unknown
The missing information could plausibly alter the overall interpretation of the event.

**R4 does not mean incriminating information is present.**

It means the withheld material occupies a position where disclosure could have unusually high evidentiary value.

---

# Redaction Pattern Analysis

Never analyze redactions only individually.

Track patterns across an entire collection.

Look for:

- The same person's name repeatedly redacted
- One agency consistently withheld while others are visible
- Redactions concentrated around specific dates
- Redactions surrounding authorization decisions
- Redactions around intelligence failures
- Redactions near assassination, surveillance, funding, or covert-action discussions
- Previously redacted material becoming visible in later releases
- Different versions of the same document with different redactions
- Partial declassification revealing what older versions concealed
- Entire pages or attachments withheld
- References to documents that are absent from the archive

---

# Version Comparison

Whenever multiple versions exist, BlackIndex should compare them.

Record:

**Version A:** date/release  
**Version B:** date/release

Then identify:

- Newly revealed names
- Newly revealed agencies
- Changed classification markings
- Removed redactions
- Added redactions
- Missing pages
- Changed wording
- Previously withheld attachments

This can be extremely valuable.

A redaction that looks meaningless in 1998 may become significant when the same passage is partially revealed in 2025.

---

# Redaction Context Window

For every significant redaction, preserve:

- 2–3 sentences before
- Redacted passage
- 2–3 sentences after
- Page number
- Document title
- Document date
- Classification markings
- Declassification/release date

The surrounding language often allows the likely function of the missing information to be inferred without guessing its exact contents.

---

# Incriminating-Potential Field

Add:

`potential_evidentiary_significance`

Values:

- **None**
- **Low**
- **Moderate**
- **High**
- **Potentially Decisive**
- **Unknown**

This field measures the **potential importance of the missing information**, not whether it is actually incriminating.

Better wording:

> **Potentially Decisive:** If the withheld information concerns responsibility, foreknowledge, authorization, intent, or source credibility, its disclosure could materially change the assessment.

Never write:

> “This redaction probably hides incriminating information.”

unless independent evidence supports that conclusion.

---

# Redaction Anomaly Flags

Add flags for:

- `CRITICAL_PLACEMENT`
- `ENTIRE_PAGE_WITHHELD`
- `MISSING_ATTACHMENT`
- `UNKNOWN_ACTOR`
- `UNKNOWN_DECISION_MAKER`
- `UNKNOWN_SOURCE`
- `UNKNOWN_TARGET`
- `AUTHORIZATION_REDACTED`
- `FOREKNOWLEDGE_REDACTED`
- `FINANCIAL_LINK_REDACTED`
- `LATER_UNREDACTED`
- `INCONSISTENT_REDACTION`
- `REDACTION_WITHOUT_CLEAR_BASIS`
- `ARCHIVE_VERSION_CONFLICT`

---

# Relationship to Obstruction Score

Redactions do **not automatically increase the Obstruction / Anomaly Score**.

Routine lawful redactions should have little or no effect.

Obstruction should increase when there is evidence of:

- inconsistent redaction practices
- material withheld after justification expires
- documents withheld contrary to disclosure orders
- unexplained removal of previously public information
- destruction rather than redaction
- misleading descriptions of withheld material
- repeated withholding of information later shown to contradict official accounts

---

# Required Redaction Record

For important redactions, BlackIndex should store:

**Document:**  
**Page:**  
**Location in passage:**  
**Approximate redaction length:**  
**Likely information type:**  
**Stated exemption:**  
**Placement significance:** `__/5`  
**Interpretive impact:** `__/5`  
**Redaction Impact:** `__/15`  
**Concern Class:** `R0–R4`  
**Potential evidentiary significance:**  
**Later version available:** Yes / No  
**Notes:**  

---

# Core Rule

BlackIndex should distinguish:

**Redacted → Potentially Important → Materially Relevant → Evidence of Concealment → Evidence of Underlying Wrongdoing**

Those are **not the same thing**.

A redaction can justify further investigation.

It cannot, by itself, establish what the missing text says.