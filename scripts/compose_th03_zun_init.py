"""Retained -2-only composition diagnostic. Never assembles or grants acceptance."""
import hashlib,json,os,re,stat,tomllib
from pathlib import Path
from lib.zun import compose_launcher,parse_launcher,dispatch_observation
from verify_th03_zun_init_standalone import verify_outputs,TARGET_SHA
from build_th03_zun_init import SOURCE_SHA,STAGED_SHA
sha=lambda raw:hashlib.sha256(raw).hexdigest()
WRAPPER_RECEIPT='.analysis/th03-zun-launcher/sol-zun-launcher-cached-final-20261006/receipt.json'
WRAPPER_SHA='66a7768581c9ab808afcba4b9f1b958b2ca09464db0147521abb6b0849e5c547'
WRAPPER_RUN='.analysis/th03-zun-launcher/sol-zun-launcher-20261006-final'
INIT_RECEIPT='.analysis/zun-init-cold-continuation-output-20261021-v01/completion.json'
INIT_RECEIPT_SHA='4fb3cf03ef57da9ae3da738f0f650da385b546abb3fff35975760d75449f70c8'
INIT_WORKS=('.analysis/toolchain/wineprefix/drive_c/ZC9467D4','.analysis/toolchain/wineprefix/drive_c/ZCC3A129')
DIFFERENCES=[0x353a,0x353b,0x35ae,0x35af,0x35b0,0x35bf,0x35c0,0x35c1,0x3a53,0x3a54]
def require(ok,message):
    if not ok:raise ValueError(message)
def read_plain(path):
    for p in (path,*path.parents):require(not p.is_symlink(),'symlink input/output')
    before=path.stat();require(stat.S_ISREG(before.st_mode),'regular input required')
    raw=path.read_bytes();after=path.stat()
    require((before.st_dev,before.st_ino,before.st_mode,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_mode,after.st_size,after.st_mtime_ns),'unstable input')
    return raw
def compose_init(modules,scaffold,init_com):
    """Keep the old four unowned payloads and compiled wrapper, replace only -2."""
    require(set(modules)=={'launcher','transfer_call','transfer_helper'},'three maintained wrapper modules')
    old=parse_launcher(scaffold,223);names=[p['name'] for p in old['payloads']]
    require(names==['-1','-2','-3','-4','-5'],'fixed five-payload order')
    selected=old['payloads'][1];start=selected['decoded_file_offset'];end=start+selected['size']
    require(start==0x5c4 and selected['size']==1390 and len(init_com)==1390 and sha(init_com)==TARGET_SHA,'maintained init identity/layout')
    payloads=[scaffold[p['decoded_file_offset']:p['decoded_file_offset']+p['size']] for p in old['payloads']]
    payloads[1]=init_com
    data=compose_launcher(modules['launcher'],modules['transfer_call'],modules['transfer_helper'],names,payloads)
    require(len(data)==len(scaffold) and data[:start]==scaffold[:start] and data[end:]==scaffold[end:],'outside -2 changed')
    require(data[start:end]==init_com,'selected init input not composed')
    require(parse_launcher(data,223)==old,'scaffold metadata changed')
    return data

def prepare_pair(root):
    """Authenticate existing proof and source, then compose both rounds in memory."""
    root=Path(root);frozen={}
    def pin(name,expected=None):
        raw=read_plain(root/name)
        require(expected is None or sha(raw)==expected,'input identity: '+name)
        require(name not in frozen or frozen[name]==raw,'input changed between uses')
        frozen[name]=raw;return raw
    wr=json.loads(pin(WRAPPER_RECEIPT,WRAPPER_SHA));ir=json.loads(pin(INIT_RECEIPT,INIT_RECEIPT_SHA))
    require(wr['cached_candidates_checked'] and not wr['cold_wrapper_checks_pass'] and not wr['exact_acceptance'],'retained wrapper receipt scope')
    require(ir['complete'] and ir['errors']==[] and ir['owned_lock_release_complete'] and not ir['exact_acceptance'] and not ir['wrapper_integration'],'standalone receipt scope')
    require(ir['result']['independent_materializations']==2 and ir['result']['equality']==dict(raw_omf_equal=True,raw_com_equal=True,raw_map_equal=True,normalization=False),'standalone pair equality')
    pin('src/zun/init.asm',SOURCE_SHA)
    config=tomllib.loads(pin('config/th03_zun_launcher.toml',wr['source_inputs']['config/th03_zun_launcher.toml']).decode())
    decoded=pin(config['decoded_path'],wr['decoded_sha256'])
    pin('.analysis/targets/th03/zun.com',wr['stored_sha256'])
    rounds=[];raw_inits=[]
    for number,work in enumerate(INIT_WORKS,1):
        row=wr['rounds'][number-1];modules={}
        for module in ('launcher','transfer_call','transfer_helper'):
            name=f'{WRAPPER_RUN}/round{number}/{module}'
            content={suffix:pin(name+'.'+suffix,wr['source_inputs'][name+'.'+suffix]) for suffix in ('asm','com','obj','map','rsp')}
            source=pin('src/zun/'+module+'.asm',row['source_associations'][module]['maintained_source_sha256'])
            if content['asm']!=source:
                require(module=='launcher' and sha(content['asm'])==config['cached_launcher_before_empty_line_cleanup_sha256'] and content['asm'].count(b'\t\t\n')==1 and content['asm'].replace(b'\t\t\n',b'\n',1)==source,'unreviewed wrapper source association')
            modules[module]=content['com']
        name=f'{WRAPPER_RUN}/round{number}/zun.com';scaffold=pin(name,wr['source_inputs'][name])
        require(sha(scaffold)==config['scaffold_sha256'],'scaffold identity')
        directory=parse_launcher(scaffold,223)
        require([p['sha256'] for p in directory['payloads']]==[p['sha256'] for p in config['payloads']],'other payload identities')
        init=[pin(work+'/init.'+suffix) for suffix in ('obj','com','map')]
        pin(work+'/src/zun/init.asm',STAGED_SHA)
        proof=verify_outputs(*init,decoded[0x5c4:0xb32]);require(proof['omf_sha256']==ir['result']['proofs'][number-1]['omf_sha256'],'init object proof association')
        data=compose_init(modules,scaffold,init[1]);differences=[i for i,(a,b) in enumerate(zip(data,decoded)) if a!=b]
        require(len(data)==len(decoded)==22812 and differences==DIFFERENCES,'ten original -4 differences changed')
        fourth=directory['payloads'][3]
        require(all(fourth['decoded_file_offset']<=i<fourth['decoded_file_offset']+fourth['size'] for i in differences),'difference outside -4')
        rounds.append((data,dict(round=number,maintained_init_input=work+'/init.com',source='src/zun/init.asm',com_sha256=sha(data),init_sha256=sha(init[1]),outside_init_raw_equal=True,other_payloads_unchanged=4,scaffold_raw_equal=data==scaffold,different_target_offsets=differences)))
        raw_inits.append(init)
    require(rounds[0][0]==rounds[1][0] and raw_inits[0]==raw_inits[1],'independent input/composition pair differs')
    for name,raw in frozen.items():require(read_plain(root/name)==raw,'input changed during composition')
    return rounds,{name:sha(raw) for name,raw in frozen.items()}

def replay(root,run_id,cached_run):
    require(re.fullmatch(r'[A-Za-z0-9_-]{1,64}',run_id) is not None,'safe run ID required')
    require(cached_run=='sol-zun-launcher-20261006-final','explicit reviewed retained wrapper required')
    rounds,inputs=prepare_pair(root)
    output=Path(root)/'.analysis/zun-init-wrapper-composition'/run_id
    for p in (output,*output.parents):require(not p.is_symlink(),'symlink output ancestor')
    output.parent.mkdir(exist_ok=True);output.mkdir()
    runtime=[]
    for number,(data,row) in enumerate(rounds,1):
        with (output/('round%d.com'%number)).open('xb') as f:f.write(data)
        directory=parse_launcher(data,223)
        observations=[dispatch_observation(data,directory,'',''),dispatch_observation(data,directory,' -X','-X')]
        for index in range(1,6):
            observed=dispatch_observation(data,directory,f'  -{index} hello',f'-{index}')
            require(observed['tail']==' hello' and observed['sp']==0xfffc and observed['remaining_count']==6-index and not observed['flags']&0x400,'wrapper dispatch ABI')
            observations.append(observed)
        listing='\r\n'+''.join(' '+p['name'].ljust(8)+' ' for p in directory['payloads'])+'\r\n'
        require(observations[0]['stdout']==listing,'procedure listing output')
        require(observations[1]['stdout']=='No COM-Soft !!!\r\n\n','unknown option output')
        runtime.append(observations)
    broken=bytearray(rounds[0][0]);broken[directory['helper_offset']+4]=1
    try:dispatch_observation(bytes(broken),directory,' -1 hello','-1')
    except ValueError as error:require('missed the payload entry' in str(error),'unexpected negative-control failure')
    else:raise ValueError('wrong transfer address escaped negative control')
    for name,digest in inputs.items():require(sha(read_plain(Path(root)/name))==digest,'retained input changed')
    receipt=dict(kind='th03-zun-maintained-init-retained-wrapper-composition',run_id=run_id,rounds=[r for _,r in rounds],source_inputs=inputs,runtime=runtime,native_invocations=0,new_wrapper_cold_build=False,standalone_materializations=2,retained_wrapper_modules=True,raw_omf_normalization=False,full_decoded_raw_equal=False,different_bytes=10,wrapper_integration='-2-only retained composition',payload_source_acceptance=False,exact_acceptance=False,stored_diet_rebuilt=False,wrong_transfer_address_rejected=True,whole_game_percentage=None)
    with (output/'receipt.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    print('PASS maintained -2 composition; other four payloads/scaffold unchanged; ten -4 target bytes still differ: '+str(output))
    return receipt
