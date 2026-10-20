"""One whole-TU bomb candidate on the accepted score graph; no generic waivers.

The named producer splice and seven literal MAP display ties come from the
separate reviewed retained diagnostic. Historical failures stay immutable.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import struct
from lib import th03_score_candidate as score
from lib.omf import normalize_dependency_timestamps, parse_omf

require = score.require
digest = score.digest
SOURCE = 'src/main/player/bomb_yumemi.cpp'
HEADER = 'src/main/player/yumemi_gameplay.hpp'
MODULE = 'src/main/player/bomb~cxk.cpp'
OBJECT = 'obj/th03/bomb_yumemi.obj'
ALIAS = 'obj/th03/bomb~cxk.obj'
CANDIDATE_PATH = 'config/th03_main_yumemi_bomb_candidate.toml'
CANDIDATE_DIGEST = 'cebea0d601d071ef1beda425c80b3ad19685f13116e9eb43c4198b28e049f6a6'
UNIT_DIGEST = '8d3db710ef2b91d6f70e6f99cc079d7eef14e11f8caeb8891e8f86ec5bd2761a'
SOURCE_PINS = {
 SOURCE:'215fbce1405f4a807314b45bf2d87ffb70631859ccc43077a5d676b7506e6cc9',
 HEADER:'1c707162a4c4eb4fb8c75eda9b6d3e2565cfc29829f2aef50751955943aa4cf7',
 score.MODULE:score.DEFAULT_SCORE_SOURCE_SHA,
 'src/main/player/score_add.inl':score.INCLUDE_SHA}
ROOT_AFTER = '356b650b19c833abbbc3e8daf381879c1519df1e83a460723c3e83f386401446'
OMF_SHA = '9fd137f830a133c0711bcf31123f20ea01993977dbf3961c495f6b30769ca7fb'
SPANS = [[0x159FF,0x15CB9]]
PAIRS = [[0x139D,0x202F+n] for n in (692,609,596,502,489,472,461,428,423,409,360,319,291,257,208,167,135,111,87,25)]
RAW_SHA = '5e65f17d18f4ff0478df6aa2239fdaad2685366b40a34951c25a824147dcafee'
OUTSIDE_SHA = '65faf8fc7813123baa84cf12d69ca755587e498bdc1d46aaf2f2257e1f0aee11'
BASELINE = '.analysis/th03-main-exact/gpt-dots-score-default-cold-v01'
PROOF_GUARD = '.analysis/gpt-dots-yumemi-bomb-retained-continuation-v01/proof-guards.json'
PROOF_GUARD_SHA = 'f689bbd51e3c09901e25c2063c71904d69ab9a119ae55265e794579f814d090b'
PROVIDER_REPORT = '.analysis/gpt-dots-yumemi-bomb-producer-boundary-review-v01/provider-report.json'
PROVIDER_REPORT_SHA = '7b4a81372a3d0adeb59b7ce41a74ef3a8c8dea751516a2b70162701e8bbacc1a'
TIES = {
 (0,0x21AA):(('VSYNC_END','VSYNC_LEAVE'),('VSYNC_LEAVE','VSYNC_END')),
 (0,0x3313):(('PSUB@','F_PSUB@'),('F_PSUB@','PSUB@')),
 (0x1D56,0x7C):(('__version','__osversion','__osmajor'),('__osversion','__version','__osmajor')),
 (0x1D56,0x310):(('pfkey','_pfkey'),('_pfkey','pfkey')),
 (0x1D56,0x596):(('_TextVramAdr','TextVramAdr'),('TextVramAdr','_TextVramAdr')),
 (0x1D56,0x598):(('TextVramSeg','_TextVramSeg'),('_TextVramSeg','TextVramSeg')),
 (0x1D56,0x11EA):(('_vsync_Count1','vsync_Count1'),('vsync_Count1','_vsync_Count1'))}

def sha(raw): return hashlib.sha256(raw).hexdigest()

def bind_candidate(accepted, additions, manifest_name):
    score.bind_default(accepted)  # Validate BEFORE adding any descriptor.
    require(manifest_name == CANDIDATE_PATH, 'bomb manifest path changed')
    require(digest(additions) == CANDIDATE_DIGEST, 'bomb descriptor changed')
    require(len(additions['units']) == 1 and is_bomb_owner(additions['units'][0]), 'bomb owner identity changed')


def is_bomb_owner(unit):
    return unit.get('id') == 'th03-main-yumemi-bomb' and digest(unit) == UNIT_DIGEST


def check_sources(work):
    for name, pin in SOURCE_PINS.items():
        p = Path(work)/name
        require(p.is_file() and not p.is_symlink() and sha(p.read_bytes()) == pin, 'source drift: '+name)
    require((Path(work)/score.MODULE).read_bytes().count(b'include src/main/player/score_add.inl') == 1,
            'score_add must remain included once')


def transform_root(raw):
    require(sha(raw) == score.REDUCED_ROOT_SHA, 'pre-bomb root is not accepted score root')
    start, end = b'yumemi_bomb\tproc far\r\n', b'yumemi_bomb\tendp\r\n'
    require(raw.count(start) == raw.count(end) == 1, 'bomb root boundary')
    a = raw.index(start); b = raw.index(end,a)+len(end)
    out = raw[:a]+b'; Complete Yumemi bomb moved to maintained natural producer.\r\n'+raw[b:]
    edits = [(b'\textern _execl:proc\r\n',b'\textern _execl:proc\r\n\textern @yumemi_bomb$qv:far\r\n')]
    for who in (b'p1', b'p2'):
        edits.append((b'\t\tsetfarfp\tbomb_'+who+b', yumemi_bomb\r\n',
                      b'\t\tsetfarfp\tbomb_'+who+b', @yumemi_bomb$qv\r\n'))
    anchor = b'\t\tdb 0C0h\r\n\t\tdb  15h\r\n\t\tdb  6Bh\t; k\r\n\t\tdb  40h\r\n\t\tdb 0EBh\r\n\t\tdb  95h\r\npublic _yumemi_groups\r\n'
    edits.append((anchor,b'public _yumemi_bomb_triangle_angles\r\n_yumemi_bomb_triangle_angles label byte\r\n'+anchor))
    for old,new in edits:
        require(out.count(old) == 1, 'bomb root interface drift')
        out = out.replace(old,new,1)
    require(sha(out) == ROOT_AFTER, 'post-bomb root identity changed')
    return out


def stage_bomb(work):
    work = Path(work)
    score.check_stage(work, default=True)
    check_sources(work)
    path = work/'th03_main.asm'
    path.write_bytes(transform_root(path.read_bytes()))


def validate_object(raw):
    require(sha(normalize_dependency_timestamps(raw)) == OMF_SHA,
            'bomb OMF differs from reviewed actual maintained-path alias identity')
    return dict(sha256=sha(raw), normalized_sha256=OMF_SHA, code_bytes=698,
                external_fixups=53, far_pointers=20, data_bytes=0, bss_bytes=0,
                module=MODULE, empty_segment='BOMB~CXK_TEXT')


def precompile(work, env, logs, execute):
    work,logs = Path(work),Path(logs)
    check_sources(work)
    require(sha((work/'th03_main.asm').read_bytes()) == ROOT_AFTER, 'bomb root not staged')
    for name in (ALIAS,OBJECT,'obj/th03/bm_yume.obj'):
        require(not (work/name).exists(), 'cached/duplicate bomb object: '+name)
    before = {p.relative_to(work).as_posix():sha(p.read_bytes()) for p in work.rglob('*.obj')}
    command = ['wine','cmd','/d','/c',
        r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M' -nobj/th03/ src/main/player/bomb_yumemi.cpp"]
    result = execute(command,work,env,logs/'bomb-maintained-compile.log')
    require(result.get('exit_code') == 0, 'bomb compile not successful')
    check_sources(work)
    require(sha((work/'th03_main.asm').read_bytes()) == ROOT_AFTER, 'compile modified root')
    after = {p.relative_to(work).as_posix():sha(p.read_bytes()) for p in work.rglob('*.obj')}
    require(set(after)-set(before) == {ALIAS} and all(after.get(n)==h for n,h in before.items()),
            'compiler did not emit only fresh literal bomb alias')
    require(not (work/ALIAS).is_symlink(), 'bomb alias symlink')
    raw = (work/ALIAS).read_bytes(); proof = validate_object(raw)
    os.replace(work/ALIAS,work/OBJECT)  # Physical filename only; never edit OMF bytes.
    require((work/OBJECT).read_bytes() == raw and not (work/ALIAS).exists(), 'bomb physical move failed')
    return dict(compile=result, emitted_path=ALIAS, managed_path=OBJECT,
                byte_identical_move=True, omf=proof, cached_object_used=False)


def guard_baseline(root):
    root = Path(root)
    score.guard_baseline(root)
    raw = (root/PROOF_GUARD).read_bytes()
    require(sha(raw) == PROOF_GUARD_SHA, 'accepted score proof guard changed')
    saved = json.loads(raw)[BASELINE]; base = root/BASELINE
    require(not base.is_symlink() and oct(stat.S_IMODE(base.stat().st_mode)) == saved['root_mode'], 'baseline root mode')
    files,dirs = set(),{}
    for p in base.rglob('*'):
        require(not p.is_symlink(), 'baseline symlink')
        name = p.relative_to(base).as_posix()
        if p.is_file(): files.add(name)
        elif p.is_dir(): dirs[name] = oct(stat.S_IMODE(p.stat().st_mode))
        else: raise ValueError('baseline special file')
    require(files == set(saved['files']) and dirs == saved['dirs'], 'baseline inventory drift')
    for name,pin in saved['files'].items(): score.read_pinned(base/name,pin)
    providers = (root/PROVIDER_REPORT).read_bytes()
    require(sha(providers) == PROVIDER_REPORT_SHA and json.loads(providers)['pass'], 'provider proof drift')
    return saved['files']


def expected_stream(old):
    require(len(old) == 1553 and digest(old) == '1058ed77991dec8c4e10572c3f3f7375d7258f3fc2c8995709e9179e49112192', 'baseline literal stream changed')
    require(old[946:966] == list(reversed(PAIRS)) and old[839] == [0x96E,0x3111], 'baseline owner/C7F1 positions')
    # Genuine standalone producer is inserted before root, after bm_mima.
    # Remaining root prefix494/suffix12 and every other entry remain literal.
    return old[:452]+PAIRS+old[452:946]+old[966:]


def inserted(rows, anchor, value):
    require(rows.count(anchor) == 1, 'public insertion anchor drift')
    result = rows[:]; result.insert(result.index(anchor),value)
    return result


def expected_publics(old):
    names,values = [x[:] for x in old]
    for address,(before,after) in TIES.items():
        indices = [i for i,row in enumerate(values) if row[:2] == address]
        require(indices and indices == list(range(indices[0],indices[0]+len(before)))
                and tuple(values[i][2] for i in indices) == before, 'literal public tie baseline drift')
        for i,name in zip(indices,after): values[i] = (*address,name)
    bomb = (0x139D,0x202F,'yumemi_bomb()')
    angles = (0x1D56,0x78C,'_yumemi_bomb_triangle_angles')
    names = inserted(names,(0x18FE,0x19D0,'yumemi_exatt_render_one()'),bomb)
    names = inserted(names,(0x1D56,0x1E43,'_yumemi_chase_until'),angles)
    values = inserted(values,(0x139D,0x22E9,'combo_add_raw(unsigned char,unsigned char,unsigned int)'),bomb)
    values = inserted(values,(0x1D56,0x792,'_yumemi_groups'),angles)
    return [names,values]


def expected_map(text):
    result,seen = [],[]
    for row in score.map_rows(text):
        if row[6] == 'th03_main.asm':
            if row[4] == 'P_COMBO_TEXT':
                require(row == (0x139D,0x202F,698,'CODE','P_COMBO_TEXT','MAIN_04','th03_main.asm',28), 'bomb root MAP geometry')
                result.append((*row[:6],MODULE,row[7])); row = (0x139D,0x22E9,0,*row[3:]); seen.append('P_COMBO_TEXT')
            elif row[4] == 'MAIN_06_TEXT':
                require(row[:3] == (0x18FE,0x11C7,0), 'empty code MAP anchor')
                result.append((0x18FE,0x11C7,0,'CODE','BOMB~CXK_TEXT','MAIN_06',MODULE,28)); seen.append('BOMB~CXK_TEXT')
            elif row[4] in ('_DATA','_BSS'):
                require(row[:2] == (0x1D56,0x90 if row[4]=='_DATA' else 0x1182), 'empty storage MAP anchor')
                result.append((row[0],row[1],0,*row[3:6],MODULE,row[7])); seen.append(row[4])
        result.append(row)
    require(seen == ['P_COMBO_TEXT','BOMB~CXK_TEXT','_DATA','_BSS'], 'bomb MAP insertion inventory')
    prefix = text.split('Detailed map of segments')[0]
    anchor = ' 1A1A7H 1A1A7H 00000H BM_MIMA_TEXT       CODE\r\n'
    require(prefix.count(anchor) == 1, 'aggregate empty segment anchor')
    return result,prefix.replace(anchor,anchor+' 1A1A7H 1A1A7H 00000H BOMB~CXK_TEXT      CODE\r\n',1)


def groups(text):
    return text[max(x.end() for x in score.ROW.finditer(text)):text.index('Publics by Name')]


def compare_main(target, candidate, baseline, oldmap, newmap):
    from lib.pc98 import parse_mz
    t,c,b = [parse_mz(x) for x in (target,candidate,baseline)]
    require(all(x.valid for x in (t,c,b)), 'invalid MZ')
    literal = score.ordered_literal
    require(sha(t.program_image[0x159FF:0x15CB9]) == RAW_SHA and literal(t,SPANS) == PAIRS, 'target bomb drift')
    outside = literal(b,SPANS,True)
    require(len(outside) == 1533 and sha(b''.join(struct.pack('<HH',o,s) for s,o in outside)) == OUTSIDE_SHA, 'baseline outside scope')
    before = [[r.segment,r.offset] for r in b.relocations]
    after = [[r.segment,r.offset] for r in c.relocations]
    rows,prefix = expected_map(oldmap)
    checks = dict(
        bomb698_raw_and_20_literal_order=t.program_image[0x159FF:0x15CB9] == c.program_image[0x159FF:0x15CB9] and literal(c,SPANS) == PAIRS,
        outside1533_literal_order=outside == literal(c,SPANS,True),
        complete_outside_raw=b.program_image[:0x159FF]+b.program_image[0x15CB9:] == c.program_image[:0x159FF]+c.program_image[0x15CB9:],
        full1553_producer_boundary_stream=after == expected_stream(before),
        complete_MAP_vector=score.map_rows(newmap) == rows,
        aggregate_prefix=newmap.split('Detailed map of segments')[0] == prefix,
        complete_public_sequences=score.public_sections(newmap) == expected_publics(score.public_sections(oldmap)),
        group_inventory=groups(newmap) == groups(oldmap),
        header_overlay=b.header == c.header and b.overlay == c.overlay,
        angle_storage=b.program_image[0x1DCEC:0x1DCF2] == c.program_image[0x1DCEC:0x1DCF2] == bytes.fromhex('c0156b40eb95'))
    score_checks = dict(
        new366_raw_and_six_literal_order=literal(t,score.SPANS) == literal(c,score.SPANS) == score.PAIRS and all(t.program_image[a:z] == c.program_image[a:z] for a,z in score.SPANS),
        score_add88_raw_no_relocations=sha(c.program_image[0xD5B0:0xD608]) == score.BINDING['owned_raw_sha256'] and not literal(c,[[0xD5B0,0xD608]]),
        storage_equal=all(b.program_image[s*16+o:s*16+o+n] == c.program_image[s*16+o:s*16+o+n] and literal(b,[[s*16+o,s*16+o+n]]) == literal(c,[[s*16+o,s*16+o+n]]) for s,o,n,k,*_ in score.map_rows(oldmap) if k in ('DATA','BSS','STACK') and n),
        complete_score_MAP_contributions=all(r in score.map_rows(newmap) for r in score.map_rows(oldmap) if r[6] == score.MODULE))
    score_checks['pass_'] = all(score_checks.values())
    return dict(checks=checks,score_preservation=score_checks,
                pass_=all(checks.values()) and score_checks['pass_'])


def check_round(root, work, target, proof):
    root,work = Path(root),Path(work)
    def old(name): return score.read_pinned(root/BASELINE/name,proof[name])
    check_sources(work)
    require(sha((work/'th03_main.asm').read_bytes()) == ROOT_AFTER, 'root changed after staging')
    validate_object((work/OBJECT).read_bytes())
    require(not (work/ALIAS).exists() and not (work/'obj/th03/bm_yume.obj').exists(), 'extra bomb object')
    require(sha(normalize_dependency_timestamps((work/'obj/th03/score_hud.obj').read_bytes())) == score.SCORE_OMF_NORMALIZED_SHA, 'accepted score OMF drift')
    current = (work/'bin/th03/main.exe').read_bytes()
    newmap = (work/'obj/th03/main.map').read_bytes().decode('ascii')
    import tomllib
    accepted = tomllib.loads((root/'config/th03_main_exact_units.toml').read_text())
    score.bind_default(accepted)
    object_roots = accepted['determinism_object_roots']
    current_objects = {p.relative_to(work).as_posix() for p in (work/'obj').rglob('*.obj')}
    current_game = {n for n in current_objects if any(n.startswith(d+'/') for d in object_roots)}
    receipt = json.loads(old('receipt.json')); checks=[]
    for number in (1,2):
        prefix = f'round{number}/source/'
        products = sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',n[len(prefix):]))
        maps = sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and n.endswith('.map'))
        require(len(products) == 31 and len(maps) == 43, 'baseline product/MAP inventory')
        actual_products = sorted(p.relative_to(work).as_posix() for p in (work/'bin').rglob('*') if p.is_file() and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',p.relative_to(work).as_posix()))
        require(actual_products == products and sorted(p.relative_to(work).as_posix() for p in work.rglob('*.map')) == maps, 'fresh product/MAP inventory')
        response = old(prefix+'obj/th03/main.@l')
        token = b'obj\\th03\\main.obj'
        require(response.count(token) == 1 and b'obj\\th03\\bomb_yumemi.obj' not in response, 'baseline link response drift')
        expected_response = response.replace(token,b'obj\\th03\\bomb_yumemi.obj '+token,1)
        require((work/'obj/th03/main.@l').read_bytes() == expected_response, 'literal complete MAIN link response changed')
        main = compare_main(target,current,old(prefix+'bin/th03/main.exe'),old(prefix+'obj/th03/main.map').decode('ascii'),newmap)
        others = all((work/n).read_bytes() == old(prefix+n) for n in products if n!='bin/th03/main.exe')
        other_maps = all((work/n).read_bytes() == old(prefix+n) for n in maps if n!='obj/th03/main.map')
        objects = receipt['rounds'][number-1]['game_objects']
        require(current_game == set(objects)|{OBJECT}, 'fresh game-object inventory changed beyond bomb')
        require(current_objects == set(receipt['rounds'][number-1]['all_objects'])|{OBJECT}, 'fresh complete object inventory changed beyond bomb')
        object_equal = all(sha(normalize_dependency_timestamps((work/n).read_bytes())) == h for n,h in objects.items() if n!='obj/th03/main.obj')
        checks.append(dict(baseline_round=number,main=main,other30_products=others,other42_maps=other_maps,
                           prior_nonroot_objects=object_equal,exact_game_object_inventory=True,exact_all_object_inventory=True,exact_link_response=True,pass_=main['pass_'] and others and other_maps and object_equal))
    providers = check_providers(root,work)
    score_result = dict(baselines=[x['main']['score_preservation'] for x in checks],
                        exact_score_OMF=True,maintained_source_and_include=True,
                        pass_=all(x['main']['score_preservation']['pass_'] for x in checks))
    return dict(baselines=checks,score_preservation=score_result,public_providers=providers,
                pass_=all(x['pass_'] for x in checks) and providers['pass_'],
                exact_acceptance=False,original_global_interposition_proved=False,
                limitations=['Existing mandatory input/math DOS probe remains required.',
                             'No new device timing or reset-intent semantics claimed.'])


def modules(data):
    # Only the rebuilt root OMF is parsed here, never a library member search.
    require(data and data[0] == 0x80, 'root provider OMF header')
    yield 0,data


# PUBDEF parser retained from the reviewed provider proof.
def idx(b, p):
    a = b[p]
    p += 1
    if a & 128:
        a = (a & 127) << 8 | b[p]
        p += 1
    return (a, p)

def string(b, p):
    n = b[p]
    return (b[p + 1:p + 1 + n].decode('latin1'), p + 1 + n)

def publics(path):
    out = []
    for memberoff, blob in modules(path.read_bytes()):
        rs = parse_omf(blob)
        module = string(rs[0].data, 0)[0]
        names = ['']
        segs = [None]
        groups = [None]
        for r in rs:
            b = r.data
            if r.record_type == 150:
                p = 0
                while p < len(b):
                    s, p = string(b, p)
                    names.append(s)
            elif r.record_type in (152, 153):
                p = 1
                if b[0] >> 5 == 0:
                    p += 3
                width = 4 if r.record_type == 153 else 2
                length = int.from_bytes(b[p:p + width], 'little')
                p += width
                n, p = idx(b, p)
                c, p = idx(b, p)
                o, p = idx(b, p)
                segs.append({'name': names[n], 'class': names[c], 'length': length, 'attribute': b[0]})
            elif r.record_type == 154:
                n, p = idx(b, 0)
                groups.append(names[n])
        for ri, r in enumerate(rs):
            if r.record_type not in (144, 145):
                continue
            b = r.data
            g, p = idx(b, 0)
            s, p = idx(b, p)
            frame = None
            if not s:
                frame = int.from_bytes(b[p:p + 2], 'little')
                p += 2
            ordinal = 0
            while p < len(b):
                n, p = string(b, p)
                w = 4 if r.record_type == 145 else 2
                off = int.from_bytes(b[p:p + w], 'little')
                p += w
                ty, p = idx(b, p)
                out.append({'name': n, 'module': module, 'member_offset': memberoff, 'record_index': ri, 'record_offset': memberoff + r.offset, 'record_sha256': sha(blob[r.offset:r.offset + 3 + r.length]), 'record_checksum_sum': sum(blob[r.offset:r.offset + 3 + r.length]) % 256, 'public_ordinal': ordinal, 'segment_index': s, 'segment': segs[s] if s else None, 'group_index': g, 'group': groups[g] if g else None, 'offset': off, 'frame': frame, 'type_index': ty})
                ordinal += 1
    return out


def check_providers(root,work):
    import tomllib
    from lib.toolchain import tree_identity
    root,work = Path(root),Path(work)
    raw = (root/PROVIDER_REPORT).read_bytes()
    require(sha(raw) == PROVIDER_REPORT_SHA, 'provider report changed')
    report = json.loads(raw)
    require(report['pass'] and len(report['ties']) == 7, 'provider proof scope')
    actual = publics(work/'obj/th03/main.obj')
    identity = ['name','module','segment_index','segment','group_index','group','offset','frame','type_index','record_sha256']
    root_groups = 0
    for tie in report['ties']:
        prior = [p['baseline'] for p in tie['providers'] if p['baseline']['logical']=='obj/th03/main.obj']
        if not prior: continue
        root_groups += 1; names = [p['name'] for p in prior]
        found = [p for p in actual if p['name'] in names]
        require(len(found) == len(prior) and all(sum(p['name']==n for p in found)==1 for n in names), 'root tied PUBDEF count changed')
        for old in prior:
            new = next(p for p in found if p['name']==old['name'])
            require(new['record_checksum_sum']==0 and all(new[k]==old[k] for k in identity), 'root tied PUBDEF provider drift')
        require([p['name'] for p in found] == tie['provider_public_order'], 'root tied PUBDEF emitted order drift')
    require(root_groups == 5, 'root provider group count')
    config = tomllib.loads((root/'config/toolchain.toml').read_text())
    surface = next(s for s in config['surfaces'] if s['id']=='tc40j-lib')
    library = root / surface['path']
    actual_tree = tree_identity(library)
    expected_tree = report['historical_runtime_evidence']['tree']
    require(actual_tree.sha256 == expected_tree['sha256'] == surface['sha256']
            and actual_tree.file_count == expected_tree['file_count'] == surface['file_count'], 'runtime library identity drift')
    for entry in report['runtime_inputs']:
        current = library/entry['logical'].upper()
        require(sha(current.read_bytes()) == entry['baseline']['sha256'] == entry['candidate']['sha256'], 'runtime provider bytes changed')
    return dict(root_provider_groups=5,exact_root_PUBDEF_identity_and_order=True,
                runtime_provider_tree_and_members=True,pass_=True,
                provenance='Historical accepted cold attestation plus pinned installed LIB tree, not absent baseline runtime copies.')
