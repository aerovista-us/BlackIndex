#!/usr/bin/env python3
"""Reconcile the living BlackIndex ledger with completed Review 007 milestones.

This edits only known status rows and is safe to rerun. It never touches evidence
objects or local source artifacts. If neither an expected old row nor its current
replacement exists, the helper fails instead of guessing.
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


def ensure_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"ledger anchor missing: {anchor}")
    return text.replace(anchor, anchor + "\n" + line, 1)


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
    additions = [
        "| Review 007E physical-page gate | `COMPLETE` | 4/4 target positions exact-mapped to physical PDF pages; 0 unresolved; no OCR/fuzzy matching |",
        "| Review 007 verified source-image bundle | `COMPLETE` | 3/3 bounded review slices created only after every page in each range exact-matched the parent PDF |",
        "| Review 007 boundary diagnostic | `PREPARED` | structural before/range/after diagnostic ready; publishes no source text and cannot promote records |",
    ]
    cursor = anchor
    for line in additions:
        text = ensure_after(text, cursor, line)
        cursor = line

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

    text = replace_once(
        text,
        "| CIA IG 9/11 Accountability | `PARTIAL` | acquired + published; image-only primary PDF preserved; deliberate extraction plan 007C prepared |",
        "| CIA IG 9/11 Accountability | `PARTIAL` | acquired + published; image-only primary PDF preserved; 007C release/version mapping active; pivotal page-image verification pending |",
    )
    text = replace_once(
        text,
        "| Review 007C CIA OIG extraction plan | `PREPARED` | preserve primary image-only artifact; official text-bearing companion preferred; OCR last-resort derivative |",
        "| Review 007C CIA OIG extraction plan | `ACTIVE` | 2007 executive-summary vs 2015 full-report release distinction clarified; search/index text is navigation-only; page-image verification pending |",
    )
    text = replace_once(
        text,
        "| Review 007 boundary diagnostic | `PREPARED` | structural before/range/after diagnostic ready; publishes no source text and cannot promote records |",
        "| Review 007 boundary diagnostic | `COMPLETE` | executed at 36/0; CAND-0005 and CAND-0013 require visual confirmation; Benomrane remained a segmentation-gap review |",
    )
    text = replace_once(
        text,
        "| Review 007F boundary hypotheses | `ACTIVE` | CAND-0005 and CAND-0013 may be bracketed by a next-record start but remain unconfirmed pending visual/source-image review |",
        "| Review 007F boundary hypotheses | `COMPLETE` | CAND-0005 and CAND-0013 are bracketed hypotheses pending visual/source-image confirmation; no boundary claim or promotion |",
    )
    text = replace_once(
        text,
        "| Review 007F Benomrane expansion | `ACTIVE` | widened exact-page structural search seeks nearest strong record starts around pages 173/175; any emitted range is review-only |",
        "| Review 007F Benomrane expansion | `COMPLETE` | exact physical-page scan 138-210 found no strong record-start signals and emitted no range; boundary recovery is on HOLD pending a new identifier/source lead |",
    )
    text = replace_once(
        text,
        "| Named upstream Thumairy source bundle | `ACTIVE` | Benomrane family has §2(b)(i) candidates at normalized text pages 173/175; core 2002 Thumairy ECs remain unmapped |",
        "| Named upstream Thumairy source bundle | `ACTIVE` | Benomrane pages 173/175 are physically verified but boundary-unresolved on HOLD after exact scan 138-210; core 2002 Thumairy ECs remain unmapped |",
    )
    text = replace_once(
        text,
        "| Named upstream Bayoumi source bundle | `ACTIVE` | Caysan Bin Don / Isamu Dyson family has §2(c) candidates at normalized text pages 60/118; other named Bayoumi records remain unmapped |",
        "| Named upstream Bayoumi source bundle | `ACTIVE` | CAND-0005 (58-63; anchor 60) and CAND-0013 (116-122; anchor 118) are physically verified/bracketed hypotheses pending visual confirmation; other Bayoumi records remain unmapped |",
    )

    path.write_text(text, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
