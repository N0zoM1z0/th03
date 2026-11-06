#!/usr/bin/env python3
"""Six typed locale/character/error DATA owners and six metadata-only members.

Complete original initialized payloads, ordered FAR fields and literal ALIAS records.
"""
import argparse,fcntl,json,os,shutil,struct,subprocess,tomllib,sys
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
from pathlib import Path

import build_th03_mainl_after532_work as parent
import build_th03_mainl_work as build
import build_th03_mainl_xx_work as xx
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_mainl_large_fixups import original_literal_fixups
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_after533_work.py'
PREFIX='.analysis/work/mainl-after533-'
MODES={'locale-tables-aliases-twelve':('clocale', 'clower', 'cupper', 'ctype', 'syserrls', 'MBCTYPE', 'delf', 'delfarry', 'nearheap', 'nheapchk', 'MBCS', 'JSTR')}
NATIVE={'clocale': {'index': 124,
             'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 2657), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [],
                                    '2': [(0, '__Clocale'),
                                          (2459, '__LocaleCatNames'),
                                          (2491, '__pLocale'),
                                          (2495, '__LocaleLibName')],
                                    '3': []},
             'imports': ['_strcmp', '_strxfrm', '__ctype', '__lower', '__upper'],
             'fields': 14,
             'fpu_sites': [],
             'near_frame_sites': [],
             'near_frame_targets': {},
             'code_segment': 1,
             'group': '08ff02ff03',
             'uninitialized_sites': {'1': [], '2': [], '3': []},
             'alias_records': [],
             'modend_records': ['00']},
 'clower': {'index': 125,
            'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 256), ('_BSS', 'BSS', 0)],
            'segment_attributes': [40, 72, 72],
            'publics_by_segment': {'1': [], '2': [(0, '__lower')], '3': []},
            'imports': [],
            'fields': 0,
            'fpu_sites': [],
            'near_frame_sites': [],
            'near_frame_targets': {},
            'code_segment': 1,
            'group': '08ff02ff03',
            'uninitialized_sites': {'1': [], '2': [], '3': []},
            'alias_records': [],
            'modend_records': ['00']},
 'cupper': {'index': 126,
            'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 256), ('_BSS', 'BSS', 0)],
            'segment_attributes': [40, 72, 72],
            'publics_by_segment': {'1': [], '2': [(0, '__upper')], '3': []},
            'imports': [],
            'fields': 0,
            'fpu_sites': [],
            'near_frame_sites': [],
            'near_frame_targets': {},
            'code_segment': 1,
            'group': '08ff02ff03',
            'uninitialized_sites': {'1': [], '2': [], '3': []},
            'alias_records': [],
            'modend_records': ['00']},
 'ctype': {'index': 127,
           'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 257), ('_BSS', 'BSS', 0)],
           'segment_attributes': [40, 72, 72],
           'publics_by_segment': {'1': [], '2': [(0, '__ctype')], '3': []},
           'imports': [],
           'fields': 0,
           'fpu_sites': [],
           'near_frame_sites': [],
           'near_frame_targets': {},
           'code_segment': 1,
           'group': '08ff02ff03',
           'uninitialized_sites': {'1': [], '2': [], '3': []},
           'alias_records': [],
           'modend_records': ['00']},
 'syserrls': {'index': 318,
              'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 699), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [], '2': [(0, '__sys_errlist')], '3': []},
              'imports': [],
              'fields': 48,
              'fpu_sites': [],
              'near_frame_sites': [],
              'near_frame_targets': {},
              'code_segment': 1,
              'group': '08ff02ff03',
              'uninitialized_sites': {'1': [], '2': [], '3': []},
              'alias_records': [],
              'modend_records': ['00']},
 'MBCTYPE': {'index': 585,
             'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 257), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [], '2': [(0, '__mbctype')], '3': []},
             'imports': [],
             'fields': 0,
             'fpu_sites': [],
             'near_frame_sites': [],
             'near_frame_targets': {},
             'code_segment': 1,
             'group': '08ff02ff03',
             'uninitialized_sites': {'1': [], '2': [], '3': []},
             'alias_records': [],
             'modend_records': ['00']},
 'delf': {'index': 18,
          'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
          'segment_attributes': [40, 72, 72],
          'publics_by_segment': {'1': [], '2': [], '3': []},
          'imports': [],
          'fields': 0,
          'fpu_sites': [],
          'near_frame_sites': [],
          'near_frame_targets': {},
          'code_segment': 1,
          'group': '08ff02ff03',
          'uninitialized_sites': {'1': [], '2': [], '3': []},
          'alias_records': [],
          'modend_records': ['00']},
 'delfarry': {'index': 19,
              'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [], '2': [], '3': []},
              'imports': [],
              'fields': 0,
              'fpu_sites': [],
              'near_frame_sites': [],
              'near_frame_targets': {},
              'code_segment': 1,
              'group': '08ff02ff03',
              'uninitialized_sites': {'1': [], '2': [], '3': []},
              'alias_records': [],
              'modend_records': ['00']},
 'nearheap': {'index': 179,
              'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 0)],
              'segment_attributes': [40, 72],
              'publics_by_segment': {'1': [], '2': []},
              'imports': [],
              'fields': 0,
              'fpu_sites': [],
              'near_frame_sites': [],
              'near_frame_targets': {},
              'code_segment': 1,
              'group': '06ff02',
              'uninitialized_sites': {'1': [], '2': []},
              'alias_records': [],
              'modend_records': ['00']},
 'nheapchk': {'index': 358,
              'segments': [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 0)],
              'segment_attributes': [40, 72],
              'publics_by_segment': {'1': [], '2': []},
              'imports': [],
              'fields': 0,
              'fpu_sites': [],
              'near_frame_sites': [],
              'near_frame_targets': {},
              'code_segment': 1,
              'group': '06ff02',
              'uninitialized_sites': {'1': [], '2': []},
              'alias_records': [],
              'modend_records': ['00']},
 'MBCS': {'index': 584,
          'segments': [],
          'segment_attributes': [],
          'publics_by_segment': {},
          'imports': [],
          'fields': 0,
          'fpu_sites': [],
          'near_frame_sites': [],
          'near_frame_targets': {},
          'code_segment': 1,
          'group': None,
          'uninitialized_sites': {},
          'alias_records': ['085f5f6d6273636174075f737472636174',
                            '085f5f6d6273637079075f737472637079',
                            '085f5f6d6273647570075f737472647570',
                            '095f5f666d6273636174095f5f66737472636174',
                            '095f5f666d6273637079095f5f66737472637079',
                            '095f5f666d6273647570095f5f66737472647570'],
          'modend_records': ['00']},
 'JSTR': {'index': 645,
          'segments': [],
          'segment_attributes': [],
          'publics_by_segment': {},
          'imports': [],
          'fields': 0,
          'fpu_sites': [],
          'near_frame_sites': [],
          'near_frame_targets': {},
          'code_segment': 1,
          'group': None,
          'uninitialized_sites': {},
          'alias_records': ['085f5f6a6374797065095f5f6d626374797065',
                            '055f62746f6d0a5f5f6d62736e63636e74',
                            '095f63686b6374797065095f5f6d626274797065',
                            '095f68616e746f7a656e0a5f5f6d6262746f6d6263',
                            '085f69736b6d6f6a690d5f5f69736d62626b616c706861',
                            '075f69736b70756e0d5f5f69736d62626b70756e6374',
                            '075f69736b616e610b5f5f69736d62626b616e61',
                            '075f69736b6174610b5f5f69736d62626b616e61',
                            '095f6973616c6b616e610c5f5f69736d6262616c706861',
                            '095f6973706e6b616e610c5f5f69736d626270756e6374',
                            '0b5f6973616c6e6d6b616e610c5f5f69736d6262616c6e756d',
                            '095f697370726b616e610c5f5f69736d62627072696e74',
                            '095f697367726b616e610c5f5f69736d62626772617068',
                            '085f69736b616e6a690b5f5f69736d62626c656164',
                            '095f69736b616e6a69320c5f5f69736d6262747261696c',
                            '085f6a6973686972610b5f5f69736d626368697261',
                            '085f6a69736b616e610b5f5f69736d62636b617461',
                            '085f6a69736b6174610b5f5f69736d62636b617461',
                            '095f6a69736b69676f750d5f5f69736d626373796d626f6c',
                            '065f6a69736c30095f5f69736d62636c30',
                            '065f6a69736c31095f5f69736d62636c31',
                            '065f6a69736c32095f5f69736d62636c32',
                            '095f6a69737072696e740c5f5f69736d62637072696e74',
                            '095f6a6973746f6a6d730d5f5f6d62636a6973746f6a6d73',
                            '075f6a69737a656e0c5f5f69736d62636c6567616c',
                            '095f6a6d73746f6a69730d5f5f6d62636a6d73746f6a6973',
                            '085f6a737472616476095f5f6d62736e696e63',
                            '085f6a737472636872085f5f6d6273636872',
                            '085f6a737472636d70085f5f6d6273636d70',
                            '095f6a7374726373706e095f5f6d62736373706e',
                            '085f6a7374726c656e085f5f6d62736c656e',
                            '0a5f6a7374726d61746368095f5f6d62737062726b',
                            '095f6a7374726e636174095f5f6d62736e636174',
                            '095f6a7374726e636d70095f5f6d62736e636d70',
                            '095f6a7374726e637079095f5f6d62736e637079',
                            '095f6a7374726e736574095f5f6d62736e736574',
                            '095f6a73747272636872095f5f6d627372636872',
                            '085f6a737472726576085f5f6d6273726576',
                            '085f6a737472736574085f5f6d6273736574',
                            '095f6a737472736b6970095f5f6d627373706e70',
                            '085f6a73747273706e085f5f6d627373706e',
                            '085f6a737472737472085f5f6d6273737472',
                            '085f6a737472746f6b085f5f6d6273746f6b',
                            '085f6a746f686972610b5f5f6d6263746f68697261',
                            '085f6a746f6b616e610b5f5f6d6263746f6b617461',
                            '085f6a746f6b6174610b5f5f6d6263746f6b617461',
                            '055f6d746f620a5f5f6d62736e62636e74',
                            '095f7a656e746f68616e0a5f5f6d6263746f6d6262',
                            '075f5f6662746f6d0b5f5f666d62736e63636e74',
                            '0a5f5f666a7374726164760a5f5f666d62736e696e63',
                            '0a5f5f666a737472636872095f5f666d6273636872',
                            '0a5f5f666a737472636d70095f5f666d6273636d70',
                            '0b5f5f666a7374726373706e0a5f5f666d62736373706e',
                            '0a5f5f666a7374726c656e095f5f666d62736c656e',
                            '0c5f5f666a7374726d617463680a5f5f666d62737062726b',
                            '0b5f5f666a7374726e6361740a5f5f666d62736e636174',
                            '0b5f5f666a7374726e636d700a5f5f666d62736e636d70',
                            '0b5f5f666a7374726e6370790a5f5f666d62736e637079',
                            '0b5f5f666a7374726e7365740a5f5f666d62736e736574',
                            '0b5f5f666a737472726368720a5f5f666d627372636872',
                            '0a5f5f666a737472726576095f5f666d6273726576',
                            '0a5f5f666a737472736574095f5f666d6273736574',
                            '0b5f5f666a737472736b69700a5f5f666d627373706e70',
                            '0a5f5f666a73747273706e095f5f666d627373706e',
                            '0a5f5f666a737472737472095f5f666d6273737472',
                            '0a5f5f666a737472746f6b095f5f666d6273746f6b',
                            '075f5f666d746f620b5f5f666d62736e62636e74'],
          'modend_records': ['00']}}
TASM_FLAGS=['/m','/mx','/kh32768','/t']
INCLUDES=('src/mainl/crt/char_tables.inl','src/mainl/crt/locale_fields.inc')
SOURCE_PATHS={n:'src/mainl/crt/'+n+'.asm' for n in NATIVE}





def original_library_member(member):
    """Read the original CL.LIB member as OMF without rewriting its program.

    A valid empty THEADR is only a parser envelope: library members have no
    standalone THEADR and object_program_records deliberately excludes it.
    The original record sequence, including its non-semantic COMENTs, is
    borrowed unchanged from the pinned original library.
    """
    return b'\x80\x02\x00\x00\x7e' + member.program_records


def original_member_programs():
    """Use the pinned compiler library, distinct from the 28-source carrier baseline."""
    raw=(ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    members=library_members(raw)
    need(len(members)==893 and all(members[NATIVE[n]['index']].name==n for n in NATIVE),
         'original Japanese compiler library slot identities')
    return {n:original_library_member(members[NATIVE[n]['index']]) for n in NATIVE},sha(raw)


def original_fields(blob):
    return literal_fields(blob)


def named_fields(blob):
    imports=externs(blob);out=[]
    for field in literal_fields(blob):
        row=dict(field)
        if row['target_method']==2:row['target']=imports[row['target']-1]
        out.append(row)
    return out


def frame_differences(original,native):
    a=named_fields(original);b=named_fields(native)
    need(len(a)==len(b),'complete ordered raw field population')
    return [dict(original=f,native=g) for f,g in zip(a,b) if f!=g]


def fixed_fields(name,blob):
    fields=literal_fields(blob)
    need(len(fields)==NATIVE[name]['fields'],'complete literal field population '+name)
    keys=('segment','site','location_type','width','segment_relative',
          'frame_method','frame','target_method','target','addend')
    return [tuple(row[k] for k in keys) for row in fields]


def initialized_payload(blob):
    """Read actual LEDATA/LIDATA; never invent values for uninitialized extents."""
    result=payload(blob)
    for record in parse_omf(blob):
        if record.name!='LIDATA':continue
        data=record.data
        need(len(data)>=3 and data[0]<128,'bounded 16-bit iterated segment index')
        segment=data[0];offset=int.from_bytes(data[1:3],'little');cursor=3
        def block():
            nonlocal cursor
            need(cursor+4<=len(data),'complete original iterated block header')
            repeat,count=struct.unpack('<2H',data[cursor:cursor+4]);cursor+=4
            if count:value=b''.join(block() for _ in range(count))
            else:
                need(cursor<len(data),'iterated literal size present')
                size=data[cursor];cursor+=1
                need(cursor+size<=len(data),'complete iterated literal')
                value=data[cursor:cursor+size];cursor+=size
            need(len(value)*repeat<=65536,'16-bit native iterated initializer')
            return value*repeat
        value=b''
        while cursor<len(data):value+=block()
        need(offset+len(value)<=65536,'16-bit initialized segment extent')
        for i,v in enumerate(value):
            need((segment,offset+i) not in result,'disjoint native data records')
            result[segment,offset+i]=v
    return result


def scope(name,blob):
    q=NATIVE[name]
    need(describe_omf(blob)['valid'],'actual native OMF '+name)
    ss=segment_definitions(blob)
    need([(s['name'],s['class'],s['size']) for s in ss]==q['segments'] and
         [r.data[0] for r in parse_omf(blob) if r.name=='SEGDEF']==q['segment_attributes'],
         'complete original segment order, sizes, packing and alignment '+name)
    publics={str(s['index']):code_publics(blob,s['index']) for s in ss}
    need(publics==q['publics_by_segment'],'all original public offsets and segments '+name)
    need(externs(blob)==q['imports'],'complete original import identity/order '+name)
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==([q['group']] if q['group'] is not None else []),
         'original native group '+name)
    aliases=[r.data.hex() for r in parse_omf(blob) if r.name=='ALIAS']
    need(aliases==q['alias_records'] and
         [r.data.hex() for r in parse_omf(blob) if r.name=='MODEND']==q['modend_records'],
         'all original ordered alias definitions and module entry semantics '+name)
    p=initialized_payload(blob)
    all_sites={(s['index'],i) for s in ss for i in range(s['size'])}
    need(set(p)<=all_sites,'initialized records within their original segment extents')
    missing={str(s['index']):[i for i in range(s['size']) if (s['index'],i) not in p]
             for s in ss}
    need(missing==q['uninitialized_sites'],
         'exact initialized coverage and original uninitialized extents '+name)
    profiles=[];code=b'';data=b'';init=b'';bss=0
    for seg in ss:
        raw=bytes(p[seg['index'],i] for i in range(seg['size']) if (seg['index'],i) in p)
        profiles.append(dict(index=seg['index'],name=seg['name'],
             segment_class=seg['class'],extent=seg['size'],initialized_bytes=len(raw),
             initialized_sha256=sha(raw),uninitialized_sites=missing[str(seg['index'])]))
        if seg['class']=='CODE':
            need(len(raw)==seg['size'],'all CODE bytes have source instruction/table owners')
            code+=raw
        elif seg['class']=='DATA':data+=raw
        elif seg['class']=='INITDATA':init+=raw
        elif seg['class']=='BSS':
            need(not raw,'original BSS has no initialized bytes');bss+=seg['size']
    return dict(CODE_bytes=len(code),CODE_sha256=sha(code),
                DATA_bytes=len(data),DATA_sha256=sha(data),BSS_bytes=bss,
                INITDATA_initialized_bytes=len(init),INITDATA_sha256=sha(init),
                segment_profiles=profiles,segment_attributes=q['segment_attributes'],
                publics_by_segment=publics,imports=q['imports'],
                ordered_logical_relocation_fields=fixed_fields(name,blob),
                near_frame_sites=q['near_frame_sites'],
                ordered_alias_records=aliases,module_end_records=q['modend_records'])


def retained():
    """Revalidate unchanged 62→877 native source-bound evidence, then extend it.

    Reads actual parent OBJ/LIB/EXE/MAP rounds; never launches cold replay.
    """
    base,files,accepted,members,previous,parent_hash=parent.retained()
    mode='math-runtime-storage-twenty-one'
    raw=(ROOT/(parent.PREFIX+mode+'-build.json')).read_bytes()
    record=json.loads(raw)
    names=parent.MODES[mode]
    source_paths={n:parent.SOURCE_PATHS[n] for n in names}
    need(record['complete'] and not record['source_acceptance'] and
         not record['original_cold_rebuilt'] and
         record['added_accepted_bytes']==0 and
         record['parent_receipt_sha256']==parent_hash and
         record['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         record['accepted_library_sha256']==sha(accepted) and
         record['source_paths']==source_paths and
         record['source_sha256']=={n:sha((ROOT/path).read_bytes())
                                  for n,path in source_paths.items()} and
         record['assembler_flags']==parent.TASM_FLAGS and
         record['compatible_assembler_flags']==parent.ASSEMBLER_FLAGS and
         record['assembler_attestation']==parent.assembler_attestation() and
         record['source_include_sha256']=={p:sha((ROOT/p).read_bytes())
                                           for p in parent.INCLUDES} and
         tuple(record['names'])==names and record['mode']==mode and
         len(record['rounds'])==2,
         'native parent 877-source build bound to unchanged source')
    original_programs,compiler_hash=parent.original_member_programs()
    need(record['original_compiler_library_sha256']==compiler_hash,
         'original compiler library hash inherited independently of the carrier')
    expected={n:parent.scope(n,original_programs[n]) for n in names}
    need(record['original_profiles']==json.loads(json.dumps(expected)),
         'complete inherited original member scope')
    carry=[]
    vectors=[]
    for i,row in enumerate(record['rounds']):
        need(row['round']==i+1 and
             set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete round vector with all new native member programs')
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'original retained OBJ/LIB/EXE/MAP bytes '+kind)
            out[kind]=blob
        need(all(parent.scope(n,out[n])==expected[n] for n in names),
             'selected original inherited CODE/DATA/FIXUPP sites and targets')
        if any(parent.NATIVE[n].get('fpu_sites') or parent.NATIVE[n].get('near_frame_sites')
               for n in names):
            gaps={n:parent.frame_differences(original_programs[n],out[n]) for n in names}
            need(row['raw_frame_differences_by_member']==gaps,
                 'all inherited explicitly disclosed raw FP/near-call frame descriptions')
        src=dict(previous[i][0],**{n:out[n] for n in names})
        comparison=compare_members(members,library_members(out['lib']),src)
        need(comparison==row['library_comparison'] and len(src)==877 and
             comparison['contextual_members_unchanged']==16 and
             out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             '877 original-source members and complete Japanese link parity')
        carry.append((src,out['lib']))
        vectors.append(out)
    need(vectors[0]==vectors[1] and carry[0][0]==carry[1][0],
         'unchanged byte-identical two-round 877-source carrier')
    return base,files,accepted,members,carry,sha(raw)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,carry,parent_hash=retained()
    need(not set(names)&set(carry[0][0]), 'newly selected native CRT slots only')
    need(all(members[NATIVE[n]['index']].name==n for n in names),
         'correct original member indices')
    originals,original_library_hash=original_member_programs()
    # The standalone vendor programs agree with original CODE/ABI/fields;
    # retain the actual CL.LIB record as the authoritative ordered OMF.
    need(all(scope(n,(WORK/'vendor'/(n+'.obj')).read_bytes())==scope(n,originals[n])
             for n in names),
         'original Japanese locale/table/alias native member scope')
    expected={n:scope(n,originals[n]) for n in names}
    inputs={n:(ROOT/SOURCE_PATHS[n]).read_bytes() for n in names}
    source_includes={p:(ROOT/p).read_bytes() for p in INCLUDES}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    player=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    # A fresh stage preserves both complete native rounds for its source DAG.
    scratch=WORK/'probe/af533b'
    report=dict(complete=False,mode=mode,names=list(names),
                source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,parent_receipt_sha256=parent_hash,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                original_compiler_library_sha256=original_library_hash,
                source_sha256={n:sha(x) for n,x in inputs.items()},
                source_paths={n:SOURCE_PATHS[n] for n in names},
                source_include_sha256={p:sha(raw) for p,raw in source_includes.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                assembler_flags=TASM_FLAGS,original_profiles=expected,
                literal_OMF_FIXUPP_equal=False,phases=[],rounds=[])
    save=lambda:(ROOT/(PREFIX+mode+'-build.json')).write_text(json.dumps(report,indent=2)+'\n')
    def run(argv,cwd,label):
        cp=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        dest=f'.analysis/work/af533b-{mode}-{label}.log'
        (ROOT/dest).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,returncode=cp.returncode,
               command=argv,log_path=dest,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-2190:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not scratch.exists(), 'fresh incremental scoped native workdir')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(carry[0][1])
            (scratch/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(player+['tlib','@extract.rsp'],scratch,'extract')
            extracted={f.stem.lower():f for f in scratch.iterdir()
                       if f.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all 893 inherited native CRT member programs extracted')
            old=library_members(carry[0][1])
            for m in old:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'native inherited member intact '+m.name)
                dest=scratch/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            for n,b in inputs.items():
                (scratch/(n+'.asm')).write_bytes(b)
                os.utime(scratch/(n+'.asm'),(946744800,946744800))
            for p,raw in source_includes.items():
                (scratch/Path(p).name).write_bytes(raw)
                os.utime(scratch/Path(p).name,(946744800,946744800))
            response=build.response(r'probe\af533b\newcrt.lib /E',
                ['+probe\\af533b\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\af533b\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\af533b\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\af533b\\newcrt.lib')):
                need(link.count(old)==1,'native MAINL link response binding')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(response)
            (scratch/'link.lnk').write_bytes(link)
            for idx in (1,2):
                for name in [*(n+'.obj' for n in names),'newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map']:
                    (scratch/name).unlink(missing_ok=True)
                compiled={}
                literal_omf={}
                original_programs={}
                frame_gaps={}
                for n in names:
                    run(dos+TASM_FLAGS+[n+'.asm',n+'.obj'],scratch,
                        f'round{idx}-assemble-{n}')
                    obj=(scratch/(n+'.obj')).read_bytes()
                    need(scope(n,obj)==expected[n],
                         'all original CODE/DATA bytes, public interface, targets '+n)
                    literal_omf[n]=(literal_fields(obj)==original_fields(originals[n]))
                    need(literal_omf[n], 'every original literal ordered FIXUPP attribute '+n)
                    frame_gaps[n]=frame_differences(originals[n],obj)
                    need(len(frame_gaps[n])==len(NATIVE[n]['near_frame_sites']),
                         'zero raw field differences for all twelve DATA/metadata members')
                    original_programs[n]=(object_program_records(obj)==
                        object_program_records(originals[n]))
                    compiled[n]=obj
                all_sources=dict(carry[idx-1][0],**compiled)
                for n,b in carry[idx-1][0].items():
                    (scratch/(n+'.obj')).write_bytes(b)
                run(player+['tlib',r'@probe\af533b\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\af533b\link.lnk'],WORK,
                    f'round{idx}-link')
                if ((scratch/'linked.exe').read_bytes()!=
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() or
                     (scratch/'linked.map').read_bytes()!=
                     (WORK/'obj/th03/mainl.map').read_bytes()):
                    debug=WORK/'probe/after533-failed-native-link'
                    debug.mkdir(parents=True,exist_ok=True)
                    (debug/('round'+str(idx)+'.exe')).write_bytes(
                        (scratch/'linked.exe').read_bytes())
                    (debug/('round'+str(idx)+'.map')).write_bytes(
                        (scratch/'linked.map').read_bytes())
                    (debug/('round'+str(idx)+'.obj')).write_bytes(compiled[names[0]])
                    (debug/('round'+str(idx)+'.lib')).write_bytes(
                        (scratch/'newcrt.lib').read_bytes())
                need((scratch/'linked.exe').read_bytes()==
                       (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                       (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete decoded Japanese MAINL EXE/MAP raw identical')
                out={}
                for kind,file in [(n,n+'.obj') for n in names]+[
                        ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]:
                    blob=(scratch/file).read_bytes()
                    path=f'.analysis/work/af533b-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                    literal_omf_fixupp_equal_by_member=literal_omf,
                    raw_frame_differences_by_member=frame_gaps,
                    original_program_equal_by_member=original_programs,
                    library_comparison=comparison))
                save()
                print(f'after533 {mode}: {len(all_sources)} source CRT members, '
                      f'Japanese EXE/MAP exact round {idx}',flush=True)
            need(len(report['rounds'])==2 and
                 {n:q['sha256'] for n,q in report['rounds'][0]['outputs'].items()}==
                 {n:q['sha256'] for n,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical independent native output rounds')
        finally:
            # Keep all new stage material until an independent storage audit.
            save()
    need(inputs=={n:(ROOT/SOURCE_PATHS[n]).read_bytes() for n in names},
         'native locale/table/alias files unchanged during two producer rounds')
    need(source_includes=={p:(ROOT/p).read_bytes() for p in INCLUDES},
         'bounded includes unchanged during both native rounds')
    report['literal_OMF_FIXUPP_equal']=all(
        report['rounds'][0]['literal_omf_fixupp_equal_by_member'].values())
    report['complete']=True
    save()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(MODES))
    main(ap.parse_args().mode)
