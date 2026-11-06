#!/usr/bin/env python3
"""Assemble complete MAIN held-key scan with natural EVEN; scoped native links only.

No target-byte arrays, codestring, object patches or full cold replay.
Original Turbo C++ emits the 417-byte function, then linker supplies a 00
alignment gap. Native TASM EVEN after the complete symbolic 417-byte function
instead generates the Japanese target's NOP at the same CODE address.
"""
import fcntl
import json
import os
import subprocess

import build_th03_main_eight_boss_after561_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER='scripts/build_th03_main_input_after565_work.py'
CONFIG='config/main_work/input_scan_after565.json'
PREFIX='.analysis/work/main-input-after565-native-'
REPORT=PREFIX+'build.json'
STAGE='af565s'
SCRATCH=WORK/('probe/'+STAGE)
TASM=ROOT/'.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE'

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    need(cfg['schema']=='th03-main-input-scan-after565-v1' and
         cfg['parent_report']==parent.REPORT and
         cfg['source']=='src/main/hardware/input_scan.asm' and
         cfg['original_cold_object']=='obj/th03/input_s.obj' and
         (cfg['instruction_bytes'],cfg['instruction_count'],cfg['original_CODE_allocation'],
          cfg['native_even_CODE_allocation'],cfg['natural_code_even_bytes'],
          cfg['literal_OMF_fields'],cfg['retf_instruction_start'],cfg['decoded_main_alignment_site'],
          cfg['ordered_main_MZ_relocations'])==(417,115,417,418,1,42,416,60461,1553) and
         cfg['full_original_MZ_file_accepted'] is False and
         cfg['whole_source_game_accepted'] is False and
         cfg['canonical_credit_changed'] is False,
         'complete MAIN keyboard/word-alignment source, no fabricated whole-file acceptance')
    return cfg,sha((ROOT/CONFIG).read_bytes())

def transported(source):
    need(source.isascii() and b'\r' not in source and
         b'    even\nSHARED ends' in source and
         b'    retf' in source and b'org ' not in source.lower() and
         b'codestring' not in source.lower() and b'    db ' not in source.lower(),
         'linear symbolic 8086 input function, assembler-generated EVEN')
    return source.replace(b'\n',b'\r\n')

def response(number):
    rsp=(WORK/'obj/th03/main.@l').read_bytes()
    cfg,_=inputs()
    parent_cfg,_=parent.inputs()
    need(sha(rsp)==parent_cfg['normal_link_response_sha256'],
         'unchanged native MAIN first-use response/99-object order')
    for old,new in [(rb'obj\th03\input_s.obj',f'probe\\{STAGE}\\r{number}.obj'.encode()),
                    (rb'bin\th03\main.exe',f'probe\\{STAGE}\\r{number}.exe'.encode()),
                    (rb'obj\th03\main.map',f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(rsp.count(old)==1,'replace exactly one genuine native input/out '+str(old))
        rsp=rsp.replace(old,new)
    return rsp

def map_normalized(raw):
    name=f'M=probe\\{STAGE}\\input_s.asm'.encode()
    need(raw.count(name)==3,'all three native root CODE/DATA/BSS contributions')
    raw=raw.replace(name,b'M=th03/input_s.cpp')
    # The assembler owns the previously unowned single CODE alignment byte.
    old=b'0E8F:019C 01A2 C=CODE   S=SHARED         G=(none)  M=th03/input_s.cpp ACBP=48'
    new=b'0E8F:019C 01A1 C=CODE   S=SHARED         G=(none)  M=th03/input_s.cpp ACBP=48'
    need(raw.count(old)==1,'one one-byte source CODE-extent MAP addition')
    return raw.replace(old,new)

def field_multiset(raw):
    return sorted(json.dumps(x,sort_keys=True) for x in literal_fields(raw))

def verify_object(native,original,cfg):
    old=payload(original); fresh=payload(native)
    # Explicitly compare actual object rather than making a synthetic target.
    need(len(old)==417 and len(fresh)==418 and
         all(old[1,i]==fresh[1,i] for i in range(417)) and
         fresh[1,417]==0x90 and
         len(literal_fields(native))==len(literal_fields(original))==42 and
         field_multiset(original)==field_multiset(native) and
         public_offsets(original)==public_offsets(native),
         'complete 417-byte original instructions, native EVEN and all OMF field sites')
    original_segments=segment_definitions(original)
    candidate_segments=segment_definitions(native)
    need(candidate_segments==[
        dict(row,size=(418 if row['index']==1 else row['size'])) for row in original_segments],
        'original three OMF segments with just one natural CODE alignment byte')
    machine=bytes(fresh[1,i] for i in range(417))
    disasm=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(machine,0))
    need(len(disasm)==115 and sum(i.size for i in disasm)==417 and
         disasm[-1].address==416 and disasm[-1].mnemonic=='retf',
         'all 115 complete input-scan instructions and original RETF boundary')
    return dict(complete_function_instructions=115,complete_instruction_bytes=417,
        native_CODE_alignment_bytes=1,object_CODE_bytes=418,
        original_literal_field_sites=42,
        native_FIXUPP_order_matches_original=(literal_fields(original)==literal_fields(native)),
        source_public_entries=public_offsets(native))

def main():
    cfg,cfg_hash=inputs()
    prev,prev_hash=parent.inputs(),sha((ROOT/parent.REPORT).read_bytes())
    need(json.loads((ROOT/parent.REPORT).read_text())['complete'] and
         prev_hash==cfg['parent_report_sha256'],
         'actual selected after561 complete eight-boss source-native parent')
    original=(WORK/cfg['original_cold_object']).read_bytes()
    native_exe,native_map,target,reference=parent.native_parents(prev[0])
    target_mz=parse_mz(target)
    source=(ROOT/cfg['source']).read_bytes()
    native_source=transported(source)
    need(sha(TASM.read_bytes())=='ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'original installed Borland TASM 5.0')
    report=dict(complete=False,canonical_credit_changed=False,cold_rebuilt=False,
        existing_GAME_objects_reused=98,game_objects_recompiled_per_round=1,
        original_99_object_link_order=True,original_MZ_header_exact=False,
        original_FULL_japanese_FILE_accepted=False,
        correct_main_instruction_bytes=417,natural_assembler_even_bytes=1,
        source_sha256=sha(source),transported_source_sha256=sha(native_source),
        config_sha256=cfg_hash,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        parent_report_sha256=prev_hash,original_input_OBJ_sha256=sha(original),
        original_native_main_EXE_sha256=sha(native_exe),
        original_native_main_MAP_sha256=sha(native_map),
        pinned_japanese_MAIN_sha256=sha(target),
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    asm=['/usr/bin/wine-stable',str(TASM)]
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=p.returncode,
            log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'new preserved scoped input source stage')
        SCRATCH.mkdir()
        (SCRATCH/'input_s.asm').write_bytes(native_source)
        os.utime(SCRATCH/'input_s.asm',(946684800,946684800))
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for number in (1,2):
            run(asm+['/m','/mx','/kh32768','/t','/dGAME=3',
                f'probe\\{STAGE}\\input_s.asm,probe\\{STAGE}\\r{number}.obj'],
                f'round{number}-natural-TASM')
            obj=(SCRATCH/f'r{number}.obj').read_bytes()
            scope=verify_object(obj,original,cfg)
            rsp=response(number)
            (SCRATCH/f'r{number}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.@l'],
                f'round{number}-normal-TLINK')
            exe=(SCRATCH/f'r{number}.exe').read_bytes()
            m=(SCRATCH/f'r{number}.map').read_bytes()
            parsed=parse_mz(exe)
            need(parsed.program_image==target_mz.program_image and
                 parsed.relocations==target_mz.relocations and
                 len(parsed.relocations)==1553,
                 'all 124642 original Japanese MAIN load-image bytes and ordered 1553 MZ fields')
            need(len(exe)==132322 and len(target)==130882 and
                 exe!=target and
                 map_normalized(m)==native_map and
                 [i for i,(a,b) in enumerate(zip(parse_mz(native_exe).program_image,
                                                 parsed.program_image)) if a!=b]==[0xEC2D],
                 'only original input alignment site changes; external header difference remains')
            v=dict(obj=obj,exe=exe,map=m)
            outputs={}
            for key,raw in v.items():
                file=PREFIX+f'round{number}-{key}.bin'
                (ROOT/file).write_bytes(raw)
                outputs[key]=dict(path=file,bytes=len(raw),sha256=sha(raw))
            report['rounds'].append(dict(round=number,outputs=outputs,
                native_response_sha256=sha(rsp),object_scope=scope,
                full_original_japanese_program_image_equal=True,
                all_original_1553_ordered_MZ_fields_equal=True,
                full_original_japanese_EXE_file_equal=False))
            save()
            vectors.append(v)
            print('MAIN input round',number,'417 original 8086 instructions + native EVEN, all 124642 target load bytes/1553 MZ fields exact',flush=True)
        need(vectors[0]==vectors[1] and (ROOT/cfg['source']).read_bytes()==source,
             'both entire native OBJ/EXE/MAP vectors/source repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
