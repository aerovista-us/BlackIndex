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


## v1.1 research navigation — 2026-10-02

The dashboard now turns valid AI citations such as `[L172]` and `[L172-L180]` into clickable source links.

Clicking a citation:

1. switches the current record to Source Text;
2. renders the normalized text with stable line numbers;
3. scrolls to the cited range;
4. highlights the cited lines; and
5. preserves the most recent AI result for that document so the researcher can check the source without losing the answer.

Line numbers are a derived presentation layer over the preserved normalized text. They do not alter source bytes or evidence objects.

### Learning modes

Three additional learning controls are available:

- **Timeline** — Quick mode performs an instant source-grounded date-line extract; Deep mode uses the local AI model to synthesize chronology from a broader sampled source set.
- **People & Organizations** — Quick mode performs an instant source-grounded named-entity scan with exact line citations; Deep mode uses AI for role/relationship synthesis.
- **Explain Simply** — uses the local AI model to explain sampled source material in plainer language while preserving attribution and uncertainty.

Quick Timeline and Quick People/Organizations intentionally do not call a language model. This avoids slow CPU generation and hallucinated entity/date synthesis while still providing immediate research navigation. Their UI result identifies the mode as an extractive source-grounded aid rather than AI synthesis.

Deep model requests have a separate longer timeout (default 240 seconds, configurable with `BLACKINDEX_AI_DEEP_TIMEOUT`) because the 8B model is CPU-bound on NXCore.
