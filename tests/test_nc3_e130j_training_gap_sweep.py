import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

class Nc3E130jTrainingGapSweepTests(unittest.TestCase):
    def test_training_option_is_reviewed_and_canon(self):
        m=load('metadata/DOD-2026-contract-announcements-004.json')
        rc=load('objects/research_classifications/RC-NC3-e130j-p00011-training-2026.json')
        self.assertEqual(m['evidence_status'],'reviewed')
        self.assertEqual(rc['canonical_status'],'canon')
        self.assertIn('does not establish aircraft delivery',rc['reason'])

    def test_training_option_is_dependent_same_contract_state(self):
        sd=load('objects/source_dependencies/SD-NC3-e130j-p00011-to-2024-award.json')
        self.assertEqual(sd['independence'],'dependent')
        self.assertEqual(sd['dependency_type'],'same-contract-longitudinal-execution-state')

    def test_training_support_does_not_close_aircraft_execution_gap(self):
        sc=load('objects/statement_comparisons/SC-NC3-e130j-2024-award-to-2026-training-option.json')
        self.assertIn('does not establish aircraft delivery',sc['internal_content'])
        gap=load('objects/missing_evidence/ME-NC3-tacamo-execution-confirmation.json')
        unresolved=' '.join(gap['unresolved_named_records'])
        self.assertIn('full-system/final weapon-system Preliminary Design Review',unresolved)
        self.assertIn('EMD aircraft build completion/delivery',unresolved)

    def test_secondary_pdr_lead_is_not_promoted(self):
        gap=load('objects/missing_evidence/ME-NC3-tacamo-execution-confirmation.json')
        hits=[x for x in gap['retrieval_attempts'] if 'full-system' in x.get('record','')]
        self.assertTrue(hits)
        self.assertFalse(hits[-1]['artifact_preserved'])
        self.assertIn('secondary',hits[-1]['result'])

    def test_afgscmd_and_saffm_live_failures_remain_gaps(self):
        gap=load('objects/missing_evidence/ME-NC3-public-program-source-gaps.json')
        self.assertIn('AFGSCMD 63-101',gap['unresolved_named_records'][0])
        text=' '.join(x['result'] for x in gap['retrieval_attempts'][-2:])
        self.assertIn('returns 403',text)
        self.assertIn('return 404',text)
        self.assertIn('TLSV1_ALERT_INTERNAL_ERROR',text)

if __name__=='__main__': unittest.main()
