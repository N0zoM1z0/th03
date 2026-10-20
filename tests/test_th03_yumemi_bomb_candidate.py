"""Source-only controls; fixture replay never launches a native tool."""
import copy
import os
from pathlib import Path
import struct
import tempfile
import tomllib
import unittest
from lib import th03_player_tail_candidate as tail
from lib import th03_yumemi_bomb_candidate as bomb
from lib import th03_score_candidate as score
from lib.pc98 import parse_mz

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('TH03_BOMB_PRIVATE_ROOT',ROOT))
BASE = PRIVATE/bomb.BASELINE/'round1/source'
RETAINED = PRIVATE/'.analysis/gpt-dots-yumemi-bomb-retained-continuation-v01/run-first-v01/source'

class Composition(unittest.TestCase):
    def setUp(self):
        self.default = tail.pre_tail_config(tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text()))
        self.accepted = bomb.pre_bomb_config(self.default)
        self.candidate = tomllib.loads((ROOT/bomb.CANDIDATE_PATH).read_text())

    def test_default_exact_inverse_and_unchanged_return(self):
        before = copy.deepcopy(self.default)
        result, original = bomb.bind_default(self.default)
        self.assertEqual(result, before)
        self.assertEqual(self.default, before)
        self.assertEqual(original, score.ORIGINAL_OWNER)
        self.assertEqual(bomb.digest(self.accepted), score.DEFAULT_CONFIG_DIGEST)
        expected = copy.deepcopy(self.accepted)
        expected['units'] += copy.deepcopy(self.candidate['units'])
        expected['functions'] += copy.deepcopy(self.candidate['functions'])
        self.assertEqual(expected, self.default)
        result['units'][-1]['source'] += '.changed'
        self.assertEqual(self.default, before)

    def test_default_rejects_prior_candidate_and_duplicate_candidate(self):
        with self.assertRaises(ValueError): bomb.bind_default(self.accepted)
        with self.assertRaises(ValueError):
            bomb.bind_candidate(self.default, self.candidate, bomb.CANDIDATE_PATH)

    def test_default_every_append_and_prior_graph_change_rejected(self):
        mutations = [
            lambda c: c['units'][-1].update(source='other.cpp'),
            lambda c: c['functions'][-1].update(size=697),
            lambda c: c['units'][0].update(source='other.cpp'),
            lambda c: c['units'].reverse(),
            lambda c: c['functions'].reverse(),
            lambda c: c['units'].append(copy.deepcopy(c['units'][-1])),
            lambda c: c['functions'].append(copy.deepcopy(c['functions'][-1])),
            lambda c: c['units'].pop(),
            lambda c: c['functions'].pop(),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                changed = copy.deepcopy(self.default)
                mutate(changed)
                with self.assertRaises(ValueError): bomb.pre_bomb_config(changed)
                with self.assertRaises(ValueError): bomb.bind_default(changed)

    def test_inverse_checks_independent_of_outer_digest(self):
        # Prove descriptor and inverse gates independently, even if a mistaken
        # future edit were to repin the full-default digest.
        from unittest.mock import patch
        for field in ('units', 'functions'):
            changed = copy.deepcopy(self.default)
            changed[field][-1]['extra'] = 'drift'
            with patch.object(bomb, 'DEFAULT_CONFIG_DIGEST', bomb.digest(changed)):
                with self.assertRaisesRegex(ValueError, 'final bomb'):
                    bomb.pre_bomb_config(changed)
        changed = copy.deepcopy(self.default)
        changed['units'][0]['source'] += '.changed'
        with patch.object(bomb, 'DEFAULT_CONFIG_DIGEST', bomb.digest(changed)):
            with self.assertRaisesRegex(ValueError, 'prior score ownership'):
                bomb.pre_bomb_config(changed)

    def test_binding_does_not_modify(self):
        before = copy.deepcopy(self.accepted),copy.deepcopy(self.candidate)
        bomb.bind_candidate(self.accepted,self.candidate,bomb.CANDIDATE_PATH)
        self.assertEqual(before,(self.accepted,self.candidate))
        self.assertTrue(bomb.is_bomb_owner(self.candidate['units'][0]))

    def test_accepted_score_drift_rejected(self):
        self.accepted['units'][0]['source'] += '.changed'
        with self.assertRaises(ValueError): bomb.bind_candidate(self.accepted,self.candidate,bomb.CANDIDATE_PATH)

    def test_addition_drift_rejected(self):
        self.candidate['units'][0]['source'] += '.changed'
        self.assertFalse(bomb.is_bomb_owner(self.candidate['units'][0]))
        with self.assertRaises(ValueError): bomb.bind_candidate(self.accepted,self.candidate,bomb.CANDIDATE_PATH)

    def test_wrong_manifest_rejected(self):
        with self.assertRaises(ValueError): bomb.bind_candidate(self.accepted,self.candidate,'config/other.toml')

    def test_mixed_graph_not_accepted_baseline(self):
        self.accepted['units'] += self.candidate['units']
        with self.assertRaises(ValueError): bomb.bind_candidate(self.accepted,self.candidate,bomb.CANDIDATE_PATH)

@unittest.skipUnless((RETAINED/'bin/th03/main.exe').is_file(),'private retained fixtures unavailable')
class RetainedControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target=(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes()
        cls.baseline=(BASE/'bin/th03/main.exe').read_bytes()
        cls.current=(RETAINED/'bin/th03/main.exe').read_bytes()
        cls.oldmap=(BASE/'obj/th03/main.map').read_bytes().decode('ascii')
        cls.newmap=(RETAINED/'obj/th03/main.map').read_bytes().decode('ascii')
        cls.object=(RETAINED/bomb.OBJECT).read_bytes()

    def compare(self,current=None,newmap=None):
        return bomb.compare_main(self.target,self.current if current is None else current,self.baseline,self.oldmap,self.newmap if newmap is None else newmap)

    def payload_mutation(self,address):
        raw=bytearray(self.current);start=int.from_bytes(raw[8:10],'little')*16
        raw[start+address]^=1
        return bytes(raw)

    def relocation_stream(self,pairs):
        raw=bytearray(self.current);offset=int.from_bytes(raw[24:26],'little')
        self.assertEqual(len(pairs),1553)
        for i,(s,o) in enumerate(pairs):struct.pack_into('<HH',raw,offset+i*4,o,s)
        return bytes(raw)

    def test_retained_positive(self):self.assertTrue(self.compare()['pass_'])

    def test_complete_models_match_frozen_model(self):
        import json
        model=json.loads((PRIVATE/'.analysis/gpt-dots-yumemi-bomb-producer-boundary-review-v01/expected-model.json').read_bytes())
        old=[[r.segment,r.offset] for r in parse_mz(self.baseline).relocations]
        self.assertEqual(bomb.expected_stream(old),model['full_literal_stream'])
        rows,prefix=bomb.expected_map(self.oldmap)
        self.assertEqual([list(r) for r in rows],model['rows'])
        self.assertEqual(prefix,model['aggregate_prefix'])
        self.assertEqual([[list(r) for r in section] for section in bomb.expected_publics(score.public_sections(self.oldmap))],model['public_sections'])

    def test_bomb_raw_mutation(self):
        r=self.compare(self.payload_mutation(0x159FF));self.assertFalse(r['pass_']);self.assertFalse(r['checks']['bomb698_raw_and_20_literal_order'])

    def test_outside_raw_mutation(self):
        r=self.compare(self.payload_mutation(0xC7F0));self.assertFalse(r['pass_']);self.assertFalse(r['checks']['complete_outside_raw'])

    def test_score_new366_mutation(self):
        self.assertFalse(self.compare(self.payload_mutation(0xD50E))['score_preservation']['pass_'])

    def test_score_old88_mutation(self):
        self.assertFalse(self.compare(self.payload_mutation(0xD5B0))['score_preservation']['score_add88_raw_no_relocations'])

    def test_angle_storage_mutation(self):
        r=self.compare(self.payload_mutation(0x1DCEC));self.assertFalse(r['checks']['angle_storage']);self.assertFalse(r['score_preservation']['storage_equal'])

    def test_wrong_producer_boundary_rejected_even_outside_equal(self):
        old=[[r.segment,r.offset] for r in parse_mz(self.baseline).relocations]
        wrong=old[:946]+bomb.PAIRS+old[966:]
        r=self.compare(self.relocation_stream(wrong))
        self.assertTrue(r['checks']['outside1533_literal_order'])
        self.assertFalse(r['checks']['full1553_producer_boundary_stream']);self.assertFalse(r['pass_'])

    def test_outside_literal_swap_rejected(self):
        pairs=[[r.segment,r.offset] for r in parse_mz(self.current).relocations]
        pairs[0],pairs[1]=pairs[1],pairs[0]
        r=self.compare(self.relocation_stream(pairs));self.assertFalse(r['pass_']);self.assertFalse(r['checks']['outside1533_literal_order'])

    def test_bomb_literal_swap_rejected(self):
        pairs=[[r.segment,r.offset] for r in parse_mz(self.current).relocations]
        pairs[452],pairs[453]=pairs[453],pairs[452]
        self.assertFalse(self.compare(self.relocation_stream(pairs))['checks']['bomb698_raw_and_20_literal_order'])

    def test_MAP_module_case_not_normalized(self):
        altered=self.newmap.replace('bomb~cxk.cpp','BOMB~CXK.cpp')
        self.assertNotEqual(altered,self.newmap)
        self.assertFalse(self.compare(newmap=altered)['checks']['complete_MAP_vector'])

    def test_MAP_zero_segment_not_ignored(self):
        altered=self.newmap.replace('BOMB~CXK_TEXT','BOMB~CYK_TEXT')
        r=self.compare(newmap=altered);self.assertFalse(r['checks']['aggregate_prefix']);self.assertFalse(r['checks']['complete_MAP_vector'])

    def test_public_tie_order_not_generic(self):
        names,values=self.newmap.split('Publics by Value')
        values=values.replace('VSYNC_END','XX_TEMP_XX').replace('VSYNC_LEAVE','VSYNC_END').replace('XX_TEMP_XX','VSYNC_LEAVE')
        self.assertFalse(self.compare(newmap=names+'Publics by Value'+values)['checks']['complete_public_sequences'])

    def test_source_transform_exact(self):
        raw=(BASE/'th03_main.asm').read_bytes();result=bomb.transform_root(raw)
        self.assertEqual(bomb.sha(result),bomb.ROOT_AFTER)
        self.assertEqual(result,(RETAINED/'th03_main.asm').read_bytes())
        with self.assertRaises(ValueError):bomb.transform_root(raw+b' ')
        with self.assertRaises(ValueError):bomb.transform_root(result)

    def test_actual_OMF_identity_and_mutation(self):
        self.assertEqual(bomb.validate_object(self.object)['normalized_sha256'],bomb.OMF_SHA)
        raw=bytearray(self.object);raw[10]^=1
        with self.assertRaises((ValueError,AssertionError)):bomb.validate_object(bytes(raw))

    def test_providers_positive(self):self.assertTrue(bomb.check_providers(PRIVATE,RETAINED)['pass_'])

    def test_root_provider_mutation_rejected(self):
        # Keep OMF framing/checksum valid while changing a tied PUBDEF.
        from lib.omf import parse_omf
        raw=bytearray((RETAINED/'obj/th03/main.obj').read_bytes())
        record=next(r for r in parse_omf(bytes(raw)) if r.record_type==0x90 and b'VSYNC_END' in r.data)
        i=record.offset+3+record.data.index(b'VSYNC_END')
        raw[i]^=1
        end=record.offset+3+record.length
        raw[end-1]=(-sum(raw[record.offset:end-1]))&255
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);(work/'obj/th03').mkdir(parents=True)
            (work/'obj/th03/main.obj').write_bytes(raw)
            with self.assertRaises(ValueError):bomb.check_providers(PRIVATE,work)


    def staging(self,work,default=False):
        for n in bomb.SOURCE_PINS:
            p=work/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((PRIVATE/n).read_bytes())
        (work/'th03_main.asm').write_bytes((BASE/'th03_main.asm').read_bytes())
        (work/'build.bat').write_bytes((BASE/'build.bat').read_bytes())
        (work/'obj/th03').mkdir(parents=True);bomb.stage_bomb(work,default=default)

    def test_default_stage_keeps_original_build_and_checks_mode(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work,default=True)
            self.assertEqual((work/'build.bat').read_bytes(), (BASE/'build.bat').read_bytes())
            self.assertEqual(bomb.sha((work/'th03_main.asm').read_bytes()), bomb.ROOT_AFTER)
            bomb.check_build(work, default=True)
            with self.assertRaises(ValueError): bomb.check_build(work)
            with self.assertRaises(ValueError): bomb.stage_bomb(work, default=True)
            (work/'build.bat').write_bytes((work/'build.bat').read_bytes()+b' ')
            with self.assertRaises(ValueError): bomb.check_build(work, default=True)
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work)
            bomb.check_build(work)
            with self.assertRaises(ValueError): bomb.check_build(work, default=True)

    def test_default_precompile_original_build_and_fresh_output(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work,default=True)
            original=(work/'build.bat').read_bytes()
            def simulated(argv,cwd,env,log):
                (cwd/bomb.ALIAS).write_bytes(self.object)
                return {'exit_code':0,'simulated_test_only':True}
            result=bomb.precompile(work,{},work,simulated,default=True)
            self.assertTrue(result['byte_identical_move'])
            self.assertEqual((work/'build.bat').read_bytes(),original)
            with self.assertRaises(ValueError):
                bomb.precompile(work,{},work,lambda *a:self.fail('cached'),default=True)

    def test_both_modes_reject_wrong_root_before_writing_build(self):
        for default in (False,True):
            with tempfile.TemporaryDirectory() as d:
                work=Path(d)
                for n in bomb.SOURCE_PINS:
                    p=work/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((PRIVATE/n).read_bytes())
                raw=(BASE/'th03_main.asm').read_bytes()+b' '
                build=(BASE/'build.bat').read_bytes()
                (work/'th03_main.asm').write_bytes(raw)
                (work/'build.bat').write_bytes(build)
                with self.assertRaises(ValueError): bomb.stage_bomb(work,default=default)
                self.assertEqual((work/'th03_main.asm').read_bytes(),raw)
                self.assertEqual((work/'build.bat').read_bytes(),build)

    def test_precompile_contract_simulated_callback_only(self):
        calls=[]
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work)
            def simulated(argv,cwd,env,log):
                calls.append(argv);(cwd/bomb.ALIAS).write_bytes(self.object)
                return {'exit_code':0,'simulated_test_only':True}
            result=bomb.precompile(work,{},work,simulated)
            self.assertEqual(len(calls),1)
            self.assertIn('src/main/player/bomb_yumemi.cpp',calls[0][-1])
            self.assertEqual((work/bomb.OBJECT).read_bytes(),self.object)
            self.assertFalse((work/bomb.ALIAS).exists());self.assertTrue(result['byte_identical_move'])

    def test_precompile_creates_fresh_output_parent_before_runner(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work)
            (work/'obj/th03').rmdir();(work/'obj').rmdir()
            self.assertFalse((work/'obj').exists())
            self.assertFalse((work/'obj/th03').exists())
            calls=[]
            def simulated(argv,cwd,env,log):
                self.assertTrue((cwd/'obj/th03').is_dir())
                self.assertEqual(list((cwd/'obj/th03').iterdir()),[])
                calls.append(argv);(cwd/bomb.ALIAS).write_bytes(self.object)
                return {'exit_code':0,'simulated_test_only':True}
            result=bomb.precompile(work,{},work,simulated)
            self.assertEqual(len(calls),1)
            self.assertTrue(result['byte_identical_move'])
            self.assertEqual((work/bomb.OBJECT).read_bytes(),self.object)

    def test_precompile_rejects_symlink_output_parent(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)/'stage';work.mkdir();self.staging(work)
            (work/'obj/th03').rmdir();(work/'obj').rmdir()
            outside=Path(d)/'outside';outside.mkdir();(work/'obj').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):
                bomb.precompile(work,{},work,lambda *a:self.fail('must not execute'))
            self.assertEqual(list(outside.iterdir()),[])

    def test_precompile_cached_object_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work);(work/bomb.OBJECT).write_bytes(self.object)
            with self.assertRaises(ValueError):bomb.precompile(work,{},work,lambda *a:self.fail('must not execute'))

    def test_precompile_extra_object_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work)
            def simulated(argv,cwd,env,log):
                (cwd/bomb.ALIAS).write_bytes(self.object);(cwd/'obj/th03/extra.obj').write_bytes(self.object)
                return {'exit_code':0}
            with self.assertRaises(ValueError):bomb.precompile(work,{},work,simulated)

    def test_complete_round_model_both_baselines_and_extra_object(self):
        self.complete_round_model(default=False)

    def test_default_complete_round_model_both_baselines_and_extra_object(self):
        self.complete_round_model(default=True)

    def complete_round_model(self,default):
        # This is a source-only model assembled from already-frozen evidence,
        # not a native/cold execution or evidence for fresh object provenance.
        import json
        proof=json.loads((PRIVATE/bomb.PROOF_GUARD).read_bytes())[bomb.BASELINE]['files']
        receipt=json.loads((PRIVATE/bomb.BASELINE/'receipt.json').read_bytes())
        prefix='round1/source/'
        names=set(receipt['rounds'][0]['all_objects'])
        names.update(n[len(prefix):] for n in proof if n.startswith(prefix) and
                     (n.endswith('.map') or n[len(prefix):].startswith('bin/')))
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)
            for n in names:
                p=work/n;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to((BASE/n).resolve())
            for n in (*bomb.SOURCE_PINS,'th03_main.asm',bomb.OBJECT,'obj/th03/main.obj','obj/th03/main.map','obj/th03/main.@l','bin/th03/main.exe'):
                p=work/n;p.parent.mkdir(parents=True,exist_ok=True)
                if p.is_symlink():p.unlink()
                origin=PRIVATE/n if n in bomb.SOURCE_PINS else RETAINED/n
                p.write_bytes(origin.read_bytes())
            # Source-only fixture root: the historical proof/library surfaces stay
            # read-only and only the selected config and build carrier vary.
            fixture=work/'fixture-root';(fixture/'config').mkdir(parents=True)
            (fixture/'.analysis').symlink_to((PRIVATE/'.analysis').resolve(),target_is_directory=True)
            (fixture/'config/toolchain.toml').write_bytes((PRIVATE/'config/toolchain.toml').read_bytes())
            full=(ROOT/'config/th03_main_exact_units.toml').read_text()
            tail_candidate=(ROOT/tail.CANDIDATE_PATH).read_text()
            tail_suffix=tail_candidate[tail_candidate.index('[[units]]'):]
            self.assertTrue(full.endswith(tail_suffix))
            current=tomllib.loads(full);full=full[:-len(tail_suffix)]
            self.assertEqual(tomllib.loads(full),tail.pre_tail_config(current))
            integration_note='\n# Complete PLAYER_M tail: source-present default integration; cold proof pending.\n'
            self.assertTrue(full.endswith(integration_note));full=full[:-len(integration_note)]
            prior=bomb.pre_bomb_config(tomllib.loads(full))
            if not default:
                # Exact final candidate text only, followed by parsed inverse
                # equality. This is fixture setup, never production binding.
                candidate=(ROOT/bomb.CANDIDATE_PATH).read_text()
                suffix=candidate[candidate.index('[[units]]'):]
                self.assertTrue(full.endswith(suffix))
                full=full[:-len(suffix)]
                self.assertEqual(tomllib.loads(full),prior)
            (fixture/'config/th03_main_exact_units.toml').write_text(full)
            build=(BASE/'build.bat').read_bytes()
            if not default: build=build.replace(bomb.BUILD_BEFORE,bomb.BUILD_AFTER,1)
            (work/'build.bat').write_bytes(build)
            result=bomb.check_round(fixture,work,self.target,proof,default=default)
            self.assertTrue(result['pass_']);self.assertTrue(result['score_preservation']['pass_'])
            self.assertEqual([x['baseline_round'] for x in result['baselines']],[1,2])
            (work/'obj/th03/extra.obj').write_bytes(self.object)
            with self.assertRaisesRegex(ValueError,'inventory'):
                bomb.check_round(fixture,work,self.target,proof,default=default)

    def test_stage_requires_accepted_score(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d);self.staging(work)
            with self.assertRaises(ValueError):bomb.stage_bomb(work)
            (work/score.MODULE).write_bytes(b'drift')
            with self.assertRaises(ValueError):bomb.check_sources(work)

if __name__=='__main__':unittest.main()
