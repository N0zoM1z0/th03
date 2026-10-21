"""Read-only actual cold-product structural/ownership audit; never promotes ledgers."""
import csv, hashlib, json, re, sys
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.pc98 import parse_mz
from lib.omf import describe_omf
OUT = ROOT / '.analysis/mainl-acceptance-schema-plan-20261021-v01'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), sha256=sha(b))

def main():
    mpath = ROOT / '.analysis/mainl-fullcold-r2-g10-20261021-v02-proposal/manifest.json'
    m = json.loads(mpath.read_text())
    work = ROOT / m['work']
    recipe = json.loads((ROOT / m['source_recipe']['path']).read_text())
    canonical = (ROOT / m['canonical']['path']).read_bytes()
    target = (ROOT / m['target']['path']).read_bytes()
    candidate = (work / 'bin/th03/mainl.exe').read_bytes()
    packed = (work / 'MAINL.EXE').read_bytes()
    images = [parse_mz(b) for b in [canonical, target, candidate, packed]]
    if not all((x.valid for x in images)):
        raise ValueError('MAINL static ownership audit failed')
    if not (canonical == packed and target == candidate):
        raise ValueError('MAINL static ownership audit failed')
    graph = {r['output']: r for r in recipe['object_graph']}
    objects = {}
    for name in m['project_outputs'] + m['crt_outputs']:
        d = describe_omf((work / name).read_bytes())
        objects[name] = {k: v for k, v in d.items() if k != 'records'}
        objects[name]['source_graph'] = graph.get(name)

    def lf(b):
        return b.replace(b'\r\n', b'\n')

    def include_closure(name, seen=None):
        seen = set() if seen is None else seen
        if name in seen or not (work / name).is_file():
            return seen
        seen.add(name)
        body = (work / name).read_text(errors='replace')
        targets = re.findall('^\\s*#include\\s+"([^"\\n]+)"', body, re.M) + re.findall('^\\s*include\\s+([^;\\s]+)', body, re.M | re.I)
        for target in targets:
            target = target.strip('"').replace('\\', '/')
            if (work / target).is_file():
                include_closure(target, seen)
            elif (work / Path(name).parent / target).is_file():
                include_closure((Path(name).parent / target).as_posix(), seen)
        return seen
    closures = {n: include_closure(g['wrapper']) for n, g in graph.items()}
    for stem, name in m['crt_objects'].items():
        source = 'src/mainl/crt/' + stem + '.asm'
        if not lf((work / (stem + '.asm')).read_bytes()) == lf((ROOT / source).read_bytes()):
            raise ValueError('MAINL static ownership audit failed')
        objects[name]['source_graph'] = dict(source=source, wrapper=stem + '.asm', recipe='actual fullcold CRT source materialization')
        closures[name] = {source}
    text = (work / 'obj/th03/mainl.map').read_text(errors='strict')
    pattern = '^\\s*([0-9A-F]{4}):([0-9A-F]{4})\\s+([0-9A-F]{4})\\s+C=(\\S+)\\s+S=(\\S+)\\s+G=(\\S+)\\s+M=(\\S+)\\s+ACBP=(\\S+)\\s*$'
    contributions = []
    for match in re.finditer(pattern, text, re.M):
        seg, off, size, cls, segment, group, module, acbp = match.groups()
        start = int(seg, 16) * 16 + int(off, 16)
        size = int(size, 16)
        if not size:
            continue
        names = [n for n, d in objects.items() if d['module_name'].replace('/', '\\').lower() == module.replace('/', '\\').lower()]
        if module in m['crt_objects']:
            name = m['crt_objects'][module]
            if not objects[name]['module_name'] == module + '.asm':
                raise ValueError('MAINL static ownership audit failed')
            names = [name]
        contributions.append(dict(start=start, size=size, end=start + size, map_class=cls, map_segment=segment, map_group=group, map_module=module, acbp=acbp, object_candidates=names))
    units = [r for r in csv.DictReader((ROOT / 'config/units.csv').read_text().splitlines()) if r['artifact'] == 'th03-mainl']
    rows = []
    for u in units:
        start = int(u['segment'].split(':')[1], 16) * 16 + int(u['offset'], 0)
        size = int(u['compare_size'], 0)
        end = start + size
        if not len(images[1].program_image[start:end]) == size:
            raise ValueError('MAINL static ownership audit failed')
        actual = images[2].program_image[start:end]
        expected = images[1].program_image[start:end]
        if not actual == expected:
            raise ValueError('MAINL static ownership audit failed')
        parts = [x for x in contributions if start < x['end'] and x['start'] < end]
        covered = set()
        for part in parts:
            covered.update(range(max(start, part['start']), min(end, part['end'])))
        rels = lambda img: [(r.segment, r.offset) for r in img.relocations if start <= r.linear < end]
        if not rels(images[1]) == rels(images[2]):
            raise ValueError('MAINL static ownership audit failed')
        source = (ROOT / u['source']).read_bytes()
        direct = []
        for part in parts:
            for name in part['object_candidates']:
                g = objects[name]['source_graph']
                if g and g['source'] == u['source']:
                    direct.append(name)
                elif u['source'] in closures.get(name, set()) and (work / u['source']).is_file() and (lf((work / u['source']).read_bytes()) == lf((ROOT / u['source']).read_bytes())):
                    direct.append(name)
        gaps = []
        if len(covered) != size:
            gaps.append('map contribution extent coverage incomplete')
        if not all((len(p['object_candidates']) == 1 for p in parts)):
            gaps.append('map module to fresh OMF identity needs explicit alias binding')
        if not all((len(p['object_candidates']) == 1 and p['object_candidates'][0] in direct for p in parts)):
            gaps.append('every intersecting MAP contribution needs owner source lineage')
        if u['boundary_state'] not in ['reviewed', 'shared']:
            gaps.append('unit boundary not reviewed')
        rows.append(dict(unit_id=u['id'], origin=u['origin'], source=u['source'], source_sha256=sha(source), decoded_linear_start=start, size=size, canonical_file_offset=None, raw_equal=True, raw_sha256=sha(actual), ordered_relocations_equal=True, relocation_count=len(rels(images[1])), reviewed_boundary=u['boundary_state'] in ['reviewed', 'shared'], map_covered_bytes=len(covered), map_parts=parts, direct_source_objects=sorted(set(direct)), lineage_gaps=gaps, formal_exact=False))
    report = dict(schema='mainl-actual-fullcold-owner-audit-v1', product_identity_verified=True, format_integrity_verified=True, canonical_bytes=len(canonical), decoded_bytes=len(candidate), mixed_product_authored_credit=0, manifest=pin(mpath), source_recipe=pin(ROOT / m['source_recipe']['path']), products=[pin(work / n) for n in ['bin/th03/mainl.exe', 'obj/th03/mainl.map', 'MAINL.EXE', 'RESTORE.EXE']], fresh_objects=objects, owners=rows, summary=dict(owners=len(rows), raw_equal=sum((r['raw_equal'] for r in rows)), map_fully_covered=sum((r['map_covered_bytes'] == r['size'] for r in rows)), direct_source_mapping=sum((bool(r['direct_source_objects']) for r in rows)), lineage_complete=sum((not r['lineage_gaps'] for r in rows))), formal_exact=False, notes='Static audit only; fullcold source-bound replay and scope-correct Oracle publication remain independent gates.')
    (OUT / 'actual-cold-owner-audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['summary'], indent=2))
    print('gap sources', sorted({r['source'] for r in rows if r['lineage_gaps']}))
if __name__ == '__main__':
    main()
