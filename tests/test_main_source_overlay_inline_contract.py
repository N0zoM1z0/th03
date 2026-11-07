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


class ReimuSplitNativeHistory(unittest.TestCase):
    def test_old_source_receipts_did_not_force_embedded_reimu_impls(self):
        for stage in ('af602a', 'af709a', 'af764d'):
            self.assertEqual(owner_inline_paths('ex_rfly', stage), ())
            self.assertEqual(owner_inline_paths('ex_reup', stage), ())

    def test_current_split_requires_all_three_real_impls(self):
        self.assertEqual(owner_inline_paths('ex_rfly', 'af765d'), (
            'src/main/player/exatt_flight.inl',
            'src/main/player/exatt_reimu_prefix.inl',
        ))
        self.assertEqual(owner_inline_paths('ex_reup', 'af765d'), (
            'src/main/player/exatt_reimu_update.inl',
        ))

    def test_both_original_physical_compilers_read_current_impls(self):
        flight=(ROOT/'src/main/player/exatt_flight_reimu.cpp').read_bytes()
        rooted=rooted_source('ex_rfly', 'af765d', 1, flight)
        for part in ('exatt_flight.inl', 'exatt_reimu_prefix.inl'):
            self.assertIn((f'#include "probe/af765d/r1/src/main/player/{part}"').encode(),
                          rooted)
            self.assertNotIn((f'#include "src/main/player/{part}"').encode(),
                             rooted)
        update=(ROOT/'src/main/player/exatt_reimu.cpp').read_bytes()
        rooted=rooted_source('ex_reup', 'af765d', 2, update)
        self.assertIn(b'#include "probe/af765d/r2/src/main/player/exatt_reimu_update.inl"', rooted)
        # This conditional prefix is deliberately *not* compiled by the
        # update-only original physical TU. The flight owner checks it.
        self.assertIn(b'#include "src/main/player/exatt_reimu_prefix.inl"', rooted)
        self.assertNotIn(b'#include "probe/af765d/r2/src/main/player/exatt_reimu_prefix.inl"', rooted)


if __name__ == '__main__':
    unittest.main()
