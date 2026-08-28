#!/usr/bin/env python3
"""Reconcile the living BlackIndex ledger with Review 007 page/boundary milestones.

This edits only known status rows and is safe to rerun. It never touches evidence
objects or local source artifacts.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"expected ledger marker not found: {old}")
    return text.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    path = root / "docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "| Physical PDF page mapper | `QUEUED` | required before segment/text-page indices can be treated as physical pages |",
        "| Physical PDF page mapper | `COMPLETE` | Review 007 exact mapper verified 4/4 named-source positions against physical PDF pages with no OCR/fuzzy matching |",
    )

    anchor = "| Review 007D recovery interpretation | `ACTIVE` | durable interpretation separates citation localization from underlying-container recovery |"
    additions = "\n".join([
        anchor,
        "| Review 007E physical-page gate | `COMPLETE` | 4/4 target positions exact-mapped to physical PDF pages; 0 unresolved; no OCR/fuzzy matching |",
        "| Review 007 verified source-image bundle | `COMPLETE` | 3/3 bounded review slices created only after every page in each range exact-matched the parent PDF |",
        "| Review 007 boundary diagnostic | `PREPARED` | structural before/range/after diagnostic ready; publishes no source text and cannot promote records |",
    ])
    if "| Review 007E physical-page gate |" not in text:
        if anchor not in text:
            raise RuntimeError("Review 007D ledger anchor missing")
        text = text.replace(anchor, additions, 1)

    checkpoint_anchor = "- Review 007 localization result: **15/15 target families had a citation/synthesis hit; 2/15 also had EO 14040 FBI-container candidates; 13/15 remain citation-localized only**"
    checkpoint_add = "\n".join([
        checkpoint_anchor,
        "- Review 007 physical-page result: **4/4 exact physical-page mappings; 0 unresolved; no OCR/fuzzy matching**",
        "- Review 007 verified source bundle: **3/3 review slices ready; 0 boundary claims; 0 promotions**",
    ])
    if "- Review 007 physical-page result:" not in text:
        if checkpoint_anchor not in text:
            raise RuntimeError("corpus checkpoint anchor missing")
        text = text.replace(checkpoint_anchor, checkpoint_add, 1)

    path.write_text(text, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
