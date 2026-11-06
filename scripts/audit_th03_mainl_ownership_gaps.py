#!/usr/bin/env python3
"""Locate project allocations outside published decoded ownership; never promote credit."""
import argparse
import json
import re

import build_th03_runtime_after548_work as runtime
import build_th03_mainl_work as cold_build
from build_th03_mainl_resources_work import need, sha
from lib.omf import describe_omf

ROOT = runtime.ROOT
REPORT = ROOT / '.analysis/work/mainl-ownership-gap-audit.json'


def audit():
    root, root_hash = runtime.base.load(runtime.REPORT)
    cold, cold_hash = runtime.base.load('.analysis/work/mainl-build.json')
    publication, publication_hash = runtime.base.load('config/mainl_work/scoped_acceptance.json')
    need(root['complete'] and cold['complete'] and cold['raw_repeat_equal'] and
         publication['audit']['cold_report_sha256'] == cold_hash and
         cold['rounds'][0]['outputs'] == cold['rounds'][1]['outputs'], 'actual unchanged published cold pair')
    target = runtime.base.checked(root['rounds'][0]['outputs']['mainl_exe'])
    mapping = runtime.base.checked(root['rounds'][0]['outputs']['mainl_map'])
    image = target[int.from_bytes(target[8:10], 'little') * 16:]
    covered = set()
    for unit, oracles in publication['owner_oracles'].items():
        bounds = [e for e in oracles.values() if e['oracle'] == 'boundary-ownership']
        raw = [e for e in oracles.values() if e['oracle'] == 'raw-bytes']
        need(len(bounds) == len(raw) == 1, 'one actual ownership/byte scope ' + unit)
        a, size = int(bounds[0]['extent_start']), int(bounds[0]['extent_size'])
        need(0 <= a < a + size <= len(image) and sha(image[a:a + size]) == raw[0]['output_sha256'],
             'published extent still agrees with current original image ' + unit)
        covered.update(range(a, a + size))
    modules, object_pins = {}, {}
    for name, pin in cold['rounds'][0]['outputs'].items():
        if not (name.startswith('obj/') and name.endswith('.obj')):
            continue
        raw = (cold_build.WORK / name).read_bytes()
        need(pin == dict(bytes=len(raw), sha256=sha(raw)), 'actual cold project object ' + name)
        module = describe_omf(raw)['module_name'].casefold()
        need(module not in modules, 'unambiguous native module')
        modules[module] = name
        object_pins[name] = pin
    pattern = r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=(\S+)\s*$'
    rows = []
    for match in re.finditer(pattern, mapping.decode(), re.M):
        segment, offset, size, kind, section, group, module, flags = match.groups()
        a, size = int(segment, 16) * 16 + int(offset, 16), int(size, 16)
        if not size or module.casefold() not in modules:
            continue
        remaining = sorted(set(range(a, a + size)) - covered)
        if not remaining:
            continue
        spans = []
        for site in remaining:
            if not spans or spans[-1][1] != site:
                spans.append([site, site + 1])
            else:
                spans[-1][1] += 1
        rows.append(dict(object=modules[module.casefold()], module=module, kind=kind, section=section,
                         group=group, flags=flags, decoded_start=a, allocation_bytes=size,
                         uncovered_bytes=len(remaining), uncovered_intervals=spans))
    return dict(schema='th03-mainl-published-ownership-gap-audit-v1', diagnostic_only=True,
        active_runtime_root=runtime.REPORT, active_runtime_root_sha256=root_hash,
        cold_report_sha256=cold_hash, publication_sha256=publication_hash,
        project_object_pins=object_pins, published_owners=len(publication['owner_oracles']),
        CODE_uncovered_bytes=sum(r['uncovered_bytes'] for r in rows if r['kind'] == 'CODE'),
        CODE_contributions_with_uncovered_bytes=sum(r['kind'] == 'CODE' for r in rows),
        allocations=rows, canonical_credit_changed=False, whole_game_denominator_known=False,
        note='Uncovered means outside published decoded ownership, not missing functions or source; tables, alignment and BSS remain separate.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    options = parser.parse_args()
    result = audit()
    if options.check:
        need(json.loads(REPORT.read_text()) == result, 'current complete saved audit')
    else:
        REPORT.write_text(json.dumps(result, indent=2) + '\n')
    print('MAINL project CODE outside published ownership:', result['CODE_uncovered_bytes'],
          'bytes across', result['CODE_contributions_with_uncovered_bytes'], 'contributions; diagnostic only')
