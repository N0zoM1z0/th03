#!/usr/bin/env python3
"""Fourteen native stream members: float/BCD, manipulators, assignment and seek.

Full CODE/DATA, ordered logical fields, and explicitly bounded OMF frame gaps.
"""
import argparse,fcntl,json,os,shutil,subprocess,tomllib,sys
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
from pathlib import Path

import build_th03_mainl_after525_work as parent
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
DRIVER='scripts/build_th03_mainl_after526_work.py'
PREFIX='.analysis/work/mainl-after526-'
MODES={'streams-float-bcd-manip-seek-fourteen':('bcd2', 'istskoff', 'istskpos', 'mnrstflg', 'mnsetflg', 'mnsetw', 'mnsfill', 'mnsprec', 'ostasn1', 'ostfloat', 'ostasn2', 'ostosfx', 'ostskoff', 'ostskpos')}
NATIVE={'bcd2': {'index': 196,
          'segments': [('_TEXT', 'CODE', 151), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
          'segment_attributes': [40, 72, 72],
          'publics_by_segment': {'1': [(0, '@$BLSH$QM7OSTREAMM3BCD'),
                                       (58, '@$BRSH$QM7ISTREAMM3BCD')],
                                 '2': [],
                                 '3': []},
          'imports': ['@istream@$brsh$qmg',
                      '@ostream@$blsh$qg',
                      '__BCD_TOBINARY',
                      '__BCD_TODECIMAL',
                      'FIDRQQ',
                      'FIWRQQ',
                      'N_SCOPY@',
                      '__turboFloat'],
          'fields': 12,
          'fpu_sites': [115, 106, 99, 95, 91, 34, 30],
          'near_frame_sites': [135],
          'code_segment': 1,
          'group': '08ff02ff03'},
 'istskoff': {'index': 785,
              'segments': [('_TEXTA', 'CODE', 108), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(0, '@istream@seekg$ql12ios@seek_dir')],
                                     '2': [],
                                     '3': []},
              'imports': ['@ios@setstate$qi'],
              'fields': 1,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'},
 'istskpos': {'index': 786,
              'segments': [('_TEXTA', 'CODE', 105), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(0, '@istream@seekg$ql')], '2': [], '3': []},
              'imports': ['@ios@setstate$qi'],
              'fields': 1,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'},
 'mnrstflg': {'index': 789,
              'segments': [('_TEXTA', 'CODE', 143), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(35, '@resetiosflags$ql')], '2': [], '3': []},
              'imports': ['@$bnew$qui', '@ios@unsetf$ql'],
              'fields': 4,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'},
 'mnsetflg': {'index': 791,
              'segments': [('_TEXTA', 'CODE', 143), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(35, '@setiosflags$ql')], '2': [], '3': []},
              'imports': ['@$bnew$qui', '@ios@setf$ql'],
              'fields': 4,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'},
 'mnsetw': {'index': 792,
            'segments': [('_TEXTA', 'CODE', 139), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
            'segment_attributes': [40, 72, 72],
            'publics_by_segment': {'1': [(44, '@setw$qi')], '2': [], '3': []},
            'imports': ['@$bnew$qui'],
            'fields': 3,
            'fpu_sites': [],
            'near_frame_sites': [],
            'code_segment': 1,
            'group': '08ff02ff03'},
 'mnsfill': {'index': 793,
             'segments': [('_TEXTA', 'CODE', 140), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [(45, '@setfill$qi')], '2': [], '3': []},
             'imports': ['@$bnew$qui'],
             'fields': 3,
             'fpu_sites': [],
             'near_frame_sites': [],
             'code_segment': 1,
             'group': '08ff02ff03'},
 'mnsprec': {'index': 794,
             'segments': [('_TEXTA', 'CODE', 139), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [(44, '@setprecision$qi')], '2': [], '3': []},
             'imports': ['@$bnew$qui'],
             'fields': 3,
             'fpu_sites': [],
             'near_frame_sites': [],
             'code_segment': 1,
             'group': '08ff02ff03'},
 'ostasn1': {'index': 803,
             'segments': [('_TEXTA', 'CODE', 44), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [(0, '@ostream_withassign@$basg$qm7ostream')],
                                    '2': [],
                                    '3': []},
             'imports': ['@ios@init$qn9streambuf'],
             'fields': 1,
             'fpu_sites': [],
             'near_frame_sites': [],
             'code_segment': 1,
             'group': '08ff02ff03'},
 'ostfloat': {'index': 804,
              'segments': [('_TEXTA', 'CODE', 0),
                           ('_DATA', 'DATA', 2),
                           ('_BSS', 'BSS', 0),
                           ('_TEXT', 'CODE', 165)],
              'segment_attributes': [40, 72, 72, 40],
              'publics_by_segment': {'1': [], '2': [], '3': [], '4': [(0, '@ostream@$blsh$qg')]},
              'imports': ['@ostream@outstr$qnxct1',
                          '__REALCVT',
                          'FIDRQQ',
                          'FIWRQQ',
                          '__turboFloat'],
              'fields': 8,
              'fpu_sites': [68, 64, 61, 58, 54],
              'near_frame_sites': [126],
              'code_segment': 4,
              'group': '0aff02ff03'},
 'ostasn2': {'index': 805,
             'segments': [('_TEXTA', 'CODE', 36), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [(0, '@ostream_withassign@$basg$qn9streambuf')],
                                    '2': [],
                                    '3': []},
             'imports': ['@ios@init$qn9streambuf'],
             'fields': 1,
             'fpu_sites': [],
             'near_frame_sites': [],
             'code_segment': 1,
             'group': '08ff02ff03'},
 'ostosfx': {'index': 817,
             'segments': [('_TEXTA', 'CODE', 78), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
             'segment_attributes': [40, 72, 72],
             'publics_by_segment': {'1': [(0, '@ostream@do_osfx$qv')], '2': [], '3': []},
             'imports': ['@ostream@flush$qv', '_cout', '_clog'],
             'fields': 5,
             'fpu_sites': [],
             'near_frame_sites': [],
             'code_segment': 1,
             'group': '08ff02ff03'},
 'ostskoff': {'index': 820,
              'segments': [('_TEXTA', 'CODE', 108), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(0, '@ostream@seekp$ql12ios@seek_dir')],
                                     '2': [],
                                     '3': []},
              'imports': ['@ios@setstate$qi'],
              'fields': 1,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'},
 'ostskpos': {'index': 821,
              'segments': [('_TEXTA', 'CODE', 105), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
              'segment_attributes': [40, 72, 72],
              'publics_by_segment': {'1': [(0, '@ostream@seekp$ql')], '2': [], '3': []},
              'imports': ['@ios@setstate$qi'],
              'fields': 1,
              'fpu_sites': [],
              'near_frame_sites': [],
              'code_segment': 1,
              'group': '08ff02ff03'}}
TASM_FLAGS=['/m','/mx','/kh32768','/t']
INCLUDES=('src/mainl/crt/stream_seek_offset_body.inl',
          'src/mainl/crt/stream_seek_position_body.inl',
          'src/mainl/crt/stream_flag_manip_body.inl',
          'src/mainl/crt/stream_word_manip_body.inl')



def original_library_member(member):
    """Read the original CL.LIB member as OMF without rewriting its program.

    A valid empty THEADR is only a parser envelope: library members have no
    standalone THEADR and object_program_records deliberately excludes it.
    The original record sequence, including its non-semantic COMENTs, is
    borrowed unchanged from the pinned original library.
    """
    return b'\x80\x02\x00\x00\x7e' + member.program_records


FPU={'FIDRQQ','FIWRQQ'}
NEAR={'ostfloat':'__REALCVT','bcd2':'N_SCOPY@'}


def original_fields(blob):
    try:
        return literal_fields(blob)
    except ValueError:
        return original_literal_fixups(blob)


def named_fields(blob):
    imports=externs(blob)
    result=[]
    for field in original_fields(blob):
        row=dict(field)
        if row['target_method']==2:
            row['target']=imports[row['target']-1]
        result.append(row)
    return result


def frame_differences(original,native):
    a=named_fields(original);b=named_fields(native)
    need(len(a)==len(b),'complete ordered raw field population')
    return [dict(original=f,native=g) for f,g in zip(a,b) if f!=g]


def fixed_fields(name,blob):
    q=NATIVE[name]
    fields=named_fields(blob)
    need(len(fields)==q['fields'],'complete native symbolic field population '+name)
    fpu=[];near=[];result=[]
    keys=('segment','site','location_type','width','segment_relative',
          'frame_method','frame','target_method','target','addend')
    for f in fields:
        row=dict(f)
        if row['target_method']==2 and row['target'] in FPU:
            need(row['segment']==q['code_segment'] and row['location_type']==1
                 and row['width']==2 and row['segment_relative'] and
                 (row['frame_method'],row['frame']) in ((4,None),(5,None)),
                 'only original x87 frame-4 / TASM frame-5 sites allowed')
            fpu.append(row['site']);row['frame_method']=99
        elif name in NEAR and row['target_method']==2 and row['target']==NEAR[name]:
            need(row['segment']==q['code_segment'] and row['location_type']==1
                 and row['width']==2 and not row['segment_relative'] and
                 row['addend']==0 and (row['frame_method'],row['frame']) in
                 ((5,None),(0,q['code_segment'])),
                 'only pinned original TARGET / TASM same-CODE near-call frame')
            near.append(row['site']);row['frame_method']=98;row['frame']=None
        result.append(tuple(row[k] for k in keys))
    need(fpu==q['fpu_sites'] and near==q['near_frame_sites'],
         'all and only the twelve x87 and two near-call exceptions, in original order')
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
    imports=externs(blob)
    need(imports==q['imports'] or (bool(q['fpu_sites']) and
         imports==q['imports']+['FIWRQQ','FIDRQQ']),
         'original import order and only two native EMUL duplicate declarations '+name)
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==[q['group']],
         'original native group '+name)
    p=payload(blob)
    expected={(s['index'],i) for s in ss if s['class']!='BSS'
              for i in range(s['size'])}
    need(set(p)==expected,'complete CODE/DATA coverage without holes or padding '+name)
    profiles=[];code=b'';data=b''
    for seg in ss:
        raw=bytes(p[seg['index'],i] for i in range(seg['size']))
        profiles.append(dict(index=seg['index'],name=seg['name'],
             segment_class=seg['class'],bytes=len(raw),sha256=sha(raw)))
        if seg['class']=='CODE':code+=raw
        elif seg['class']=='DATA':data+=raw
    return dict(CODE_bytes=len(code),CODE_sha256=sha(code),
                DATA_bytes=len(data),DATA_sha256=sha(data),BSS_bytes=0,
                segment_profiles=profiles,segment_attributes=q['segment_attributes'],
                publics_by_segment=publics,imports=q['imports'],
                ordered_logical_relocation_fields=fixed_fields(name,blob),
                x87_frame_sites=q['fpu_sites'],near_frame_sites=q['near_frame_sites'])


def retained():
    """Revalidate unchanged 62→752 native source-bound evidence, then extend it.

    Reads actual parent OBJ/LIB/EXE/MAP rounds; never launches cold replay.
    """
    base,files,accepted,members,previous,parent_hash=parent.retained()
    mode='string-find-resize-status-ten'
    raw=(ROOT/(parent.PREFIX+mode+'-build.json')).read_bytes()
    record=json.loads(raw)
    names=parent.MODES[mode]
    source_paths={n:'src/mainl/crt/'+n+'.asm' for n in names}
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
         record['source_include_sha256']=={p:sha((ROOT/p).read_bytes())
                                           for p in parent.INCLUDES} and
         tuple(record['names'])==names and record['mode']==mode and
         len(record['rounds'])==2,
         'native parent 752-source build bound to unchanged source')
    expected={n:parent.scope(n,parent.original_library_member(
        members[parent.NATIVE[n]['index']])) for n in names}
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
        src=dict(previous[i][0],**{n:out[n] for n in names})
        comparison=compare_members(members,library_members(out['lib']),src)
        need(comparison==row['library_comparison'] and len(src)==752 and
             comparison['contextual_members_unchanged']==141 and
             out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             '752 original-source members and complete Japanese link parity')
        carry.append((src,out['lib']))
        vectors.append(out)
    need(vectors[0]==vectors[1] and carry[0][0]==carry[1][0],
         'unchanged byte-identical two-round 752-source carrier')
    return base,files,accepted,members,carry,sha(raw)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,carry,parent_hash=retained()
    need(not set(names)&set(carry[0][0]), 'newly selected native CRT slots only')
    need(all(members[NATIVE[n]['index']].name==n for n in names),
         'correct original member indices')
    originals={n:original_library_member(members[NATIVE[n]['index']]) for n in names}
    need(all(object_program_records(originals[n])==
             members[NATIVE[n]['index']].program_records for n in names),
         'original Japanese library program records, not alternate OBJ')
    # The standalone vendor programs agree with original CODE/ABI/fields;
    # retain the actual CL.LIB record as the authoritative ordered OMF.
    need(all(scope(n,(WORK/'vendor'/(n+'.obj')).read_bytes())==scope(n,originals[n])
             for n in names),
         'original Japanese dual-CODE string members and native logical fields')
    expected={n:scope(n,originals[n]) for n in names}
    inputs={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names}
    include_bytes=(ROOT/'src/mainl/crt/stdio_layout.inc').read_bytes()
    source_includes={p:(ROOT/p).read_bytes() for p in INCLUDES}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    player=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    scratch=WORK/'probe/after526'
    report=dict(complete=False,mode=mode,names=list(names),
                source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,parent_receipt_sha256=parent_hash,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                source_sha256={n:sha(x) for n,x in inputs.items()},
                source_paths={n:'src/mainl/crt/'+n+'.asm' for n in names},
                stdio_layout_sha256=sha(include_bytes),
                source_include_sha256={p:sha(raw) for p,raw in source_includes.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                assembler_flags=TASM_FLAGS,original_profiles=expected,
                literal_OMF_FIXUPP_equal=False,phases=[],rounds=[])
    save=lambda:(ROOT/(PREFIX+mode+'-build.json')).write_text(json.dumps(report,indent=2)+'\n')
    def run(argv,cwd,label):
        cp=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        dest=f'.analysis/work/after526-{mode}-{label}.log'
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
            (scratch/'stdio_layout.inc').write_bytes(include_bytes)
            for p,raw in source_includes.items():
                (scratch/Path(p).name).write_bytes(raw)
                os.utime(scratch/Path(p).name,(946744800,946744800))
            response=build.response(r'probe\after526\newcrt.lib /E',
                ['+probe\\after526\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\after526\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\after526\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\after526\\newcrt.lib')):
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
                    need(literal_omf[n]==(not bool(NATIVE[n]['fpu_sites'])),
                         'actual original literal FIXUPP status with only disclosed FP members '+n)
                    frame_gaps[n]=frame_differences(originals[n],obj)
                    need(len(frame_gaps[n])==len(NATIVE[n]['fpu_sites'])+len(NATIVE[n]['near_frame_sites']),
                         'precisely fourteen disclosed field-frame differences across selected members')
                    original_programs[n]=(object_program_records(obj)==
                        members[NATIVE[n]['index']].program_records)
                    compiled[n]=obj
                all_sources=dict(carry[idx-1][0],**compiled)
                for n,b in carry[idx-1][0].items():
                    (scratch/(n+'.obj')).write_bytes(b)
                run(player+['tlib',r'@probe\after526\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\after526\link.lnk'],WORK,
                    f'round{idx}-link')
                if ((scratch/'linked.exe').read_bytes()!=
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() or
                     (scratch/'linked.map').read_bytes()!=
                     (WORK/'obj/th03/mainl.map').read_bytes()):
                    debug=WORK/'probe/after526-failed-native-link'
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
                    path=f'.analysis/work/after526-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                    literal_omf_fixupp_equal_by_member=literal_omf,
                    raw_frame_differences_by_member=frame_gaps,
                    original_program_equal_by_member=original_programs,
                    library_comparison=comparison))
                save()
                print(f'after526 {mode}: {len(all_sources)} source CRT members, '
                      f'Japanese EXE/MAP exact round {idx}',flush=True)
            need(len(report['rounds'])==2 and
                 {n:q['sha256'] for n,q in report['rounds'][0]['outputs'].items()}==
                 {n:q['sha256'] for n,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical independent native output rounds')
        finally:
            # Keep all new stage material until an independent storage audit.
            save()
    need(inputs=={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names},
         'native string source files unchanged during two producer rounds')
    need(include_bytes==(ROOT/'src/mainl/crt/stdio_layout.inc').read_bytes(),
         'maintained include stable during native source rounds')
    need(source_includes=={p:(ROOT/p).read_bytes() for p in INCLUDES},
         'bounded string includes unchanged during both native rounds')
    report['literal_OMF_FIXUPP_equal']=all(
        report['rounds'][0]['literal_omf_fixupp_equal_by_member'].values())
    report['complete']=True
    save()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(MODES))
    main(ap.parse_args().mode)
