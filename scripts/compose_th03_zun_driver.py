"""Opt-in maintained -2/-4 composition using actual independently produced inputs.

Wrapper modules and the other three payloads remain retained. No native tools,
payload/device execution, target fallback, normalization or acceptance changes.
"""
import json,re
from pathlib import Path
import compose_th03_zun_init as init
from lib.zun import compose_launcher,parse_launcher,dispatch_observation
from verify_th03_zun_driver_hybrid import verify,CANDIDATE
sha=init.sha
require=init.require
read_plain=init.read_plain
DRIVER_WORKS=tuple('.analysis/toolchain/wineprefix/drive_c/ZDSA%02d'%n for n in (2,3))
DRIVER_RUNS=tuple('.analysis/zun-driver-standalone-native-output-20261021-v%02d'%n for n in (2,3))
COMPLETIONS=('52d3c3f8722e254fa3ab73963c228453fd39b488ee507d470b8ee681a5138a08','4ed2bafe36a4a3ab8e0be2f344158c6e66cd2fa2eabe6ec3ec5ab618799b47e4')
MANIFESTS=('ff8a6a0dfb6025dbce6695a7861b93ebeb2f9e255c45a4985d0911f58e4617a9','0a36ad8dc97dad4f297a24382ad7af1c151e4c426a4cd51bc254e9887a4ff012')
STAGE_SHA='3dc6d404195517dda508ad3ff03a0fcfba4f862f46807849ac116453ff6266e5'

def compose_driver(modules,base,driver_com):
    """Replace -4 only in the already maintained-init composition."""
    require(set(modules)=={'launcher','transfer_call','transfer_helper'},'three wrapper modules')
    old=parse_launcher(base,223);names=[p['name'] for p in old['payloads']]
    require(names==['-1','-2','-3','-4','-5'],'five payloads')
    selected=old['payloads'][3];start=selected['decoded_file_offset'];end=start+selected['size']
    require(start==0x32a2 and selected['size']==4224 and len(driver_com)==4224 and sha(driver_com)==CANDIDATE,'actual maintained driver candidate/layout')
    payloads=[base[p['decoded_file_offset']:p['decoded_file_offset']+p['size']] for p in old['payloads']]
    payloads[3]=driver_com
    data=compose_launcher(modules['launcher'],modules['transfer_call'],modules['transfer_helper'],names,payloads)
    require(len(data)==len(base) and data[:start]==base[:start] and data[end:]==base[end:],'outside -4 changed')
    require(data[start:end]==driver_com and parse_launcher(data,223)==old,'driver input or scaffold changed')
    return data

def prepare_pair(root):
    root=Path(root);init_rounds,inputs=init.prepare_pair(root);frozen={}
    def pin(name,expected=None):
        raw=read_plain(root/name)
        require(expected is None or sha(raw)==expected,'input identity: '+name)
        require(name not in inputs or inputs[name]==sha(raw),'inherited input changed')
        require(name not in frozen or frozen[name]==raw,'input changed')
        frozen[name]=raw;return raw
    import tomllib
    config=tomllib.loads(pin('config/th03_zun_launcher.toml',inputs['config/th03_zun_launcher.toml']).decode())
    decoded=pin(config['decoded_path'],inputs[config['decoded_path']])
    rounds=[];raw_drivers=[]
    for index,(run,work) in enumerate(zip(DRIVER_RUNS,DRIVER_WORKS)):
        receipt=json.loads(pin(run+'/completion.json',COMPLETIONS[index]))
        stage=json.loads(pin(run+'/stage.json',STAGE_SHA))
        manifest=json.loads(pin(run+'/manifest.json',MANIFESTS[index]))
        require(receipt['complete'] and receipt['errors']==[] and receipt['owned_lock_released'] and receipt['native_invocations']==2 and not receipt['exact_acceptance'],'driver completion scope')
        require(stage['complete_driver_source_owned'] and stage['retained_source_inputs']==[] and len(stage['inputs'])==10,'ten maintained source producers')
        for name,digest in stage['inputs'].items():pin(name,digest)
        pin(manifest['stager']['path'],manifest['stager']['sha256'])
        pin(manifest['verifier']['path'],manifest['verifier']['sha256'])
        driver=[]
        for suffix in ('obj','com','map'):
            name='driver.'+suffix;raw=pin(work+'/'+name,receipt['outputs'][name]['sha256'])
            require(len(raw)==receipt['outputs'][name]['bytes'],'driver output size');driver.append(raw)
        for name,digest in stage['outputs'].items():pin(work+'/'+name,digest)
        if index==1:
            require(receipt['pair']==dict(independent_materializations=2,raw_omf_equal=True,raw_com_equal=True,raw_map_equal=True,normalization=False,object_reuse=False,first_run_predeclared_pair=False,second_source_mtimes_declared=True,exact_acceptance=False),'independent driver pair scope')
            require(manifest['first_completion']['path']==DRIVER_RUNS[0]+'/completion.json' and manifest['first_completion']['sha256']==COMPLETIONS[0],'first driver receipt association')
        base,init_row=init_rounds[index];modules={}
        for module in ('launcher','transfer_call','transfer_helper'):
            name=init.WRAPPER_RUN+'/round%d/'%(index+1)+module+'.com';modules[module]=pin(name,inputs[name])
        candidate=base[0x32a2:0x4322];proof=verify(*driver,candidate,decoded[0x32a2:0x4322],scope='all-procedures')
        require(proof['maintained_procedures']==55 and proof['maintained_instruction_bytes']==2844 and proof['target_differing_bytes']==10,'driver boundaries/differences')
        data=compose_driver(modules,base,driver[1])
        differences=[i for i,(a,b) in enumerate(zip(data,decoded)) if a!=b]
        require(len(data)==len(decoded)==22812 and differences==init.DIFFERENCES,'exact ten original target differences')
        rounds.append((data,dict(round=index+1,maintained_init_input=init_row['maintained_init_input'],maintained_driver_input=work+'/driver.com',driver_sha256=sha(driver[1]),com_sha256=sha(data),outside_driver_raw_equal=True,other_payloads_unchanged=4,retained_payloads=3,wrapper_raw_equal=data==base,different_target_offsets=differences)))
        raw_drivers.append(driver)
    require(raw_drivers[0]==raw_drivers[1] and rounds[0][0]==rounds[1][0],'raw independent driver/composition equality')
    for name,raw in frozen.items():require(read_plain(root/name)==raw,'input changed during composition')
    inputs.update({n:sha(v) for n,v in frozen.items()})
    return rounds,inputs

def replay(root,run_id,cached_run):
    require(re.fullmatch(r'[A-Za-z0-9_-]{1,64}',run_id) is not None,'safe run ID required')
    require(cached_run=='sol-zun-launcher-20261006-final','explicit reviewed retained wrapper required')
    rounds,inputs=prepare_pair(root)
    output=Path(root)/'.analysis/zun-driver-wrapper-composition'/run_id
    for p in (output,*output.parents):require(not p.is_symlink(),'symlink output ancestor')
    output.parent.mkdir(exist_ok=True);output.mkdir();runtime=[]
    for number,(data,row) in enumerate(rounds,1):
        with (output/('round%d.com'%number)).open('xb') as f:f.write(data)
        directory=parse_launcher(data,223)
        observations=[dispatch_observation(data,directory,'',''),dispatch_observation(data,directory,' -X','-X')]
        for index in range(1,6):
            observed=dispatch_observation(data,directory,f'  -{index} hello',f'-{index}')
            require(observed['tail']==' hello' and observed['sp']==0xfffc and observed['remaining_count']==6-index and not observed['flags']&0x400,'wrapper dispatch ABI')
            observations.append(observed)
        listing='\r\n'+''.join(' '+p['name'].ljust(8)+' ' for p in directory['payloads'])+'\r\n'
        require(observations[0]['stdout']==listing and observations[1]['stdout']=='No COM-Soft !!!\r\n\n','wrapper text behavior')
        runtime.append(observations)
    broken=bytearray(rounds[0][0]);broken[directory['helper_offset']+4]=1
    try:dispatch_observation(bytes(broken),directory,' -1 hello','-1')
    except ValueError as error:require('missed the payload entry' in str(error),'negative control failure')
    else:raise ValueError('wrong transfer escaped negative control')
    for name,digest in inputs.items():require(sha(read_plain(Path(root)/name))==digest,'retained input changed')
    receipt=dict(kind='th03-zun-maintained-init-driver-retained-wrapper-composition',run_id=run_id,rounds=[r for _,r in rounds],source_inputs=inputs,runtime=runtime,
        native_invocations=0,new_wrapper_cold_build=False,driver_materializations=2,driver_first_run_predeclared_pair=False,
        second_driver_source_mtimes_declared=True,retained_wrapper_modules=True,retained_payloads=3,
        raw_omf_normalization=False,full_decoded_raw_equal=False,different_bytes=10,
        wrapper_integration='-2/-4 retained composition',payload_source_acceptance=False,exact_acceptance=False,
        stored_diet_rebuilt=False,wrong_transfer_address_rejected=True,whole_game_percentage=None)
    with (output/'receipt.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print('PASS maintained -2/-4 composition; three retained payloads/scaffold unchanged; ten target bytes differ: '+str(output))
    return receipt
