"""Palette, VSync IRQ and gaiji ownership with natural native call production."""
import hashlib
import json
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM,X86_REG_CS
from build_th03_mainl_display_work import (STATE,NATURAL,CONTEXT,CONTEXT_STATE,SUBJECTS,DATA_EXTERN,DRIVER,REPORT,
    wrapper,response,mini_wrappers,mini_response,literal_fields,equivalent_root,payload)
from lib.omf import parse_omf,describe_omf
from lib.pc98 import parse_mz
from lib.decoded_mainl_file_native import byte_map
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.mainl_staff_source import statements
from lib.decoded_mainl_root_helpers_layout import native as root_native,OBJECT,WRAPPER,CODE_BASE,DATA_BASE,DS
from probe_th03_main_boss_marisa_cpp import code_publics

PREFIX='th03-mainl-decoded-'
DATA=(('palette-initialized-data',0x578,56,STATE[0][1]),('vsync-initialized-data',0x842,7,STATE[2][1]),
      ('gaiji-backup-data',0x55A,2,STATE[5][1]),('gaiji-dimensions-data',0x55C,8,STATE[6][1]))
DATA_SOURCES={PREFIX+n:src for n,_,_,src in DATA}
P=lambda name,off,size,pop=0,ret='retf',public=True:(name,off,size,pop,ret,public)
SCOPES=(
 ('palette-black-fades',0x536,130,['palette_black_in','palette_black_out'],[P('PALETTE_BLACK_IN',0x536,67,2),P('PALETTE_BLACK_OUT',0x57A,62,2)],[0x579],7),
 ('palette-show',0x17D0,266,['palette_show'],[P('PALETTE_SHOW',0x17D0,266)],[],4),
 ('palette-rgb',0x1A68,66,['palette_entry_rgb'],[P('PALETTE_ENTRY_RGB',0x1A68,66,4)],[],3),
 ('palette-wait-white-fades',0x2064,166,['vsync_wait','palette_white_in','palette_white_out'],[P('VSYNC_WAIT',0x2064,38),P('PALETTE_WHITE_IN',0x208A,63,2),P('PALETTE_WHITE_OUT',0x20CA,64,2)],[0x20C9],11),
 ('vsync-library',0x1F6A,250,['vsync'],[P('VSYNC_START',0x1F6E,106),P('CRTBIOS_COOK',0x1FD8,9,ret='iret',public=False),P('VSYNC_COUNT',0x1FE2,58,ret='iret',public=False),P('VSYNC_END',0x201C,71)],[0x1FE1,0x2063],27),
 ('dos-setvect',0x704,32,['dos_setvect'],[P('DOS_SETVECT',0x704,31,6)],[0x723],0),
 ('dos-close',0xA98,22,['../resources/dos_close'],[P('DOS_CLOSE',0xA98,21,2)],[0xAAD],0),
 ('gaiji-backup',0xC72,64,['gaiji_backup'],[P('GAIJI_BACKUP',0xC72,36),P('GAIJI_RESTORE',0xC96,28)],[],4),
 ('gaiji-load',0xCB2,150,['gaiji_entry_bfnt'],[P('GAIJI_ENTRY_BFNT',0xCB2,150,4)],[],1),
 ('gaiji-read',0xD48,108,['gaiji_read'],[P('GETFONTW',0xD48,33,ret='ret',public=False),P('GAIJI_READ',0xD6A,37,6),P('GAIJI_READ_ALL',0xD90,36,4)],[0xD69,0xD8F],0),
 ('gaiji-write',0xDB4,112,['gaiji_write'],[P('SETFONTW',0xDB4,33,ret='ret',public=False),P('GAIJI_WRITE',0xDD6,39,6),P('GAIJI_WRITE_ALL',0xDFE,38,4)],[0xDD5,0xDFD],0),
)


def need(value,message):
    if not value:
        raise ValueError('MAINL display native: '+str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(name):
    return 'src/mainl/resources/dos_close.asm' if name.startswith('../') else 'src/mainl/display_hardware/'+name+'.asm'


def selected_pair(root, work, files):
    report_raw = (root / REPORT).read_bytes()
    report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == {n: sha((root / n).read_bytes()) for n in list(dict.fromkeys([n for _,n in STATE]+list(NATURAL.values())+CONTEXT_STATE))}, 'complete maintained state/recipe/cold context binding')
    generated, link = wrapper(files), response(files)
    need(report['wrapper_sha256'] == sha(generated) and report['response_sha256'] == sha(link) and
         (root / '.analysis/work/display-root.asm').read_bytes() == generated and
         (root / '.analysis/work/display-root.lnk').read_bytes() == link, 'actual include and unchanged link position')
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    prefix = root / config['paths']['wine_prefix']
    tasm = ['/usr/bin/wine-stable', str(prefix/'drive_c/TASM50/bin/TASM32.EXE'), '/m','/mx','/kh32768','/t','/dGAME=3']
    dos = ['/usr/bin/wine-stable', str(root/config['paths']['msdos_player']), '-e','-x','tlink']
    commands = []
    for n in (1,2):
        commands += [(f'round{n}-assemble',tasm+[WRAPPER,r'probe\dpyroot.obj'],0),
                     (f'round{n}-link',dos+[r'@probe\dpyroot.lnk'],0)]
        commands += [(f'round{n}-mini-{name}',tasm+[rf'probe\dpy-{name}.asm',rf'probe\dpy-{name}.obj'],0) for name in mini_wrappers()]
        commands += [(f'round{n}-mini-link',dos+[r'@probe\dpymini.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in report['native_phases']] == commands, 'two actual root and native far-call module schedules')
    need([r['round'] for r in report['rounds']] == [1, 2], 'two complete selected output vectors')
    rounds = []
    for row in report['rounds']:
        outputs = {}
        need(set(row['outputs']) == {'obj', 'exe', 'map'}, 'whole selected vector')
        for kind, info in row['outputs'].items():
            raw = (root / info['path']).read_bytes()
            need(info['bytes'] == len(raw) and info['sha256'] == sha(raw), 'current selected raw output')
            outputs[kind] = raw
        need(outputs['exe'] == (work / 'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map'] == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP equality')
        rounds.append(outputs)
    need(rounds[0] == rounds[1], 'complete raw selected OBJ/EXE/MAP repeat equality')
    raw, baseline = rounds[0]['obj'], (work / OBJECT).read_bytes()
    need(equivalent_root(raw,baseline),
         'literal native payload/fixup order and complete public identity')
    description = describe_omf(raw)
    replacements = {old:new for index,(old,new) in enumerate(STATE) if index != 2}
    need(description['valid'] and description['module_name'] == WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['dependency_paths'] == [replacements.get(n, n) for n in describe_omf(baseline)['dependency_paths']],
         'actual maintained state/body includes and complete native dependency closure')
    for index in (1,3,4,5,6):
        old,new = STATE[index]
        need(statements(files[old]) == statements((root/new).read_bytes()), 'complete original typed display/BSS declarations')
    for name,src in NATURAL.items():
        old = files['src/mainl/display_hardware/'+name+'.asm'].replace(b'\r\n',b'\n').replace(b'nopcall\t',b'call\t')
        if name == 'palette_show':
            old = old.replace(b'\torg $-1\nPALSHOW_XORVAL\tdb ?',b'PALSHOW_XORVAL EQU $-1')
            old = old.replace(b'mov\tCS:PALSHOW_XORVAL,AL',b'mov\tbyte ptr CS:[PALSHOW_XORVAL],AL')
        need(statements(old) == statements((root/src).read_bytes()), 'only natural call/operand-alias source transformations: '+name)
    compact = lambda b:tuple(b''.join(row).upper() for row in statements(b))
    need(compact(files['libs/master.lib/vs[data].asm']) == compact((root/STATE[2][1]).read_bytes()), 'ordinary original VSync state and EVEN intent; root090 gap remains contextual')
    need(all((root/f'.analysis/work/display-mini-{name}.asm').read_bytes() == content for name,content in mini_wrappers().items()) and
         (root/'.analysis/work/display-mini.lnk').read_bytes() == mini_response(), 'actual preserved standalone native source and response inputs')
    need([r['round'] for r in report['mini_rounds']] == [1,2], 'two independent far-call module vectors')
    vectors = []
    for row in report['mini_rounds']:
        need(set(row['outputs']) == {*mini_wrappers(),'exe','map'}, 'complete real display-module mini outputs')
        vector = {}
        for name,meta in row['outputs'].items():
            data = (root/meta['path']).read_bytes()
            need((len(data),sha(data)) == (meta['bytes'],meta['sha256']), 'current raw mini output')
            vector[name] = data
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'whole native mini OBJ/EXE/MAP repetition')
    common = ['ReC98.inc','libs/master.lib/func.inc','libs/master.lib/super.inc','libs/master.lib/bgm.inc','libs/master.lib/pf.inc',
              'libs/master.lib/clip.inc','libs/master.lib/macros.inc','libs/kaja/kaja.inc','twobyte.inc','pc98.inc','th01/hardware/egc.inc','th02/formats/pi_slots.inc']
    extras = {'context':['src/mainl/'+n for n,_,_ in CONTEXT]+[STATE[0][1],STATE[2][1],CONTEXT_STATE[0],
        'libs/master.lib/tx[data].asm','libs/master.lib/bfnt_id[data].asm','libs/master.lib/dos_ropen[data].asm',
        STATE[1][1],STATE[3][1],STATE[4][1],CONTEXT_STATE[1]]}
    for name in SUBJECTS:
        extras[name] = ([STATE[5][1]] if name == 'gaiji_backup' else [STATE[6][1]] if name == 'gaiji_entry_bfnt' else [])+[NATURAL[name]]
    for name in mini_wrappers():
        d = describe_omf(vectors[0][name]);module = rf'probe\dpy-{name}.asm'
        need(d['valid'] and d['module_name'] == module and d['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
             d['dependency_paths'] == [module,*common,*extras[name]], 'actual complete native mini dependency closure')
    return raw,vectors[0],report,sha(report_raw)


def externs(raw):
    names=[]
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n
                need(r.data[at]==0,'native untyped external symbol');at+=1
    return names


def mini_proof(minis,table,target,candidate):
    linked=parse_mz(minis['exe']);mt=minis['map'].decode()
    need(linked.valid and len(linked.program_image)==2386,'complete native display mini MZ')
    ds=address(mt,'PaletteTone')[0]
    allocations={};cursor=0
    for name in mini_wrappers():
        size=sum(n for _,_,n in CONTEXT) if name=='context' else SUBJECTS[name][1]
        data_size=88 if name=='context' else 2 if name=='gaiji_backup' else 8 if name=='gaiji_entry_bfnt' else 0
        records=list(parse_omf(minis[name]));segs=[r.data for r in records if r.name=='SEGDEF']
        need([int.from_bytes(r[1:3],'little') for r in segs]==([size,data_size,32,66] if name=='context' else [size,data_size]) and
             [r[0] for r in segs]==([0x48,0x48,0x74,0x48] if name=='context' else [0x48,0x48]),'complete native WORD code/data and uninitialized storage')
        need([r.data for r in records if r.name=='GRPDEF']==[bytes.fromhex('0aff04ff03ff02') if name=='context' else bytes.fromhex('06ff02')],'literal native mini group identity')
        match,=re.findall(rf'(?m)^\s*0000:([0-9A-F]{{4}})\s+{size:04X}\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=probe\\dpy-{name}\.asm\s+ACBP=48\s*$',mt)
        need(int(match,16)==cursor,'complete module order and actual code bases')
        data_match,=re.findall(rf'(?m)^\s*{ds:04X}:([0-9A-F]{{4}})\s+{data_size:04X}\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=probe\\dpy-{name}\.asm\s+ACBP=48\s*$',mt)
        allocations[name]=dict(code=cursor,size=size,data=int(data_match,16),data_size=data_size);cursor+=size
    bss,=re.findall(rf'(?m)^\s*{ds:04X}:([0-9A-F]{{4}})\s+0042\s+C=BSS\s+S=_BSS\s+G=DGROUP\s+M=probe\\dpy-context\.asm\s+ACBP=48\s*$',mt)
    bss=int(bss,16)
    need(cursor==2276 and allocations['context']['data']==0 and not byte_map(minis['context'],3) and not byte_map(minis['context'],4),'real mini CODE extent and no stack/BSS file credit')
    def project(name,segment,offset,mode):
        if mode=='mini':
            if segment==1:return 0,allocations[name]['code']+offset
            if segment==2:return ds,allocations[name]['data']+offset
            need(name=='context' and segment==4,'actual containing BSS member')
            return ds,bss+offset
        if segment==1:
            need(name!='context','context CODE is verified at its real mini layout, not re-laid out into product')
            return 0,SUBJECTS[name][0]+offset
        need(segment==2 and name in ('gaiji_backup','gaiji_entry_bfnt'),'actual private DATA member')
        return DS,(0x55A if name=='gaiji_backup' else 0x55C)+offset
    def resolve_module(name,mode):
        raw=minis[name];size=allocations[name]['size'];data=byte_map(raw,1)
        holes=set(range(4)) if name=='vsync' else set()
        need(set(data)==set(range(size))-holes,'complete native initializer coverage; only original CS vector WORDs uninitialized')
        code_base=allocations[name]['code']
        image=bytearray(data[i] if i in data else linked.program_image[code_base+i] for i in range(size))
        originals=bytes(image);names=externs(raw);relocs=[];far=[];details=[]
        for f in literal_fields(raw):
            need(f['segment']==1,'code-only native mini field stream')
            site=f['site'];kind=f['location_type'];value=None
            need(site+f['width']<=size,'whole native mini field')
            if f['target_method']==0:
                seg,off=project(name,f['target'],f['addend'],mode)
            elif f['target_method']==2:
                symbol=names[f['target']-1]
                seg,off=address(mt if mode=='mini' else table,symbol)
                off+=f['addend']
            else:
                need(f['target']==1 and kind==2 and f['addend']==0,'actual native DGROUP segment field')
                seg,off=(ds if mode=='mini' else DS),0
            actual=project(name,1,site,mode)[1]
            if kind==3:
                need(f['target_method']==2 and f['frame_method']==5 and f['segment_relative'] and seg==0 and
                     originals[site-1:site+4]==b'\x9a\0\0\0\0','ordinary complete external far CALL with zero native addend')
                image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(actual+4))&65535).to_bytes(2,'little')
                far.append(dict(site=actual-1,symbol=names[f['target']-1],target=off))
            elif kind==2:
                need(f['target_method']==1 and f['frame_method']==5,'sole explicit group segment load')
                image[site:site+2]=seg.to_bytes(2,'little');relocs.append([0,actual])
            else:
                need(kind==1 and f['width']==2,'complete native offset WORD')
                if f['segment_relative']:
                    need(seg in (0,ds if mode=='mini' else DS),'same code or DGROUP offset frame')
                    value=off
                else:
                    need(seg==0,'self-relative native near CALL destination')
                    value=(off-(actual+2))&65535
                image[site:site+2]=value.to_bytes(2,'little')
            details.append(dict(site=actual,location_type=kind,target_method=f['target_method'],target=f['target']))
        return bytes(image),relocs,far,details
    mz=[];far_calls=[];all_details=[]
    for name in mini_wrappers():
        code,relocs,far,details=resolve_module(name,'mini')
        start=allocations[name]['code'];need(code==linked.program_image[start:start+len(code)],'independently resolved complete native mini CODE')
        mz+=relocs;all_details+=details
        data=byte_map(minis[name],2)
        need(set(data)==set(range(allocations[name]['data_size'])),'complete native mini DATA coverage')
        begin=ds*16+allocations[name]['data']
        need(bytes(data[i] for i in range(len(data)))==linked.program_image[begin:begin+len(data)],'whole emitted native mini DATA')
        if name in SUBJECTS:
            code,relocs,far,_=resolve_module(name,'product')
            extent((target,candidate),code,0,SUBJECTS[name][0],relocs)
            far_calls+=far
    need([[r.segment,r.offset] for r in linked.relocations]==mz and mz==[[0,allocations['vsync']['code']+123]],'complete literal ordered mini MZ vector')
    need(len(far_calls)==19,'all nineteen compatibility calls independently produced as ordinary far calls')
    return dict(modules=6,rounds=2,far_calls=far_calls,native_mini_fields=all_details,ordered_MZ=mz,
        CS_vector_storage_bytes=4,CS_vector_has_native_initializer=False,CS_vector_bytes_from_real_repeated_link=True,
        source_padding_added=False,context_runtime_execution_claimed=False,uncredited_root_DATA_gap=[DS,0x849,1])


def root_resolve(raw,start,size,linked,holes=()):
    data=byte_map(raw,1);missing={i for i in range(start,start+size) if i-CODE_BASE not in data}
    need(missing==set(holes),'complete root native coverage except original saved-vector storage')
    image=bytearray(data[i-CODE_BASE] if i-CODE_BASE in data else linked.program_image[i] for i in range(start,start+size));fields=[];mz=[]
    for f in literal_fields(raw):
        if f['segment']!=1:continue
        site=CODE_BASE+f['site'];width=f['width']
        if not start<=site<start+size:
            need(not any(site<b<site+width for b in (start,start+size)),'no straddling root field');continue
        need(width==2 and f['segment_relative'] and not set(range(site,site+2))&set(holes),'whole emitted root WORD field')
        if f['location_type']==2:
            need((f['target_method'],f['target'],f['frame_method'],f['addend'])==(1,1,5,0),'actual root DGROUP segment load')
            value=DS;mz.append([0,site])
        else:
            need(f['location_type']==1 and f['target_method']==0 and f['target'] in (1,2,9),'actual own CODE/DATA/BSS offset field')
            value={1:CODE_BASE,2:DATA_BASE,9:0x13F6}[f['target']]+f['addend']
        image[site-start:site-start+2]=value.to_bytes(2,'little');fields.append(dict(f,site=site,value=value))
    return bytes(image),fields,mz


def verify(root,work,target,candidate,graph,files):
    raw,minis,report,report_sha=selected_pair(root,work,files)
    root_native((work/OBJECT).read_bytes())  # Existing helper records bind the unchanged cold carrier's packet layout.
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['kind'],row['game'],row['binary'])==(WRAPPER,WRAPPER,'tasm',3,'L'),'actual containing root producer')
    for name in {n for s in SCOPES for n in s[3]}:
        src=source(name)
        need(files[WRAPPER].count(('include '+src).encode())==1 and files[src]==(work/src).read_bytes() and
             files[src].replace(b'\r\n',b'\n')==(root/src).read_bytes().replace(b'\r\n',b'\n') and
             statements(files[src])==statements(files['libs/master.lib/'+src.rsplit('/',1)[1]]),'complete actual original library provider')
    table=(work/'obj/th03/mainl.map').read_text()
    for cls,base,size,name,seg,group in (('CODE',CODE_BASE,10944,'_TEXT',0,'(none)'),('DATA',DATA_BASE,2036,'_DATA',DS,'DGROUP'),('BSS',0x13F6,5108,'_BSS',DS,'DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$',table))==1,'complete native containing segment/group layout')
    mini=mini_proof(minis,table,target,candidate)
    linked=parse_mz((root/report['rounds'][0]['outputs']['exe']['path']).read_bytes())
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    owners=[];native=[];instructions=[]
    for unit,start,size,names,procs,evens,count in SCOPES:
        holes=range(0x1F6A,0x1F6E) if unit=='vsync-library' else ()
        image,fields,mz=root_resolve(raw,start,size,linked,holes)
        need(len(fields)==count and mz==([[0,0x1FE5]] if unit=='vsync-library' else []),'complete root field count and literal ordered MZ vector')
        extent((target,candidate),image,0,start,mz)
        offset=4 if unit=='vsync-library' else 0
        ins=list(decoder.disasm(image[offset:],start+offset));instructions+=ins;bounds={i.address for i in ins}
        need(sum(i.size for i in ins)+offset==size,'complete instruction/storage partition')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):
                need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'all static local branches enter instructions')
        procedures=[]
        for name,off,length,pop,ret,public in procs:
            body=[i for i in ins if off<=i.address<off+length]
            need(sum(i.size for i in body)==length and body[-1].mnemonic==ret and
                 (ret=='iret' or (int(body[-1].op_str,0) if body[-1].op_str else 0)==pop),'complete native procedure/interrupt return and cleanup')
            if public:need((off-CODE_BASE,name) in code_publics(raw,1) and address(table,name)==(0,off),'actual native and both MAP public entries')
            procedures.append(dict(name=name,offset=off-start,size=length,callee_pop_bytes=pop,return_kind=ret,public=public))
        need(sum(p['size'] for p in procedures)+len(evens)+offset==size and all(next(i for i in ins if i.address==a).mnemonic=='nop' for a in evens),'complete bodies/outer-EVEN/CS-storage partition')
        o=owner(PREFIX+unit,source(names[0]),0,start,image,size-offset,offset,procedures,mz,report)
        if names[0] in NATURAL:o['maintained_native_source']=NATURAL[names[0]]
        owners.append(o);native.append(dict(unit_id=PREFIX+unit,fields=fields,ordered_relocations=mz,ordinary_outer_EVEN_bytes=evens))
    need(address(table,'VSYNC_LEAVE')==address(table,'VSYNC_END')==(0,0x201C) and
         (0x201C-CODE_BASE,'VSYNC_LEAVE') in code_publics(raw,1),'LEAVE and END alias one native procedure')
    writer,=[i for i in instructions if i.mnemonic=='mov' and i.operands[0].type==X86_OP_MEM and i.operands[0].mem.segment==X86_REG_CS and i.operands[0].mem.disp==0x18B8]
    consumer=next(i for i in instructions if i.address<=0x18B8<i.address+i.size)
    need(writer.operands[0].size==1 and consumer.mnemonic=='xor' and consumer.imm_size==1 and consumer.address+consumer.imm_offset==0x18B8,'real byte self-modifying XOR operand, without ORG')
    palette=b''.join(bytes((0x77,)*3) if n==8 else bytes(((n>>b)&1)*(0xFF if n<8 else 0xAA) for b in (1,2,0)) for n in range(16))
    expected=[struct.pack('<H',100)+palette+struct.pack('<3H',0,0,0),b'\0'*7,struct.pack('<H',0),struct.pack('<4H',16,16,0,255)]
    data=byte_map(raw,2)
    need('REPT 16' in (root/STATE[0][1]).read_text(),'semantic default RGB palette generator')
    for (unit,off,size,src),semantic in zip(DATA,expected):
        image=bytes(data[i] for i in range(off-DATA_BASE,off-DATA_BASE+size));need(image==semantic,'complete semantic initialized display state')
        extent((target,candidate),image,DS,off,[])
        owners.append(owner(PREFIX+unit,src,DS,off,image,0,size,[],[],report))
        if unit=='vsync-initialized-data':owners[-1]['maintained_native_object']=report['mini_rounds'][0]['outputs']['context']['path']
    aliases=[('PaletteTone',0x578),('PalettesInit',0x57A),('PaletteNote',0x5AA),('ResPalSeg',0x5AC),('SdiExists',0x5AE),
             ('Palettes',0x141E),('vsync_Count1',0x144E),('vsync_Count2',0x1450),('vsync_OldVect',0x1452),('vsync_Proc',0x842),('vsync_Delay',0x846),('vsync_OldMask',0x848)]
    for name,off in aliases:need(address(table,name)==address(table,'_'+name)==(DS,off),'both initialized/BSS aliases in both MAP tables')
    need(address(table,'vsync_delay_count')==(DS,0x1456) and not byte_map(raw,9),'uninitialized58-byte palette/VSync state; no BSS initializers')
    need(re.search(rb'raw_crtbios\s+dw\s+\?',(root/NATURAL['vsync']).read_bytes()) and re.search(rb'raw_crtbios_seg\s+dw\s+\?',(root/NATURAL['vsync']).read_bytes()),'source retains the original uninitialized CS vector')
    return dict(owners=owners,source_CODE_bytes=sum(o['code_bytes'] for o in owners),source_file_DATA_bytes=sum(o['initialized_data_bytes'] for o in owners),
        procedures=sum(o['procedure_count'] for o in owners),native_scopes=native,independent_native_modules=mini,
        IRQ_entries=[0x1FD8,0x1FE2],VSYNC_END_LEAVE_same_body=True,palette_XOR_operand_alias=0x18B8,palette_XOR_source_ORG_removed=True,
        generated_palette_colors=16,uninitialized_CS_file_storage_bytes=4,source_CS_vector_initializer_added=False,
        BSS_bytes=58,BSS_file_byte_credit=0,uncredited_DATA0849_byte=0x90,root_packetization_changed=True,
        absolute_ordered_root_fields_preserved=True,selected_build_report_sha256=report_sha,selected_assembly_link_rounds=2,
        context_project_objects_reused=35,original_cold_rebuilt=False,runtime_matrix_required=False,physical_hardware_execution_claimed=False,
        whole_product_accepted=False)


def owner(unit,src,seg,off,image,code,data,procs,mz,report):
    return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=src,object=OBJECT,origin='library',segment=seg,offset=off,start=seg*16+off,
        size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),
        ordered_relocations=mz,code_bytes=code,initialized_data_bytes=data,procedure_count=len(procs),procedures=procs,
        private_data_bytes=0,private_bss_bytes=0,maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
        abi='original16-bit far Pascal display APIs,private near font helpers and two real IRET entries')


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['display_native'],indent=2))
