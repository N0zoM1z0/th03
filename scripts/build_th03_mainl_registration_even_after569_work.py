#!/usr/bin/env python3
"""Recover MAINL registration DATA's original extra word alignment via TASM EVEN.

Historical after554 DATA303 source is preserved as-is. This separate natural
variant adds an assembler directive, not a copied target zero or padded object.
Two independently recompiled native DATA objects replace only regpre in the
actual after566 MAINL normal link. All old C0/CRT and 35 peers remain reused.
"""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_mainl_input_after566_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.omf import parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER='scripts/build_th03_mainl_registration_even_after569_work.py'
CONFIG='config/mainl_work/registration_even_after569.json'
PREFIX='.analysis/work/mainl-register-even-after569-native-'
REPORT=PREFIX+'build.json'
STAGE='af569r'
SCRATCH=WORK/('probe/'+STAGE)
TASM=parent.TASM

def inputs():
    cfg,cfg_sha=base.load(CONFIG)
    need(cfg['schema']=='th03-mainl-registration-even-after569-v1' and
         cfg['parent_report']==parent.REPORT and
         cfg['previous_pinned_source']=='src/mainl/data/registration.asm' and
         cfg['aligned_source']=='src/mainl/data/registration_even.asm' and
         cfg['maintained_codes']=='src/mainl/hiscore/regi_codes.inc' and
         cfg['original_context_object']=='obj/th03/regpre.obj' and
         (cfg['initialized_native_DATA_bytes'],cfg['semantic_DATA_bytes'],
          cfg['TASM_even_initialized_align_byte'],cfg['original_ordered_fixups'],
          cfg['original_PUBLIC_definitions'],cfg['decoded_japanese_MAINL_EXE_bytes'],
          cfg['ordered_MZ_relocations'])==(304,303,1,2,35,67372,677) and
         cfg['whole_product_source_accepted'] is False and
         cfg['canonical_credit_changed'] is False,
         'bounded original registration DATA and native word alignment only')
    return cfg,cfg_sha

def sources(cfg):
    old=(ROOT/cfg['previous_pinned_source']).read_bytes()
    new=(ROOT/cfg['aligned_source']).read_bytes()
    codes=(ROOT/cfg['maintained_codes']).read_bytes()
    before=b'; The historical extra final zero is excluded; the linker owns any following gap.\n'
    after=b'; Natural TASM EVEN owns the historical initialized word-alignment byte.\n'
    need(old.count(before)==1 and old.count(b'\tend\n')==1 and
         new==old.replace(before,after).replace(b'\tend\n',b'\teven\n\tend\n') and
         new.endswith(b'\teven\n\tend\n') and
         all(x in new for x in (b'.model use16 large _TEXT',
              b'include src/mainl/hiscore/regi_codes.inc')),
         'natural existing registration source, unchanged semantic bytes and one true EVEN')
    return old,new,codes

def transport(raw):
    return raw.decode('utf-8').encode('cp932').replace(b'\n',b'\r\n')

def response(number):
    rsp=parent.response(number)
    for old,new in [(rb'probe\af558s\regpre.obj',f'probe\\{STAGE}\\regpre.obj'.encode()),
                    (f'probe\\af566m\\r{number}.exe'.encode(),f'probe\\{STAGE}\\r{number}.exe'.encode()),
                    (f'probe\\af566m\\r{number}.map'.encode(),f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(rsp.count(old)==1,'one normal-link DATA object/output only '+str(old))
        rsp=rsp.replace(old,new)
    return rsp

def program_metadata(raw):
    return [(r.name,r.data) for r in parse_omf(raw)
            if r.name not in ('THEADR','COMENT','PUBDEF','LEDATA','FIXUPP')]

def scope(native,original):
    original_initialized=payload(original)
    new_initialized=payload(native)
    need(original_initialized==new_initialized and
         len([k for k in new_initialized if k[0]==2])==296 and
         new_initialized[2,303]==0 and
         len(literal_fields(original))==len(literal_fields(native))==2 and
         literal_fields(original)==literal_fields(native) and
         public_offsets(original)==public_offsets(native) and
         len(public_offsets(original))==35 and
         segment_definitions(original)==segment_definitions(native) and
         program_metadata(original)==program_metadata(native),
         'all original 304 DATA allocation, 2 literal fields/35 publics/other OMF')
    return dict(native_DATA_allocation_bytes=304,
                initialized_semantic_DATA_bytes=303,original_TASM_even_byte=1,
                complete_original_context_payload=True,
                original_ordered_fixups_equal=True,
                original_PUBLIC_definitions_equal=True,
                nonvariable_other_OMF_equal=True)

def canonical_map(raw):
    # Native THEADR is "regpre.asm"; only the initialized original 304-byte
    # contribution row changes relative to the after566 303-byte link.
    old=b'0E3F:092E 0130 C=DATA   S=_DATA          G=DGROUP  M=regpre.asm ACBP=48'
    new=b'0E3F:092E 012F C=DATA   S=_DATA          G=DGROUP  M=regpre.asm ACBP=48'
    need(raw.count(old)==1,'one original DATA even alignment contribution')
    return raw.replace(old,new)

def main():
    cfg,cfg_sha=inputs()
    p,p_sha=base.load(parent.REPORT)
    need(p['complete'] and p_sha==cfg['parent_report_sha256'],
         'actual latest MAINL after566 native source parent')
    old,source,codes=sources(cfg)
    original=(WORK/cfg['original_context_object']).read_bytes()
    need(sha(TASM.read_bytes())=='ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'pinned original TASM native producer')
    report=dict(complete=False,cold_rebuilt=False,game_objects_recompiled_per_round=1,
        remaining_project_objects_reused=35,CRT_rebuilt=False,canonical_credit_changed=False,
        whole_product_source_accepted=False,source_TASM_semantic_DATA_bytes=303,
        source_NATIVE_even_DATA_bytes=1, original_context_object_sha256=sha(original),
        parent_report_sha256=p_sha, original_unaligned_source_sha256=sha(old),
        aligned_source_sha256=sha(source),code_definitions_sha256=sha(codes),
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),config_sha256=cfg_sha,
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(TASM)]
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']

    def run(argv,cwd,label):
        done=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,timeout=100)
        name=PREFIX+label+'.log'
        (ROOT/name).write_bytes(done.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=done.returncode,
                log=name,log_sha256=sha(done.stdout)))
        save()
        need(done.returncode==0,label+': '+done.stdout.decode(errors='replace')[-1100:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh independently source-native registration stage')
        (SCRATCH/'src/mainl/hiscore').mkdir(parents=True)
        for file,raw in [('regpre.asm',transport(source)),
                         ('src/mainl/hiscore/regi_codes.inc',transport(codes)),
                         ('driver.py',(ROOT/DRIVER).read_bytes()),
                         ('config.json',(ROOT/CONFIG).read_bytes())]:
            (SCRATCH/file).write_bytes(raw)
        os.utime(SCRATCH/'regpre.asm',(946684800,946684800))
        os.utime(SCRATCH/'src/mainl/hiscore/regi_codes.inc',(946684800,946684800))
        vector=[]
        for n in (1,2):
            run(tasm+['/m','/mx','/kh32768','/t','/dGAME=3','regpre.asm,regpre.obj'],
                SCRATCH,f'round{n}-assemble')
            obj=(SCRATCH/'regpre.obj').read_bytes()
            match=scope(obj,original)
            rsp=response(n)
            (SCRATCH/f'r{n}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.lnk'],WORK,f'round{n}-link')
            exe=(SCRATCH/f'r{n}.exe').read_bytes()
            m=(SCRATCH/f'r{n}.map').read_bytes()
            before=p['rounds'][n-1]
            need(exe==base.checked(before['outputs']['exe']) and len(exe)==67372 and
                 len(parse_mz(exe).relocations)==677 and
                 canonical_map(m)==base.checked(before['outputs']['map']),
                 'every original Japanese MAINL EXE byte and all normal LINK MAP rows unchanged')
            outputs={}
            raw=dict(obj=obj,exe=exe,map=m)
            for key,value in raw.items():
                path=PREFIX+f'round{n}-{key}.bin'
                (ROOT/path).write_bytes(value)
                outputs[key]=dict(path=path,bytes=len(value),sha256=sha(value))
            report['rounds'].append(dict(round=n,outputs=outputs,
                response_sha256=sha(rsp),complete_original_DATA_scope=match,
                actual_japanese_decoded_exe_equal=True,
                unchanged_original_MAP_outside_REGPRE_row=True))
            save()
            vector.append(raw)
            print('MAINL registration round',n,'natural TASM EVEN at DATA+303, original 304 native DATA; full 67372 EXE exact',flush=True)
        need(vector[0]==vector[1] and
             (ROOT/cfg['aligned_source']).read_bytes()==source,
             'both complete raw OBJ/EXE/MAP vectors and unchanged maintained source')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
