# Platform Review 014 — Discovery Layer and Capability Registry

Status: COMPLETE TO DURABLE OBJECT / LOCAL UI MILESTONE
Date: 2026-10-02

## Scope

Implement the two first-class research layers that remained queued after the current corpus gate:

- Discovery objects for ad hoc leads, sources, artifacts, entities, capability leads, contradictions, gaps, and research questions.
- Time-scoped Capability objects for recording what an actor or system is evidenced or reported to be capable of doing.

## Safety / epistemic boundary

Discovery workflow state is not evidence status.

Capability possession is not event use. The Capability schema requires \`use_in_event_inferred: false\`; the dependency-free validator independently enforces the same rule. Evidence that a capability was used in a specific event must be represented separately.

## Delivered

- \`discovery\` and \`capability\` object types in \`objects/schema-v1.json\`.
- Fallback + JSON Schema validation, including linked-document and linked-object checks.
- \`evidence-map discovery\` and \`evidence-map capability\` CLI creation paths.
- \`local/dashboard/discovery-inbox.html\`.
- \`local/dashboard/capability-registry.html\`.
- Open Discovery integration in Work Queue.
- Evidence Map indexing/counts include discoveries, capabilities, and research classifications.
- Platform health generates both new UIs.
- Unit tests cover CLI creation, validation, UI safety language, and rejection of capability event-use inference.

## Verification

Platform health: PASS.
Corpus: 77 / 77.
Existing durable evidence objects: 192 / 192 valid.
Unit tests: 197 / 197.

## Next use

Use Discovery for new ad hoc material before promotion. Use Capability for Toka and similar capability research, with time scope and evidence lineage explicit. Toka capability evidence must not be converted into proof of use in any event.
