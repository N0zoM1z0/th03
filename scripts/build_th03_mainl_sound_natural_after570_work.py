#!/usr/bin/env python3
"""Two real TASM/TLINK rounds replacing all 4 codestring sound TUs with EVEN.

Reconstructs all original instructions and four native word-alignment bytes
via symbolic assembler source; no target hex arrays, manual NOP or product
binary patches. Keeps older Turbo C++ source/receipts as historical evidence.
"""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_mainl_registration_even_after569_work as prior
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=prior.ROOT
WORK=prior.WORK
base=prior.base
DRIVER='scripts/build_th03_mainl_sound_natural_after570_work.py'
CONFIG='config/mainl_work/sound_natural_after570.json'
PREFIX='.analysis/work/mainl-sound-natural-after570-native-'
REPORT=PREFIX+'build.json'
STAGE='af570n'
SCRATCH=WORK/('probe/'+STAGE)
TASM=prior.TASM
REFERENCE_CPP={'snd_mode':'snd_mode.c','snd_pmdr':'snd_pmdr.c',
               'snd_dlyv':'snd_dlyv.c','snd_se_r':'snd_se_r.cpp'}
ORDER=['snd_mode','snd_pmdr','snd_dlyv','snd_se_r']

def inputs():
    cfg,cfg_sha=base.load(CONFIG)
    required=[
        ('snd_mode','src/mainl/sound/mode_detect.asm',30,29,3),
        ('snd_pmdr','src/mainl/sound/pmd_resident.asm',58,57,4),
        ('snd_dlyv','src/mainl/sound/volume_wait.asm',28,27,1),
        ('snd_se_r','src/mainl/sound/se_reset.asm',12,11,2)]
    need(cfg['schema']=='th03-mainl-sound-natural-after570-v1' and
         cfg['parent_report']==prior.REPORT and
         [(u['stem'],u['source'],u['CODE_bytes'],u['instructions_bytes'],u['literal_fixups'])
          for u in cfg['sources']]==required and
         (cfg['total_CODE_bytes'],cfg['total_function_bytes'],
          cfg['natural_TASM_even_bytes'],cfg['whole_original_decoded_EXE_bytes'],
          cfg['whole_original_MZ_relocations'])==(128,124,4,67372,677) and
         cfg['original_OMF_FIXUPP_packet_order_proved'] is False and
         cfg['original_compiler_identity_proved'] is False and
         cfg['canonical_credit_changed'] is False,
         'bounded source-natural four sound original CODE allocations')
    return cfg,cfg_sha

def sources(cfg):
    values={u['stem']:(ROOT/u['source']).read_bytes() for u in cfg['sources']}
    for stem,raw in values.items():
        need(raw.isascii() and b'\r' not in raw and
             raw.count(b'    even\nSHARED ends')==1 and
             b'codestring' not in raw.lower() and b'    db ' not in raw.lower() and
             b'    nop' not in raw.lower(),
             'symbolic 8086-only body with true assembler CODE EVEN '+stem)
    return values

def field_set(raw):
    return sorted(json.dumps(x,sort_keys=True) for x in literal_fields(raw))

def object_scope(native,reference,u):
    a,b=payload(native),payload(reference)
    size=u['CODE_bytes']
    need(len(a)==len(b)==size and a==b and a[1,size-1]==0x90 and
         len(literal_fields(native))==len(literal_fields(reference))==u['literal_fixups'] and
         field_set(native)==field_set(reference) and
         public_offsets(native)==public_offsets(reference) and
         segment_definitions(native)==segment_definitions(reference),
         'all original sound instruction CODE, 1 EVEN, OMF field tuples/PUBLICs/segment flags '+u['stem'])
    return dict(original_initialized_CODE_bytes=size,
        natural_8086_function_bytes=u['instructions_bytes'],natural_TASM_CODE_even_bytes=1,
        original_literal_FIXUPP_sites=u['literal_fixups'],
        original_FIXUPP_order_equal=(literal_fields(native)==literal_fields(reference)),
        full_source_CODE_exact=True)

def response(number):
    rsp=prior.response(number)
    for stem in ORDER:
        before=f'probe\\af558s\\{stem}.obj'.encode()
        after=f'probe\\{STAGE}\\{stem}.obj'.encode()
        need(rsp.count(before)==1,'one original sound producer object in first-use link '+stem)
        rsp=rsp.replace(before,after)
    for before,after in [(f'probe\\af569r\\r{number}.exe'.encode(),
                          f'probe\\{STAGE}\\r{number}.exe'.encode()),
                         (f'probe\\af569r\\r{number}.map'.encode(),
                          f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(rsp.count(before)==1,'one real target source native output')
        rsp=rsp.replace(before,after)
    return rsp

def normalize_map(raw):
    # TASM's THEADR file paths and its segment combination code (ACBP)
    # are diagnostic differences. All contribution sizes/locations/IDs
    # must otherwise match exactly.
    rows=raw.splitlines(keepends=True)
    for stem in ORDER:
        original=f'M=probe/af558s/{REFERENCE_CPP[stem]}'.encode()
        new=f'M=probe\\{STAGE}\\{stem}.asm'.encode()
        need(sum(new in r for r in rows)==3,'one source CODE+DATA+BSS row group '+stem)
        for i,line in enumerate(rows):
            if new not in line: continue
            if stem in ('snd_pmdr','snd_dlyv') and b' C=CODE ' in line:
                need(line.count(b'ACBP=48')==1,'native original compiler ACBP=28 link comparison')
                line=line.replace(b'ACBP=48',b'ACBP=28')
            rows[i]=line.replace(new,original)
    return b''.join(rows)

def main():
    cfg,cfg_sha=inputs()
    parent,parent_sha=base.load(prior.REPORT)
    need(parent['complete'] and parent_sha==cfg['parent_report_sha256'],
         'latest after569 source-native registration/input and C0/CRT parent')
    maintained=sources(cfg)
    originals={s:(WORK/f'obj/th02/{s}.obj').read_bytes() for s in ORDER}
    need(sha(TASM.read_bytes())=='ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'genuine pinned Borland TASM5 emitter')
    record=dict(complete=False,canonical_credit_changed=False,
        whole_game_source_accepted=False,cold_rebuilt=False,library_rebuilt=False,
        four_game_objects_recompiled_per_round=4,other_game_objects_reused=32,
        native_source_instruction_bytes=124,native_code_alignment_bytes=4,
        parent_report_sha256=parent_sha,config_sha256=cfg_sha,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        sources_sha256={s:sha(raw) for s,raw in maintained.items()},
        original_objects_sha256={s:sha(raw) for s,raw in originals.items()},
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(record,indent=2)+'\n')
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),
             MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(TASM)]
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        record['phases'].append(dict(label=label,argv=argv,returncode=p.returncode,
                log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh retained natural 4-sound stage')
        SCRATCH.mkdir()
        for s,raw in maintained.items():
            (SCRATCH/f'{s}.asm').write_bytes(raw.replace(b'\n',b'\r\n'))
            os.utime(SCRATCH/f'{s}.asm',(946684800,946684800))
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for number in (1,2):
            before=parent['rounds'][number-1]
            native={}
            scopes={}
            for u in cfg['sources']:
                stem=u['stem']
                run(tasm+['/m','/mx','/kh32768','/t','/dGAME=3',
                    f'probe\\{STAGE}\\{stem}.asm,probe\\{STAGE}\\{stem}.obj'],
                    f'round{number}-{stem}-assemble')
                obj=(SCRATCH/f'{stem}.obj').read_bytes()
                scopes[stem]=object_scope(obj,originals[stem],u)
                native[stem+'_obj']=obj
            rsp=response(number)
            (SCRATCH/f'r{number}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.lnk'],f'round{number}-link')
            native.update(exe=(SCRATCH/f'r{number}.exe').read_bytes(),
                          map=(SCRATCH/f'r{number}.map').read_bytes())
            need(native['exe']==base.checked(before['outputs']['exe']) and
                 len(native['exe'])==67372 and len(parse_mz(native['exe']).relocations)==677 and
                 normalize_map(native['map'])==base.checked(before['outputs']['map']),
                 'entire original decoded MAINL EXE and all 677 MZ relocations + unchanged MAP')
            outputs={}
            for key,raw in native.items():
                path=PREFIX+f'round{number}-{key}.bin'
                (ROOT/path).write_bytes(raw)
                outputs[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            record['rounds'].append(dict(round=number,outputs=outputs,
                    input_objects_exact=scopes,link_response_sha256=sha(rsp),
                    whole_original_MAINL_exe_equal=True,all_677_ordered_MZ_relocations_equal=True))
            save()
            vectors.append(native)
            print('Natural sound round',number,'4 source-assembled far functions + 4 EVEN; entire 67372-byte Japanese MAINL EXE exact',flush=True)
        need(vectors[0]==vectors[1] and sources(cfg)==maintained,
             'both raw 6-product native vectors repeat and source unchanged')
    record['complete']=True
    save()

if __name__=='__main__':
    main()
