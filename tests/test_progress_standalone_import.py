"""Fresh-process imports work without inherited PYTHONPATH or populated sys.modules."""
import os
from pathlib import Path
import subprocess
import sys
import unittest

SOURCE=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
    def test_progress_and_status_spec_import_without_pythonpath(self):
        env=dict(os.environ)
        env.pop('PYTHONPATH',None)
        code=(
            "import importlib.util,sys; from pathlib import Path; "
            "p=Path(sys.argv[1]); "
            "s=importlib.util.spec_from_file_location('isolated_progress_module',p); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "assert callable(m.op_decoded_status); assert callable(m.main); "
            "assert m.ROOT==p.resolve().parents[1]; print('import-ok')"
        )
        for name in ['progress.py','status.py']:
            with self.subTest(module=name):
                result=subprocess.run([sys.executable,'-I','-B','-c',code,
                    str(SOURCE/'scripts'/name)],env=env,capture_output=True,text=True,timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(result.stdout.strip(),'import-ok')
if __name__=='__main__':unittest.main()
