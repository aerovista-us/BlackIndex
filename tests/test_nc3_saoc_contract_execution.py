import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

class Nc3SaocContractExecutionTests(unittest.TestCase):
    def test_three_modifications_are_reviewed_and_canon(self):
        for i,mod in [('001','p00026'),('002','p00031'),('003','p00037')]:
            doc='DOD-2026-contract-announcements-'+i
            self.assertEqual(load('metadata/'+doc+'.json')['evidence_status'],'reviewed')
            rc=load('objects/research_classifications/RC-NC3-saoc-'+mod+'-2026.json')
            self.assertEqual(rc['canonical_status'],'canon')
            self.assertIn('does not establish successful performance',rc['reason'])

    def test_modifications_share_contract_lineage(self):
        for mod in ('p00026','p00031','p00037'):
            sd=load('objects/source_dependencies/SD-NC3-saoc-'+mod+'-to-2024-award.json')
            self.assertEqual(sd['independence'],'dependent')
            self.assertEqual(sd['dependency_type'],'same-contract-longitudinal-execution-state')

    def test_emd1_repair_is_bounded_execution_fact(self):
        sc=load('objects/statement_comparisons/SC-NC3-saoc-2024-award-to-2026-contract-execution.json')
        self.assertIn('stringer cracks',sc['internal_content'])
        self.assertIn('not successful repair',sc['internal_content'])

    def test_acceptance_gap_remains_open(self):
        me=load('objects/missing_evidence/ME-NC3-saoc-government-test-acceptance-performance.json')
        self.assertEqual(me['status'],'unresolved')
        joined=' '.join(me['unresolved_named_records'])
        self.assertIn('delivery and government acceptance',joined)
        self.assertIn('flight-test',joined)

    def test_saffm_retry_is_recorded_without_artifact(self):
        me=load('objects/missing_evidence/ME-NC3-public-program-source-gaps.json')
        hits=[x for x in me['retrieval_attempts'] if '0604288F' in x.get('record','')]
        self.assertTrue(hits)
        self.assertFalse(hits[-1]['artifact_preserved'])
        self.assertIn('TLSV1_ALERT_INTERNAL_ERROR',hits[-1]['result'])

if __name__=='__main__': unittest.main()
