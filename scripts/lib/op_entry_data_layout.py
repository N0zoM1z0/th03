"""Semantic ownership of all487 initialized bytes in the natural OP_01 TU.

The six BSS bytes start at the decoded image end. Their file-backed ownership
is deliberately not inferred from this separate initialized DATA extent.
"""
import hashlib
import re
import struct
from lib.op_cfg_layout import SOURCE,WRAPPER,OBJECT,verify as enclosing_layout
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

DS,START,SIZE=0xD7F,0x90,487
MENU='src/op/menu/menu_state.inl'
UNIT='th03-op-decoded-entry-data'
STAGE7=(1,0,0,2,0,3,5,4,6)
PAIRINGS=tuple(2*character+1 for character in (1,0,2,6,3,5,4,2))
SEEDS=(600,1000,3200,500)


def need(value,message):
    if not value:raise ValueError('OP initialized DATA: '+str(message))


def glyphs(first,count):
    return bytes(range(first,first+count))


def text(value):
    return value.encode('cp932')+b'\0'


MENU_STRINGS=(
    ('COMMAND_STORY',glyphs(0x30,3)+b'\0'),('COMMAND_VS',glyphs(0x33,6)+b'\0'),
    ('COMMAND_MUSICROOM',glyphs(0x41,7)+b'\0'),('COMMAND_REGIST_VIEW',glyphs(0x82,5)+b'\0'),
    ('COMMAND_OPTION',glyphs(0x3D,4)+b'\0'),('COMMAND_QUIT',glyphs(0x48,3)+b'\0'),
    ('LABEL_RANK',glyphs(0x6E,3)+b'\0'),('LABEL_MUSIC',glyphs(0x4B,4)+b'\0'),
    ('LABEL_KEYCONFIG',glyphs(0x5C,6)+b'\0'),('UNUSED_SPACES',bytes([0xCF])*4+b'\0'),
    ('VALUE_EASY',glyphs(0x71,3)+b'\0'),('VALUE_NORMAL',glyphs(0x74,4)+b'\0'),
    ('VALUE_HARD',glyphs(0x78,3)+b'\0'),('VALUE_LUNATIC',glyphs(0x7B,4)+b'\0'),
    ('VALUE_OFF',bytes([0xCF])*2+glyphs(0x5A,2)+bytes([0xCF])*3+b'\0'),
    ('VALUE_FM',bytes([0xCF])+glyphs(0x4F,4)+bytes([0xCF])*2+b'\0'),
    ('VALUE_MIDI',glyphs(0x53,7)+b'\0'),
    ('VALUE_TYPE_1',glyphs(0x62,3)+bytes([0x65,0])),
    ('VALUE_TYPE_2',glyphs(0x62,3)+bytes([0x66,0])),
    ('VALUE_TYPE_3',glyphs(0x62,3)+bytes([0x67,0])),
    ('VALUE_KEY_KEY',glyphs(0x68,2)+glyphs(0x6C,2)+glyphs(0x68,2)+b'\0'),
    ('VALUE_JOY_KEY',glyphs(0x6A,2)+glyphs(0x6C,2)+glyphs(0x68,2)+b'\0'),
    ('VALUE_KEY_JOY',glyphs(0x68,2)+glyphs(0x6C,2)+glyphs(0x6A,2)+b'\0'),
)
LITERALS=(('CFG_FN_CAPS',text('YUME.CFG')),('BINARY_MAINL',text('mainl')),
    ('TEXT_SPACES',text('        ')),
    ('ERROR_GDC_5MHZ_1',text('ＧＤＣクロックが５ＭＨｚになっています。\n')),
    ('ERROR_GDC_5MHZ_2',text('東方夢時空は２．５ＭＨｚでないと正常にゲームがプレイ出来ません\n')),
    ('ERROR_GDC_5MHZ_3',text('\nお手数ですが２．５ＭＨｚに切り替えて、もう一度実行してね。\n')),
    ('OP_AND_END_PF_FN',text('夢時空1.dat')),
    ('ERROR_OUT_OF_MEMORY',text('\nメモリ不足です。メモリ空きを増やしてから実行してくりゃれ\n')),
    ('GAIJI_FN',text('MIKOFT.bft')))


def parts():
    fields=[('snd_sel_disabled',b'\0',SOURCE),('cfg_zero_template',bytes(8),SOURCE),
        ('opponent_seen',bytes(7),SOURCE),('STAGE7_OPPONENT_FOR',bytes(STAGE7),SOURCE),
        ('VS_1P_CPU',glyphs(0x88,4)+glyphs(0x8C,4)+b'\0',SOURCE),
        ('VS_1P_2P',glyphs(0x88,4)+glyphs(0x96,4)+b'\0',SOURCE),
        ('VS_CPU_CPU',glyphs(0x92,4)+glyphs(0x8C,4)+b'\0',SOURCE),
        ('PAIRINGS',bytes(PAIRINGS),SOURCE),('RAND',struct.pack('<4i',*SEEDS),SOURCE)]
    fields += [(name,raw,MENU) for name,raw in MENU_STRINGS]
    fields += [(name,bytes([value]),MENU) for name,value in
        (('menu_sel',0),('quit',0),('in_main',1),('main_initialized',0),('option_initialized',0))]
    fields += [(name,raw,SOURCE) for name,raw in LITERALS]
    offset=0
    result=[]
    for name,raw,source in fields:
        result.append(dict(offset=offset,name=name,size=len(raw),source=source,raw=raw))
        offset+=len(raw)
    need(offset==SIZE,'complete semantic declaration/literal pool without holes')
    return result


PARTS=parts()
BY_NAME={p['name']:p for p in PARTS}
STRINGS={START+p['offset']:p['raw'] for p in PARTS if p['name'] in
    {name for name,_ in MENU_STRINGS+LITERALS}|{'VS_1P_CPU','VS_1P_2P','VS_CPU_CPU'}}
PUBLICS=tuple((p['offset'],'_'+p['name']) for p in PARTS if p['name'] in
    {'snd_sel_disabled','menu_sel','quit','in_main'}|{name for name,_ in MENU_STRINGS})
STATIC_ONLY=tuple(range(173,188))


def semantic_image():
    return b''.join(p['raw'] for p in PARTS)


def verify(root,work,target,candidate):
    enclosing_layout(work,target,candidate)
    native=(work/OBJECT).read_bytes()
    raw,blocks=code_bytes(native,2)
    need([(b['offset'],b['size']) for b in blocks]==[(0,SIZE)] and raw==semantic_image(),
        'one entire independent semantic DATA LEDATA, including unused declarations')
    need(tuple(code_publics(native,2))==PUBLICS,'all27 natural DATA public boundaries')
    block=None
    for rec in parse_omf(native):
        if rec.name=='LEDATA':block=rec.data[0]
        if rec.name=='FIXUPP':need(block!=2,'no DATA native fixup field omitted')
    start=DS*16+START
    need(raw==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],
        'whole semantic/native/target/candidate DATA equality')
    table=(work/'obj/th03/op.map').read_text()
    for offset,name in PUBLICS:
        need(len(re.findall(rf'(?m)^\s*{DS:04X}:{START+offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',table))==2,
            'both public MAP tables: '+name)
    for image in (target,candidate):
        need(not any(r.linear<start+SIZE and r.linear+2>start for r in image.relocations),'complete empty ordered MZ vector; no straddling field')
        need(len(image.program_image)==DS*16+0x118A,'BSS starts exactly after initialized load image')
        for load in (0x1000,0x3000):
            need(image.relocated_program_image(load)[start:start+SIZE]==semantic_image(),'complete DATA remains invariant at both loads')
    digest=hashlib.sha256(raw).hexdigest()
    owner=dict(unit_id=UNIT,name='OP entry initialized DATA',source=SOURCE,object=OBJECT,segment=DS,offset=START,
        start=start,size=SIZE,coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,
        ordered_relocations=[],procedure_count=0,procedures=[],code_bytes=0,initialized_data_bytes=SIZE,private_data_bytes=SIZE,private_bss_bytes=0,
        abi='WORD-aligned DGROUP DATA; BYTE flags/gaiji/Shift-JIS literals; nine opponent BYTEs,eight pairing BYTEs,four signed DWORD seeds')
    return dict(owners=[owner],functions=0,code_bytes=0,initialized_data_bytes=SIZE,bss_bytes=0,
        declarations=[{k:v for k,v in p.items() if k!='raw'} for p in PARTS],publics=[list(p) for p in PUBLICS],
        ordered_native_fields=[],ordered_relocations=[],initialized_holes=0,
        static_only_unused_bytes=list(STATIC_ONLY),BSS_extent=[DS,0x118A,6],BSS_file_backed=False,
        containing_CODE_or_BSS_newly_accepted=False,whole_product_accepted=False)
