#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

EXPECTED_DEPENDENCIES = {
    'SD-2002-joint-inquiry-bayoumi-source-base': 'dependent',
    'SD-2004-commission-abdullah-to-named-fbi-records': 'dependent',
    'SD-2004-commission-bayoumi-to-named-fbi-cia-records': 'dependent',
    'SD-2004-commission-ch7-to-fbi-cia-source-base': 'dependent',
    'SD-2004-commission-note22-to-fbi-toma-ec': 'dependent',
    'SD-2004-commission-note23-to-fbi-may17-abdullah-ec': 'dependent',
    'SD-2004-commission-thumairy-to-named-fbi-records': 'dependent',
    'SD-2004-financing-monograph-source-base': 'partially-independent',
    'SD-2004-travel-monograph-source-base': 'partially-independent',
    'SD-2005-cia-oig-exec-summary-to-full-report': 'dependent',
    'SD-2005-cia-oig-to-joint-inquiry': 'dependent',
    'SD-2016-joint-inquiry-28-pages-to-2002-joint-inquiry': 'dependent',
    'SD-2021-operation-encore-closing-to-2016-ec': 'dependent',
    'SD-20260826T020823Z-b0c0edc7': 'dependent',
}
EXPECTED_CLASSIFICATIONS = {
    'RC-911-commission-ch7-support-network-synthesis': 'dependent',
    'RC-911-financing-monograph-synthesis': 'partially-independent',
    'RC-911-joint-inquiry-bayoumi-synthesis': 'dependent',
    'RC-911-travel-monograph-synthesis': 'partially-independent',
}
COMPARISON_GUARDS = {
    'SC-2004-2016-bayoumi-assistance-evolution',
    'SC-2004-2016-thumairy-assistance-evolution',
}

def load_by_id(directory: Path) -> dict[str, dict]:
    out={}
    for p in directory.glob('*.json'):
        try: d=json.loads(p.read_text(encoding='utf-8'))
        except Exception: continue
        oid=d.get('object_id')
        if oid: out[oid]=d
    return out

def main() -> int:
    ap=argparse.ArgumentParser(description='Fail-closed anti-double-counting audit for Review 007 official layers.')
    ap.add_argument('--root', default='.')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    deps=load_by_id(root/'objects'/'source_dependencies')
    classes=load_by_id(root/'objects'/'research_classifications')
    comps=load_by_id(root/'objects'/'statement_comparisons')
    errors=[]; dep_rows=[]; class_rows=[]; comp_rows=[]
    for oid,expected in EXPECTED_DEPENDENCIES.items():
        d=deps.get(oid)
        if not d:
            errors.append(f'missing source dependency: {oid}'); continue
        actual=d.get('independence')
        dep_rows.append({'object_id':oid,'expected':expected,'actual':actual,'source_id':d.get('source_id'),'depends_on':d.get('depends_on')})
        if actual != expected: errors.append(f'{oid}: independence={actual!r}, expected {expected!r}')
        if actual == 'independent': errors.append(f'{oid}: high-risk official-layer edge must not silently become independent')
    for oid,expected in EXPECTED_CLASSIFICATIONS.items():
        d=classes.get(oid)
        if not d:
            errors.append(f'missing research classification: {oid}'); continue
        actual=d.get('source_independence')
        class_rows.append({'object_id':oid,'expected':expected,'actual':actual,'canonical_status':d.get('canonical_status')})
        if actual != expected: errors.append(f'{oid}: source_independence={actual!r}, expected {expected!r}')
        if actual == 'independent': errors.append(f'{oid}: synthesis classification must not silently become independent')
    for oid in sorted(COMPARISON_GUARDS):
        d=comps.get(oid)
        if not d:
            errors.append(f'missing statement comparison: {oid}'); continue
        text=' '.join(str(d.get(k,'')) for k in ('internal_content','notes','relationship')).lower()
        guarded=('underlying' in text or 'source' in text) and ('independent' in text or 'trace' in text or 'mapping' in text or 'records' in text)
        comp_rows.append({'object_id':oid,'source_mapping_guard_present':guarded})
        if not guarded: errors.append(f'{oid}: source-mapping / independence caution no longer detectable')
    result={
        'ok':not errors,
        'scope':'Review 007 official-layer anti-double-counting control; validates encoded independence treatment, not historical truth or complete genealogy',
        'source_dependencies_checked':len(dep_rows),
        'classifications_checked':len(class_rows),
        'comparisons_checked':len(comp_rows),
        'independent_high_risk_edges':sum(1 for r in dep_rows if r['actual']=='independent'),
        'dependency_rows':dep_rows,
        'classification_rows':class_rows,
        'comparison_rows':comp_rows,
        'errors':errors,
    }
    print(json.dumps(result,indent=2))
    return 0 if result['ok'] else 1

if __name__=='__main__':
    raise SystemExit(main())
