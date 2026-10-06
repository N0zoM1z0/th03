"""Candidate file diagnostics must retain partial scope and failed equality."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import review_rec98_th03_mainl_intake as d


class CandidateIntakeTests(unittest.TestCase):
    def fixture(self, gap=0, raw=False):
        unit = dict(id='u', artifact='th03-mainl', segment='decoded:0000',
                    boundary_state='reviewed', state='boundary-reviewed', source='',
                    file_offset='', evidence_ids='e')
        evidence = dict(id='e', artifact='th03-mainl', oracle='analysis-bundle',
                        result='pass', output_sha256='b'*64)
        observed = [dict(carrier=dict(module='a.cpp',segment=0,offset=10,size=3),
                         independent_unit_bytes=3-gap, overlapping_unit_bytes=0,
                         unit_intersections=[dict(unit='u')])]
        comps = {(0,10): [dict(raw_slice_equal=raw,ordered_relocations_equal=False)]*2}
        rows = d.summarize(['a.cpp'],observed,comps,{'a.cpp':'a'*64},{'u':unit},{'e':evidence})
        return rows, {'a.cpp':'a'*64}, {'u':unit}, {'e':evidence}, observed, comps

    def test_complete_and_gap_diagnostics_preserve_raw_failure(self):
        for gap in (0,1):
            rows,h,u,e,*_ = self.fixture(gap)
            d.validate(rows,h,u,e)
            self.assertEqual(rows[0]['raw_equal'],'false')
            self.assertEqual(rows[0]['exact_accepted'],'false')
            self.assertEqual(rows[0]['gap_bytes'],str(gap))
            self.assertEqual(rows[0]['state'],'code-gap-candidate' if gap else 'code-covered-candidate')

    def test_provenance_and_source_acceptance_cannot_be_inherited(self):
        for key,value in [('artifact','th03-main'),('frozen_revision','HEAD'),('frozen_sha256','c'*64),
                          ('scope','whole-file'),('source_accepted','true'),('exact_accepted','true'),('receipt','other.json')]:
            rows,h,u,e,*_ = self.fixture();rows[0][key]=value
            with self.assertRaisesRegex(ValueError,'provenance/scope/acceptance'):d.validate(rows,h,u,e)

    def test_membership_coverage_state_and_open_scope_are_guarded(self):
        rows,h,u,e,*_ = self.fixture()
        with self.assertRaisesRegex(ValueError,'membership'):d.validate(rows*2,h,u,e)
        with self.assertRaisesRegex(ValueError,'membership'):d.validate(rows,{},u,e)
        for key,value,msg in [('gap_bytes','1','accounting'),('covered_bytes','4','accounting'),
                              ('state','accepted','state'),('notes','complete','open scope')]:
            mutant=deepcopy(rows);mutant[0][key]=value
            with self.assertRaisesRegex(ValueError,msg):d.validate(mutant,h,u,e)
        rows,h,u,e,*_ = self.fixture(1);rows[0]['state']='code-covered-candidate'
        with self.assertRaisesRegex(ValueError,'state'):d.validate(rows,h,u,e)

    def test_unit_namespace_source_and_evidence_union_are_guarded(self):
        for key,value in [('artifact','th03-main'),('segment','0000'),('state','exact'),
                          ('boundary_state','unknown'),('source','src/main/a.cpp'),('file_offset','10')]:
            rows,h,u,e,*_ = self.fixture();u['u'][key]=value
            with self.assertRaisesRegex(ValueError,'unit namespace'):d.validate(rows,h,u,e)
        rows,h,u,e,*_ = self.fixture();rows[0]['evidence_ids']='other'
        with self.assertRaisesRegex(ValueError,'reference union'):d.validate(rows,h,u,e)
        rows[0]['unit_ids']=''
        with self.assertRaisesRegex(ValueError,'references empty'):d.validate(rows,h,u,e)

    def test_missing_failed_and_wrong_oracle_evidence_are_rejected(self):
        rows,h,u,e,*_ = self.fixture()
        with self.assertRaisesRegex(ValueError,'evidence missing'):d.validate(rows,h,u,{})
        for key,value in [('artifact','th03-op'),('oracle','oracle-accepted'),('output_sha256','')]:
            mutant=deepcopy(e);mutant['e'][key]=value
            with self.assertRaisesRegex(ValueError,'evidence missing'):d.validate(rows,h,u,mutant)
        mutant=deepcopy(e);mutant['e']['result']='fail'
        with self.assertRaisesRegex(ValueError,'failed evidence'):d.validate(rows,h,u,mutant)
        rows[0]['failed_evidence_ids']='e'
        with self.assertRaisesRegex(ValueError,'lacks passing'):d.validate(rows,h,u,mutant)
        mutant['f']=dict(mutant['e'],id='f',result='pass');u['u']['evidence_ids']='e;f';rows[0]['evidence_ids']='e;f'
        d.validate(rows,h,u,mutant)

    def test_missing_and_overlapping_carriers_are_rejected(self):
        rows,h,u,e,observed,comps = self.fixture()
        with self.assertRaisesRegex(ValueError,'carrier missing'):d.summarize(['a.cpp'],[],comps,h,u,e)
        observed[0]['overlapping_unit_bytes']=1
        with self.assertRaisesRegex(ValueError,'ownership overlaps'):d.summarize(['a.cpp'],observed,comps,h,u,e)


if __name__=='__main__':unittest.main()
