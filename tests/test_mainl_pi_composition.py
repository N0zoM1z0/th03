"""Composition closes scoped bytes, never whole-product exact acceptance."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/mainl-pi-composition-output-20261021-v01/completion.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
proof=load('composition_proof',ROOT/'scripts/replay_th03_mainl_pi_composition.py')
progress=load('composition_progress',ROOT/'scripts/progress.py')
class CompositionProofTests(unittest.TestCase):
    def test_retained_scope_and_selected_runtime(self):
        result=proof.replay();detail=result['linked_diagnostics']
        self.assertTrue(result['checks_pass']);self.assertEqual(result['native_invocations_this_replay'],0)
        self.assertEqual(result['retained_other_objects'],29);self.assertFalse(result['exact_acceptance'])
        self.assertTrue(result['fresh_scanner_context_only']);self.assertTrue(result['preexisting_independent_owned_object_pairs'])
        self.assertEqual(detail['owned_bytes'],6144);self.assertTrue(detail['owned_raw_target_equal'])
        self.assertEqual(detail['full_decoded_target_difference_count'],21)
        self.assertEqual(detail['full_target_relocations']['left_count'],677)
        self.assertTrue(detail['full_target_relocations']['membership_equal']);self.assertFalse(detail['full_target_relocations']['ordered_equal'])
        self.assertEqual([x['registration']['entry_calls'] for x in detail['runtime_runs']],[152]*3)
        self.assertEqual([x['cutscene']['entry_calls'] for x in detail['runtime_runs']],[65]*3)
        self.assertFalse(detail['contextual_scanner']['owned'])
    def test_source_identity_mutation_rejected(self):
        m=copy.deepcopy(proof.retained('manifest'));m['sources']['src/mainl/regist.cpp']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity differs'):proof.source_bindings(m)
    def test_retained_identity_mutation_rejected(self):
        with self.assertRaisesRegex(ValueError,'identity differs'):
            proof.reg.read_verified(proof.PROOF_DIRECTORY+'/completion.json','0'*64)
    def test_byte_diff_records_lengths_without_normalization(self):
        self.assertEqual(proof.byte_differences(b'ab',b'acd'),[{'linear':1,'left':98,'right':99},{'linear':2,'left':None,'right':100}])

def fixture():
    units=[];evidence=[]
    for name,offset,size in [('cutscene','0xb3e','3195'),('scoredat','0x17b9','229'),('regist','0x189e','2720')]:
        uid='th03-mainl-decoded-'+name;eid='ev-th03-mainl-'+name+'-pi-composition-raw'
        units.append(dict(id=uid,artifact='th03-mainl',segment='decoded:095F',offset=offset,size=size,state='source-present',boundary_state='reviewed',source='src/mainl/'+name+'.cpp',evidence_ids=eid))
        evidence.append(dict(id=eid,artifact='th03-mainl',unit_id=uid,oracle='analysis-bundle',extent_start=offset,extent_size=size,evidence_class='binary',result='pass',output_sha256=progress.MAINL_PI_COMPOSITION_RECEIPT))
    return units,evidence
class CompositionCaptionTests(unittest.TestCase):
    def test_evidence_caption_does_not_grant_exact(self):
        units,evidence=fixture();self.assertTrue(progress.mainl_pi_composed(units,evidence))
        svg=progress.render_svg(units,[],evidence)
        self.assertIn('6,144 B target-equal',svg);self.assertIn('Historical PI composition: 6,144 B target-equal · 9 gaps closed · not current total',svg)
        self.assertIn('Source 3/3',svg);self.assertIn('exact 0/3',svg)
    def test_incomplete_mutated_or_wrong_source_hides_caption(self):
        units,evidence=fixture();self.assertFalse(progress.mainl_pi_composed(units,evidence[:-1]))
        for key,value in [('result','fail'),('output_sha256','0'*64),('extent_size','3194')]:
            bad=copy.deepcopy(evidence);bad[0][key]=value;self.assertFalse(progress.mainl_pi_composed(units,bad))
        units[0]['source']='src/other.cpp';self.assertFalse(progress.mainl_pi_composed(units,evidence))
