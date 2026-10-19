"""Bounded score-only physical binding and conjunctive preservation checks.

No symbol normalization, generic owner override, or acceptance
state mutation. The eight public display ties are the independently reviewed
retained diagnostic rule; all other ordering remains literal.
"""
from pathlib import Path
import hashlib
import json
import re
import struct

SPANS = [[0xD50E, 0xD5B0], [0xD608, 0xD6D4]]
PAIRS = [[0x96E,x] for x in (0x3E57,0x3E93,0x3EA3,0x3F39,0x3F80,0x3F99)]
OUTSIDE_SHA = '7e573b59e04bc2ce728be309b422f32758ea6ad560513ef3f044c3b0e740ed41'
OLD = (0x96E,0x29F8,0x15FC,'CODE','PLAYER_M_TEXT','MAIN_01','th03_main.asm',28)
MODULE = 'src/main/hud/score.asm'
# These are every SEGDEF in the historical genuine score OMF, including zeros.
INSERTIONS = {
    '_TEXT': (0,0x2EB0,0,'CODE','_TEXT','(none)',MODULE,48),
    '_DATA': (0x1D56,0xBEC,0,'DATA','_DATA','DGROUP',MODULE,48),
    '_BSS': (0x1D56,0x68DC,0,'BSS','_BSS','DGROUP',MODULE,48),
    'HUD_STAT_TEXT': (0x96E,0x2217,0,'CODE','HUD_STAT_TEXT','MAIN_01',MODULE,28),
    'PLAYER_M_TEXT': (0x96E,0x3E2E,454,'CODE','PLAYER_M_TEXT','MAIN_01',MODULE,28)}
NEW_PUBLICS = [(0x96E,s-0x96E0,n) for n,s in [
    ('score_glyph_put',0xD50E),('score_hud_render',0xD52E),
    ('background_overlap_clear',0xD5A2),('score_bonus_digits_put',0xD668),
    ('score_credit_digit_set',0xD6C0)]] + [(0x1D56,0x39CC,'_background_particles')]
BINDING = {
 'schema_version':1,'kind':'score-only-candidate-physical-binding',
 'owner':'th03-main-score-add',
 'accepted_owner_digest':'36d05e86485b71bc19b7e1c01e76f2111694a1ad02c767f2b7d076ed53388ec9',
 'accepted_function_digest':'72337536150cf76339f14ac209bc0388cfc4941e3dbbcfdee692357585bf045a',
 'owned_raw_sha256':'b4a01ace234c93d087f13342d43a6857f4fdc36a1a09b1c5ed294846e49ae287',
 'old_carrier':dict(segment=0x96E,start=0x29F8,size=0x15FC,map_module='th03_main.asm',map_segment='PLAYER_M_TEXT',map_group='MAIN_01',map_acbp=28),
 'replacement_contributions':[
 dict(segment=0x96E,start=0x29F8,size=0x1436,map_module='th03_main.asm',map_segment='PLAYER_M_TEXT',map_group='MAIN_01',map_acbp=28),
 dict(segment=0x96E,start=0x3E2E,size=454,map_module=MODULE,map_segment='PLAYER_M_TEXT',map_group='MAIN_01',map_acbp=28)],
 'accepted_semantic_extent':dict(segment=0x96E,start=0x3ED0,size=88),
 'candidate_object_path':'obj/th03/score_hud.obj',
 'default_binding':'separately digest-validated physical descriptor',
 'new_credit_bytes':366,'new_raw_exclusion_spans':SPANS}

def require(value, message):
    if not value: raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate_binding_manifest(accepted):
    owners=[u for u in accepted['units'] if u['id']==BINDING['owner']]
    require(len(owners)==1,'missing/duplicate score_add owner')
    functions=[f for f in accepted['functions'] if f['object']=='score_add']
    require(len(functions)==1,'missing/duplicate score_add function')
    require(digest(owners[0])==BINDING['accepted_owner_digest'],'accepted owner/source/ABI drift')
    require(digest(functions[0])==BINDING['accepted_function_digest'],'accepted function/public/ABI drift')

ROW = re.compile(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4,8})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=(\d+)\s*$',re.M)
def map_rows(text):
    rows=[(int(a,16),int(b,16),int(c,16),d,e,f,g.replace(chr(92),'/'),int(h))
          for a,b,c,d,e,f,g,h in ROW.findall(text)]
    require(rows and len(rows)==len(re.findall(r'^.*\bC=.*\bS=.*\bG=.*\bM=.*$',text,re.M)),
            'missing/unparsed detailed MAP rows')
    return rows

def expected_map(old):
    require(old.count(OLD)==1,'old carrier missing/duplicate/geometry drift')
    expected=[]; inserted=[]
    for row in old:
        if row==OLD: row=(row[0],row[1],0x1436,*row[3:])
        expected.append(row)
        if row[6]=='th03_main.asm' and row[4] in INSERTIONS:
            expected.append(INSERTIONS[row[4]]);inserted.append(row[4])
    require(sorted(inserted)==sorted(INSERTIONS),'missing/duplicate root segment')
    return expected

def public_sections(text):
    require(text.count('Publics by Name')==text.count('Publics by Value')==1,'missing/duplicate public section')
    before,values=text.split('Publics by Value')
    names=before.split('Publics by Name')[1]
    pat=re.compile(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?(\S[^\r\n]*?)\s*$',re.M)
    return [[(int(s,16),int(o,16),n) for s,o,n in pat.findall(part)] for part in (names,values)]

# Exact incidental equal-address display ties observed in frozen TLINK MAPs.
# No symbol identity/address/multiplicity or inter-address ordering is waived.
VALUE_TIES = {
 (0x0000,0x073A): (('EGC_END','EGC_START'),('EGC_START','EGC_END')),
 (0x0000,0x08D2): (('DOS_CLOSE','FONTFILE_CLOSE'),('FONTFILE_CLOSE','DOS_CLOSE')),
 (0x0000,0x3224): (('LMOD@','F_LMOD@'),('F_LMOD@','LMOD@')),
 (0x0000,0x3313): (('F_PSUB@','PSUB@'),('PSUB@','F_PSUB@')),
 (0x139D,0x2FB3): (('ELLEN_TARGET_SET','sub_16983'),('sub_16983','ELLEN_TARGET_SET')),
 (0x1D56,0x007C): (('__osversion','__version','__osmajor'),('__version','__osversion','__osmajor')),
 (0x1D56,0x0310): (('_pfkey','pfkey'),('pfkey','_pfkey')),
 (0x1D56,0x11EA): (('vsync_Count1','_vsync_Count1'),('_vsync_Count1','vsync_Count1')),
}
def value_public_order_equal(before, after):
    import itertools
    if [p[:2] for p in before]!=[p[:2] for p in after]:return False
    a=[(k,tuple(r[2] for r in g)) for k,g in itertools.groupby(before,key=lambda p:p[:2])]
    b=[(k,tuple(r[2] for r in g)) for k,g in itertools.groupby(after,key=lambda p:p[:2])]
    if len(a)!=len(b):return False
    seen=set()
    for (address,old),(other,new) in zip(a,b):
        if address!=other:return False
        if address in VALUE_TIES:
            if address in seen or old!=VALUE_TIES[address][0] or new not in VALUE_TIES[address]:return False
            seen.add(address)
        elif old!=new:return False
    return seen==set(VALUE_TIES)


def map_diagnostic(reference,candidate):
    old,new=map_rows(reference),map_rows(candidate)
    expected=expected_map(old)
    require(reference.split('Detailed map of segments')[0]==candidate.split('Detailed map of segments')[0],
            'ordered segment aggregate inventory changed')
    oldpub,newpub=public_sections(reference),public_sections(candidate)
    public_ok=True
    for section,(before,after) in enumerate(zip(oldpub,newpub)):
        public_ok &= all(after.count(p)==1 and before.count(p)==0 for p in NEW_PUBLICS)
        retained=[p for p in after if p not in NEW_PUBLICS]
        public_ok &= (retained==before if section==0 else value_public_order_equal(before,retained))
        public_ok &= after.count((0x96E,0x3ED0,'score_add(unsigned int,unsigned char)'))==1
    # Everything between detailed rows and public section contains group bases.
    def groups(t):
        end=max(m.end() for m in ROW.finditer(t))
        return t[end:t.index('Publics by Name')].strip()
    return dict(expected_complete_ordered_vector=expected,candidate_complete_ordered_vector=new,
        complete_ordered_vector_equal=new==expected,all_prior_publics_and_bounded_additions=bool(public_ok),
        group_inventory_equal=groups(reference)==groups(candidate),
        pass_=new==expected and public_ok and groups(reference)==groups(candidate))


CANDIDATE_PATH = "config/th03_main_score_candidate.toml"
CANDIDATE_DIGEST = 'e678b81e3ee3e7ab81a2b48a139e36049d5a75495fef7cfa340425a0d2048cf3'
SCORE_UNIT_DIGEST = 'fa910645c71a7503d8f4701acc4fc46ab242bda772740b6990ad34107de62084'
SCORE_SOURCE_SHA = '838cad4521b431e4c287173ef6dcc29c2958ef4cafad30643688c1a5cd1e0a8b'
REDUCED_ROOT_SHA = '6c157d483d1822ba9f78c63eb03d2ccac8a4311f99967bbe0eddc78f453c58d1'
INCLUDE_SHA = '05553706931e625f087c7380095e681e5a6634ac03339a93845841605d796b47'

# Historical proof inventory stays in place, never copied into a new build tree.
PROOF_GUARD = '.analysis/gpt-dots-score-retained-diagnostic-v02/proof-guards.json'
PROOF_GUARD_SHA = '5e86b1ea903ab7bf5a366ede72db231b2ade27d2b79b9d4ceb80f4c45ab69f50'
BASELINE = '.analysis/th03-main-exact/gpt-dots-gameplay-promoted-default-cold-v01'
SCORE_OMF_NORMALIZED_SHA = 'b07127fbb34727ef1558b95c2d5325ee6c7dedb07b58a6ba1fef3a7afe55db73'



# The original root descriptor is retained only as a pre-transformation guard.
# The default manifest itself must describe the real maintained physical carrier.
ORIGINAL_OWNER = {'id': 'th03-main-score-add', 'source': 'src/main/player/score_add.inl', 'header': 'src/main/player/score_add.hpp', 'object': 'score_add', 'ownership': 'bounded-include', 'carrier_path': 'th03_main.asm', 'carrier_sha256': '94c52b803ebcf3df018c18cffc35891f074c45b3cafbf5927db1907024f54d62', 'overlay_path': 'th03/main/player/score_add.asm', 'object_path': 'obj/th03/main.obj', 'map_module': 'th03_main.asm', 'translator_comment': 'Turbo Assembler  Version 5.0', 'code_extents': [{'name': 'code', 'ledger_id': 'th03-main-score-add', 'segment': 2414, 'start': 16080, 'size': 88, 'map_start': 10744, 'map_size': 5628, 'map_acbp': 28, 'map_segment': 'PLAYER_M_TEXT', 'map_group': 'MAIN_01', 'producer_ranges': []}]}
PRE_SCORE_CONFIG_DIGEST = '85b8c9eb0b197b1289387ac9a61c9d13d6959abba32e3406a8e16176bce6710c'
DEFAULT_SCORE_UNIT_DIGEST = 'dde08ee406a33505429cdef89c4b61bc163137dd601b3b3c5de5f58fbe9a24ac'
DEFAULT_CONFIG_DIGEST = '8ede8dc00460e93dfd5699141249a11605dd61127290190eacbff98fbd9f5fe8'

def bind_default(config):
    """Validate the one reviewed default transition; never rewrite its metadata."""
    import copy
    require(digest(config) == DEFAULT_CONFIG_DIGEST, 'default score configuration drift')
    result = copy.deepcopy(config)
    owners = [u for u in result['units'] if u['id'] == BINDING['owner']]
    require(len(owners) == 1, 'default score_add missing/duplicate')
    # All fields, including logical source, ABI and extent, are covered by the
    # complete default digest and independently reversed historical digest.
    result['units'] = [copy.deepcopy(ORIGINAL_OWNER) if u['id'] == BINDING['owner'] else u
                       for u in result['units'] if u['id'] != 'th03-main-score-hud']
    result['functions'] = [f for f in result['functions'] if f['object'] != 'score_hud']
    require(digest(result) == PRE_SCORE_CONFIG_DIGEST, 'default changed prior ownership')
    validate_binding_manifest(result)
    return copy.deepcopy(config), copy.deepcopy(ORIGINAL_OWNER)


def is_score_owner(unit):
    """Only this complete reviewed descriptor may use disjoint physical CODE."""
    return unit.get('id') == 'th03-main-score-hud' and digest(unit) in (SCORE_UNIT_DIGEST, DEFAULT_SCORE_UNIT_DIGEST)


def bind_candidate(config, candidate, manifest_name):
    """Return a private effective physical binding; never modify caller inputs."""
    import copy
    require(manifest_name == CANDIDATE_PATH, 'score candidate path changed')
    require(digest(candidate) == CANDIDATE_DIGEST, 'score candidate descriptor changed')
    validate_binding_manifest(config)
    require(sum(is_score_owner(u) for u in config['units']) == 1, 'score producer absent/duplicate')
    result = copy.deepcopy(config)
    owner = next(u for u in result['units'] if u['id'] == BINDING['owner'])
    original = copy.deepcopy(owner)
    owner.update(carrier_path=MODULE, carrier_sha256=SCORE_SOURCE_SHA,
                 overlay_path='src/main/player/score_add.inl',
                 object_path=BINDING['candidate_object_path'], map_module=MODULE.replace('/', chr(92)))
    owner['code_extents'][0].update(map_start=0x3E2E, map_size=454)
    # Source, header, logical object/owner, function, ABI and credited span stay put.
    return result, original


DEFAULT_SCORE_SOURCE_SHA = 'ec13b2fb32376e0b068ab6fbb49183bbfcad4487bdc0e06a7e7b9bc8356ae62e'

def check_stage(work, *, default=False):
    work = Path(work)
    for name, expected in [('th03_main.asm', REDUCED_ROOT_SHA), (MODULE, DEFAULT_SCORE_SOURCE_SHA if default else SCORE_SOURCE_SHA),
                           ('src/main/player/score_add.inl', INCLUDE_SHA)]:
        require(hashlib.sha256((work/name).read_bytes()).hexdigest() == expected, 'score staged source drift: '+name)
    require(not re.search(rb'^\s*include\s+[^\r\n]*score_add\.(?:asm|inl)\s*$',
                          (work/'th03_main.asm').read_bytes(), re.M|re.I), 'duplicate root score_add include')
    require((work/MODULE).read_bytes().count(b'include src/main/player/score_add.inl') == 1,
            'score_add include must occur exactly once')


def read_pinned(path, pin):
    import stat
    require(path.is_file() and not path.is_symlink(), 'missing/symlink proof input: '+str(path))
    data = path.read_bytes()
    require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
            and oct(stat.S_IMODE(path.stat().st_mode)) == pin['mode'], 'proof bytes/mode drift: '+str(path))
    return data


def guard_baseline(root):
    """Protect the historical complete proof tree before/after cold execution."""
    import stat
    root = Path(root)
    raw = (root/PROOF_GUARD).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PROOF_GUARD_SHA, 'historical proof inventory drift')
    saved = json.loads(raw)[BASELINE]
    base = root/BASELINE
    require(oct(stat.S_IMODE(base.stat().st_mode)) == saved['root_mode'], 'baseline root mode drift')
    files, dirs = set(), {}
    for path in base.rglob('*'):
        require(not path.is_symlink(), 'unexpected baseline symlink')
        name = path.relative_to(base).as_posix()
        if path.is_file(): files.add(name)
        elif path.is_dir(): dirs[name] = oct(stat.S_IMODE(path.stat().st_mode))
        else: raise ValueError('unexpected baseline special file')
    require(files == set(saved['files']) and dirs == saved['dirs'], 'baseline proof inventory changed')
    for name, pin in saved['files'].items(): read_pinned(base/name, pin)
    return saved['files']


def ordered_literal(image, spans, outside=False):
    result = []
    for reloc in image.relocations:
        p = reloc.linear
        require(not any(p < edge < p+2 for span in spans for edge in span), 'edge-straddling relocation')
        inside = any(lo <= p < hi for lo, hi in spans)
        if inside != outside: result.append([reloc.segment, reloc.offset])
    return result


def outside_payload(image):
    require(len(image.program_image) >= SPANS[-1][1], 'short MAIN image')
    a,b = SPANS
    return image.program_image[:a[0]] + image.program_image[a[1]:b[0]] + image.program_image[b[1]:]


def compare_main(target, candidate, baseline, old_map, new_map):
    from lib.pc98 import parse_mz
    images = [parse_mz(b) for b in (target, candidate, baseline)]
    require(all(i.valid for i in images), 'invalid score MZ')
    t,c,b = images
    require(ordered_literal(t, SPANS) == PAIRS, 'target six-pair scope drift')
    new_ok = ordered_literal(c, SPANS) == PAIRS and all(
        t.program_image[lo:hi] == c.program_image[lo:hi] for lo,hi in SPANS)
    old_pairs = ordered_literal(b, SPANS, True)
    require(len(old_pairs) == 1547 and hashlib.sha256(b''.join(
        struct.pack('<HH', off, seg) for seg,off in old_pairs)).hexdigest() == OUTSIDE_SHA,
        'baseline outside literal scope drift')
    outside_ok = old_pairs == ordered_literal(c, SPANS, True) and outside_payload(b) == outside_payload(c)
    score_ok = (hashlib.sha256(c.program_image[0xD5B0:0xD608]).hexdigest() == BINDING['owned_raw_sha256']
                and not ordered_literal(c, [[0xD5B0,0xD608]]))
    maps = map_diagnostic(old_map, new_map)
    header_ok = b.header == c.header and b.overlay == c.overlay
    storage_ok = True
    for seg,off,size,kind,*_ in map_rows(old_map):
        if kind in ('DATA','BSS','STACK') and size:
            lo,hi = seg*16+off,seg*16+off+size
            storage_ok &= (b.program_image[lo:hi] == c.program_image[lo:hi]
                           and ordered_literal(b,[[lo,hi]]) == ordered_literal(c,[[lo,hi]]))
    return dict(new366_raw_and_six_literal_order=new_ok, outside_raw_and_1547_literal_order=outside_ok,
                score_add_88_raw_and_empty_relocations=score_ok, map_inventory=maps,
                header_and_overlay_equal=header_ok, storage_equal=bool(storage_ok),
                pass_=bool(new_ok and outside_ok and score_ok and maps['pass_'] and header_ok and storage_ok))


def check_round(root, work, target, frozen):
    """Compare one freshly built complete graph against BOTH accepted rounds."""
    from lib.omf import normalize_dependency_timestamps
    root,work = Path(root),Path(work)
    def sha(data): return hashlib.sha256(data).hexdigest()
    def old(name): return read_pinned(root/BASELINE/name, frozen[name])
    current = (work/'bin/th03/main.exe').read_bytes()
    newmap = (work/'obj/th03/main.map').read_bytes().decode('ascii', errors='strict')
    omf = (work/'obj/th03/score_hud.obj').read_bytes()
    require(sha(normalize_dependency_timestamps(omf)) == SCORE_OMF_NORMALIZED_SHA,
            'fresh score OMF differs beyond existing dependency timestamp comparison')
    # Literal maintained path/case, all22 fixups, all454 CODE bytes and no storage
    # allocation are bound by this complete native-object identity, not patched.
    receipt = json.loads(old('receipt.json'))
    checks = []
    for number in (1,2):
        prefix = f'round{number}/source/'
        products = sorted(n[len(prefix):] for n in frozen if n.startswith(prefix)
                          and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)', n[len(prefix):]))
        maps = sorted(n[len(prefix):] for n in frozen if n.startswith(prefix) and n.endswith('.map'))
        require(len(products)==31 and len(maps)==43, 'baseline complete product/MAP vector drift')
        actual_products = sorted(p.relative_to(work).as_posix() for p in (work/'bin').rglob('*')
                                 if p.is_file() and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',p.relative_to(work).as_posix()))
        actual_maps = sorted(p.relative_to(work).as_posix() for p in work.rglob('*.map'))
        require(actual_products==products and actual_maps==maps, 'candidate product/MAP inventory drift')
        main = compare_main(target,current,old(prefix+'bin/th03/main.exe'),
                            old(prefix+'obj/th03/main.map').decode(),newmap)
        other_products = all((work/n).read_bytes()==old(prefix+n) for n in products if n!='bin/th03/main.exe')
        other_maps = all((work/n).read_bytes()==old(prefix+n) for n in maps if n!='obj/th03/main.map')
        # Existing dependency-timestamp normalization only; no symbol/FIXUPP rewrite.
        objects = receipt['rounds'][number-1]['game_objects']
        old_objects = all(sha(normalize_dependency_timestamps((work/n).read_bytes()))==h
                          for n,h in objects.items() if n!='obj/th03/main.obj')
        checks.append(dict(baseline_round=number,main=main,game_products=31,map_files=43,
                           other_products_equal=other_products,other_maps_equal=other_maps,
                           prior_nonroot_game_objects_equal=old_objects,
                           pass_=bool(main['pass_'] and other_products and other_maps and old_objects)))
    return dict(baselines=checks,pass_=all(c['pass_'] for c in checks),
                exact_acceptance=False,original_global_interposition_proved=False,
                score_device_semantics_proved=False,
                limitations=['Existing input/math DOS probe remains required; no new score/device trace claimed.',
                             'DS provenance/reset intent and physical VRAM/GRCG timing remain unproved supporting semantics.',
                             'Keep native assembler logs, including BYTE/EVEN alignment warnings.'])


def check_original_build(work):
    # Same already-reviewed candidate -j1 transform as the existing adapter.
    require(hashlib.sha256((Path(work)/'build.bat').read_bytes()).hexdigest() ==
            '400349385d38fcb72d17f14c0e4680d677d8d704c15bcfbabb17725a6f2c9a95',
            'score candidate original build carrier drift')
