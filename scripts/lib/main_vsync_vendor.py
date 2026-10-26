"""Restore the original master.lib VS dependency; no authored-source credit.

Only source declarations are split here. TLIB extracts the unchanged vendor
module during each native build; neither source generation nor extraction
reads target bytes or rewrites OMF. The vendor assembler remains unidentified.
"""
import hashlib
import re
from collections import Counter

ARCHIVE = 'bin/masters.lib'
ARCHIVE_SHA = '6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6'
OBJECT = 'obj/th03/vs.obj'
OBJECT_SHA = '3bb280d22f01581b08c4fed605f09c198f54cde8b9b6767a4fef5a09953a8318'
TLIB_SHA = '2d65d72b8800f7f3d4716218ed508bdd198e73b5f96f4830c1e14d1bb56546e2'
TAIL = 'th03/mst_tail.asm'
TAIL_OBJECT = 'obj/th03/mst_tail.obj'
HEAD_EXPORTS = set('AtanTable8 ClipXL ClipXW ClipXR ClipYT ClipYH ClipYB ClipYT_seg ClipYB_adr EDGES backup_mseg bfnt_header2 graph_VramSeg graph_VramWords graph_VramLines graph_VramWidth graph_VramZoom PaletteTone PaletteNote ResPalSeg random_seed TextVramSeg TextShown trapez_a trapez_b ylen Palettes'.split())
VS_EXPORTS = set('vsync_Proc vsync_Delay vsync_OldMask vsync_Count1 vsync_Count2 vsync_OldVect'.split())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def split(raw, speeds):
    """Split complete real DATA/BSS contributions at their existing VS includes."""
    text = raw.decode('latin1').replace('\r\n', '\n')
    markers = ('include libs/master.lib/vs[data].asm', '\t.data?\n',
               'include libs/master.lib/vs[bss].asm', '\t.data\n')
    if any(text.count(m) != 1 for m in markers):
        raise ValueError('unique MAIN VSync storage boundaries required')
    before, rest = text.split(markers[0])
    data_tail, rest = rest.split(markers[1])
    bss_head, bss_tail = rest.split(markers[2])
    aliases = before.splitlines()[:4]
    if aliases[1:3] != ['_playfield_transition_vertices = word_1FBC4',
                        '_transition_hmask = trapezoid_hmask']:
        raise ValueError('MAIN transition aliases changed')
    before = '\n'.join(before.splitlines()[4:]) + '\n'
    code, data_head = before.split(markers[3])
    moved = []
    kept = set()
    def public(match):
        names = [n.strip() for n in match[1].split(',')]
        kept.update(n for n in names if n in HEAD_EXPORTS)
        moved.extend(n for n in names if n not in HEAD_EXPORTS | VS_EXPORTS)
        names = [n for n in names if n in HEAD_EXPORTS]
        return 'public ' + ','.join(names) if names else ''
    code = re.sub(r'^\s*public ([^\n]+)$', public, code, flags=re.M | re.I)
    if kept != HEAD_EXPORTS:
        raise ValueError('MAIN head storage exports changed')
    imports = ('\nextrn mem_AllocID:word,trapezoid_hmask:word,pfint21_entries:word\n'
               'extrn _pi_buffers:dword,_randring:byte,_randring_p:byte\n')
    head = code + markers[3] + data_head + markers[1] + bss_head + imports + '\nend\n'
    # The same existing types are required by both complete storage producers.
    if sha(speeds) != '21652f069b33b83c3bf8006f96a697fa83d2d6c965263c8fda8c67cf37ab34de':
        raise ValueError('original player speed type input changed')
    types = speeds.decode('latin1').replace('\r\n', '\n').split('public _PLAYCHAR_SPEEDS')[0]
    header = text[text.index('\t\t.386'):text.index('GBA_GAUGE_LEVEL_MIN')]
    header = header.replace("BINARY = 'M'", '')  # no duplicate absolute _address_0 export
    constants = '\n'.join(l for l in text.splitlines()[4:]
                          if re.match(r'^\w+\s*=\s*', l) and not l.startswith('BINARY'))
    exports = '\n'.join('public ' + ','.join(moved[i:i+8]) for i in range(0, len(moved), 8))
    tail = (header + '\n' + types + '\n' + constants + '\n' + '\n'.join(aliases)
            + '\n' + exports + '\n' + markers[3] + data_tail + markers[1] + bss_tail)
    return {name: value.replace('\n', '\r\n').encode('latin1')
            for name, value in [('th03_main.asm', head), (TAIL, tail)]}


def replaced_contribution(line):
    line = line.replace('\\', '/')
    return (('C=DATA ' in line or 'C=BSS ' in line)
            and any('M=' + n + ' ' in line for n in ('th03_main.asm', TAIL, 'VS.ASM')))


def public_rows(raw):
    text = raw.decode('latin1')
    a = text.index('  Address         Publics by Name')
    b = text.index('  Address         Publics by Value')
    c = text.index('Program entry point', b)
    sections = []
    for section in (text[a:b], text[b:c]):
        rows = []
        for line in section.splitlines()[1:]:
            if not line.strip():
                continue
            m = re.fullmatch(r'\s+([0-9A-F]{4}:[0-9A-F]{4})\s+(?:(idle)\s+)?(.+?)\s*', line)
            if not m:
                raise ValueError('unparsed MAIN public row')
            rows.append((m[1], bool(m[2]), m[3]))
        sections.append(rows)
    if Counter(sections[0]) != Counter(sections[1]):
        raise ValueError('MAIN public sections disagree')
    return sections[0]


def review(work):
    from probe_th03_main_bomb_rikako_cpp import segment_definitions
    from lib.omf import parse_omf
    raw = (work / OBJECT).read_bytes()
    if sha(raw) != OBJECT_SHA:
        raise ValueError('original VS vendor object changed')
    segments = segment_definitions(raw)
    if [(s['name'], s['class'], s['size']) for s in segments] != [
            ('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 8), ('_BSS', 'BSS', 8)]:
        raise ValueError('original VS vendor segment ownership changed')
    if any(r.name in ('FIXUPP', 'FIXUPP32') for r in parse_omf(raw)):
        raise ValueError('original VS vendor has unexpected fixups')
    text = (work / 'obj/th03/main.map').read_text().replace('\\', '/')
    allocations = [
        (0x90, 0x50E, 'DATA', '_DATA', 'th03_main.asm'),
        (0x59E, 8, 'DATA', '_DATA', 'VS.ASM'),
        (0x5A6, 0x646, 'DATA', '_DATA', TAIL),
        (0x1182, 0x68, 'BSS', '_BSS', 'th03_main.asm'),
        (0x11EA, 8, 'BSS', '_BSS', 'VS.ASM'),
        (0x11F2, 0x56EA, 'BSS', '_BSS', TAIL),
    ]
    for start, size, cls, seg, module in allocations:
        pattern = (rf'(?m)^\s*1D56:{start:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+'
                   rf'G=DGROUP\s+M={re.escape(module)}\s+ACBP=48\s*$')
        if len(re.findall(pattern, text)) != 1:
            raise ValueError('VSync storage MAP ownership changed: ' + module)
    tail = segment_definitions((work / TAIL_OBJECT).read_bytes())
    if [(s['name'], s['class'], s['size']) for s in tail if s['size']] != [
            ('_DATA', 'DATA', 0x646), ('_BSS', 'BSS', 0x56EA)]:
        raise ValueError('MAIN storage tail added executable or unrelated storage')
    return dict(origin='original-prebuilt-vendor-context', archive_sha256=ARCHIVE_SHA,
                object_sha256=OBJECT_SHA, data_bytes=8, bss_bytes=8, code_bytes=0,
                new_authored_credit=0, source_generated_vendor=False)
