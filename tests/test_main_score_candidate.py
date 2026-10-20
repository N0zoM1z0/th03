"""Pure score-candidate controls; no native invocation or acceptance publication."""
import copy
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from types import SimpleNamespace

from lib import th03_player_cpu_candidate as cpu
from lib import th03_score_candidate as c
from replay_th03_main_exact_units import (
    add_candidate_owners, apply_carrier_edits, normalized_code_extents,
    physical_object_count_delta, verify_disjoint_ownership, verify_include_carrier,
)
ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('TH03_SCORE_PRIVATE_ROOT', str(ROOT)))
BASE = PRIVATE/c.BASELINE
CANDIDATE = tomllib.loads((ROOT/c.CANDIDATE_PATH).read_text())
# Preserve the exact historical score-only contract through the validated
# inverse of the separately pinned, source-present bomb default addition.
from lib import th03_player_tail_candidate as tail
from lib import th03_yumemi_bomb_candidate as bomb
DEFAULT = bomb.pre_bomb_config(tail.pre_tail_config(cpu.pre_cpu_config(tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text()))))
ACCEPTED = copy.deepcopy(DEFAULT)
ACCEPTED['units'] = [copy.deepcopy(c.ORIGINAL_OWNER) if u['id']==c.BINDING['owner'] else u
                     for u in ACCEPTED['units'] if u['id']!='th03-main-score-hud']
ACCEPTED['functions'] = [f for f in ACCEPTED['functions'] if f['object']!='score_hud']
assert c.digest(ACCEPTED) == c.PRE_SCORE_CONFIG_DIGEST



class ScoreDescriptor(unittest.TestCase):
    def bind(self, candidate=CANDIDATE, accepted=ACCEPTED, path=c.CANDIDATE_PATH):
        return c.bind_candidate(add_candidate_owners(accepted,candidate),candidate,path)

    def test_only_physical_binding_changes(self):
        frozen=copy.deepcopy(ACCEPTED)
        effective,original=self.bind()
        self.assertEqual(ACCEPTED,frozen)
        owner=next(u for u in effective['units'] if u['id']==c.BINDING['owner'])
        self.assertEqual(original,next(u for u in ACCEPTED['units'] if u['id']==c.BINDING['owner']))
        restored=copy.deepcopy(owner)
        for key in ('carrier_path','carrier_sha256','overlay_path','object_path','map_module'):
            restored[key]=original[key]
        restored['code_extents'][0]['map_start']=original['code_extents'][0]['map_start']
        restored['code_extents'][0]['map_size']=original['code_extents'][0]['map_size']
        self.assertEqual(restored,original)
        self.assertEqual(effective['functions'][:len(ACCEPTED['functions'])],ACCEPTED['functions'])
        self.assertEqual(owner['object'],'score_add')
        self.assertEqual(owner['source'],'src/main/player/score_add.inl')

    def test_historical_descriptor_unchanged(self):
        unit=next(u for u in ACCEPTED['units'] if u['id']==c.BINDING['owner'])
        extent=normalized_code_extents(unit,ACCEPTED['segment'])[0]
        self.assertEqual((extent['map_start'],extent['map_size']),(0x29F8,0x15FC))
        self.assertEqual(extent['map_module'],'th03_main.asm')
        self.assertFalse(c.is_score_owner(unit))

    def test_generic_replacement_remains_forbidden(self):
        for units, functions in [([ACCEPTED['units'][0]], []), ([], [ACCEPTED['functions'][0]])]:
            with self.assertRaises(ValueError):
                add_candidate_owners(ACCEPTED,dict(schema_version=1,units=units,functions=functions))

    def test_receipt_score_field_remains_conditionally_conjunctive(self):
        import ast
        tree=ast.parse((ROOT/'scripts/replay_th03_main_exact_units.py').read_text())
        receipts=[node for node in ast.walk(tree) if isinstance(node,ast.Dict)
                  and {'candidate_sha256','behavior_pass'} <= {k.value for k in node.keys if isinstance(k,ast.Constant)}]
        self.assertEqual(len(receipts),1)
        self.assertNotIn('score_candidate_preservation',[k.value for k in receipts[0].keys if isinstance(k,ast.Constant)])
        guarded=[node for node in ast.walk(tree) if isinstance(node,ast.If)
                 and ast.unparse(node.test)=='score_preservation is not None']
        self.assertEqual(len(guarded),2)
        receipt_guards=[node for node in guarded if "report['rounds'][-1]['score_candidate_preservation'] = score_preservation" in ast.unparse(node)]
        failure_guards=[node for node in guarded if "if not score_preservation['pass_']:" in ast.unparse(node)]
        self.assertEqual(len(receipt_guards),1)
        self.assertEqual(len(failure_guards),1)

    def test_scope_and_object_count_are_additive(self):
        effective,_=self.bind()
        extents={u['id']:normalized_code_extents(u,effective['segment']) for u in effective['units']}
        verify_disjoint_ownership(extents)
        flat=[e for es in extents.values() for e in es]
        self.assertEqual((len(flat),sum(e['size'] for e in flat),len(effective['functions'])),(80,59990,377))
        self.assertEqual(physical_object_count_delta(CANDIDATE['units'][0]),1)
        self.assertEqual(sum(e['size'] for e in extents['th03-main-score-hud']),366)
        self.assertEqual(sum(p['size'] for e in extents['th03-main-score-hud'] for p in e['producer_ranges']),4)

    def test_unknown_or_changed_candidate_fields_rejected(self):
        variants=[]
        for key,value in [('source','src/main/elsewhere.asm'),('object','score_add'),('map_module','fake'),('unknown',True)]:
            x=copy.deepcopy(CANDIDATE);x['units'][0][key]=value;variants.append(x)
        x=copy.deepcopy(CANDIDATE);x['units'][0]['code_extents'][1]['start']-=1;variants.append(x)
        x=copy.deepcopy(CANDIDATE);x['functions'][0]['abi']='fake';variants.append(x)
        x=copy.deepcopy(CANDIDATE);x['units'][0]['physical_objects_additive']=False;variants.append(x)
        x=copy.deepcopy(CANDIDATE);del x['units'][0]['support_files'];variants.append(x)
        for x in variants:
            with self.subTest(x=x),self.assertRaises(ValueError):self.bind(x)
        with self.assertRaises(ValueError):self.bind(path='config/renamed.toml')

    def test_no_arbitrary_interior_owner_allowance(self):
        unit=copy.deepcopy(CANDIDATE['units'][0]);unit['id']='unrelated'
        with self.assertRaises(ValueError):normalized_code_extents(unit,0x96E)
        unit=copy.deepcopy(CANDIDATE['units'][0]);unit['code_extents'][1]['map_group']='fake'
        with self.assertRaises(ValueError):normalized_code_extents(unit,0x96E)

    def test_accepted_semantics_cannot_be_changed(self):
        for field in ('source','object','map_module','carrier_sha256'):
            x=copy.deepcopy(ACCEPTED);u=next(u for u in x['units'] if u['id']==c.BINDING['owner']);u[field]='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):self.bind(accepted=x)
        for field in ('abi','map_public','offset','size'):
            x=copy.deepcopy(ACCEPTED);f=next(f for f in x['functions'] if f['object']=='score_add');f[field]='changed'
            with self.subTest(field=field),self.assertRaises(ValueError):self.bind(accepted=x)

class DefaultScoreControls(unittest.TestCase):
    def test_exact_default_transition(self):
        effective, original = c.bind_default(DEFAULT)
        self.assertEqual(effective, DEFAULT)
        self.assertEqual(original, c.ORIGINAL_OWNER)
        expected, _ = ScoreDescriptor().bind()
        owner = next(u for u in expected['units'] if u['id']=='th03-main-score-hud')
        owner['carrier_edits'] = [e for e in owner['carrier_edits'] if e['path']!='build.bat']
        next(u for u in expected['units'] if u['id']==c.BINDING['owner'])['carrier_sha256']=c.DEFAULT_SCORE_SOURCE_SHA
        self.assertEqual(DEFAULT, expected)
        self.assertTrue(c.is_score_owner(owner))
        self.assertEqual(c.digest(owner),c.DEFAULT_SCORE_UNIT_DIGEST)

    def test_comment_only_source_transition(self):
        import hashlib
        raw=(ROOT/c.MODULE).read_bytes()
        new=b'; Maintained score HUD assembly; acceptance is recorded in the ledgers.'
        old=b'; Research source proposal, not compiled, installed or credited.'
        self.assertTrue(raw.startswith(new))
        prior=raw.replace(new,old,1)
        self.assertEqual(prior.split(b'\n',1)[1],raw.split(b'\n',1)[1])
        self.assertEqual(hashlib.sha256(prior).hexdigest(),c.SCORE_SOURCE_SHA)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),c.DEFAULT_SCORE_SOURCE_SHA)

    def test_duplicate_candidate_rejected(self):
        with self.assertRaises(ValueError):add_candidate_owners(DEFAULT,CANDIDATE)

    def test_no_stale_or_generic_default_binding(self):
        for field in ('carrier_path','carrier_sha256','object_path','overlay_path','map_module','source','object'):
            bad=copy.deepcopy(DEFAULT)
            owner=next(u for u in bad['units'] if u['id']==c.BINDING['owner'])
            owner[field]=c.ORIGINAL_OWNER[field] if owner[field]!=c.ORIGINAL_OWNER[field] else 'changed'
            with self.subTest(field=field),self.assertRaises(ValueError):c.bind_default(bad)
        for field in ('size','map_start','map_size'):
            bad=copy.deepcopy(DEFAULT)
            next(u for u in bad['units'] if u['id']==c.BINDING['owner'])['code_extents'][0][field]+=1
            with self.assertRaises(ValueError):c.bind_default(bad)
        bad=copy.deepcopy(DEFAULT);bad['functions'][0]['abi']='changed'
        with self.assertRaises(ValueError):c.bind_default(bad)
        bad=copy.deepcopy(DEFAULT);bad['units'][-1]['carrier_edits'].append(CANDIDATE['units'][0]['carrier_edits'][-1])
        with self.assertRaises(ValueError):c.bind_default(bad)

    def test_default_activation_and_precheck_order(self):
        text=(ROOT/'scripts/replay_th03_main_exact_units.py').read_text()
        self.assertIn('config, score_original = score_candidate.bind_default(config)',text)
        self.assertLess(text.index('verify_include_carrier(score_original, work)'),text.index('apply_carrier_edits(module, work)'))
        self.assertLess(text.index('shutil.copy2(snapshot / module["source"], overlay)'),text.index('score_candidate.check_stage(work, default=candidate_manifest is None or bomb_proof is not None)'))


class LiteralControls(unittest.TestCase):
    def image(self, pairs):
        return SimpleNamespace(relocations=[SimpleNamespace(segment=s,offset=o,linear=s*16+o) for s,o in pairs])

    def test_literal_order_and_representation_preserved(self):
        im=self.image([(1,3),(0,0x12),(1,3)])
        self.assertEqual(c.ordered_literal(im,[[0x10,0x20]]),[[1,3],[0,0x12],[1,3]])
        self.assertEqual(c.ordered_literal(im,[[0x10,0x20]],True),[])

    def test_both_edges_fail_closed(self):
        for offset in (0x0F,0x1F):
            with self.assertRaises(ValueError):c.ordered_literal(self.image([(0,offset)]),[[0x10,0x20]])

    def test_eight_ties_only(self):
        before=[];after=[]
        for (s,o),(old,new) in c.VALUE_TIES.items():
            before += [(s,o,n) for n in old];after += [(s,o,n) for n in new]
        self.assertTrue(c.value_public_order_equal(before,after))
        self.assertTrue(c.value_public_order_equal(before,before))
        for mutation in ('name','address','missing','duplicate','third'):
            bad=after[:]
            if mutation=='name':bad[0]=(*bad[0][:2],'unknown')
            elif mutation=='address':bad[0]=(bad[0][0],bad[0][1]+1,bad[0][2])
            elif mutation=='missing':bad.pop()
            elif mutation=='duplicate':bad.append(bad[-1])
            else:
                ii=[i for i,p in enumerate(bad) if p[:2]==(0x1D56,0x7C)];bad[ii[1]],bad[ii[2]]=bad[ii[2]],bad[ii[1]]
            with self.subTest(mutation=mutation):self.assertFalse(c.value_public_order_equal(before,bad))
        before += [(0xFFFF,1,'a'),(0xFFFF,1,'b')];after += [(0xFFFF,1,'b'),(0xFFFF,1,'a')]
        self.assertFalse(c.value_public_order_equal(before,after))


@unittest.skipUnless((BASE/'receipt.json').is_file(),'private retained evidence not installed')
class RetainedReadOnlyControls(unittest.TestCase):
    def test_exact_source_carve_and_build_anchor(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)
            (work/'th03_main.asm').write_bytes((BASE/'round1/source/th03_main.asm').read_bytes())
            build=(BASE/'round1/source/build.bat').read_bytes().replace(
                b':tup\r\nbin\\tup -j1\r\ngoto return_from_tup\r\n',
                b':tup\r\nbin\\tup\r\ngoto return_from_tup\r\n')
            (work/'build.bat').write_bytes(build)
            c.check_original_build(work)
            apply_carrier_edits(CANDIDATE['units'][0],work)
            self.assertIn(b'bin\\tup -j1', (work/'build.bat').read_bytes())
            for n in ('src/main/hud/score.asm','src/main/player/score_add.inl'):
                p=work/n;p.parent.mkdir(parents=True,exist_ok=True)
                raw=(ROOT/n).read_bytes()
                if n==c.MODULE:
                    raw=raw.replace(b'; Maintained score HUD assembly; acceptance is recorded in the ledgers.',b'; Research source proposal, not compiled, installed or credited.',1)
                p.write_bytes(raw)
            c.check_stage(work)
            effective,_=ScoreDescriptor().bind()
            verify_include_carrier(next(u for u in effective['units'] if u['id']==c.BINDING['owner']),work)
            (work/'th03_main.asm').write_bytes((work/'th03_main.asm').read_bytes()+b'include th03/main/player/score_add.asm\r\n')
            with self.assertRaises(ValueError):c.check_stage(work)
        unit=CANDIDATE['units'][0];text=(BASE/'round1/source/Tupfile.lua').read_text()
        self.assertEqual(text.count(unit['build_anchor']),1)
        replaced=text.replace(unit['build_anchor'],unit['build_replacement'])
        self.assertEqual(replaced.count('{ "src/main/hud/score.asm", o = "score_hud.obj" }'),1)

    def test_default_stage_and_original_binding(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)
            (work/'th03_main.asm').write_bytes((BASE/'round1/source/th03_main.asm').read_bytes())
            build=(BASE/'round1/source/build.bat').read_bytes().replace(
                b':tup\r\nbin\\tup -j1\r\ngoto return_from_tup\r\n',
                b':tup\r\nbin\\tup\r\ngoto return_from_tup\r\n')
            (work/'build.bat').write_bytes(build)
            c.check_original_build(work)
            # Historical carrier include is checked against its original hash
            # before applying the default extraction.
            original=work/c.ORIGINAL_OWNER['overlay_path']
            original.parent.mkdir(parents=True,exist_ok=True)
            original.write_bytes((ROOT/c.ORIGINAL_OWNER['source']).read_bytes())
            import tarfile
            prepared_root=(work/'th03_main.asm').read_bytes()
            with tarfile.open(BASE/'reference.tar') as archive:
                original_root=archive.extractfile('th03_main.asm').read()
            (work/'th03_main.asm').write_bytes(original_root)
            verify_include_carrier(c.ORIGINAL_OWNER,work)
            (work/'th03_main.asm').write_bytes(original_root+b'; drift')
            with self.assertRaises(ValueError):verify_include_carrier(c.ORIGINAL_OWNER,work)
            # The historical accepted root already contains preceding owners'
            # transformations. Test score extraction on that exact cached input.
            (work/'th03_main.asm').write_bytes(prepared_root)
            apply_carrier_edits(DEFAULT['units'][-1],work)
            self.assertEqual((work/'build.bat').read_bytes(),build)
            for name in (c.MODULE,c.ORIGINAL_OWNER['source']):
                p=work/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
            c.check_stage(work,default=True)
            verify_include_carrier(next(u for u in DEFAULT['units'] if u['id']==c.BINDING['owner']),work)
            with self.assertRaises(ValueError):c.check_stage(work)
            (work/c.MODULE).write_bytes((work/c.MODULE).read_bytes()+b'\ninclude src/main/player/score_add.inl\n')
            with self.assertRaises(ValueError):c.check_stage(work,default=True)

    def test_complete_cached_fixture_preserves_raw_crlf_maps(self):
        import hashlib,re
        proof_raw=(PRIVATE/c.PROOF_GUARD).read_bytes()
        self.assertEqual(hashlib.sha256(proof_raw).hexdigest(),c.PROOF_GUARD_SHA)
        proof=json.loads(proof_raw)[c.BASELINE]['files']
        receipt=json.loads((BASE/'receipt.json').read_text())
        names=set(receipt['rounds'][0]['game_objects'])
        for n in proof:
            prefix='round1/source/'
            if n.startswith(prefix):
                q=n[len(prefix):]
                if q.endswith('.map') or re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',q):names.add(q)
        retained=PRIVATE/'.analysis/gpt-dots-score-retained-diagnostic-v02/run-first-v01/source'
        self.assertIn(b'\r\n',(retained/'obj/th03/main.map').read_bytes())
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)
            for n in names|{'obj/th03/score_hud.obj'}:
                p=work/n;p.parent.mkdir(parents=True,exist_ok=True)
                origin=(retained if n in {'bin/th03/main.exe','obj/th03/main.map','obj/th03/main.obj','obj/th03/score_hud.obj'} else BASE/'round1/source')/n
                p.symlink_to(origin)
            result=c.check_round(PRIVATE,work,(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes(),proof)
            self.assertTrue(result['pass_'])
            self.assertFalse(result['exact_acceptance'])
            self.assertEqual([r['baseline_round'] for r in result['baselines']],[1,2])

    def test_retained_native_main_is_only_a_comparator_fixture(self):
        retained=PRIVATE/'.analysis/gpt-dots-score-retained-diagnostic-v02/run-first-v01/source'
        target=(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes()
        result=c.compare_main(target,(retained/'bin/th03/main.exe').read_bytes(),
                              (BASE/'round1/source/bin/th03/main.exe').read_bytes(),
                              (BASE/'round1/source/obj/th03/main.map').read_text(),
                              (retained/'obj/th03/main.map').read_text())
        self.assertTrue(result['pass_'])
        original=(retained/'bin/th03/main.exe').read_bytes()
        from lib.pc98 import parse_mz
        header=parse_mz(original).header.header_size
        for offset in (0xD50E,0xD5B0,0xD608,0xD6D4):
            bad=bytearray(original);bad[header+offset]^=1
            x=c.compare_main(target,bytes(bad),(BASE/'round1/source/bin/th03/main.exe').read_bytes(),
                             (BASE/'round1/source/obj/th03/main.map').read_text(),
                             (retained/'obj/th03/main.map').read_text())
            self.assertFalse(x['pass_'])

if __name__=='__main__':unittest.main()
