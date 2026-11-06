#!/usr/bin/env python3
"""Close the four baseline CRT source owners without rebuilding the cold graph.

This is an ownership audit, not four new recoveries. Preserve literal original
and native metadata, including the baseline's PUBLIC/GROUP/FIXUPP order gaps.
"""
import json
import sys
from pathlib import Path

import setuptools  # Required by the unchanged historical Unicorn import chain.

sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))
import build_th03_mainl_after533_work as b
import review_th03_mainl_after533_work as previous
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, object_program_records

ROOT = Path(__file__).resolve().parents[1]
DRIVER = 'scripts/review_th03_mainl_after534_work.py'
REPORT = '.analysis/work/mainl-after534-baseline-ownership-review.json'
MODE = 'locale-tables-aliases-twelve'
OWNERS = {'h_llsh': (68, 33), 'h_padd': (72, 96),
          'ioerror': (79, 82), 'lseek': (87, 45)}


def load(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(raw), sha(raw)


def retained(meta):
    raw = (ROOT / meta['path']).read_bytes()
    need(meta == dict(path=meta['path'], bytes=len(raw), sha256=sha(raw)),
         'retained raw vector ' + meta['path'])
    return raw


def profile(blob):
    segments = b.segment_definitions(blob)
    data = b.initialized_payload(blob)
    need(set(data) == {(s['index'], i) for s in segments for i in range(s['size'])},
         'all four baseline owners have complete initialized segment coverage')
    records = b.parse_omf(blob)
    return dict(
        segments=segments,
        segment_attributes=[r.data[0] for r in records if r.name == 'SEGDEF'],
        initialized_bytes=[dict(segment=s['index'], bytes=s['size'], sha256=sha(
            bytes(data[s['index'], i] for i in range(s['size'])))) for s in segments],
        publics={str(s['index']): b.code_publics(blob, s['index']) for s in segments},
        imports=b.externs(blob),
        literal_fields=b.literal_fields(blob),
        literal_records={name: [r.data.hex() for r in records if r.name == name]
                         for name in ('PUBDEF', 'GRPDEF', 'ALIAS', 'MODEND')})


def review():
    # Reuses the unchanged source-bound DAG and reads its native pairs. This
    # launches neither native writers nor ancestor runtime models.
    prior = previous.review(MODE)
    latest, latest_hash = load(b.PREFIX + MODE + '-build.json')
    cold, cold_hash = load('.analysis/work/mainl-build.json')
    stdio, stdio_hash = load('.analysis/work/mainl-stdio-build.json')
    need(prior['complete'] and prior['native_source_members'] == 889 and
         prior['retained_context_members'] == 4 and
         cold['raw_repeat_equal'] and len(cold['rounds']) == 2 and
         cold['rounds'][0]['outputs'] == cold['rounds'][1]['outputs'],
         'current 889-source closure and frozen cold pair')
    need(stdio['complete'] and not stdio['whole_product_cold_rebuilt'] and
         stdio['cold_report_sha256'] == cold_hash and
         stdio['driver_sha256'] == sha((ROOT / 'scripts/build_th03_mainl_stdio_work.py').read_bytes()) and
         stdio['source_sha256'] == {p: sha((ROOT / ('.analysis/work/stdio-source-' + Path(p).name)).read_bytes())
                                   for p in stdio['source_sha256']} and
         stdio['source_sha256']['src/mainl/crt/lseek.asm'] ==
         sha((ROOT / 'src/mainl/crt/lseek.asm').read_bytes()) and
         stdio['layout_header_sha256'] == sha((ROOT / 'src/mainl/crt/stdio_layout.inc').read_bytes()),
         'maintained stdio producer and include binding')
    stdio_vectors = [{k: retained(v) for k, v in row['outputs'].items()}
                     for row in stdio['rounds']]
    need(len(stdio_vectors) == 2 and stdio_vectors[0] == stdio_vectors[1],
         'two retained raw stdio OBJ/LIB/EXE/MAP vectors')
    for phase in stdio['native_phases']:
        need(phase['returncode'] == 0 and phase['log_sha256'] == sha(
            (ROOT / ('.analysis/work/stdio-' + phase['label'] + '.log')).read_bytes()),
            'retained native stdio writer log')
    original_raw = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_raw) == cold['vendor_library_sha256'] ==
         prior['original_compiler_library_sha256'], 'pinned original compiler library')
    originals = library_members(original_raw)
    latest_vectors = [{k: retained(v) for k, v in row['outputs'].items()}
                      for row in latest['rounds']]
    linked = [library_members(v['lib']) for v in latest_vectors]
    incremental = set(latest['rounds'][0]['library_comparison']['replaced_members'])
    need(set(m.name for m in originals) - incremental == set(OWNERS) and
         len(incremental) == 889, 'exact complementary owner set; no duplicate credit')
    owners = {}
    for name, (slot, size) in OWNERS.items():
        source = 'src/mainl/crt/' + name + '.asm'
        source_hash = sha((ROOT / source).read_bytes())
        need(originals[slot].name == name, 'original library slot ' + name)
        original = b.original_library_member(originals[slot])
        if name == 'lseek':
            objects = [v[name] for v in stdio_vectors]
            source_receipt = stdio_hash
            object_paths = [row['outputs'][name]['path'] for row in stdio['rounds']]
        else:
            key = 'owned/' + name + '.asm'
            need(cold['source_sha256'][key] == source_hash and
                 (b.WORK / key).read_bytes() == (ROOT / source).read_bytes(),
                 'frozen maintained/consumed source ' + name)
            path = b.WORK / 'owned' / (name + '.obj')
            obj = path.read_bytes()
            need(all(row['outputs']['owned/' + name + '.obj'] ==
                     dict(bytes=len(obj), sha256=sha(obj)) for row in cold['rounds']),
                 'retained cold object matches both native round inventories')
            # The historical cold builder retained one raw vector with equal
            # per-round hashes. Do not invent two independently stored files.
            objects = [obj, obj]
            source_receipt = cold_hash
            object_paths = [str(path.relative_to(ROOT))]
        for i, obj in enumerate(objects):
            need(linked[i][slot].name == name and
                 linked[i][slot].program_records == object_program_records(obj),
                 'actual latest library adopts earlier source object ' + name)
        a, z = profile(original), profile(objects[0])
        for key in ('segments', 'segment_attributes', 'initialized_bytes', 'publics', 'imports'):
            need(a[key] == z[key], 'complete original/native ' + key + ' ' + name)
        need(a['segments'][0]['size'] == size and
             sorted(a['literal_fields'], key=lambda f: (f['segment'], f['site'])) ==
             sorted(z['literal_fields'], key=lambda f: (f['segment'], f['site'])),
             'every literal field agrees; independently retain original order')
        need([f['site'] for f in a['literal_fields']] ==
             ([22, 28, 45, 39, 51] if name == 'ioerror' else
              [12, 38] if name == 'lseek' else []) and
             [f['site'] for f in z['literal_fields']] ==
             ([22, 28, 39, 45, 51] if name == 'ioerror' else
              [12, 38] if name == 'lseek' else []), 'literal ordered field transcript')
        equal = {k: a['literal_records'][k] == z['literal_records'][k]
                 for k in a['literal_records']}
        need(equal == dict(PUBDEF=name not in ('h_padd', 'ioerror'),
                           GRPDEF=name != 'ioerror', ALIAS=True, MODEND=True),
             'explicit bounded baseline metadata differences')
        owners[name] = dict(slot=slot, source=source, source_sha256=source_hash,
            producer_receipt_sha256=source_receipt, raw_object_paths=object_paths,
            raw_object_sha256=sha(objects[0]), latest_library_program_equal=True,
            original_profile=a, native_profile=z, literal_record_equality=equal,
            literal_ordered_fields_equal=a['literal_fields'] == z['literal_fields'])
    return dict(complete=True, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        latest_build_sha256=latest_hash, cold_build_sha256=cold_hash,
        stdio_build_sha256=stdio_hash, original_compiler_library_sha256=sha(original_raw),
        incremental_source_members=889, earlier_baseline_source_members=4,
        source_owned_library_members=893, new_source_members=0, new_CODE_bytes=0,
        baseline_CODE_bytes=256, source_owned_CODE_bytes=209272,
        whole_EXE_MAP_equal=prior['complete_native_link_EXE_MAP_equal'],
        cold_rebuilt=False, source_acceptance=False,
        all_literal_ordered_FIXUPP_equal=False, all_literal_OBJ_metadata_equal=False,
        historical_cold_raw_storage='one retained vector; equal two-round inventories',
        owners=owners)


if __name__ == '__main__':
    result = review()
    (ROOT / REPORT).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'owners'}, indent=2))
