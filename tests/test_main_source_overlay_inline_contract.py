"""Stage-bound source provenance: genuine old hyper-only versus new nested core."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from probe_th03_main_exatt_layout import (
    owner_direct_inline_paths,
    owner_inline_paths,
    rooted_source,
    rooted_inline_source,
)


class CoreNativeInlineHistory(unittest.TestCase):
    def test_original_after709_only_claims_original_hyper_include(self):
        self.assertEqual(owner_inline_paths('core', 'af709a'),
                         ('src/main/player/hyper.inl',))
        self.assertEqual(owner_direct_inline_paths('core', 'af709a'),
                         ('src/main/player/hyper.inl',))

    def test_from_after725_all_ten_live_core_sources_are_required(self):
        self.assertEqual(len(owner_direct_inline_paths('core', 'af725a')), 5)
        self.assertEqual(len(owner_inline_paths('core', 'af725a')), 10)
        self.assertEqual(owner_inline_paths('core', 'af730a'),
                         owner_inline_paths('core', 'af725a'))
        for name in ('src/main/player/update.inl',
                     'src/main/player/bomb.inl',
                     'src/main/player/knock.inl'):
            self.assertIn(name, owner_inline_paths('core', 'af730a'))

    def test_stage_local_root_only_rewrites_actually_proved_inputs(self):
        root=(ROOT/'src/main/player/core.cpp').read_bytes()
        old=rooted_source('core', 'af709a', 1, root)
        new=rooted_source('core', 'af730a', 1, root)
        self.assertIn(b'#include "probe/af709a/r1/src/main/player/hyper.inl"', old)
        self.assertIn(b'#include "src/main/player/state.inl"', old)
        self.assertNotIn(b'#include "src/main/player/state.inl"', new)
        self.assertIn(b'#include "probe/af730a/r1/src/main/player/state.inl"', new)

    def test_stage_local_state_follows_five_nested_implementations(self):
        state=(ROOT/'src/main/player/state.inl').read_bytes()
        materialized=rooted_inline_source('src/main/player/state.inl',
                                          'af730a', 2, state)
        for nested in ('update', 'render', 'overlay', 'knock', 'bomb'):
            self.assertIn((f'#include "probe/af730a/r2/'
                           f'src/main/player/{nested}.inl"').encode(),materialized)
            self.assertNotIn((f'#include "src/main/player/{nested}.inl"').encode(),
                             materialized)


if __name__ == '__main__':
    unittest.main()
