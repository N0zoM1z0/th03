"""Current MAINL native refresh preserves its cold ancestor and rejects drift."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_current as current
from lib.omf import describe_omf, parse_omf
from lib.decoded_mainl_root_state_native import historical_parent


def encode_record(kind, data):
    header = bytes([kind]) + (len(data) + 1).to_bytes(2, 'little')
    return header + data + bytes([(-sum(header + data)) & 255])


class StageNames(unittest.TestCase):
    def test_stage_paths_reject_escaping_or_unrelated_names(self):
        for stage in ('../af1055m', 'af1055m/other', 'af1055r', 'mainl'):
            with self.subTest(stage=stage), self.assertRaises(ValueError):
                current.paths(stage)


@unittest.skipUnless((ROOT / '.analysis/work/mainl-current-af1055m.json').is_file(),
                     'private current MAINL native pair absent')
class CurrentPair(unittest.TestCase):
    def test_current_native_pair_reuses_unchanged_cold_outputs(self):
        result = current.review('af1055m')
        self.assertTrue(result['full_original_EXE_MAP_equal'])
        self.assertFalse(result['cold_rebuilt'])
        self.assertEqual(result['rounds'], 2)
        self.assertEqual(sum(row['CODE_bytes'] for row in result['scopes'].values()), 6153)
        self.assertEqual(sum(row['DATA_bytes'] for row in result['scopes'].values()), 336)

    def test_staging_passes_current_cpp_through_and_preserves_the_frozen_graph(self):
        record, _, old, live, graph = current.ancestor()
        self.assertEqual(record['source_sha256'], {n: current.sha(b) for n, b in old.items()})
        self.assertEqual({n for n in live if live[n] != old[n]}, {'rootdata.cpp', 'staffdat.cpp'})
        for stem, source in current.SOURCES.items():
            self.assertEqual(live[stem + '.cpp'], (ROOT / source).read_bytes())

    def test_native_byte_and_field_order_controls_are_rejected(self):
        scratch, _ = current.paths('af1055m')
        original = (current.cold.WORK / 'obj/th03/rootdata.obj').read_bytes()
        raw = (scratch / 'r1/rootdata.obj').read_bytes()
        current.object_scope(raw, original)
        for mode in ('CODE byte', 'FIXUPP order'):
            changed = False
            encoded = []
            for row in parse_omf(raw):
                data = row.data
                if not changed and mode == 'CODE byte' and row.name == 'LEDATA' and data[0] == 1:
                    data = data[:3] + bytes([data[3] ^ 1]) + data[4:]
                    changed = True
                elif not changed and mode == 'FIXUPP order' and row.name == 'FIXUPP':
                    first = 5 if data[2] in (0x14, 0x16) else 4
                    second = 5 if data[first + 2] in (0x14, 0x16) else 4
                    data = data[first:first + second] + data[:first] + data[first + second:]
                    changed = True
                encoded.append(encode_record(row.record_type, data))
            mutant = b''.join(encoded)
            self.assertTrue(changed)
            self.assertTrue(describe_omf(mutant)['valid'])
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                current.object_scope(mutant, original)

    def test_changed_consumed_source_snapshot_stops_review(self):
        scratch, _ = current.paths('af1055m')
        source = scratch / 'src/rootdata.cpp'
        read = Path.read_bytes
        def drift(path):
            raw = read(path)
            return raw.replace(b'mainl_story_dispatch', b'wrong_story_dispatch', 1) if path == source else raw
        with patch.object(Path, 'read_bytes', drift), self.assertRaisesRegex(ValueError, 'consumed source snapshot'):
            current.review('af1055m')

    def test_historical_parent_keeps_its_full_recorded_inventory(self):
        import build_th03_mainl_root_state_work as builder
        config, _ = builder.inputs()
        record, _ = builder.base.load(builder.REPORT)
        historical_parent(ROOT, builder, config, record)
        changed = deepcopy(record)
        row = next(iter(changed['parent_review']['source_inventory'].values()))
        row['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'historical source/recipe inventory'):
            historical_parent(ROOT, builder, config, changed)


if __name__ == '__main__':
    unittest.main()
