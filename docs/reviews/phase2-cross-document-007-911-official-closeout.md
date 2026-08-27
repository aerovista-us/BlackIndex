# Phase 2 Cross-Document Review 007 — 9/11 Official-Layer Closeout

## Status

`ACTIVE — source-genealogy and wording-evolution pass started`

This review closes the currently defined official-interpretation layer around the existing Operation Encore corpus before BlackIndex opens a new major research cluster.

It does not render a final historical conclusion.

## Acquisition gate — COMPLETE

The controlled official-layer closeout and collision-safe resume are complete.

Authoritative local verifier after the resume:

- **36 checked**
- **0 failures**
- `ok: true`

Durable run reports:

- `docs/run-reports/2026-08-27-911-official-closeout.md`
- `docs/run-reports/2026-08-27-911-official-closeout-resume.md`

The two failed first-pass monograph intakes were recovered without deleting or overwriting the pre-existing immutable raw artifact. The recovery used canonical source `COMMISSION` plus separate collection namespaces.

## Source set

### Congressional inquiry layer

- `US CONGRESS-2002-9-11-joint-inquiry-001`
  - Joint Inquiry into Intelligence Community Activities Before and After the Terrorist Attacks of September 11, 2001 — declassified final report
  - early congressional inquiry / official interpretation layer
  - substantive review remains incomplete

### Commission layer

- `COMMISSION-2004-9-11-commission-001`
  - official U.S. Government edition of the 9/11 Commission Final Report
  - adopted Commission report
  - Chapter 7 is the principal current comparison focus for Hazmi / Mihdhar / Bayoumi / Thumairy

- `COMMISSION-2004-9-11-commission-terrorist-financing-staff-monograph-001`
  - staff analytical monograph
  - explicitly not Commissioner-approved text
  - staff says evolving monograph material was used in staff statements and draft final-report sections
  - staff also reports significant access to classified raw/finished intelligence, law-enforcement records, State/Treasury files, and interviews

- `COMMISSION-2004-9-11-commission-terrorist-travel-staff-monograph-001`
  - staff analytical monograph
  - explicitly not Commissioner-approved text
  - based on extensive agency records and more than 200 interviews
  - some border-inspection source material reused prior DOJ OIG interviews that were available to Commission staff

### CIA accountability layer

- `CIA-2005-9-11-cia-accountability-001`
  - CIA Office of Inspector General report
  - official retrospective/accountability review
  - image-only local PDF at intake; deliberate extraction path still required
  - the released report explicitly states that its review focuses on Joint Inquiry findings relating to CIA

### Existing later FBI investigative layer

- `FBI-2016-operation-encore-underlying-records-001`
  - April 4, 2016 Operation Encore EC
  - substantive first-pass extraction complete
  - synthesis layer dependent on interviews, communications analysis, financial/logistical records, historical serials, source reporting, and liaison material

- EO 14040 §2(b)(i) Part 1
- EO 14040 §2(b)(i) Part 2
- EO 14040 §2(c) Part 1
- later rereview / closing-assessment lineage already encoded in part

## Source-class discipline

These sources must remain distinct:

| Layer | What it can establish directly |
|---|---|
| Joint Inquiry | what the congressional inquiry reported, reviewed, requested, and concluded at that time |
| Commission staff monograph | what Commission staff reported/analysed; not automatically Commissioner-approved findings |
| Commission final report | what the Commission formally published in its adopted final report |
| CIA OIG | what the CIA Inspector General review reported about CIA performance/accountability |
| FBI / Operation Encore | what the later FBI investigative record reported and how its assessment evolved |
| Underlying FD-302 / serial / financial / telecom / liaison record | the underlying recorded interview, transaction, communication, or investigative event itself |

Repeated statements across these layers are not independent corroboration when they derive from the same underlying record.

## Source genealogy — initial encoded pass

The following durable dependency objects now exist:

- `SD-2002-joint-inquiry-bayoumi-source-base`
  - Joint Inquiry Bayoumi/support assertions → FBI written responses, interviews, financial records, and investigative documents

- `SD-2004-commission-ch7-to-fbi-cia-source-base`
  - Commission Chapter 7 California-support synthesis → FBI interviews/ECs/reports/telephone records plus CIA analytical material cited in the notes

- `SD-2004-financing-monograph-source-base`
  - financing monograph → classified intelligence, law-enforcement records, State/Treasury files, interviews, and shared Commission staff work

- `SD-2004-travel-monograph-source-base`
  - travel monograph → agency records, Commission interviews, prior DOJ OIG interviews, and shared Commission staff work

- `SD-2005-cia-oig-to-joint-inquiry`
  - CIA OIG accountability frame → Joint Inquiry findings relating to CIA

Already-existing Operation Encore genealogy remains in force:

- 2016 EC → underlying FBI serials/interviews/liaison/analytical products
- 2021 closing EC → 2016 EC

### Current graph interpretation

The safe model is therefore not:

`Joint Inquiry + Commission + CIA OIG + FBI EC = four independent confirmations`

It is closer to:

`underlying FBI / CIA / financial / telecom / interview / agency records`

`→ Joint Inquiry synthesis`

`→ Commission staff studies and adopted Commission synthesis`

`→ CIA OIG review for CIA-related Joint Inquiry findings`

and, on a partially overlapping later path:

`underlying FBI serials / later interviews / communications / liaison / analytical products`

`→ 2016 Operation Encore EC`

`→ later FBI rereview / closing synthesis`

Some upstream records overlap across the branches. The exact overlap is still being mapped.

## Wording-evolution pass — started

### Hazmi and Mihdhar — arrival and assistance

The Commission Final Report places Hazmi and Mihdhar in Los Angeles on January 15, 2000 and says their first two weeks remain incompletely reconstructed. It explicitly treats advance assistance as plausible and says it did not credit KSM's denial that al Qaeda had agents in Southern California, while distinguishing that inference from proof of any particular helper's knowledge.

This is important because BlackIndex must keep separate:

`need for assistance` → `actual assistance` → `knowledge of the plot` → `direction by another actor or institution`

The source record strongly supports that practical assistance occurred. Knowledge and direction remain separate propositions.

### Omar al-Bayoumi — Joint Inquiry → Commission → 2016 FBI rereview

The public Joint Inquiry records a more suspicious presentation of the February 2000 encounter: it attributes to FBI agents and written FBI responses the view that the restaurant meeting may not have been accidental, and it describes substantial assistance after the move to San Diego. It also preserves conflicting record interpretations about whether Hazmi and Mihdhar reimbursed the rent/deposit money.

The 2004 Commission Final Report is more cautious on intentionality. It says it did not know whether the lunch encounter occurred by chance or design. It separately states that the Commission had seen no credible evidence that Bayoumi believed in violent extremism or knowingly aided extremist groups. At the same time, it documents concrete assistance: apartment search, lease help, co-signing, bank-account assistance, certified-check/deposit help, community introductions, and later logistical assistance.

The 2016 FBI EC then reexamines the encounter, prior and later statements, communications analysis, and the assistance network. The EC is not treated as a final reversal of the Commission. It is evidence that the questions remained subject to later investigative analysis and that some evidentiary inputs changed or were revisited.

Durable comparison object:

- `SC-2004-2016-bayoumi-assistance-evolution`

### Fahad al-Thumairy — Commission negative finding → later FBI rereview

The Commission reported circumstantial reasons Thumairy was a logical person to investigate and documented problems with some of his denials about contacts. It nevertheless recorded a scoped negative finding: after exploring the available leads, the Commission said it had not found evidence that Thumairy provided assistance to Hazmi and Mihdhar.

The 2016 FBI EC contains later Thumairy / King Fahad Mosque relationship and communications material and questions concerning possible prior knowledge or facilitation. Much of the surrounding detail remains redacted.

This is not yet encoded as a contradiction. The correct question is whether later records or interviews materially changed the evidence set underlying the Commission's 2004 negative finding.

Durable comparison object:

- `SC-2004-2016-thumairy-assistance-evolution`

### Financing — scope warning

The Terrorist Financing staff monograph reports that extensive investigation found no substantial domestic source of financial support for the hijackers and separately states that it found no persuasive evidence that al Qaeda was financially sponsored by a foreign government. Those are staff findings with defined scope and source access, not universal statements that no foreign-linked assistance of any type occurred.

The monograph also distinguishes al Qaeda's overall funding ecology from financing of the specific 9/11 plot. BlackIndex must not collapse:

`al Qaeda funding` → `9/11 plot funding` → `domestic logistical assistance` → `government direction`

into one financial-support claim.

### Travel — source reuse warning

The Terrorist Travel monograph is particularly useful for entry chronology, visa/passport issues, watchlisting, border processes, and information flow. Its source base mixes original Commission interviews with large agency-record collections and reused DOJ OIG interview material. Its repetition of a fact therefore cannot automatically be counted as independent corroboration of another report using the same upstream record.

## Required comparison topics still open

### 1. Hazmi and Mihdhar — California arrival / early support

Continue capturing separately:

- established chronology;
- source for chronology;
- assistance described;
- actor knowledge described or inferred;
- confidence language;
- later changes in assessment.

### 2. Omar al-Bayoumi

For every important statement record:

- exact wording;
- source layer;
- underlying source if identifiable;
- whether the statement is fact, witness report, investigator assessment, or inference;
- corroboration that is genuinely independent;
- contradictory material;
- omitted/unavailable records.

### 3. Fahad al-Thumairy

Continue separating:

- contact / association evidence;
- institutional role;
- alleged assistance;
- investigator treatment;
- negative findings;
- later rereview or revised assessment.

### 4. Mohdar Abdullah and other witnesses

Track:

- each statement version;
- reliability treatment;
- contradictions;
- source dependence;
- whether later summaries quote or merely paraphrase earlier reports.

### 5. Saudi institutional/support questions

Do not collapse:

`contact → assistance → knowledge → direction → institutional authorization`

into one relationship.

Each link requires separate evidence.

### 6. CIA information-sharing / accountability

Compare:

- Joint Inquiry findings;
- Commission treatment;
- CIA OIG review;
- scope of records reviewed;
- accountability findings;
- negative findings;
- later CIA public characterization.

### 7. Financing

Separate:

- hijacker operational financing;
- alleged third-party support;
- Saudi-government/institutional allegations;
- negative investigative findings;
- records actually reviewed by the investigators making those findings.

### 8. Travel / border / watchlisting

Use the Terrorist Travel monograph primarily for:

- entry chronology;
- visa / passport issues;
- watchlisting;
- border-system knowledge;
- government information flows.

Do not treat it as independent evidence for unrelated support-network claims without tracing its underlying sources.

## Negative-finding matrix

For every important `no evidence`, `unable to substantiate`, `no credible evidence`, or equivalent phrase, capture:

| Field | Required |
|---|---|
| institution / investigator | yes |
| exact wording | yes |
| date | yes |
| scope | yes |
| authority/access | yes |
| evidence actually reviewed | where recoverable |
| unavailable / destroyed / excluded material | where recoverable |
| competing finding | where applicable |
| reproducibility | assess separately |

Never normalize these phrases into a generic statement of factual absence.

## Record-integrity questions

For each document family capture:

- release/declassification chronology;
- redaction chronology;
- missing attachments/workpapers;
- version family;
- custodian;
- source-access limitations;
- whether the public copy is complete or a release subset;
- whether later releases alter the evidentiary picture.

The local run currently has uncommitted generated record-integrity objects for several 9/11 records. They should be reviewed/published as evidence objects deliberately rather than committed merely to clean the working tree.

## Gate status

Completed:

1. controlled closeout acquisition run;
2. collision-safe resume;
3. local verifier recorded at 36 / 0;
4. review stubs exist for ingested records;
5. source-class distinctions preserved;
6. Bayoumi / Thumairy / Hazmi-Mihdhar comparison started;
7. initial source dependencies encoded.

Still required before opening the next major corpus cluster:

1. deepen the source map from synthesis documents to named underlying serials / interviews where recoverable;
2. capture the principal negative findings as attributed investigator-review objects with exact wording and scope;
3. address the CIA OIG image-only PDF through a deliberate extraction/review path;
4. resolve or explicitly inventory the orphan immutable raw artifact from the failed first-pass monograph namespace;
5. verify no major comparison is being counted twice through shared upstream sources.

## Next cluster after gate

Default next controlled expansion remains **Operation LOOKING GLASS / nuclear command-and-control continuity**, beginning with official Air Force historical records rather than popular retellings.

## Core rule

**BlackIndex records assertions, evidence, provenance, contradictions, omissions, and anomalies. It does not convert incomplete historical records into final determinations.**
