# BlackIndex FBI Container Segmentation Workflow

## Purpose

Large FBI Vault / EO 14040 PDFs are often release containers holding multiple investigative records. BlackIndex should preserve the container as an archive object while separately identifying lower-level records for review.

A container PDF is **not** one evidentiary assertion merely because it is one downloadable file.

## Tool

```bash
python3 tools/segment-fbi-container.py DOC_ID
```

Optional priority-only pass:

```bash
python3 tools/segment-fbi-container.py DOC_ID --only-key-entities
```

Output:

```text
local/index/segmentation/<DOC_ID>.json
```

The output is local-only and ignored by Git.

## What the tool does

The first version detects likely record boundaries from normalized text using signals such as:

- `ELECTRONIC COMMUNICATION`
- `FD-302`
- `FD-1057`
- `FEDERAL BUREAU OF INVESTIGATION`
- memorandum / information-report headings
- probable date / case / serial identifiers

It also flags mentions of the current 9/11 priority entities:

- Omar al-Bayoumi
- Fahad al-Thumairy
- Musaed al-Jarrah
- Nawaf al-Hazmi
- Khalid al-Mihdhar

These are **search aids only**.

## Hard evidence rule

Every generated candidate has:

```json
{
  "review_required": true,
  "promoted": false,
  "automatic_evidence_status": "none"
}
```

A heuristic boundary is not evidence and is not automatically promoted into `metadata/`, `extractions/`, or `objects/`.

Before promotion, compare candidate page boundaries directly with the source PDF and record:

- exact source pages;
- FBI file/case/serial number where visible;
- document type;
- original date;
- authoring office;
- interview subject, if applicable;
- redactions;
- source dependencies;
- relationship to the 2016 EC and/or 2021 closing EC;
- whether the same underlying record is reused in Commission, CIA, congressional, or later FBI reports.

## Container vs source-level graph

Preferred graph:

```text
FBI Vault release container
        ↓ contains
individual EC / FD-302 / serial / analytical product
        ↓ summarized by
April 2016 Operation Encore EC
        ↓ reviewed / reused by
2019–2020 re-review
        ↓ summarized by
2021 Operation Encore closing EC
        ↓ cited / interpreted by
later reports, litigation, media, analysis
```

Repeated summaries do not become additional independent corroboration unless they introduce genuinely independent underlying evidence.

## Missing vs unmapped

Do not label an underlying record `MISSING_EVIDENCE` solely because it has not yet been segmented.

Use:

- `UNMAPPED_REFERENCED_EVIDENCE` when the record may exist in an acquired container but has not yet been individually identified;
- `MISSING_EVIDENCE` only when the record is actually referenced but unavailable, absent, destroyed, withheld, or otherwise not present after reasonable archival tracing.

## Initial 9/11 segmentation order

1. April 4, 2016 EC — use as the assertion/source map.
2. EO 14040 §2(b)(i) Part 1.
3. EO 14040 §2(b)(i) Part 2.
4. EO 14040 §2(c) Part 1.
5. Later EO 14040 release packets only after the first four are mapped.

Within each container, prioritize records concerning:

- Bayoumi;
- Thumairy;
- al-Jarrah;
- Hazmi;
- Mihdhar;
- Saudi diplomatic/consular links;
- financial transfers/support;
- mosque/community contacts;
- contradictory or corrected interviews;
- records explicitly relied upon by later official findings.

## Promotion gate

A candidate may be promoted as an individual BlackIndex record only after source-PDF verification of its page range and identity.

Promotion does **not** mean the statements inside the record are adopted as fact. Normal BlackIndex evidence-map rules still apply:

`CLAIM → DOCUMENT CONTENT → SOURCE ATTRIBUTION → CORROBORATION → CONFLICTS → GAPS → ALTERNATIVE EXPLANATIONS → UNRESOLVED QUESTIONS → SOURCE`
