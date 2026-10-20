"""Pure candidate/default composition controls; no native replay execution."""
import ast
import copy
from pathlib import Path
import tomllib
import unittest
from unittest.mock import patch
import replay_th03_main_exact_units as replay
from lib import th03_player_cpu_candidate as cpu
from lib import th03_score_candidate as score
from lib import th03_player_tail_candidate as tail
from lib import th03_yumemi_bomb_candidate as bomb
ROOT=Path(__file__).resolve().parents[1]
NEW_DEFAULT=cpu.pre_cpu_config(tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text()))
DEFAULT=tail.pre_tail_config(NEW_DEFAULT)
SCORE_BASE=bomb.pre_bomb_config(DEFAULT)
CANDIDATE=tomllib.loads((ROOT/bomb.CANDIDATE_PATH).read_text())

def setup_only(candidate, config_override=None):
    tree=ast.parse((ROOT/'scripts/replay_th03_main_exact_units.py').read_text())
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='replay')
    prefix=[]
    for node in function.body:
        if isinstance(node,ast.If) and ast.unparse(node.test).startswith('not re.fullmatch'):
            break
        prefix.append(node)
    if config_override is not None:
        # Exercise the exact historical branch using its validated former config,
        # not a different implementation of the composition logic.
        prefix[0]=ast.Assign(targets=[ast.Name(id='config',ctx=ast.Store())],value=ast.Name(id='_fixture_config',ctx=ast.Load()))
    prefix.append(ast.Return(ast.Tuple(elts=[ast.Name(id=n,ctx=ast.Load()) for n in ['config','score_original','score_proof','bomb_proof','bomb_default']],ctx=ast.Load())))
    function.body=prefix;function.decorator_list=[]
    env=dict(replay.__dict__);env['ROOT']=ROOT;env['_fixture_config']=copy.deepcopy(config_override)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),'<setup-only>','exec'),env)
    return env['replay']('source-only-never-native',[],candidate)

class BombComposition(unittest.TestCase):
    def test_new_tail_default_keeps_bomb_and_score_proofs(self):
        with patch.object(score,'guard_baseline',return_value={'score':'proof'}),patch.object(bomb,'guard_baseline',return_value={'bomb':'proof'}),patch.object(tail,'guard_baseline',return_value={'tail':'proof'}) as tg,patch.object(tail,'freeze_expected',return_value={'stream':'frozen'}) as tf:
            config,original,scoreproof,bombproof,default=setup_only(None,NEW_DEFAULT)
        self.assertEqual(config,NEW_DEFAULT);self.assertEqual(original,score.ORIGINAL_OWNER)
        self.assertEqual(scoreproof,{'score':'proof'});self.assertEqual(bombproof,{'bomb':'proof'});self.assertTrue(default)
        tg.assert_called_once_with(ROOT);tf.assert_called_once_with(ROOT)

    def test_default_bomb_and_score_are_conjunctive(self):
        with patch.object(score,'guard_baseline',return_value={'score':'proof'}),patch.object(bomb,'guard_baseline',return_value={'bomb':'proof'}) as guard,patch.object(bomb,'bind_candidate') as candidate:
            config,original,proof,bombproof,default=setup_only(None,DEFAULT)
        self.assertEqual(config,DEFAULT);self.assertEqual(original,score.ORIGINAL_OWNER)
        self.assertEqual(proof,{'score':'proof'});self.assertEqual(bombproof,{'bomb':'proof'})
        self.assertTrue(default);guard.assert_called_once_with(ROOT);candidate.assert_not_called()

    def test_historical_no_candidate_retains_score_only_path(self):
        with patch.object(score,'guard_baseline',return_value={'score':'proof'}),patch.object(bomb,'guard_baseline') as guard,patch.object(bomb,'bind_candidate') as candidate:
            config,original,proof,bombproof,default=setup_only(None,SCORE_BASE)
        self.assertEqual(config,SCORE_BASE);self.assertEqual(original,score.ORIGINAL_OWNER)
        self.assertEqual(proof,{'score':'proof'});self.assertIsNone(bombproof);self.assertFalse(default)
        guard.assert_not_called();candidate.assert_not_called()

    def test_historical_candidate_validates_score_before_addition(self):
        events=[];real_score=score.bind_default;real_bomb=bomb.bind_candidate
        def sb(c):events.append('score');return real_score(c)
        def bb(c,a,p):
            events.append('bomb');self.assertEqual(c,SCORE_BASE);return real_bomb(c,a,p)
        with patch.object(score,'bind_default',side_effect=sb),patch.object(bomb,'bind_candidate',side_effect=bb),patch.object(score,'guard_baseline',return_value={'score':'proof'}),patch.object(bomb,'guard_baseline',return_value={'bomb':'proof'}):
            config,original,_,proof,default=setup_only(ROOT/bomb.CANDIDATE_PATH,SCORE_BASE)
        self.assertEqual(events[:2],['score','bomb']);self.assertEqual(original,score.ORIGINAL_OWNER);self.assertEqual(proof,{'bomb':'proof'})
        self.assertEqual(config,DEFAULT);self.assertFalse(default)
        self.assertEqual(replay.physical_object_count_delta(CANDIDATE['units'][0]),1)

    def test_duplicate_candidate_after_default_is_rejected_before_proofs(self):
        with patch.object(score,'guard_baseline') as scoreguard,patch.object(bomb,'guard_baseline') as bombguard:
            with self.assertRaises(ValueError):setup_only(ROOT/bomb.CANDIDATE_PATH,DEFAULT)
        scoreguard.assert_not_called();bombguard.assert_not_called()
        with self.assertRaises(ValueError):replay.add_candidate_owners(DEFAULT,CANDIDATE)

    def test_generic_replacement_is_rejected(self):
        bad=copy.deepcopy(CANDIDATE);bad['units'][0]=copy.deepcopy(SCORE_BASE['units'][0])
        with self.assertRaises(ValueError):bomb.bind_candidate(SCORE_BASE,bad,bomb.CANDIDATE_PATH)

    def test_stage_and_native_order_and_mode_remain_explicit(self):
        text=(ROOT/'scripts/replay_th03_main_exact_units.py').read_text()
        self.assertLess(text.index('score_candidate.check_stage(work'),text.index('bomb_candidate.stage_bomb(work, default=bomb_default)'))
        self.assertLess(text.index('bomb_candidate.stage_bomb(work, default=bomb_default)'),text.index('bomb_candidate.precompile(work'))
        self.assertLess(text.index('bomb_candidate.precompile(work'),text.index('compile_result = execute(build_command'))
        self.assertIn('bomb_candidate.precompile(work, env, logs, execute, default=bomb_default)',text)
        self.assertIn('bomb_candidate.check_round(ROOT, work, target, bomb_proof, default=bomb_default)',text)
        self.assertIn('score_preservation = bomb_preservation["score_preservation"]',text)
        self.assertIn('elif score_original is not None:',text)

    def test_no_unconditional_bomb_receipt_claim(self):
        tree=ast.parse((ROOT/'scripts/replay_th03_main_exact_units.py').read_text())
        receipts=[n for n in ast.walk(tree) if isinstance(n,ast.Dict) and {'candidate_sha256','behavior_pass'} <= {k.value for k in n.keys if isinstance(k,ast.Constant)}]
        self.assertEqual(len(receipts),1)
        for name in ['bomb_candidate_preservation','bomb_maintained_compilation']:
            self.assertNotIn(name,[k.value for k in receipts[0].keys if isinstance(k,ast.Constant)])
