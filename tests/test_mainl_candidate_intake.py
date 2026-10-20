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

    def test_independent_source_presence_keeps_index_acceptance_false(self):
        rows,h,u,e,*_ = self.fixture()
        u['u'].update(state='source-present', source='src/shared/formats/cdg_load.cpp',
                      replay_command='python3 scripts/replay_th03_shared_cdg_load.py --run-id NEW')
        refs=['e']
        for i, klass in enumerate(('compiler','runtime','reproducibility')):
            name=f'cold{i}';refs.append(name)
            e[name]=dict(e['e'],id=name,evidence_class=klass)
        u['u']['evidence_ids']=rows[0]['evidence_ids']=';'.join(refs)
        d.validate(rows,h,u,e)
        self.assertEqual(rows[0]['source_accepted'],'false')
        self.assertEqual(rows[0]['exact_accepted'],'false')
        for source in ('src/op/cdg.cpp','../cdg.cpp','src/shared/a.hpp'):
            bad=deepcopy(u);bad['u']['source']=source
            with self.assertRaisesRegex(ValueError,'source ownership'):d.validate(rows,h,bad,e)
        bad=deepcopy(e);bad['cold2']['evidence_class']='upstream'
        with self.assertRaisesRegex(ValueError,'independent cold'):d.validate(rows,h,u,bad)
        bad=deepcopy(u);bad['u']['replay_command']='python3 scripts/review_th03_shared_cdg_load.py'
        with self.assertRaisesRegex(ValueError,'independent cold'):d.validate(rows,h,bad,e)


class RetainedHeapSourceCheckpointTests(unittest.TestCase):
    """The one retained source exception must not relax integration/acceptance."""
    def setUp(self):
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source_bytes = (Path(__file__).resolve().parents[1] / d.RETAINED_HEAP_SOURCE).read_bytes()
        self.source = self.root / d.RETAINED_HEAP_SOURCE
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(self.source_bytes)
        root_patch = patch.object(d, 'ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def fixture(self):
        unit = dict(
            id=d.RETAINED_HEAP_UNIT, artifact='th03-mainl', kind='module-candidate',
            segment='decoded:0000', offset='0x210a', file_offset='', size='628',
            compare_size='628', boundary_state='reviewed', origin='library',
            state='source-present', source=d.RETAINED_HEAP_SOURCE,
            replay_command=d.RETAINED_HEAP_REVIEW,
            evidence_ids=';'.join(sorted(d.RETAINED_HEAP_LEGACY | set(d.RETAINED_HEAP_EVIDENCE))))
        evidence = {name: dict(id=name, artifact='th03-mainl', oracle='analysis-bundle',
                              result='pass', output_sha256='b'*64,
                              evidence_class='compiler' if name.endswith('producers') else 'runtime')
                    for name in d.RETAINED_HEAP_LEGACY}
        for name, (kind, result, location, digest) in d.RETAINED_HEAP_EVIDENCE.items():
            evidence[name] = dict(
                id=name, oracle='analysis-bundle', artifact='th03-mainl',
                unit_id=d.RETAINED_HEAP_UNIT, extent_start='0x210a', extent_size='628',
                evidence_class=kind, result=result, location=location,
                input_sha256=d.RETAINED_HEAP_SHA, output_sha256=digest)
        row = dict(
            artifact='th03-mainl', path='th03_mainl.asm', frozen_revision=d.REVISION,
            frozen_sha256='0144b4c14d948a993d5da4f9591ea39c0f17772cba9cd47a6eda1e8e52a283d6',
            scope=d.SCOPE, state='code-covered-candidate',
            unit_ids=d.RETAINED_HEAP_UNIT, evidence_ids=unit['evidence_ids'],
            failed_evidence_ids='ev-th03-mainl-heap-native-attempt-failed',
            carrier_bytes='628', covered_bytes='628', gap_bytes='0',
            raw_equal='true', ordered_relocations_equal='true',
            source_accepted='false', exact_accepted='false', receipt=d.PROOF, notes=d.OPEN)
        return [row], {row['path']: row['frozen_sha256']}, {unit['id']: unit}, evidence

    def test_exact_retained_source_admitted_without_cold_or_acceptance(self):
        rows, hashes, units, evidence = self.fixture()
        self.assertEqual(d.sha(self.source_bytes),
                         '3960b8f2ff1821475f86d947b82380957a35ce4c7169a518689e857560774432')
        self.assertNotIn('reproducibility', {e['evidence_class'] for e in evidence.values()})
        d.validate(rows, hashes, units, evidence)
        self.assertEqual(rows[0]['source_accepted'], 'false')
        self.assertEqual(rows[0]['exact_accepted'], 'false')
        self.assertEqual(evidence['ev-th03-mainl-heap-native-attempt-failed']['result'], 'fail')

    def test_wrong_unit_identity_source_path_span_and_state_rejected(self):
        changes = {
            'id': 'different', 'artifact': 'th03-main', 'kind': 'function',
            'segment': 'decoded:0001', 'offset': '0x210b', 'file_offset': '1',
            'size': '625', 'compare_size': '625', 'boundary_state': 'provisional',
            'origin': 'authored', 'state': 'exact', 'source': 'src/mainl/other.inl',
        }
        for key, value in changes.items():
            with self.subTest(key=key):
                rows, hashes, units, evidence = self.fixture()
                units[d.RETAINED_HEAP_UNIT][key] = value
                with self.assertRaises(ValueError):
                    d.validate(rows, hashes, units, evidence)

    def test_wrong_diagnostic_provenance_and_acceptance_rejected_directly(self):
        changes = {
            'artifact': 'th03-op', 'path': 'other.asm', 'frozen_revision': 'HEAD',
            'frozen_sha256': '0'*64, 'scope': 'whole-file', 'receipt': 'other.json',
            'source_accepted': 'true', 'exact_accepted': 'true',
        }
        for key, value in changes.items():
            with self.subTest(key=key):
                rows, hashes, units, evidence = self.fixture()
                rows[0][key] = value
                with self.assertRaisesRegex(ValueError, 'diagnostic provenance/acceptance'):
                    d.retained_heap_source_checkpoint(rows[0], units[d.RETAINED_HEAP_UNIT], evidence)

    def test_every_new_evidence_binding_rejects_identity_scope_hash_and_status_drift(self):
        changes = {
            'id': 'other', 'oracle': 'raw-bytes', 'artifact': 'th03-main',
            'unit_id': 'other', 'extent_start': '0x210b', 'extent_size': '625',
            'evidence_class': 'reproducibility', 'result': 'not-run',
            'location': 'other.json', 'input_sha256': '0'*64, 'output_sha256': '0'*64,
        }
        for name in d.RETAINED_HEAP_EVIDENCE:
            for key, value in changes.items():
                with self.subTest(name=name, key=key):
                    rows, hashes, units, evidence = self.fixture()
                    evidence[name][key] = value
                    with self.assertRaises(ValueError):
                        d.validate(rows, hashes, units, evidence)

    def test_original_failed_receipt_cannot_be_omitted_hidden_or_reclassified(self):
        failed = 'ev-th03-mainl-heap-native-attempt-failed'
        for mutation in ('record', 'references', 'failed-list', 'status'):
            with self.subTest(mutation=mutation):
                rows, hashes, units, evidence = self.fixture()
                if mutation == 'record':
                    del evidence[failed]
                elif mutation == 'references':
                    refs = units[d.RETAINED_HEAP_UNIT]['evidence_ids'].split(';')
                    refs.remove(failed)
                    units[d.RETAINED_HEAP_UNIT]['evidence_ids'] = rows[0]['evidence_ids'] = ';'.join(refs)
                    rows[0]['failed_evidence_ids'] = ''
                elif mutation == 'failed-list':
                    rows[0]['failed_evidence_ids'] = ''
                else:
                    evidence[failed]['result'] = 'pass'
                with self.assertRaises(ValueError):
                    d.validate(rows, hashes, units, evidence)

    def test_retained_diagnostic_cannot_claim_reproducibility_or_replay_integration(self):
        rows, hashes, units, evidence = self.fixture()
        legacy = next(iter(d.RETAINED_HEAP_LEGACY))
        evidence[legacy]['evidence_class'] = 'reproducibility'
        with self.assertRaisesRegex(ValueError, 'cannot claim cold reproducibility'):
            d.validate(rows, hashes, units, evidence)
        rows, hashes, units, evidence = self.fixture()
        units[d.RETAINED_HEAP_UNIT]['replay_command'] = 'python3 scripts/replay_th03_mainl_heap.py --run-id NEW'
        with self.assertRaisesRegex(ValueError, 'independent cold'):
            d.validate(rows, hashes, units, evidence)
        rows, hashes, units, evidence = self.fixture()
        units[d.RETAINED_HEAP_UNIT]['replay_command'] = 'python3 scripts/review_th03_mainl_heap.py --output different.json'
        with self.assertRaisesRegex(ValueError, 'independent cold'):
            d.validate(rows, hashes, units, evidence)

    def test_source_bytes_missing_file_and_symlink_are_rejected(self):
        rows, hashes, units, evidence = self.fixture()
        self.source.write_bytes(self.source_bytes + b'; drift\n')
        with self.assertRaisesRegex(ValueError, 'source SHA-256'):
            d.validate(rows, hashes, units, evidence)
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, 'source missing'):
            d.validate(rows, hashes, units, evidence)
        actual = self.root / 'actual.inl'
        actual.write_bytes(self.source_bytes)
        self.source.symlink_to(actual)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            d.validate(rows, hashes, units, evidence)

    def test_unrelated_unit_cannot_borrow_retained_exception(self):
        rows, hashes, units, evidence = self.fixture()
        unit = units.pop(d.RETAINED_HEAP_UNIT)
        unit['id'] = 'unrelated-source'
        units[unit['id']] = unit
        rows[0]['unit_ids'] = unit['id']
        with self.assertRaisesRegex(ValueError, 'independent cold'):
            d.validate(rows, hashes, units, evidence)

    def test_candidate_union_must_include_all_retained_records(self):
        rows, hashes, units, evidence = self.fixture()
        rows[0]['evidence_ids'] = ';'.join(sorted(d.RETAINED_HEAP_LEGACY))
        with self.assertRaisesRegex(ValueError, 'reference union'):
            d.validate(rows, hashes, units, evidence)
        rows, hashes, units, evidence = self.fixture()
        units[d.RETAINED_HEAP_UNIT]['evidence_ids'] += ';' + next(iter(d.RETAINED_HEAP_LEGACY))
        with self.assertRaisesRegex(ValueError, 'evidence IDs'):
            d.validate(rows, hashes, units, evidence)


if __name__=='__main__':unittest.main()
