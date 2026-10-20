"""Pure candidate composition controls; no compiler or replay execution."""
import ast
import copy
from pathlib import Path
import tomllib
import unittest
from unittest.mock import patch
import replay_th03_main_exact_units as replay
from lib import th03_score_candidate as score
from lib import th03_yumemi_bomb_candidate as bomb
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
CANDIDATE=tomllib.loads((ROOT/bomb.CANDIDATE_PATH).read_text())

def setup_only(candidate):
    tree=ast.parse((ROOT/'scripts/replay_th03_main_exact_units.py').read_text())
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='replay')
    prefix=[]
    for node in function.body:
        if isinstance(node,ast.If) and ast.unparse(node.test).startswith('not re.fullmatch'):
            break
        prefix.append(node)
    prefix.append(ast.Return(ast.Tuple(elts=[ast.Name(id=n,ctx=ast.Load()) for n in ['config','score_original','score_proof','bomb_proof']],ctx=ast.Load())))
    function.body=prefix;function.decorator_list=[]
    env=dict(replay.__dict__);env['ROOT']=ROOT
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),'<setup-only>','exec'),env)
    return env['replay']('source-only-never-native',[],candidate)

class BombComposition(unittest.TestCase):
    def test_no_candidate_retains_default_score_path(self):
        with patch.object(score,'guard_baseline',return_value={'score':'proof'}), patch.object(bomb,'guard_baseline') as guard,patch.object(bomb,'bind_candidate') as bind:
            config,original,proof,bombproof=setup_only(None)
        self.assertEqual(config,DEFAULT);self.assertEqual(original,score.ORIGINAL_OWNER)
        self.assertEqual(proof,{'score':'proof'});self.assertIsNone(bombproof);guard.assert_not_called();bind.assert_not_called()

    def test_bomb_validates_accepted_score_before_addition(self):
        events=[];real_score=score.bind_default;real_bomb=bomb.bind_candidate
        def sb(c):events.append('score');return real_score(c)
        def bb(c,a,p):
            events.append('bomb');self.assertEqual(c,DEFAULT);return real_bomb(c,a,p)
        with patch.object(score,'bind_default',side_effect=sb),patch.object(bomb,'bind_candidate',side_effect=bb),patch.object(score,'guard_baseline',return_value={'score':'proof'}),patch.object(bomb,'guard_baseline',return_value={'bomb':'proof'}):
            config,original,_,proof=setup_only(ROOT/bomb.CANDIDATE_PATH)
        self.assertEqual(events[:2],['score','bomb']);self.assertEqual(original,score.ORIGINAL_OWNER);self.assertEqual(proof,{'bomb':'proof'})
        self.assertEqual(config['units'][:-1],DEFAULT['units']);self.assertEqual(config['functions'][:-1],DEFAULT['functions'])
        self.assertEqual(replay.physical_object_count_delta(CANDIDATE['units'][0]),1)

    def test_duplicate_or_generic_replacement_is_rejected(self):
        combined=replay.add_candidate_owners(DEFAULT,CANDIDATE)
        with self.assertRaises(ValueError):replay.add_candidate_owners(combined,CANDIDATE)
        bad=copy.deepcopy(CANDIDATE);bad['units'][0]=copy.deepcopy(DEFAULT['units'][0])
        with self.assertRaises(ValueError):bomb.bind_candidate(DEFAULT,bad,bomb.CANDIDATE_PATH)

    def test_stage_and_native_order_remains_explicit(self):
        text=(ROOT/'scripts/replay_th03_main_exact_units.py').read_text()
        self.assertLess(text.index('score_candidate.check_stage(work'),text.index('bomb_candidate.stage_bomb(work)'))
        self.assertLess(text.index('bomb_candidate.stage_bomb(work)'),text.index('bomb_candidate.precompile(work'))
        self.assertLess(text.index('bomb_candidate.precompile(work'),text.index('compile_result = execute(build_command'))
        self.assertIn('score_preservation = bomb_preservation["score_preservation"]',text)
        self.assertIn('elif score_original is not None:',text)

    def test_no_unconditional_bomb_receipt_claim(self):
        tree=ast.parse((ROOT/'scripts/replay_th03_main_exact_units.py').read_text())
        receipts=[n for n in ast.walk(tree) if isinstance(n,ast.Dict) and {'candidate_sha256','behavior_pass'} <= {k.value for k in n.keys if isinstance(k,ast.Constant)}]
        self.assertEqual(len(receipts),1)
        self.assertNotIn('bomb_candidate_preservation',[k.value for k in receipts[0].keys if isinstance(k,ast.Constant)])
        self.assertNotIn('bomb_maintained_compilation',[k.value for k in receipts[0].keys if isinstance(k,ast.Constant)])
