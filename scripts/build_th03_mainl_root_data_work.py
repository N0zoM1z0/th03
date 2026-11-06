#!/usr/bin/env python3
"""Recover semantic root DATA while retaining the original contextual CODE/BSS.

Based on the after555 formula-native build, this compiles 13 maintained
state/string sources and the already-maintained CDG DATA. Nothing is patched in
objects or executables; unowned gaps stay excluded from source-byte accounting.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess

import build_th03_mainl_root_trig_work as parent
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets

ROOT = parent.ROOT
base = parent.base
WORK = parent.WORK
DRIVER = 'scripts/build_th03_mainl_root_data_work.py'
CONFIG = 'config/mainl_work/root_data_after556.json'
PREFIX = '.analysis/work/root-data-after556-native-'
REPORT = PREFIX + 'build.json'
STAGE = 'af556d'
SCRATCH = WORK / ('probe/' + STAGE)

# Each include is replaced at exactly one source location. Basename uniqueness
# is required because native TASM staging intentionally uses short DOS paths.
BANKS = {
    'root_strings.inl': 'src/mainl/data/root_strings.inl',
    'file_sharing.inl': 'src/shared/data/file_sharing.inl',
    'graphics.inl': 'src/shared/data/graphics.inl',
    'random.inl': 'src/shared/data/random.inl',
    'text_vram.inl': 'src/shared/data/text_vram.inl',
    'sprite_state.inl': 'src/shared/data/sprite_state.inl',
    'sound_active.inl': 'src/mainl/data/sound_active.inl',
    'sound_state.inl': 'src/mainl/data/sound_state.inl',
    'archive_probe.inl': 'src/mainl/data/archive_probe.inl',
    'sound_priorities.inl': 'src/mainl/data/sound_priorities.inl',
    'continue_text.inl': 'src/mainl/data/continue_text.inl',
    'pi_masks.inl': 'src/mainl/data/pi_masks.inl',
    'cutscene_text.inl': 'src/mainl/data/cutscene_text.inl'
}
INCLUDES = {
    'libs/master.lib/dos_ropen[data].asm': 'file_sharing.inl',
    'libs/master.lib/grp[data].asm': 'graphics.inl',
    'libs/master.lib/rand[data].asm': 'random.inl',
    'libs/master.lib/tx[data].asm': 'text_vram.inl',
    'libs/master.lib/super_entry_bfnt[data].asm': 'sprite_state.inl',
    'th03/snd/se_state[data].asm': 'sound_state.inl',
    'th02/formats/pfopen[data].asm': 'archive_probe.inl',
    'th03/snd/se_priority[data].asm': 'sound_priorities.inl',
    'th03/formats/pi_put_masked[data].asm': 'pi_masks.inl'
}


def inputs():
    cfg, digest = base.load(CONFIG)
    need(cfg['schema'] == 'th03-mainl-root-data-after556-v1' and
         cfg['parent_report'] == parent.REPORT and
         (cfg['context_DATA_bytes'],cfg['source_bytes'],cfg['source_initialized_DATA_bytes'],
          cfg['source_uninitialized_file_DATA_bytes'],cfg['source_BYTES_new_in_stage'],
          cfg['source_BYTES_reused_from_after555'],cfg['authored_bytes_new_in_stage'],
          cfg['library_bytes_new_in_stage']) == (2036,1859,1825,34,963,896,900,63) and
         set(BANKS.values()).issubset(cfg['inputs']) and
         set(cfg['inputs']) == set(BANKS.values()) | {cfg['inputs'][1], 'src/mainl/display_hardware/cdg_data.asm'} and
         cfg['inputs'][1] == 'src/shared/math/trig_tables.py', 'complete bounded source list')
    all_sites=set()
    for u in cfg['units']:
        n=set(range(u['offset'],u['offset']+u['size']))
        need(u['origin'] in ('library','authored') and not n & all_sites and
             u['size']>0 and max(n)<cfg['context_DATA_bytes'], 'disjoint, bounded semantic DATA ' + u['name'])
        all_sites |= n
    need(len(all_sites)==1859 and all(x not in all_sites for x in cfg['uncredited_padding_offsets']) and
         sum(u['size'] for u in cfg['units'] if u['origin']=='authored') == 900 and
         sum(u['uninitialized_file_data_bytes'] for u in cfg['units']) == 34,
         'no unpublished padding/byte ownership')
    return cfg, digest


def transported(raw):
    return raw.decode('utf-8').encode('cp932').replace(b'\n', b'\r\n')


def input_sources(cfg):
    return {n:(ROOT/n).read_bytes() for n in cfg['inputs']}


def context():
    # The actual after555 staged C0/CRT/source parent is retained, not rebuilt.
    raw = (parent.SCRATCH / 'th03_mainl.asm').read_bytes()
    need(sha(raw) == parent.base.load(parent.REPORT)[0]['context_sha256'],
         'literal staged after555 source root')
    def included(name):
        return (f'include probe/{STAGE}/banks/{name}\r\n').encode()
    def replace_span(raw, begin, end, name):
        a=raw.index(begin);b=raw.index(end,a)
        need(a<b and raw.count(begin)==1,'unique contextual DATA block '+name)
        return raw[:a]+included(name)+raw[b:]
    raw=replace_span(raw,b'public _mainl_stage_number\r\n',
                     b'include probe/af555t/generated/atan.inl\r\n','root_strings.inl')
    for old,name in INCLUDES.items():
        before=('include '+old+'\r\n').encode()
        need(raw.count(before)==1,'unique DATA include '+old)
        raw=raw.replace(before,included(name))
    # Sprite header and pool are one continuous allocation. The retained
    # library's later superpa include is consumed by the same maintained owner.
    removed=b'include libs/master.lib/superpa[data].asm\r\n'
    need(raw.count(removed)==1,'single old sprite pool context')
    raw=raw.replace(removed,b'')
    raw=replace_span(raw,b'public _snd_active\r\n',b'\t\tdb 0\r\n','sound_active.inl')
    raw=replace_span(raw,b'public _mainl_continue_digit\r\n',included('pi_masks.inl'),
                     'continue_text.inl')
    raw=replace_span(raw,b'public _CUTSCENE_KANJI\r\n',b'\tevendata\r\n',
                     'cutscene_text.inl')
    return raw


def response(number):
    previous=parent.link_response(number)
    need(previous.count(b'af555t')==9, 'exact active after555 link source paths')
    return previous.replace(b'af555t',STAGE.encode())


def map_normalize(raw):
    needle = ('M=probe\\' + STAGE + r'\th03_mainl.asm').encode()
    need(raw.count(needle)==9,'all nine root MAP contributions preserved')
    return raw.replace(needle,b'M=th03_mainl.asm')


def main():
    cfg,cfg_hash=inputs()
    prior, prior_hash=base.load(parent.REPORT)
    need(prior['complete'] and prior_hash==cfg['parent_report_sha256'],
         'source-bound after555 two-round native parent')
    sources=input_sources(cfg)
    asm=context()
    original=(WORK/'obj/th03/mainl.obj').read_bytes()
    need(sha(original)==prior['original_object_sha256'],'original contextual root fixed')
    need(sha(parent.TASM.read_bytes())=='ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'pinned assembler')
    reference_data=payload(original)
    # File-backed reservations are distinct from initialized source bytes.
    reserved=set(range(0x748,0x768)) | set(range(0x782,0x784))
    need(len(reserved)==34 and all((2,i) not in reference_data for i in reserved),
         'true BFNT header and CDG reserved file DATA')
    report=dict(complete=False, source_acceptance=False, canonical_credit_changed=False,
        whole_product_accepted=False, cold_rebuilt=False, game_objects_recompiled=1,
        library_rebuilt=False, initialized_source_DATA_bytes=1825,
        reserved_source_DATA_bytes=34, game_authored_DATA_bytes=900,
        library_DATA_bytes=959, source_sha256={k:sha(v) for k,v in sources.items()},
        native_source_sha256=sha(asm), config_sha256=cfg_hash,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()), parent_report_sha256=prior_hash,
        original_object_sha256=sha(original), phases=[], rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    env=dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'), MSDOS_PATH=r'C:\TC4\BIN',
        TZ='UTC', LANG='C', LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(parent.TASM)]

    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=110)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=p.returncode,
            log=log, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1300:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh retained DATA native stage')
        (SCRATCH/'banks').mkdir(parents=True)
        for name,sourcepath in BANKS.items():
            p=SCRATCH/'banks'/name
            p.write_bytes(transported(sources[sourcepath]))
            os.utime(p,(946684800,946684800))
        (SCRATCH/'th03_mainl.asm').write_bytes(asm)
        os.utime(SCRATCH/'th03_mainl.asm',(946684800,946684800))
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for number in (1,2):
            before=prior['rounds'][number-1]
            for key,filename in [('startup','c0l.obj'),('library',f'r{number}.lib'),
                                 ('root','rootdata.obj'),('pictures','rootpre.obj')]:
                (SCRATCH/filename).write_bytes(base.checked(before['reused'][key]))
            for key,filename in [('registration','regpre.obj'),('ending','regtail.obj')]:
                (SCRATCH/filename).write_bytes(base.checked(before['reused_banks'][key]))
            run(tasm+['/m','/mx','/kh32768','/t','/dGAME=3',
                f'probe\\{STAGE}\\th03_mainl.asm,probe\\{STAGE}\\mainl.obj'],
                f'round{number}-assemble')
            obj=(SCRATCH/'mainl.obj').read_bytes()
            need(payload(obj)==reference_data and
                 literal_fields(obj)==literal_fields(original) and
                 len(literal_fields(obj))==392 and
                 public_offsets(obj)==public_offsets(original) and
                 parent.structure_without_publics(obj)==parent.structure_without_publics(original),
                 'entire native OBJ initializer/ordered fields/definitions/structure')
            rsp=response(number)
            (SCRATCH/f'r{number}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.lnk'],
                f'round{number}-link')
            vector=dict(obj=obj,exe=(SCRATCH/f'r{number}.exe').read_bytes(),
                map=(SCRATCH/f'r{number}.map').read_bytes())
            need(vector['exe']==base.checked(before['outputs']['exe']) and
                 map_normalize(vector['map'])==parent.map_canonical(base.checked(before['outputs']['map'])),
                 'entire decoded original EXE including relocations, all MAP contributions unchanged')
            outputs={}
            for key,value in vector.items():
                filename=PREFIX+f'round{number}-{key}.bin'
                (ROOT/filename).write_bytes(value)
                outputs[key]=dict(path=filename,bytes=len(value),sha256=sha(value))
            report['rounds'].append(dict(round=number,response_sha256=sha(rsp),outputs=outputs,
                reused=before['reused'],reused_banks=before['reused_banks']))
            save()
            vectors.append(vector)
            print('MAINL root DATA round',number,'complete:1859 source bytes/34 reservations; all392 fields; entire EXE exact',flush=True)
        need(vectors[0]==vectors[1] and input_sources(cfg)==sources,
             'two complete OBJ/EXE/MAP vectors repeat and maintained sources unchanged')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
