#!/usr/bin/env python3
"""Two real TASM/TLINK rounds replacing MAINL input scanner alone.

The same natural instruction source used by source-native MAIN is included
through a locally maintained MAINL TU. Its last byte is TASM CODE EVEN,
not a manual C/C++ codestring. The historical after549 candidate and
all frozen cold/runtime/native ancestors remain untouched.
"""
import fcntl
import json
import os
import subprocess
import tomllib

import build_th03_mainl_sound_after558_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.targets import read_verified_artifact,find_artifact,load_target_manifest
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER='scripts/build_th03_mainl_input_after566_work.py'
CONFIG='config/mainl_work/input_after566.json'
PREFIX='.analysis/work/mainl-input-after566-native-'
REPORT=PREFIX+'build.json'
STAGE='af566m'
SCRATCH=WORK/('probe/'+STAGE)
TASM=ROOT/'.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE'

def inputs():
    cfg,cfg_sha=base.load(CONFIG)
    need(cfg['schema']=='th03-mainl-input-after566-v1' and
         cfg['parent_report']==parent.REPORT and
         cfg['maintained_TU']=='src/mainl/hardware/input_scan_exact.asm' and
         cfg['proved_common_scanner']=='src/main/hardware/input_scan.asm' and
         cfg['original_project_object']=='obj/th03/input_s.obj' and
         (cfg['function_instruction_bytes'],cfg['function_instructions'],
          cfg['native_CODE_even_bytes'],cfg['original_CODE_bytes'],
          cfg['literal_OMF_fixup_sites'],cfg['original_MZ_relocations'],
          cfg['whole_japanese_MAINL_EXE_bytes'])==(417,115,1,418,42,677,67372) and
         cfg['historic_original_assembler_identity_proved'] is False and
         cfg['canonical_credit_changed'] is False and
         cfg['whole_product_source_accepted'] is False,
         'complete bounded MAINL scanner owner and target identity')
    return cfg,cfg_sha

def source_snapshot(cfg):
    wrapper=(ROOT/cfg['maintained_TU']).read_bytes()
    shared=(ROOT/cfg['proved_common_scanner']).read_bytes()
    need(wrapper.isascii() and shared.isascii() and
         wrapper.count(b'include src/main/hardware/input_scan.asm')==1 and
         shared.count(b'    even\nSHARED ends')==1 and
         b'org ' not in shared.lower() and b'codestring' not in shared.lower() and
         b'    db ' not in shared.lower(),
         'true source-ordered 8086, real compiler EVEN, bounded maintained TU')
    generated=wrapper.replace(b'include src/main/hardware/input_scan.asm',
                              f'include probe/{STAGE}/scan_body.asm'.encode())
    return wrapper,shared,generated.replace(b'\n',b'\r\n'),shared.replace(b'\n',b'\r\n')

def response(number):
    raw=parent.response(number)
    need(raw.count(b'af558s')==14,'actual after558 source C0/CRT/data/vector/sound parent')
    for old,new in [(rb'obj\th03\input_s.obj',f'probe\\{STAGE}\\r{number}.obj'.encode()),
                    (f'probe\\af558s\\r{number}.exe'.encode(),f'probe\\{STAGE}\\r{number}.exe'.encode()),
                    (f'probe\\af558s\\r{number}.map'.encode(),f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(raw.count(old)==1,'one original input source or whole EXE/MAP destination')
        raw=raw.replace(old,new)
    return raw

def normalize_map(raw):
    path=f'M=probe\\{STAGE}\\input_s.asm'.encode()
    need(raw.count(path)==3,'CODE/DATA/BSS native MAINL input source contribution')
    return raw.replace(path,b'M=th03/input_s.cpp')

def field_multiset(raw):
    return sorted(json.dumps(f,sort_keys=True) for f in literal_fields(raw))

def verify_object(native,orig):
    a,b=payload(orig),payload(native)
    need(a==b and len(a)==418 and a[1,417]==0x90 and
         len(literal_fields(orig))==len(literal_fields(native))==42 and
         field_multiset(orig)==field_multiset(native) and
         public_offsets(orig)==public_offsets(native) and
         segment_definitions(orig)==segment_definitions(native),
         'entire 418 original MAINL CODE bytes, symbols, 42 fields and section layout')
    instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(
        bytes(b[1,i] for i in range(417)),0))
    need(len(instructions)==115 and sum(i.size for i in instructions)==417 and
         instructions[-1].address==416 and instructions[-1].mnemonic=='retf',
         'complete held-key scanner and separate TASM-aligned NOP')
    return dict(complete_original_CODE_bytes=418,complete_instruction_bytes=417,
        true_even_alignment_bytes=1,instructions=115,original_literal_fixup_sites=42,
        original_OMF_FIXUPP_order_equal=(literal_fields(orig)==literal_fields(native)),
        original_PUBLIC_definitions=public_offsets(orig))

def main():
    cfg,cfg_sha=inputs()
    before,parent_sha=base.load(parent.REPORT)
    need(before['complete'] and parent_sha==cfg['parent_report_sha256'],
         'actual independent source-native after558 parent, not full cold replay')
    wrapper,scanner,native_wrapper,native_scanner=source_snapshot(cfg)
    original=(WORK/cfg['original_project_object']).read_bytes()
    stored=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl'))
    target=(WORK/'bin/th03/mainl.target.exe').read_bytes()
    decoded,=[a for a in tomllib.loads((ROOT/'config/th03_diet.toml').read_text())['artifacts']
              if a['id']=='th03-mainl']
    target_image=parse_mz(target)
    need(decoded['decoded_size']==len(target)==67372 and
         decoded['decoded_sha256']==sha(target) and
         len(stored)==37975 and len(target_image.relocations)==677 and
         before['rounds'][0]['outputs']['exe']['sha256']==sha(target),
         'actual Japanese DIET-stored and SHA-bound decoded original MAINL target')
    need(sha(TASM.read_bytes())==
         'ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'pinned original native Borland TASM5 assembler')
    report=dict(complete=False,original_obj_source_accepted=False,whole_product_source_accepted=False,
        canonical_credit_changed=False,cold_rebuilt=False,library_rebuilt=False,
        game_objects_recompiled_per_round=1,other_project_objects_reused=35,
        native_CODE_bytes=418,natural_8086_instruction_bytes=417,native_even_bytes=1,
        input_TU_sha256=sha(wrapper),shared_scanner_sha256=sha(scanner),
        staged_TU_sha256=sha(native_wrapper),staged_scanner_sha256=sha(native_scanner),
        original_input_obj_sha256=sha(original),japanese_decoded_target_sha256=sha(target),
        japanese_DIET_stored_target_sha256=sha(stored),
        config_sha256=cfg_sha,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        parent_report_sha256=parent_sha,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
         WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    assembler=['/usr/bin/wine-stable',str(TASM)]
    def run(cmd,label):
        p=subprocess.run(cmd,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=100)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=cmd,log=log,
            log_sha256=sha(p.stdout),returncode=p.returncode))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh preserved MAINL scanner stage')
        SCRATCH.mkdir()
        for n,raw in [('input_s.asm',native_wrapper),('scan_body.asm',native_scanner),
                      ('maintained_TU.asm',wrapper),
                      ('driver.py',(ROOT/DRIVER).read_bytes()),
                      ('config.json',(ROOT/CONFIG).read_bytes())]:
            (SCRATCH/n).write_bytes(raw)
        os.utime(SCRATCH/'input_s.asm',(946684800,946684800))
        os.utime(SCRATCH/'scan_body.asm',(946684800,946684800))
        vectors=[]
        for number in (1,2):
            prev=before['rounds'][number-1]
            run(assembler+['/m','/mx','/kh32768','/t','/dGAME=3',
                f'probe\\{STAGE}\\input_s.asm,probe\\{STAGE}\\r{number}.obj'],
                f'round{number}-assemble')
            obj=(SCRATCH/f'r{number}.obj').read_bytes()
            scope=verify_object(obj,original)
            rsp=response(number)
            (SCRATCH/f'r{number}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.lnk'],
                f'round{number}-link')
            exe=(SCRATCH/f'r{number}.exe').read_bytes()
            mp=(SCRATCH/f'r{number}.map').read_bytes()
            need(exe==target==base.checked(prev['outputs']['exe']) and
                 parse_mz(exe).relocations==target_image.relocations and
                 normalize_map(mp)==base.checked(prev['outputs']['map']),
                 'entire 67372-byte original MAINL native EXE, all677 fields and MAP')
            v=dict(obj=obj,exe=exe,map=mp)
            output={}
            for key,raw in v.items():
                path=PREFIX+f'round{number}-{key}.bin'
                (ROOT/path).write_bytes(raw)
                output[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            report['rounds'].append(dict(round=number,outputs=output,
                response_sha256=sha(rsp),original_418_CODE_scope=scope,
                raw_japanese_MAINL_EXE_exact=True,ordered_677_relocations_equal=True,
                parent_unchanged_source_round=number))
            save()
            vectors.append(v)
            print('MAINL input round',number,'complete 417 instruction + natural EVEN and original 67372 EXE/677 relocations',flush=True)
        need(vectors[0]==vectors[1] and
             (ROOT/cfg['maintained_TU']).read_bytes()==wrapper and
             (ROOT/cfg['proved_common_scanner']).read_bytes()==scanner,
             'two raw OBJ/EXE/MAP native vectors and maintained sources repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
