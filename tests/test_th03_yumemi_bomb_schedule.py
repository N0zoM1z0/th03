"""Fresh source-stage / real Schedule contract, never a native or cold proof.

Only native execute and subprocess.run are simulated. Real frozen source/tool
bytes and the retained genuine OMF exercise staging, not compiler provenance.
No historical receipt tree is recursively copied and no pin is replaced.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import replay_th03_main_exact_units as replay
from lib import th03_score_candidate as score
from lib import th03_serial_schedule as schedule
from lib import th03_yumemi_bomb_candidate as bomb

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('TH03_BOMB_PRIVATE_ROOT', ROOT)).resolve()
BASE = PRIVATE / bomb.BASELINE / 'round1/source'
REFERENCE = PRIVATE / '_reference/ReC98'
RETAINED = PRIVATE / '.analysis/gpt-dots-yumemi-bomb-retained-continuation-v01/run-first-v01/source'
FIXTURES = [REFERENCE / 'th03_main.asm', RETAINED / bomb.OBJECT,
            *(BASE / n for n in ('th03_main.asm', 'build.bat', 'Tupfile.lua', 'Tupfile.ini', 'bin/tup.exe'))]


@unittest.skipUnless(all(p.is_file() for p in FIXTURES), 'private frozen stage fixtures unavailable')
class FreshBombSchedule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='th03-bomb-stage-schedule-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.events = []
        self.env = {'WINEPREFIX': 'source-only-no-native'}
        self.accepted = tomllib.loads((ROOT / 'config/th03_main_exact_units.toml').read_text())
        self.candidate = tomllib.loads((ROOT / bomb.CANDIDATE_PATH).read_text())
        bomb.bind_candidate(self.accepted, self.candidate, bomb.CANDIDATE_PATH)
        self.object = (RETAINED / bomb.OBJECT).read_bytes()
        bomb.validate_object(self.object)
        self.fixture_hashes = {p: bomb.sha(p.read_bytes()) for p in FIXTURES}
        self.addCleanup(self.assert_fixtures_unchanged)
        forbid = patch('subprocess.Popen', side_effect=AssertionError('native process forbidden'))
        forbid.start()
        self.addCleanup(forbid.stop)
        runner = patch.object(schedule.subprocess, 'run', side_effect=self.build)
        self.build_run = runner.start()
        self.addCleanup(runner.stop)
        self.scheduler = schedule.Schedule(self.execute, self.root, 'bomb-stage', candidate=True)

    def assert_fixtures_unchanged(self):
        self.assertEqual(self.fixture_hashes, {p: bomb.sha(p.read_bytes()) for p in FIXTURES})

    def source_stage(self, number=1):
        work = self.scheduler.output / ('round' + str(number)) / 'source'
        work.mkdir(parents=True)
        # Reproduce the real accepted carrier edits, including the score edit,
        # from the original reference root. Copy no objects or proof subtrees.
        original = (REFERENCE / 'th03_main.asm').read_bytes()
        self.assertEqual(bomb.sha(original), score.ORIGINAL_OWNER['carrier_sha256'])
        (work / 'th03_main.asm').write_bytes(original)
        for unit in self.accepted['units']:
            self.assertTrue(all(e['path'] == 'th03_main.asm' for e in unit.get('carrier_edits', [])))
            replay.apply_carrier_edits(unit, work)
        self.assertEqual((work / 'th03_main.asm').read_bytes(), (BASE / 'th03_main.asm').read_bytes())
        for name in bomb.SOURCE_PINS:
            destination = work / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / name).read_bytes())
        for name in ('build.bat', 'Tupfile.lua', 'Tupfile.ini', 'bin/tup.exe'):
            destination = work / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((BASE / name).read_bytes())
        self.assertEqual(bomb.sha((work / 'build.bat').read_bytes()), schedule.BUILD_SHA)
        self.assertEqual(bomb.sha((work / 'bin/tup.exe').read_bytes()), schedule.TUP_SHA)
        self.assertEqual(bomb.sha((work / 'Tupfile.ini').read_bytes()), schedule.EMPTY_SHA)
        score.check_stage(work, default=True)
        self.assertFalse((work / 'obj').exists())
        self.assertFalse((work / '.tup').exists())
        self.assertEqual(list(work.rglob('*.obj')), [])
        return work

    def bomb_stage(self, number=1):
        work = self.source_stage(number)
        bomb.stage_bomb(work)
        self.assertEqual(bomb.sha((work / 'th03_main.asm').read_bytes()), bomb.ROOT_AFTER)
        self.assertEqual((work / 'build.bat').read_bytes(),
                         (BASE / 'build.bat').read_bytes().replace(schedule.BEFORE, schedule.AFTER, 1))
        # Match the replay's literal candidate Tup insertion, after stage_bomb.
        unit = self.candidate['units'][0]
        path = work / unit['build_file']
        before = path.read_text()
        self.assertEqual(before.count(unit['build_anchor']), 1)
        self.assertNotIn('"' + bomb.OBJECT + '"', before)
        path.write_text(before.replace(unit['build_anchor'], unit['build_replacement'], 1))
        self.assertEqual(path.read_text().count(unit['build_replacement']), 1)
        self.assertEqual(path.read_text().replace(unit['build_replacement'], unit['build_anchor'], 1), before)
        return work

    def phase(self, work):
        return json.loads((work.parent / 'scheduling.json').read_text())['phase']

    def execute(self, argv, work, env, log):
        self.assertEqual(env, self.env)
        if 'tcc -c' in argv[-1]:
            self.assertFalse((work / '.tup').exists())
            self.assertTrue((work / 'obj/th03').is_dir())
            self.assertEqual(list(work.rglob('*.obj')), [])
            self.assertEqual(len(self.scheduler.rounds), int(work.parent.name[-1]) - 1)
            (work / bomb.ALIAS).write_bytes(self.object)
            self.events.append(('compile', work))
        elif argv[-1] == r'bin\tup init':
            self.assertEqual(self.phase(work), 'initializing')
            self.assertEqual((work / bomb.OBJECT).read_bytes(), self.object)
            self.assertFalse((work / bomb.ALIAS).exists())
            (work / '.tup').mkdir()
            (work / '.tup/db').write_bytes(b'source-only simulated Tup database')
            self.events.append(('init', work))
        elif argv[-1] == r'bin\tup options':
            self.assertEqual(self.phase(work), 'verifying-options')
            self.assertEqual((work / '.tup/options').read_bytes(), schedule.OPTIONS)
            log.write_bytes(b"Parsed option file: .tup/options\nupdater.num_jobs = '1' from .tup/options\n")
            self.events.append(('options', work))
        else:
            self.fail('unexpected native callback: ' + repr(argv))
        return {'argv': argv, 'exit_code': 0, 'simulated_test_only': True}

    def build(self, argv, *, cwd, env, stdout, stderr, timeout):
        self.assertEqual(argv, schedule.BUILD_ARGV)
        self.assertEqual(env, self.env)
        self.assertEqual((stdout, stderr, timeout), (subprocess.PIPE, subprocess.STDOUT, 300))
        self.assertEqual(self.phase(cwd), 'building')
        self.assertEqual((cwd / '.tup/options').read_bytes(), schedule.OPTIONS)
        self.events.append(('build', cwd))
        return SimpleNamespace(returncode=0, stdout=b'simulated schedule contract only; no native build')

    def cold(self, work):
        return self.scheduler(schedule.BUILD_ARGV, work, self.env, work.parent / 'cold-build.log')

    def test_two_fresh_stages_real_schedule_and_pins(self):
        for number in (1, 2):
            work = self.bomb_stage(number)
            result = bomb.precompile(work, self.env, work.parent, self.scheduler)
            self.assertTrue(result['byte_identical_move'])
            self.assertFalse(result['cached_object_used'])
            self.assertEqual((work / bomb.OBJECT).read_bytes(), self.object)
            self.assertEqual(self.cold(work)['exit_code'], 0)
            self.assertEqual([kind for kind, path in self.events if path == work],
                             ['compile', 'init', 'options', 'build'])
            row = json.loads((work.parent / 'scheduling.json').read_text())
            self.assertEqual(row['round'], number)
            self.assertEqual(row['phase'], 'finished')
            self.assertTrue(row['completed'] and row['build_unchanged'] and row['options_unchanged'])
            self.assertFalse(row['exact_acceptance'])
        self.assertEqual(len(self.scheduler.rounds), 2)
        self.assertEqual(self.build_run.call_count, 2)

    def test_original_build_drift_or_prealtered_carrier_rejected(self):
        for number, change in enumerate(('drift', 'prealtered'), 1):
            with self.subTest(change=change):
                work = self.source_stage(number)
                path = work / 'build.bat'
                raw = path.read_bytes()
                path.write_bytes(raw + b' ' if change == 'drift' else raw.replace(schedule.BEFORE, schedule.AFTER, 1))
                with self.assertRaises(ValueError):
                    bomb.stage_bomb(work)
        self.assertEqual(self.events, [])
        self.build_run.assert_not_called()

    def test_missing_j1_rejected_by_precompile_before_callback(self):
        work = self.bomb_stage()
        path = work / 'build.bat'
        path.write_bytes(path.read_bytes().replace(schedule.AFTER, schedule.BEFORE, 1))
        with self.assertRaises(ValueError):
            bomb.precompile(work, self.env, work.parent, self.scheduler)
        self.assertEqual(self.events, [])
        self.assertFalse((work / 'obj').exists())
        self.build_run.assert_not_called()

    def test_missing_j1_rejected_by_real_schedule_before_native_callbacks(self):
        work = self.bomb_stage()
        bomb.precompile(work, self.env, work.parent, self.scheduler)
        before = list(self.events)
        path = work / 'build.bat'
        path.write_bytes(path.read_bytes().replace(schedule.AFTER, schedule.BEFORE, 1))
        with self.assertRaisesRegex(ValueError, 'reviewed -j1 form'):
            self.cold(work)
        self.assertEqual(self.events, before)
        self.assertEqual(self.scheduler.rounds, [])
        self.assertFalse((work / '.tup').exists())
        self.build_run.assert_not_called()

    def test_unrelated_poststage_build_mutation_rejected_before_compile(self):
        work = self.bomb_stage()
        path = work / 'build.bat'
        path.write_bytes(path.read_bytes() + b' ')
        with self.assertRaises(ValueError):
            bomb.precompile(work, self.env, work.parent, self.scheduler)
        self.assertEqual(self.events, [])
        self.build_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
