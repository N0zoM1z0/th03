#!/usr/bin/env python3
"""Reassemble complete natural MAINL far VECTOR2 producer, re-link after556 locally.

Only one CODE object is reassembled per round; source, native object and linked
image are compared independently. The retained DATA and cold CRT parents are
reused, not cold-rebuilt or patched.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess

import build_th03_mainl_root_data_work as parent
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.omf import parse_omf

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER='scripts/build_th03_mainl_vector_work.py'
CONFIG='config/mainl_work/vector_after557.json'
PREFIX='.analysis/work/vector-after557-native-'
REPORT=PREFIX+'build.json'
STAGE='af557v'
SCRATCH=WORK/('probe/'+STAGE)


def inputs():
    config, digest=base.load(CONFIG)
    need(config['schema']=='th03-mainl-vector-after557-v1' and
         config['parent_report']==parent.REPORT and
         config['source']=='src/shared/math/vector_far.asm' and
         config['cold_object']=='obj/th03/vector_far.obj' and
         [(u['name'],u['offset'],u['size']) for u in config['function_extent']]==[
             ('VECTOR2',0,69),('VECTOR2_BETWEEN_PLUS',70,90)] and
         config['alignment']==dict(offset=69,size=1,source='EVEN',native_emitted_byte=0x90) and
         config['ordered_fixups']==5,'bounded two-function native vector extent')
    return config,digest


def wrapper():
    return f'include probe/{STAGE}/vector_body.asm\r\n'.encode()


def response(number):
    raw=parent.response(number)
    needle=rb'obj\th03\vector_far.obj'
    need(raw.count(b'af556d')==9 and raw.count(needle)==1,'single vector contributor in normal parent link')
    return raw.replace(b'af556d',STAGE.encode()).replace(needle,f'probe\\{STAGE}\\vector_far.obj'.encode())


def map_normalized(raw):
    # New THEADR path is only a diagnostic, not a different allocation.
    needle=f'M=probe\\{STAGE}\\vector_far.asm'.encode()
    need(raw.count(needle)==1,'single original vector contribution')
    return parent.map_normalize(raw.replace(needle,b'M=th03\\vector_far.asm'))


def module_metadata(raw):
    return [(x.name,x.data) for x in parse_omf(raw)
            if x.name not in ('THEADR','COMENT','PUBDEF','LEDATA','FIXUPP')]


def source_snapshot():
    source=(ROOT/'src/shared/math/vector_far.asm').read_bytes()
    need(source.isascii() and b'\r' not in source and
         b'\teven\n' in source and b'#pragma codestring' not in source.lower(),
         'symbolic far vector and true even-code alignment, without emitted opcode arrays')
    return source.replace(b'\n',b'\r\n')


def main():
    config,config_sha=inputs()
    prior,prior_hash=base.load(parent.REPORT)
    need(prior['complete'] and prior_hash==config['parent_report_sha256'],
         'actual after556 source DATA native link parent')
    source=(ROOT/config['source']).read_bytes()
    native_source=source_snapshot()
    original=(WORK/config['cold_object']).read_bytes()
    original_payload=payload(original)
    expected_publics={'VECTOR2':dict(offset=0,segment_index=1,group_index=0),
                     'VECTOR2_BETWEEN_PLUS':dict(offset=70,segment_index=1,group_index=0)}
    need(len(original_payload)==160 and original_payload[1,69]==144 and
         public_offsets(original)==expected_publics and
         len(literal_fields(original))==5 and
         (WORK/config['source']).read_bytes()==native_source,
         'attested actual original vector object, functions, reference include')
    record=dict(complete=False,cold_rebuilt=False,game_objects_recompiled=1,
        library_rebuilt=False,source_acceptance=False,whole_product_accepted=False,
        canonical_credit_changed=False, function_CODE_bytes=159,emitter_alignment_bytes=1,
        source_sha256=sha(source),transported_source_sha256=sha(native_source),
        wrapper_sha256=sha(wrapper()),config_sha256=config_sha,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),parent_report_sha256=prior_hash,
        original_object_sha256=sha(original),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(record,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),MSDOS_PATH=r'C:\TC4\BIN',
        TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(parent.parent.parent.TASM)]

    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        record['phases'].append(dict(label=label,returncode=p.returncode,
            argv=argv,log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1300:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh retained vector native stage')
        SCRATCH.mkdir()
        for name,raw in [('vector_body.asm',native_source),('vector_far.asm',wrapper()),
                         ('driver.py',(ROOT/DRIVER).read_bytes()),
                         ('config.json',(ROOT/CONFIG).read_bytes())]:
            (SCRATCH/name).write_bytes(raw)
        os.utime(SCRATCH/'vector_body.asm',(946684800,946684800))
        os.utime(SCRATCH/'vector_far.asm',(946684800,946684800))
        vectors=[]
        for number in (1,2):
            before=prior['rounds'][number-1]
            for key,filename in [('startup','c0l.obj'),('library',f'r{number}.lib'),
                                 ('root','rootdata.obj'),('pictures','rootpre.obj')]:
                (SCRATCH/filename).write_bytes(base.checked(before['reused'][key]))
            for key,filename in [('registration','regpre.obj'),('ending','regtail.obj')]:
                (SCRATCH/filename).write_bytes(base.checked(before['reused_banks'][key]))
            (SCRATCH/'mainl.obj').write_bytes(base.checked(before['outputs']['obj']))
            run(tasm+['/m','/mx','/kh32768','/t','/dGAME=3',
                f'probe\\{STAGE}\\vector_far.asm,probe\\{STAGE}\\vector_far.obj'],
                f'round{number}-assemble')
            obj=(SCRATCH/'vector_far.obj').read_bytes()
            need(payload(obj)==original_payload and
                 literal_fields(obj)==literal_fields(original) and
                 public_offsets(obj)==expected_publics and
                 module_metadata(obj)==module_metadata(original),
                 'all 160 native vector CODE bytes (including EVEN), five ordered fields, publics/metadata')
            rsp=response(number)
            (SCRATCH/f'r{number}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.lnk'],
                f'round{number}-link')
            v=dict(obj=obj,exe=(SCRATCH/f'r{number}.exe').read_bytes(),
                map=(SCRATCH/f'r{number}.map').read_bytes())
            need(v['exe']==base.checked(before['outputs']['exe']) and
                 map_normalized(v['map'])==parent.map_normalize(base.checked(before['outputs']['map'])),
                 'whole decoded EXE, MZ relocation table and full original MAP contributions exact')
            outputs={}
            for name,raw in v.items():
                f=PREFIX+f'round{number}-{name}.bin'
                (ROOT/f).write_bytes(raw)
                outputs[name]=dict(path=f,bytes=len(raw),sha256=sha(raw))
            record['rounds'].append(dict(round=number,outputs=outputs,
                response_sha256=sha(rsp),reused=before['reused'],
                reused_banks=before['reused_banks'],reused_root=before['outputs']['obj']))
            save()
            vectors.append(v)
            print('Vector round',number,'original-exact 2 far functions, CODE159+EVEN1, full EXE/MAP',flush=True)
        need(vectors[0]==vectors[1] and source==(ROOT/config['source']).read_bytes(),
             'both raw native OBJ/EXE/MAP vectors and source repeat')
    record['complete']=True
    save()

if __name__=='__main__':
    main()
