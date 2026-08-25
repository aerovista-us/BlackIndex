# Phase 2 Cross-Document Review 006 — 9/11 Underlying-Record Pass

## Scope

This pass moves below commission and closing-report summaries into the FBI EO 14040 source layer.

Initial records:

1. April 4, 2016 FBI Electronic Communication
2. EO 14040 Section 2(b)(i), Part 1
3. EO 14040 Section 2(b)(i), Part 2
4. EO 14040 Section 2(c), Part 1

## Research posture

The April 2016 EC is a synthesis document. It may summarize interviews, case serials, financial/telecommunications analysis, liaison reporting, historical PENTTBOM material, and other investigative records. Those underlying materials should be treated as distinct evidence objects wherever they can be segmented and identified.

The EC therefore does not automatically count as independent corroboration of the records it summarizes.

## Record segmentation priority

For each EO 14040 release package, extract individual records where possible and capture:

- original FBI file / serial number;
- record date;
- authoring office;
- document type;
- interview subject if applicable;
- referenced persons / organizations;
- redaction markings;
- source/lienage dependencies;
- relationship to later 2016 and 2021 syntheses.

Large release PDFs are containers, not necessarily single research assertions.

## Unmapped referenced evidence

BlackIndex should distinguish:

`missing from the historical record`

from

`not yet individually mapped in the BlackIndex corpus`.

The April 2016 EC currently receives an `UNMAPPED_REFERENCED_EVIDENCE` object for underlying investigative records not yet linked individually. That state must be revised as release-package segmentation proceeds.

## Source genealogy

Preferred graph:

`interview / raw record / liaison report / financial or telecom record → FBI serial → analytical synthesis → 2016 EC → 2021 closing EC → later public interpretation`

Repeated language across later layers is one evidentiary lineage unless an independent source is identified.

## Negative-findings discipline

Later statements that evidence was insufficient for prosecution must remain tied to:

- legal threshold;
- case scope;
- available records;
- witness access;
- investigators and prosecutors involved;
- underlying source base;
- timing of closure.

They are not transformed into a general assertion that no assistance, relationship, or relevant evidence existed.

## Next pass

After local normalization, identify and segment the highest-value underlying serials involving:

- Omar al-Bayoumi;
- Fahad al-Thumairy;
- Musaed al-Jarrah;
- Nawaf al-Hazmi;
- Khalid al-Mihdhar;
- Saudi diplomatic/consular references;
- financial support relationships;
- mosque/community contacts;
- interview contradictions or corrections;
- records reused by the 9/11 Commission or later FBI/CIA assessments.

## Project rule

Container-level releases are archive objects. Claims should be evaluated at the lowest identifiable source level available, with later summaries linked upward rather than counted as separate corroboration by default.
