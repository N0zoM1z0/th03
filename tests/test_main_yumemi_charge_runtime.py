"""Source-only runtime matrix guards. No emulator, target or candidate execution."""
import ast
import collections
import itertools
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'scripts/review_th03_main_yumemi_charge_runtime.py'
class ChargeRuntimeSourceTests(unittest.TestCase):
 def setUp(self):self.tree=ast.parse(SOURCE.read_text())
 def assignment(self,name):
  return next(n.value for n in self.tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
 def test_complete_owner_partition(self):
  funcs=ast.literal_eval(self.assignment('FUNCS'));self.assertEqual(len(funcs),10);cursor=0x2fb3
  for entry,size,far,cleanup in funcs.values():self.assertEqual(entry,cursor);cursor+=size;self.assertIn(cleanup,(0,2,4,6))
  self.assertEqual(cursor,0x3620);self.assertEqual(sum(v[1] for v in funcs.values()),1645)
  self.assertEqual(ast.literal_eval(self.assignment('TABLE')),(0x35d0,0x35f0))
 def test_matrix_population_without_native_execution(self):
  # Compile only the input-fixture generator, not module imports or run_case.
  node=next(n for n in self.tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases')
  ns={'itertools':itertools,'FUNCS':ast.literal_eval(self.assignment('FUNCS'))}
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(SOURCE),'exec'),ns)
  matrix=list(ns['cases']());self.assertEqual(len(matrix),2546)
  self.assertEqual(collections.Counter(c['kind'] for c in matrix),dict(reset=12,add=12,update=632,target=46,hit=202,ring=194,render=154,gauge=870,pellet=212,bullet=212))
 def test_one_guarded_mutant_per_function(self):
  mutants=[tuple(ast.literal_eval(v) for v in row.elts[:4]) for row in self.assignment('MUTANTS').elts];self.assertEqual(len(mutants),10)
  self.assertEqual(len({m[0] for m in mutants}),10)
  for name,off,old,new in mutants:self.assertEqual(len(bytes.fromhex(old)),len(bytes.fromhex(new)));self.assertNotEqual(old,new);self.assertTrue(0x2fb3<=off<0x3620)
 def test_entrypoint_is_guarded(self):
  self.assertIsInstance(self.tree.body[-1],ast.If)
  self.assertIn("__name__ == '__main__'",ast.unparse(self.tree.body[-1].test))
if __name__=='__main__':unittest.main()
