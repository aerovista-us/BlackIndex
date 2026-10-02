# BlackIndex AI Research Assistant — 2026-10-01

## Purpose

BlackIndex now includes a local AI learning/research layer for quickly understanding preserved documents without changing evidence state.

The assistant supports:

- **Quick Summary** — compact sampled document overview.
- **Deep Summary** — broader, slower sampled overview.
- **Summarize Selection** — summarize only source text selected in the dashboard.
- **Ask This Document** — retrieve relevant normalized-text lines and answer from those excerpts only.

AI output is always a **derived research aid — not evidence**. No AI response is automatically written into Canon, assertions, investigator findings, classifications, source-dependency objects, or any other durable evidence object.

## Local-only model boundary

The dashboard server talks only to the local Ollama service on `127.0.0.1:11434`.

Default models:

- Quick: `qwen2.5:1.5b`
- Deep: `gemma4:e4b`

The defaults can be overridden with `BLACKINDEX_AI_FAST_MODEL` and `BLACKINDEX_AI_DEEP_MODEL`.

Source text does not leave NXCore through this feature.

## Grounding

Normalized source text is split into stable line-numbered ranges such as `[L172]` or `[L172-L180]`.

For document questions, BlackIndex retrieves only the strongest matching source windows before invoking the model. For selected-section summaries, the selected browser text must map back to the normalized source text; arbitrary text cannot be submitted as a source selection.

The model prompt explicitly treats source text as untrusted data, ignores instructions embedded in the source, forbids outside knowledge, and requires source-line citations.

Returned citations are checked against the line ranges actually supplied to the model. The UI warns when citations are absent or outside the supplied ranges.

## Coverage discipline

A document summary does not silently imply full-document review.

The result reports:

- chunks used;
- total source chunks;
- whether coverage was complete; and
- exact normalized-text line ranges supplied to the model.

Quick Summary samples a small number of source chunks for speed. Deep Summary samples more source material but is still labeled with its actual coverage. Exact research should use selected-section summaries or targeted document questions.

## Runtime behavior

AI requests are serialized so multiple dashboard clicks cannot load competing models and exhaust NXCore memory.

The Quick model stays warm for a limited period for responsive follow-up questions. The larger Deep model is unloaded after each response to reduce RAM pressure.

On the current CPU-only NXCore runtime, a warmed Quick question is typically in the seconds-to-tens-of-seconds range. Deep analysis can take substantially longer.

If Ollama or the selected model is unavailable, the dashboard returns an explicit AI error; corpus/evidence state is unaffected.

## Methodological boundary

The assistant may paraphrase, summarize, organize, or explain what a source says. It must not:

- make missing evidence appear present;
- turn allegations or attributed statements into established facts;
- turn forecasts, proposals, awards, tests, delivery, readiness, authority, and use into one state;
- infer source independence;
- replace visual verification or human review where BlackIndex requires it; or
- automatically promote its output into durable evidence.

Researchers can copy AI output into their own working notes, but durable evidence-state changes continue through the existing reviewed BlackIndex workflows.
