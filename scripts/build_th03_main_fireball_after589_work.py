#!/usr/bin/env python3
"""Two Turbo C++ rounds: all original fireball and explosion collision CODE.

Reuse source-native bullet+9 BOSS+enemy-script MAIN link, compile exactly
two GAME=3/BINARY=M objects, re-link normally, compare complete original
Japanese program and MZ relocations, compact container as distinct step.
No cold replay, target-byte arrays, defensive behavior changes or OBJ patches.
"""
import fcntl,json,os,subprocess
import build_th03_main_bullet_after588_work as parent
from build_th03_mainl_resources_work import sha,need
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER='scripts/build_th03_main_fireball_after589_work.py'
CONFIG='config/main_work/fireball_after589.json'
PREFIX='.analysis/work/main-fireball-after589-native-'
REPORT=PREFIX+'build.json'
STAGE='af589f'
SCRATCH=WORK/('probe/'+STAGE)
ORDER=('e_fireb','e_expl')

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    expected=[
       ('e_fireb','src/main/enemy/fireball.cpp','src/main/enemy/producers/fireball_native.cpp',1555,1,1,115,10),
       ('e_expl','src/main/enemy/expl.cpp','src/main/enemy/producers/explosion_native.cpp',630,0,0,49,1)]
    need(cfg['schema']=='th03-main-fireball-after589-v1' and
         cfg['parent_report']==parent.REPORT and
         [(u['stem'],u['source'],u['wrapper'],u['CODE_bytes'],u['DATA_bytes'],
           u['BSS_bytes'],u['fixups'],u['publics']) for u in cfg['units']]==expected and
         (cfg['total_CODE_bytes'],cfg['total_DATA_bytes'],cfg['total_BSS_bytes'],
          cfg['total_ordered_FIXUPP'],cfg['original_PUBLICs'],
          cfg['original_main_relocations'],cfg['japanese_file_bytes'])==
          (2185,1,1,164,11,1553,130882) and
         cfg['first_use_GAME']==3 and cfg['first_use_BINARY']=='M' and
         cfg['historical_full_vendor_OMF_packet_identity'] is False and
         cfg['canonical_factory_credit_changed'] is False and
         cfg['whole_project_source_accepted'] is False,
         'full two real fireball/explosion natural C++ original source producers')
    prev=json.loads((ROOT/cfg['parent_report']).read_text())
    need(prev['complete'] and len(prev['rounds'])==2 and
         sha((ROOT/cfg['parent_report']).read_bytes())==cfg['parent_report_sha256'],
         'original after588 bullet source + all earlier nine boss/keyboard parent')
    return cfg,sha((ROOT/CONFIG).read_bytes()),prev

def source_inputs(cfg):
    values={}
    for u in cfg['units']:
        raw=(ROOT/u['source']).read_bytes()
        forward=(ROOT/u['wrapper']).read_bytes()
        need(raw and b'\r' not in raw and b'\r' not in forward and
             forward.count(f'#include "{u["source"]}"'.encode())==1 and
             forward.endswith(f'#include "{u["source"]}"\n'.encode()) and
             (WORK/u['source']).read_bytes().replace(b'\r\n',b'\n')==raw,
             'unchanged original natural large fireball/explosion collision source '+u['stem'])
        values[u['stem']]=dict(source=raw,wrapper=forward)
    return values

def original_scope(obj,reference,u):
    a,b=payload(obj),payload(reference)
    pubs=public_offsets(obj)
    need(a==b and
         len([s for s,i in a if s==1])==u['CODE_bytes'] and
         len([s for s,i in a if s==2])==u['DATA_bytes'] and
         literal_fields(obj)==literal_fields(reference) and
         len(literal_fields(obj))==u['fixups'] and
         pubs==public_offsets(reference) and len(pubs)==u['publics'] and
         segment_definitions(obj)==segment_definitions(reference) and
         segment_definitions(obj)[2]['size']==u['BSS_bytes'],
         'whole original fireball/explosion initialized CODE+DATA, BSS and ordered OMF fields')
    return dict(CODE_bytes=u['CODE_bytes'],DATA_bytes=u['DATA_bytes'],
        BSS_bytes=u['BSS_bytes'],PUBLICs=u['publics'],ordered_FIXUPP=u['fixups'],
        complete_original_linker_semantics=True,original_vendor_packet_identity=False)

def response(n):
    raw=parent.response(n)
    for stem in ORDER:
        before=f'obj\\th03\\{stem}.obj'.encode()
        after=f'probe\\{STAGE}\\r{n}\\{stem}.obj'.encode()
        need(raw.count(before)==1,'single original fireball/explosion source slot')
        raw=raw.replace(before,after)
    for before,after in [(f'probe\\{parent.STAGE}\\r{n}.exe'.encode(),
                           f'probe\\{STAGE}\\r{n}.exe'.encode()),
                         (f'probe\\{parent.STAGE}\\r{n}.map'.encode(),
                           f'probe\\{STAGE}\\r{n}.map'.encode())]:
        need(raw.count(before)==1,'normal complete source-linked MAIN output')
        raw=raw.replace(before,after)
    return raw

def map_normalized(blob,n):
    for stem in ORDER:
        label=f'M=probe/{STAGE}/r{n}/{stem}.cpp'.encode()
        need(blob.count(label)==3,'all original CODE/DATA/BSS source MAP rows '+stem)
        blob=blob.replace(label,f'M=th03/{stem}.cpp'.encode())
    return blob

def read_pin(pin):
    return parent.previous.parent.read_pin(pin)

def main():
    cfg,cfg_sha,prior=inputs()
    sources=source_inputs(cfg)
    originals={u['stem']:(WORK/f'obj/th03/{u["stem"]}.obj').read_bytes() for u in cfg['units']}
    target=parent.read_verified_artifact(ROOT,parent.find_artifact(
        parent.load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    target_mz=parse_mz(target)
    need(len(target)==130882 and len(target_mz.relocations)==1553,
         'pinned original Japanese MAIN original file and MZ references')
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        project_objects_recompiled_per_round=2,other_project_objects_reused=97,
        total_CODE_bytes=2185,total_DATA_bytes=1,total_BSS_bytes=1,
        canonical_factory_credit_changed=False,whole_project_source_accepted=False,
        config_sha256=cfg_sha,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        parent_report_sha256=cfg['parent_report_sha256'],
        source_sha256={k:{a:sha(v) for a,v in value.items()} for k,value in sources.items()},
        original_object_sha256={k:sha(v) for k,v in originals.items()},
        original_japanese_file_sha256=sha(target),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=115)
        file=PREFIX+label+'.log'
        (ROOT/file).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=argv,exit_code=p.returncode,
            log=file,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1250:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh native two-object fireball/explosion source stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            folder=SCRATCH/f'r{n}'
            folder.mkdir()
            generated={}
            scopes={}
            for u in cfg['units']:
                stem=u['stem']
                (folder/f'{stem}.cpp').write_bytes(sources[stem]['wrapper'].replace(b'\n',b'\r\n'))
                os.utime(folder/f'{stem}.cpp',(946684800,946684800))
                run(dos+['tcc','-c','-I.','-O','-b-','-3','-Z','-d','-DGAME=3','-ml',
                    "-DBINARY='M'",f'-nprobe/{STAGE}/r{n}/',f'probe/{STAGE}/r{n}/{stem}.cpp'],
                    f'round{n}-{stem}-TC4')
                obj=(folder/f'{stem}.obj').read_bytes()
                scopes[stem]=original_scope(obj,originals[stem],u)
                generated[stem+'_obj']=obj
            rsp=response(n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],f'round{n}-normal-TLINK')
            exe=(SCRATCH/f'r{n}.exe').read_bytes()
            mapped=(SCRATCH/f'r{n}.map').read_bytes()
            ancestor=prior['rounds'][n-1]['outputs']
            need(exe==read_pin(ancestor['exe']) and
                 map_normalized(mapped,n)==read_pin(ancestor['map']) and
                 parse_mz(exe).program_image==target_mz.program_image and
                 parse_mz(exe).relocations==target_mz.relocations,
                 'entire native MAIN source image and all 1553 Japanese ordered MZ relocation entries')
            compact=compact_mz(exe)
            need(compact==target,'whole original Japanese MAIN file via separately reviewed MZ serializer')
            outputs={}
            v={**generated,'exe':exe,'map':mapped,'compact_mz':compact}
            for name,bytes_out in v.items():
                path=PREFIX+f'round{n}-{name}.bin'
                (ROOT/path).write_bytes(bytes_out)
                outputs[name]=dict(path=path,bytes=len(bytes_out),sha256=sha(bytes_out))
            report['rounds'].append(dict(round=n,outputs=outputs,original_object_scope=scopes,
                original_source_response_sha256=sha(rsp),
                full_original_japanese_file_equal_after_explicit_MZ_format=True))
            save()
            vectors.append(v)
            print('Fireball/explosion round',n,'2185 original CODE + 1 DATA, 164 ordered FIXUPPs, full MAIN original exact',flush=True)
        need(vectors[0]['exe']==vectors[1]['exe'] and
             vectors[0]['compact_mz']==vectors[1]['compact_mz'] and
             all(payload(vectors[0][stem+'_obj'])==payload(vectors[1][stem+'_obj'])
                 and literal_fields(vectors[0][stem+'_obj'])==
                     literal_fields(vectors[1][stem+'_obj'])
                 for stem in ORDER) and
             source_inputs(cfg)==sources,
             'two independently real source compiled fireball/explosion groups repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
