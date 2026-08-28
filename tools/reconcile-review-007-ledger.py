#!/usr/bin/env python3
"""Reconcile the living BlackIndex ledger with completed Review 007 milestones.

This edits only known status/checkpoint rows and is safe to rerun. It never
touches evidence objects or local source artifacts. Table rows are reconciled
by stable row identity rather than by requiring an exact obsolete status string.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    """Legacy exact replacement helper retained for non-row markers/tests."""
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"expected ledger marker not found: {old}")
    return text.replace(old, new, 1)


def replace_row(text: str, row_key: str, new_line: str) -> str:
    """Replace one Markdown table row identified by its stable first-column key."""
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(row_key)]
    if not matches:
        raise RuntimeError(f"expected ledger row not found: {row_key}")
    if len(matches) > 1:
        raise RuntimeError(f"duplicate ledger rows found for: {row_key}")
    lines[matches[0]] = new_line
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def ensure_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"ledger anchor missing: {anchor}")
    return text.replace(anchor, anchor + "\n" + line, 1)


def ensure_row_after(text: str, anchor: str, row_key: str, line: str) -> str:
    """Insert a table row only when no row with the same identity exists."""
    if any(existing.startswith(row_key) for existing in text.splitlines()):
        return text
    return ensure_after(text, anchor, line)


def replace_prefixed_line(text: str, prefix: str, new_line: str, *, required: bool = True) -> str:
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if not matches:
        if required:
            raise RuntimeError(f"expected ledger line not found: {prefix}")
        return text
    if len(matches) > 1:
        raise RuntimeError(f"duplicate ledger lines found for: {prefix}")
    lines[matches[0]] = new_line
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--verifier-checked", type=int)
    ap.add_argument("--verifier-failures", type=int)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    path = root / "docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
    text = path.read_text(encoding="utf-8")

    # Stable platform row: normalize by identity, never by obsolete status wording.
    text = replace_row(
        text,
        "| Physical PDF page mapper |",
        "| Physical PDF page mapper | `COMPLETE` | Review 007 exact mapper verified 4/4 named-source positions against physical PDF pages with no OCR/fuzzy matching |",
    )

    anchor = "| Review 007D recovery interpretation | `ACTIVE` | durable interpretation separates citation localization from underlying-container recovery |"
    additions = [
        ("| Review 007E physical-page gate |", "| Review 007E physical-page gate | `COMPLETE` | 4/4 target positions exact-mapped to physical PDF pages; 0 unresolved; no OCR/fuzzy matching |"),
        ("| Review 007 verified source-image bundle |", "| Review 007 verified source-image bundle | `COMPLETE` | 3/3 bounded review slices created only after every page in each range exact-matched the parent PDF |"),
        ("| Review 007 boundary diagnostic |", "| Review 007 boundary diagnostic | `COMPLETE` | executed at 36/0; CAND-0005 and CAND-0013 require visual confirmation; Benomrane remained a segmentation-gap review |"),
    ]
    cursor = anchor
    for row_key, line in additions:
        text = ensure_row_after(text, cursor, row_key, line)
        cursor = line if line in text else cursor

    checkpoint_anchor = "- Review 007 localization result: **15/15 target families had a citation/synthesis hit; 2/15 also had EO 14040 FBI-container candidates; 13/15 remain citation-localized only**"
    text = ensure_after(
        text,
        checkpoint_anchor,
        "- Review 007 physical-page result: **4/4 exact physical-page mappings; 0 unresolved; no OCR/fuzzy matching**",
    )
    text = ensure_after(
        text,
        "- Review 007 physical-page result: **4/4 exact physical-page mappings; 0 unresolved; no OCR/fuzzy matching**",
        "- Review 007 verified source bundle: **3/3 review slices ready; 0 boundary claims; 0 promotions**",
    )
    text = ensure_after(
        text,
        "- Review 007 verified source bundle: **3/3 review slices ready; 0 boundary claims; 0 promotions**",
        "- Review 007 boundary follow-up: **CAND-0005 / CAND-0013 bracketed pending visual confirmation; Benomrane exact scan 138-210 found no strong boundary signals and is on HOLD**",
    )

    text = replace_row(
        text,
        "| CIA IG 9/11 Accountability |",
        "| CIA IG 9/11 Accountability | `PARTIAL` | full official report + separate 2007 Executive Summary companion acquired; both image-only; 007C page-image verification remains pending |",
    )
    text = replace_row(
        text,
        "| Review 007C CIA OIG extraction plan |",
        "| Review 007C CIA OIG extraction plan | `ACTIVE` | full report and 2007 official Executive Summary companion acquired; both image-only; search/index text remains navigation-only; pivotal page-image verification pending |",
    )
    text = replace_row(
        text,
        "| Review 007 boundary diagnostic |",
        "| Review 007 boundary diagnostic | `COMPLETE` | executed at 36/0; CAND-0005 and CAND-0013 require visual confirmation; Benomrane remained a segmentation-gap review |",
    )
    text = replace_row(
        text,
        "| Review 007F boundary hypotheses |",
        "| Review 007F boundary hypotheses | `COMPLETE` | CAND-0005 and CAND-0013 are bracketed hypotheses pending visual/source-image confirmation; no boundary claim or promotion |",
    )
    text = replace_row(
        text,
        "| Review 007F Benomrane expansion |",
        "| Review 007F Benomrane expansion | `COMPLETE` | exact physical-page scan 138-210 found no strong record-start signals and emitted no range; boundary recovery is on HOLD pending a new identifier/source lead |",
    )
    text = replace_row(
        text,
        "| Named upstream Thumairy source bundle |",
        "| Named upstream Thumairy source bundle | `ACTIVE` | Benomrane pages 173/175 are physically verified but boundary-unresolved on HOLD after exact scan 138-210; core 2002 Thumairy ECs remain unmapped |",
    )
    text = replace_row(
        text,
        "| Named upstream Bayoumi source bundle |",
        "| Named upstream Bayoumi source bundle | `ACTIVE` | CAND-0005 (58-63; anchor 60) and CAND-0013 (116-122; anchor 118) are physically verified/bracketed hypotheses pending visual confirmation; other Bayoumi records remain unmapped |",
    )

    # 007C companion acquisition is durable once its metadata record exists.
    companion = root / "metadata/CIA-2005-9-11-cia-accountability-executive-summary-001.json"
    if companion.is_file():
        text = ensure_after(
            text,
            "- CIA OIG 9/11 Accountability is acquired/published as `CIA-2005-9-11-cia-accountability-001`",
            "- CIA OIG 2007 Executive Summary companion is acquired/published as `CIA-2005-9-11-cia-accountability-executive-summary-001`",
        )
        text = ensure_after(
            text,
            "- Review 007 boundary follow-up: **CAND-0005 / CAND-0013 bracketed pending visual confirmation; Benomrane exact scan 138-210 found no strong boundary signals and is on HOLD**",
            "- Review 007C companion result: **official GPO/FDLP Executive Summary acquired; image-only; no OCR performed**",
        )

    if args.verifier_checked is not None and args.verifier_failures is not None:
        text = replace_prefixed_line(
            text,
            "- Authoritative local verifier checkpoint:",
            f"- Authoritative local verifier checkpoint: **{args.verifier_checked} checked / {args.verifier_failures} failures** (`2026-08-28` Review 007C CIA OIG Executive Summary companion)",
        )
        text = replace_row(
            text,
            "| Cross-document official-layer review 007 |",
            f"| Cross-document official-layer review 007 | `ACTIVE` | official-layer corpus at {args.verifier_checked}/{args.verifier_failures}; genealogy, wording evolution, negative findings and anti-double-counting controls active |",
        )

    path.write_text(text, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
