"""Complete resident, integer-angle, text, sound and TH03 joystick native ownership."""
import hashlib
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_resident_work import DRIVER,REPORT,BASE,NEW,STATE,PARTS,wrappers,response
from build_th03_mainl_display_work import literal_fields
from lib.decoded_mainl_display_native import externs,root_resolve
from lib.decoded_mainl_file_native import byte_map
from lib.decoded_mainl_root_helpers_layout import OBJECT,WRAPPER,CODE_BASE,DATA_BASE,DS,native as root_native
from lib.mainl_staff_source import statements
from lib.omf import describe_omf,parse_omf
from lib.pc98 import parse_mz
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

PREFIX='th03-mainl-decoded-'
P=lambda n,o,s,r='retf',pop=0,pub=True:(n,o,s,r,pop,pub)
SCOPES=(
 ('root-tail-atan-end',0x175E,114,'iatan2.asm','library',[P('IATAN2',0x175E,107,pop=4),P('JS_END',0x17CA,6)],[0x17C9],2),
 ('root-tail-sound-text',0x1EF6,116,'soundio.asm','library',[P('SOUND_O',0x1EF6,22,'ret',pub=False),P('SOUND_I',0x1F0C,20,'ret',pub=False),P('TEXT_CLEAR',0x1F20,17),P('TEXT_FILLCA',0x1F32,55,pop=4)],[0x1F31,0x1F69],1),
 ('root-tail-resident',0x276E,226,'respal_exist.asm','library',[P('RESPAL_EXIST',0x276E,60),P('RESPAL_CREATE',0x27AA,117),P('RESPAL_SET_PALETTES',0x2820,47)],[0x281F,0x284F],7),
 ('root-tail-joystick',0x2AAE,42,'js_start.asm','authored',[P('JS_START',0x2AAE,41)],[0x2AD7],1),
 ('root-tail-sound-joy',0x2AD8,18,'js_sense.asm','library',[P('SOUND_JOY',0x2AD8,17,'ret',pub=False)],[0x2AE9],0),
 ('root-tail-js-sense',0x2AEA,34,'js_sense.asm','authored',[P('JS_SENSE',0x2AEA,33)],[0x2B0B],2),
 ('root-tail-sajout',0x2B0C,9,'js_sense.asm','library',[P('SAJOUT',0x2B0C,9,'ret',pub=False)],[],0),
)
DATA=(('resident-signature',0x882,10,BASE+'resident_signature.inl','resident'),('joystick-initialized-data',0x570,8,BASE+'joystick_initialized.inl','joystick'))
DATA_SOURCES={PREFIX+n:src for n,_,_,src,_ in DATA}
PRIVATE={'SOUND_O':(0,0x1EF6),'SOUND_I':(0,0x1F0C)}
COMMON=['ReC98.inc','libs/master.lib/func.inc','libs/master.lib/super.inc','libs/master.lib/bgm.inc','libs/master.lib/pf.inc',
        'libs/master.lib/clip.inc','libs/master.lib/macros.inc','libs/kaja/kaja.inc','twobyte.inc','pc98.inc','th01/hardware/egc.inc','th02/formats/pi_slots.inc']


def need(v,message):
    if not v:raise ValueError('MAINL resident native: '+str(message))


def sha(b):return hashlib.sha256(b).hexdigest()


def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and not r['root_rebuilt'] and not r['whole_product_cold_rebuilt'] and
         r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and
         r['source_sha256']=={n:sha((root/n).read_bytes()) for n in NEW+STATE},'maintained bounded source/recipe/unchanged cold bindings')
    need(all((root/f'.analysis/work/resident-mini-{n}.asm').read_bytes()==b for n,b in wrappers().items()) and
         (root/'.analysis/work/resident-mini.lnk').read_bytes()==response(),'preserved complete native source and link inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t','/dGAME=3']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x','tlink']
    schedule=[]
    for number in (1,2):
        schedule += [(f'round{number}-{n}',tasm+[rf'probe\rsm-{n}.asm',rf'probe\rsm-{n}.obj'],0) for n in PARTS]
        schedule += [(f'round{number}-link',dos+[r'@probe\rsmini.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==schedule,'actual serial two-round assembly/link schedule')
    need([v['round'] for v in r['rounds']]==[1,2],'two actual complete native vectors')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={*PARTS,'exe','map'},'complete six-OBJ/EXE/MAP vector');vector={}
        for name,meta in row['outputs'].items():
            b=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),'current complete raw native output');vector[name]=b
        vectors.append(vector)
    need(vectors[0]==vectors[1],'whole raw native repetition')
    extras={
      'context':[STATE[0],'libs/master.lib/tx[data].asm','libs/master.lib/atan8[data].asm',*[src for src,_,_ in PARTS['context']],STATE[1]],
      'resident':[BASE+'resident_signature.inl',BASE+'respal_exist.inl',BASE+'resident_mcb.inc',BASE+'respal_set_palettes.asm'],
      'create':[BASE+'respal_create.inl',BASE+'resident_mcb.inc'],
      'sound':[src for src,_,_ in PARTS['sound']],
      'joystick':[BASE+'joystick_initialized.inl',*[src for src,_,_ in PARTS['joystick']],BASE+'joystick_uninitialized.inl'],
      'end':[BASE+'js_end.inl'],
    }
    for name in PARTS:
        d=describe_omf(vectors[0][name]);module=rf'probe\rsm-{name}.asm'
        need(d['valid'] and d['module_name']==module and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
             d['dependency_paths']==[module,*COMMON,*extras[name]],'complete real native dependency closure')
        for src in COMMON+extras[name]:
            if src not in NEW+STATE:need(files[src]==(work/src).read_bytes(),'unchanged actual cold source dependency')
    old=files[BASE+'respal_exist.asm'].replace(b'\r\n',b'\n');begin=old.index(b'func RESPAL_EXIST');create=old.index(b'func RESPAL_CREATE')
    strip=lambda p:(root/p).read_bytes().replace(b'include src/mainl/root_tail/resident_mcb.inc\n',b'')
    need(statements(old[begin:create])==statements(strip(BASE+'respal_exist.inl')) and
         statements(old[create:].replace(b'if GAME ge 2\n\tnop\nendif\n',b''))==statements(strip(BASE+'respal_create.inl')),'complete original resident bodies,only compatibility NOP guard removed')
    need(statements(files[BASE+'js_end.asm'].replace(b'nopcall',b'call'))==statements((root/(BASE+'js_end.inl')).read_bytes()),'only ordinary call replaces JS_END compatibility macro')
    need(statements((root/(BASE+'joystick_initialized.inl')).read_bytes())==statements(files['libs/master.lib/js[data].asm']) and
         statements((root/(BASE+'joystick_uninitialized.inl')).read_bytes())==statements(files['libs/master.lib/js[bss].asm']),'complete original typed joystick state')
    compact=lambda b:[b''.join(t).upper() for t in statements(b)]
    need(compact((root/(BASE+'resident_mcb.inc')).read_bytes())==[b'_MCB_FLGEQU0',b'_MCB_OWNEREQU1',b'_MCB_SIZEEQU3',b'IDLENEQU10'],'original DOS MCB offsets and signature length')
    return vectors[0],r,sha(raw)


def native_modules(minis,table,target,candidate):
    linked=parse_mz(minis['exe']);mt=minis['map'].decode();need(linked.valid and len(linked.program_image)==914 and not linked.relocations,'complete native mini MZ and literal empty relocation vector')
    ds=address(mt,'ResPalID')[0];need(ds==0x24,'actual native DS paragraph')
    alloc={};cursor=0
    data_sizes={'context':320,'resident':10,'create':0,'sound':0,'joystick':8,'end':0}
    for name,parts in PARTS.items():
        cursor=(cursor+1)&~1;size=sum(s for _,_,s in parts);data_size=data_sizes[name]
        raw=minis[name];segs=[r for r in parse_omf(raw) if r.name=='SEGDEF']
        sizes=[size,data_size]+([32,48] if name=='context' else [4] if name=='joystick' else [])
        need([int.from_bytes(r.data[1:3],'little') for r in segs]==sizes and [r.data[0] for r in segs]==([0x48,0x48,0x74,0x48] if name=='context' else [0x48]*len(sizes)),'complete native WORD geometry and real uninitialized stack/BSS')
        group='0aff04ff03ff02' if name=='context' else '08ff03ff02' if name=='joystick' else '06ff02'
        need([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF']==[group],'literal native mini DGROUP membership')
        match,=re.findall(rf'(?m)^\s*0000:([0-9A-F]{{4}})\s+{size:04X}\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=probe\\rsm-{name}\.asm\s+ACBP=48\s*$',mt)
        need(int(match,16)==cursor,'actual complete module order and WORD-aligned CODE base')
        data,=re.findall(rf'(?m)^\s*{ds:04X}:([0-9A-F]{{4}})\s+{data_size:04X}\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=probe\\rsm-{name}\.asm\s+ACBP=48\s*$',mt)
        alloc[name]=dict(code=cursor,data=int(data,16),size=size);cursor+=size
        if name in ('context','joystick'):
            bi=4 if name=='context' else 3;count=48 if name=='context' else 4
            bss,=re.findall(rf'(?m)^\s*{ds:04X}:([0-9A-F]{{4}})\s+{count:04X}\s+C=BSS\s+S=_BSS\s+G=DGROUP\s+M=probe\\rsm-{name}\.asm\s+ACBP=48\s*$',mt)
            alloc[name]['bss']=int(bss,16);need(not byte_map(raw,bi),'no invented BSS file initializer')
    need(cursor==566 and linked.program_image[0x22F]==0,'real one-byte inter-module WORD gap after joystick103,not source storage')
    def product_code(name,off):
        local=0
        for _,start,size in PARTS[name]:
            if local<=off<local+size:return start+off-local
            local+=size
        raise ValueError('no complete product code owner for native field')
    def own(name,segment,offset,mode):
        if mode=='mini':
            return (0,alloc[name]['code']+offset) if segment==1 else (ds,alloc[name]['data' if segment==2 else 'bss']+offset)
        if segment==1:return 0,product_code(name,offset)
        if name=='context' and segment==2:
            for local,size,start in ((0,56,0x578),(56,8,0x83C),(64,256,0x41C)):
                if local<=offset<local+size:return DS,start+offset-local
        if name=='resident' and segment==2:return DS,0x882+offset
        if name=='joystick':return DS,(0x570 if segment==2 else 0x141A)+offset
        raise ValueError('no actual local native DATA/BSS owner')
    details=[];far_calls=[]
    for name in PARTS:
        raw=minis[name];size=alloc[name]['size'];data=byte_map(raw,1);need(set(data)==set(range(size)),'complete native CODE coverage')
        names=externs(raw)
        def resolve(mode):
            image=bytearray(data[i] for i in range(size));observed=[];far=[]
            for f in literal_fields(raw):
                need(f['segment']==1 and f['site']+f['width']<=size,'complete CODE native field')
                site=f['site'];actual=own(name,1,site,mode)[1]
                if f['target_method']==0:seg,off=own(name,f['target'],f['addend'],mode);symbol='own segment'
                else:
                    need(f['target_method']==2,'actual external field');symbol=names[f['target']-1]
                    seg,off=PRIVATE[symbol] if mode=='product' and symbol in PRIVATE else address(mt if mode=='mini' else table,symbol)
                    off+=f['addend']
                if f['location_type']==3:
                    need(f['target_method']==2 and f['frame_method']==5 and f['segment_relative'] and seg==0 and f['addend']==0 and image[site-1:site+4]==b'\x9a\0\0\0\0','ordinary actual external far call')
                    image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(actual+4))&65535).to_bytes(2,'little');far.append(dict(site=actual-1,symbol=symbol,target=off))
                else:
                    need(f['location_type']==1 and f['width']==2,'native offset WORD')
                    if f['segment_relative']:
                        need((f['frame_method'],f['frame'],seg)==(1,1,ds if mode=='mini' else DS),'genuine DGROUP offset field');value=off
                    else:
                        need((f['frame_method'],f['frame'],seg)==(0,1,0),'actual same-CODE near call');value=(off-actual-2)&65535
                    image[site:site+2]=value.to_bytes(2,'little')
                observed.append(dict(f,symbol=symbol,resolved_target=[seg,off],product_site=actual))
            return bytes(image),observed,far
        image,_,_=resolve('mini');start=alloc[name]['code'];need(image==linked.program_image[start:start+size],'complete independently resolved actual mini CODE')
        image,fields,far=resolve('product');far_calls+=far;local=0
        for _,start,size in PARTS[name]:extent((target,candidate),image[local:local+size],0,start,[]);local+=size
        emitted=byte_map(raw,2);need(set(emitted)==set(range(data_sizes[name])),'complete native DATA coverage')
        native_data=bytes(emitted[i] for i in range(len(emitted)));start=ds*16+alloc[name]['data']
        need(native_data==linked.program_image[start:start+len(native_data)],'complete emitted mini DATA')
        details.append(dict(name=name,fields=fields,code_bytes=alloc[name]['size'],data_bytes=len(emitted)))
    need(sum(len(d['fields']) for d in details)==18 and far_calls==[dict(site=0x27AC,symbol='RESPAL_EXIST',target=0x276E),dict(site=0x17CA,symbol='DOS_KEYCLEAR',target=0x6FE)],'all18 module fields and both ordinary FAR call relaxations')
    need(address(mt,'SOUND_O')==(0,alloc['sound']['code']) and address(mt,'SOUND_I')==(0,alloc['sound']['code']+22),'actual exported private near provider identities')
    return dict(modules=6,rounds=2,native_modules=details,far_calls=far_calls,ordered_relocations=[],native_source_padding_added=False,
        linked_WORD_gap_after_joystick103=True,BSS_file_byte_credit=0,uncredited_product_gap_offsets=[0x2AAD,0x2B15])


def verify(root,work,target,candidate,graph,files):
    minis,report,report_sha=selected(root,work,files)
    raw=(work/OBJECT).read_bytes();root_native(raw);table=(work/'obj/th03/mainl.map').read_text()
    row,=[r for r in graph if r['output']==OBJECT];need((row['source'],row['game'],row['binary'])==(WRAPPER,3,'L'),'actual root include producer')
    for leaf in ('iatan2.asm','js_end.asm','soundio.asm','text_clear.asm','text_fillca.asm','respal_exist.asm','respal_set_palettes.asm','js_start.asm','js_sense.asm'):
        src=BASE+leaf;need(files[src]==(work/src).read_bytes() and files[src].replace(b'\r\n',b'\n')==(root/src).read_bytes().replace(b'\r\n',b'\n') and
            ('include '+src).encode() in files[WRAPPER] and statements(files[src])==statements(files['libs/master.lib/'+leaf]),'complete original library/game provider and maintained root source transport')
    mini=native_modules(minis,table,target,candidate);linked=parse_mz((work/'bin/th03/mainl.exe').read_bytes());owners=[];scopes=[]
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    for unit,start,size,leaf,origin,procs,evens,count in SCOPES:
        image,fields,mz=root_resolve(raw,start,size,linked);need(len(fields)==count and not mz,'complete root offset fields and empty literal scoped MZ')
        extent((target,candidate),image,0,start,[]);ins=list(decoder.disasm(image,start));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==size,'complete dense instructions')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'every static local branch enters a complete instruction')
        procedures=[]
        for symbol,off,length,ret,pop,pub in procs:
            body=[i for i in ins if off<=i.address<off+length]
            need(sum(i.size for i in body)==length and body[-1].mnemonic==ret and (int(body[-1].op_str,0) if body[-1].op_str else 0)==pop,'complete body and near/far Pascal cleanup')
            if pub:need((off-CODE_BASE,symbol) in code_publics(raw,1) and address(table,symbol)==(0,off),'actual public entry in native and both MAP tables')
            procedures.append(dict(name=symbol,offset=off-start,size=length,return_kind=ret,callee_pop_bytes=pop,public=pub))
        need(sum(p['size'] for p in procedures)+len(evens)==size and all(next(i for i in ins if i.address==off).mnemonic=='nop' for off in evens),'disjoint bodies and genuine outer EVEN partition')
        owners.append(owner(PREFIX+unit,BASE+leaf,origin,0,start,image,procedures))
        scopes.append(dict(unit_id=PREFIX+unit,fields=fields,outer_EVEN_bytes=evens,ordered_relocations=[]))
    data=byte_map(raw,2)
    for unit,off,size,src,module in DATA:
        image=bytes(data[i] for i in range(off-DATA_BASE,off-DATA_BASE+size));native=byte_map(minis[module],2)
        need(image==bytes(native[i] for i in range(size))==(b'pal98 grb\0' if module=='resident' else b'\0'*8),'complete semantic signature/joystick initialized DATA')
        extent((target,candidate),image,DS,off,[]);o=owner(PREFIX+unit,src,'library',DS,off,image,[])
        o['maintained_native_object']=report['rounds'][0]['outputs'][module]['path'];owners.append(o)
    for symbol,off in [('ResPalID',0x882),('js_bexist',0x570),('js_saj_port',0x572),('js_2player',0x574),('js_shift',0x576),('js_stat',0x141A)]:
        need(address(table,symbol)==(DS,off),'actual resident/joystick state MAP entry')
        if symbol!='ResPalID':need(address(table,'_'+symbol)==(DS,off),'both C/ASM joystick state aliases')
    need(not byte_map(raw,9) and not byte_map(minis['joystick'],3),'original joystick4 BSS has no initializer')
    for off in (0x2AAD,0x2B15):need(target.program_image[off]==candidate.program_image[off]==0 and all(not(o['segment']==0 and o['offset']<=off<o['offset']+o['size']) for o in owners),'legacy zero bytes excluded from every code owner')
    owners[0]['maintained_native_sources']=[BASE+'iatan2.asm',BASE+'js_end.inl']
    owners[2]['maintained_native_sources']=[BASE+'respal_exist.inl',BASE+'respal_create.inl',BASE+'respal_set_palettes.asm']
    return dict(owners=owners,source_CODE_bytes=sum(o['code_bytes'] for o in owners),source_initialized_DATA_bytes=sum(o['initialized_data_bytes'] for o in owners),procedures=sum(o['procedure_count'] for o in owners),authored_CODE_bytes=sum(o['code_bytes'] for o in owners if o['origin']=='authored'),library_bytes=sum(o['size'] for o in owners if o['origin']=='library'),
        native_scopes=scopes,independent_native_modules=mini,selected_build_report_sha256=report_sha,
        joystick_BSS_bytes=4,BSS_file_byte_credit=0,uncredited_legacy_zero_bytes=[0x2AAD,0x2B15],
        original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_hardware_execution_claimed=False,whole_product_accepted=False)


def owner(unit,src,origin,seg,off,image,procs):
    return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=src,object=OBJECT,origin=origin,segment=seg,offset=off,start=seg*16+off,
        size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),
        ordered_relocations=[],code_bytes=len(image) if seg==0 else 0,initialized_data_bytes=len(image) if seg==DS else 0,
        procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,
        abi='original16-bit Pascal far APIs,private register-ABI near sound/SAJ helpers and unchecked DOS/BIOS behavior')


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['resident_native'],indent=2))
