# BlackIndex UI Help System — 2026-10-02

## Purpose

BlackIndex now provides layered, contextual help inside the research UI so researchers can learn features where they use them without leaving the current workflow.

The help layer is presentation-only. It does not change evidence state, source content, review decisions, or durable research objects.

## Help patterns

### 1. How to

Every primary BlackIndex UI has a persistent **How to** control.

The help dialog is specific to the current page and includes:

- **Start here** — short task-oriented onboarding steps;
- **How this page works** — explanations of the page's sections and terminology;
- **Tips & tricks** — practical shortcuts and methodology reminders;
- **Keyboard / fast navigation** — supported shortcuts.

The help content is searchable inside the popup.

Press **H** while not typing in an input to open the current page's help.

### 2. Quick Tips

Every page has a persistent **Tips** control.

Tips rotate through practical page-specific suggestions. The next tip position is stored in browser-local storage so repeated use cycles through the list rather than always showing the same item.

Tips are intentionally compact and do not block the underlying workflow.

### 3. Contextual ? controls

Small **?** controls are attached to important sections, including dynamically rendered record/AI controls on the Evidence Map.

Selecting one opens the help dialog already filtered to the relevant topic.

The Evidence Map uses a MutationObserver so contextual helpers are reattached safely when the selected-record view rerenders.

### 4. Show me around

The help dialog includes a lightweight **Show me around** tour.

Each primary page has a short page-specific tour that highlights actual UI regions and explains what they are for. The tour can be exited at any point and does not modify state.

### 5. First-use hint

A small dismissible first-use hint explains that How to, Tips, contextual ?, tours, and the H shortcut are available.

Dismissal is stored only in browser-local storage.

## Page-specific coverage

### Evidence Map

Help covers:

- search/source/status filtering;
- record list and selected-record workspace;
- Review / Source Text / Metadata tabs;
- AI Research Assistant;
- clickable source citations;
- browser-local research session/export;
- Resume FBI Review;
- keyboard navigation and record movement.

### Work Queue

Help distinguishes workflow backlog from evidence and explains:

- review-state drift;
- FBI P0 reviewer dispositions;
- lineage review;
- missing-evidence objects;
- unreviewed metadata;
- queue filtering and document links.

### Named Source Recovery

Help explains:

- named upstream targets;
- citation/synthesis hits versus release-container candidates;
- EO 14040 candidate meaning;
- text-page versus verified physical-page distinctions;
- visual boundary verification and fail-closed promotion.

### Source Lineage

Help explains:

- encoded dependency edges;
- dependent versus partially-independent sources;
- shared upstream families;
- research cross-reference pairs;
- why missing edges do not imply independence.

### Entities

Help explains:

- entity search/type filters;
- canonical identities and aliases;
- document mentions;
- genealogy/relationship edges;
- the rule that association or family structure does not transfer culpability.

## UI safety / placement

The help controls use their own high-z-index presentation layer and remain dismissible.

On the Evidence Map, the fixed How to/Tips controls are raised above the existing bottom-right Resume FBI Review / shortcut controls so they do not overlap.

Mobile placement uses separate offsets and a single-column help layout.

## Regeneration

`tools/inject-help-system.py` is called by `tools/serve-dashboard.sh` after the primary pages are generated.

It injects help into:

- `blackindex-dashboard.html`
- `work-queue.html`
- `named-source-recovery.html`
- `source-lineage.html`
- `entities.html`

Injection is idempotent.


## Inline definitions / “What does this mean?” — 2026-10-02

The help layer now includes a shared inline glossary engine.

Definitions appear in two places:

- directly beside or on supported UI terms through hover/focus/tap affordances; and
- inside the searchable **How to** panel under **Glossary / What does this mean?**

The inline layer is presentation-only and deliberately skips Source Text / `<pre>` content.

### Supported definition groups

#### Record integrity

- Archive confidence
- Completeness
- Redaction concern
- Missing refs / missing evidence

Archive confidence follows the BlackIndex methodology definition: completeness and reconstructability of the accessible archive. It is not a truth score.

The numeric completeness and redaction fields are explained without inventing undocumented per-number thresholds.

#### Workflow / review states

- Unreviewed
- Reviewed
- Corroborated
- Contested
- Review-state drift
- Neutral review stub
- PROMOTE
- HOLD
- MERGE
- REJECT-BOUNDARY
- Review required

These definitions explicitly distinguish workflow state from historical truth.

#### Source lineage

- Dependent
- Partially independent
- Independent
- Independence unknown
- Shared upstream family
- Encoded dependency edge
- Research pair

The glossary preserves the BlackIndex rule that document count is not the same as independent evidentiary lineage.

#### Named-source recovery

- Candidate hit
- Citation/synthesis only
- EO 14040 candidate
- Text-page index
- Physical page

These definitions preserve the distinction between localization, container candidates, and visually verified source boundaries/pages.

#### Entities

- Document mention
- Genealogy edge
- Alias

Entity help reiterates that mentions and relationships do not transfer conduct, culpability, ideology, or evidentiary weight.

#### AI research

- Sampled AI coverage
- Complete source coverage
- AI-derived research aid
- Extractive

Sampled coverage is explicitly identified as orientation rather than exhaustive document review. Complete input coverage does not turn AI output into evidence.

#### Research classification

The searchable glossary also defines:

- Canon
- Field note
- Apocrypha
- Pseudepigrapha
- Deuterocanon
- Fragment
- Rejected
- Superseded
- Authenticity status
- Attribution status
- Provenance status
- Corroboration status
- Source independence
- Classification confidence

These definitions explain BlackIndex research state rather than asserting historical truth.

### Interaction

- Mouse hover shows the definition.
- Keyboard focus shows the definition.
- Tap/click pins the definition for mobile use.
- Escape or the close button dismisses it.
- Dense repeated status cells use dotted-underlined text instead of adding an icon to every row.
- Compact labels and summary cards may show a small `i` control.
