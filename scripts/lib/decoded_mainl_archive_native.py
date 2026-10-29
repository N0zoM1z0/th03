"""Buffered/archive readers with real native module alignment and packed state."""
import hashlib
import json
import re
import struct
import tomllib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_ES
from build_th03_mainl_archive_work import TYPES, TYPES_OLD, GETC, DATA_SOURCE, DRIVER, REPORT, wrapper, response, mini_wrappers, mini_response
from build_th03_mainl_resources_work import native_records, public_records
from lib.omf import parse_omf, describe_omf
from lib.pc98 import parse_mz
from lib.decoded_mainl_resources_native import resolve
from lib.decoded_mainl_file_native import byte_map
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.mainl_staff_source import statements
from lib.decoded_mainl_root_helpers_layout import native as root_native, OBJECT, WRAPPER, CODE_BASE, DATA_BASE, DS
from probe_th03_main_boss_marisa_cpp import code_publics

PREFIX = 'th03-mainl-decoded-'
DATA_UNIT, SELECTED_SOURCE = PREFIX+'archive-initialized-data', DATA_SOURCE
GETC_UNITS = {PREFIX+'pfread-'+n for n in ('getc','len','plain','keyed')}
# Unit, symbol, provider, decoded start, complete size, stack cleanup, return, fields.
PROCEDURES = (
    ('buffer-close','BCLOSER','bcloser',0x472,24,2,'retf',0),
    ('buffer-fill','BFILL','bfill',0x48A,59,2,'retf',0),
    ('buffer-getc','BGETC','bgetc',0x506,48,2,'retf',0),
    ('buffer-open','BOPENR','bopenr',0x5B8,83,4,'retf',5),
    ('buffer-read','BREAD','bread',0x60C,48,8,'retf',0),
    ('buffer-seek','BSEEK','bseek',0x63C,65,6,'retf',0),
    ('buffer-seek-base','BSEEK_','bseek_',0x67E,47,8,'retf',0),
    ('buffer-dos-open','DOS_ROPEN','../resources/dos_ropen',0xAAE,26,4,'retf',1),
    ('pfread-close','PFCLOSE','pfclose',0x18DA,26,2,'retf',0),
    ('pfread-getc','PFGETC','pfgetc',0x18F4,15,2,'retf',0),
    ('pfread-len','PFGETC1','pfgetc',0x1904,78,0,'ret',0),
    ('pfread-plain','PFGETX0','pfgetc',0x1952,68,0,'ret',0),
    ('pfread-keyed','PFGETX1','pfgetc',0x1996,13,0,'ret',0),
    ('pfread-read','PFREAD','pfread',0x19A4,46,8,'retf',0),
    ('pfread-rewind','PFREWIND','pfrewind',0x19D2,59,2,'retf',0),
    ('pfread-seek','PFSEEK','pfseek',0x1A0E,48,6,'retf',0),
    ('pfopen','PFOPEN','pfopen',0x2B16,281,8,'retf',7),
)
EVENS = (('align-bfnt','bfill',0x4C5),('align-bread','bopenr',0x60B),('align-bseek','bseek',0x67D),
         ('align-filesize','bseek_',0x6AD),('align-pfgetc','pfgetc',0x1903),('align-pfread','pfrewind',0x1A0D))
BFILE = (('b_hdl',0,2),('b_left',2,2),('b_pos',4,2),('b_siz',6,2),('b_buff',8,1))
PFILE = (('pf_bf',0,2),('pf_getc',2,2),('pf_getx',4,2),('pf_size',6,4),('pf_read',10,4),
         ('pf_home',14,4),('pf_loc',18,4),('pf_osize',22,4),('pf_cnt',26,2),('pf_ch',28,2),('pf_key',30,1))


def need(value, message):
    if not value:
        raise ValueError('MAINL archive native: '+str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(name):
    return 'src/mainl/resources/dos_ropen.asm' if name.startswith('../') else 'src/mainl/archive_io/'+name+'.asm'


def vector(root, row, keys):
    need(set(row['outputs']) == set(keys), 'complete native output vector')
    result = {}
    for name, info in row['outputs'].items():
        raw = (root/info['path']).read_bytes()
        need((len(raw),sha(raw)) == (info['bytes'],info['sha256']), 'current raw output: '+info['path'])
        result[name] = raw
    return result


def selected_pair(root, work, files):
    report_raw = (root/REPORT).read_bytes();report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root/DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root/'.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == {n:sha((root/n).read_bytes()) for n in (TYPES,GETC,DATA_SOURCE)}, 'complete source/recipe/cold binding')
    generated, link = wrapper(files),response(files)
    need(generated == files[WRAPPER] and (root/'.analysis/work/archive-root.asm').read_bytes() == generated and
         (root/'.analysis/work/archive-root.lnk').read_bytes() == link and
         report['wrapper_sha256'] == sha(generated) and report['response_sha256'] == sha(link), 'unchanged root and real link position')
    config = tomllib.loads((root/'config/toolchain.toml').read_text());prefix = root/config['paths']['wine_prefix']
    tasm = ['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t','/dGAME=3']
    dos = ['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x','tlink']
    commands = []
    for number in (1,2):
        commands += [(f'round{number}-assemble',tasm+[WRAPPER,r'probe\arcroot.obj'],0),
                     (f'round{number}-link',dos+[r'@probe\arcroot.lnk'],0)]
        commands += [(f'round{number}-mini-{n}',tasm+[rf'probe\arc-{n}.asm',rf'probe\arc-{n}.obj'],0) for n in mini_wrappers()]
        commands += [(f'round{number}-mini-link',dos+[r'@probe\arcmini.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in report['native_phases']] == commands, 'two actual root/five-module/link schedules')
    need([r['round'] for r in report['rounds']] == [1,2] and [r['round'] for r in report['mini_rounds']] == [1,2], 'complete repeated native rounds')
    roots = [vector(root,r,('obj','exe','map')) for r in report['rounds']]
    minis = [vector(root,r,(*mini_wrappers(),'exe','map')) for r in report['mini_rounds']]
    need(roots[0] == roots[1] and minis[0] == minis[1], 'whole raw root and five-module output repetition')
    need(all(r['exe'] == (work/'bin/th03/mainl.target.exe').read_bytes() and
             r['map'] == (work/'obj/th03/mainl.map').read_bytes() for r in roots), 'whole pinned decoded target and retained MAP')
    raw, baseline = roots[0]['obj'],(work/OBJECT).read_bytes()
    need(native_records(raw) == native_records(baseline) and public_records(raw) == public_records(baseline), 'complete native payload/public identity and literal FIXUPP order')
    expected = describe_omf(baseline)['dependency_paths'];expected.insert(expected.index(TYPES_OLD)+1,TYPES)
    need(describe_omf(raw)['dependency_paths'] == expected, 'actual maintained types forwarder and unchanged root dependencies')
    common = ['ReC98.inc','libs/master.lib/func.inc','libs/master.lib/super.inc','libs/master.lib/bgm.inc',TYPES_OLD,TYPES,
              'libs/master.lib/clip.inc','libs/master.lib/macros.inc','libs/kaja/kaja.inc','twobyte.inc','pc98.inc',
              'th01/hardware/egc.inc','th02/formats/pi_slots.inc']
    extras = {'buffer':[source('bfill'),source('bgetc')],'getc':[GETC],'read':[source('pfread')],
              'state':[DATA_SOURCE],'rand':['libs/master.lib/rand[data].asm']}
    for name in mini_wrappers():
        d = describe_omf(minis[0][name]);module = rf'probe\arc-{name}.asm'
        need(d['valid'] and d['module_name'] == module and d['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
             d['dependency_paths'] == [module,*common,*extras[name]], 'complete actual native mini producer closure: '+name)
    need(statements(files[TYPES_OLD]) == statements((root/TYPES).read_bytes()), 'complete packed types and original constants/macros')
    need(statements(files[source('pfgetc')])[:-1] == statements((root/GETC).read_bytes()) and
         statements(files[source('pfgetc')])[-1] == (b'db',b'0'), 'complete reader source without legacy explicit alignment byte')
    compact = lambda raw: tuple(b''.join(row).upper() for row in statements(raw))
    need(compact(files['libs/master.lib/pf[data].asm'])[:-1] == compact((root/DATA_SOURCE).read_bytes()) and
         compact(files['libs/master.lib/pf[data].asm'])[-1] == b'DB0', 'five genuine state bytes without legacy filler')
    return raw,minis[0],report,sha(report_raw)


def packed(text, name, expected):
    block, = re.findall(rf'(?ims)^\s*{name}\s+struc\s*\n(.*?)^\s*{name}\s+ends',text)
    result, offset = [],0
    for field,kind in re.findall(r'(?im)^\s*(\w+)\s+(db|dw|dd)\s+\?',block):
        size = {'db':1,'dw':2,'dd':4}[kind.lower()];result.append((field,offset,size));offset += size
    need(tuple(result) == expected, 'complete packed fields: '+name)
    return [dict(name=n,offset=o,size=s) for n,o,s in result]


def mini_layout(minis, table, target, candidate):
    sizes = {'buffer':(108,0),'getc':(175,0),'read':(46,0),'state':(0,5),'rand':(0,4)}
    for name,(code,data) in sizes.items():
        records = list(parse_omf(minis[name]))
        segments = [r.data for r in records if r.name == 'SEGDEF']
        need(len(segments) == (3 if name == 'buffer' else 2) and [r[0] for r in segments[:2]] == [0x48,0x48] and
             [int.from_bytes(r[1:3],'little') for r in segments[:2]] == [code,data] and
             (name != 'buffer' or segments[2] == bytes.fromhex('742000060701')) and
             [r.data for r in records if r.name == 'GRPDEF'] == [bytes((8,255,3,255,2)) if name == 'buffer' else bytes((6,255,2))], 'actual WORD-aligned native module sizes: '+name)
        need(set(byte_map(minis[name],1)) == set(range(code)) and set(byte_map(minis[name],2)) == set(range(data)), 'complete emitted mini bytes; no source gap fill')
        need([r.data for r in records if r.name == 'FIXUPP'] == ([bytes.fromhex('849e060101')] if name == 'getc' else []), 'literal sole external self-relative mini field')
        need([r.data for r in records if r.name == 'EXTDEF'] == ([b'\x05BGETC\0'] if name == 'getc' else []), 'sole actual external BGETC symbol')
    linked = parse_mz(minis['exe']);need(linked.valid and not linked.relocations and len(linked.program_image) == 346, 'complete native mini MZ, no segment fields')
    mini_map = minis['map'].decode()
    for name,off,length,cls,seg,part in (('buffer',0,108,'CODE',0,'_TEXT'),('getc',108,175,'CODE',0,'_TEXT'),
            ('read',284,46,'CODE',0,'_TEXT'),('state',0,5,'DATA',21,'_DATA'),('rand',6,4,'DATA',21,'_DATA')):
        group = '(none)' if cls == 'CODE' else 'DGROUP'
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{length:04X}\s+C={cls}\s+S={part}\s+G={re.escape(group)}\s+M=probe\\arc-{name}\.asm\s+ACBP=48\s*$',mini_map)) == 1, 'literal mini MAP contributions and real WORD gaps')
    data = byte_map(minis['getc'],1);code = bytearray(data[n] for n in range(175))
    need(code[158:160] == b'\0\0', 'zero native external relative addend')
    original = bytes(code)
    for base,callee in ((108,60),(0x18F4,0x506)):
        code[158:160] = ((callee-(base+160)) & 65535).to_bytes(2,'little')
        if base == 108:
            need(bytes(code) == linked.program_image[108:283], 'independently resolved complete native mini reader')
        else:
            extent((target,candidate),bytes(code),0,0x18F4,[])
    need(address(table,'BGETC') == (0,0x506) and address(mini_map,'BGETC') == (0,60), 'external destination in both actual MAP tables')
    for name,off in (('PFGETC',0),('PFGETC1',16),('PFGETX0',94),('PFGETX1',162)):
        need((off,name) in code_publics(minis['getc'],1) and address(mini_map,name) == (0,108+off), 'complete independent reader publics')
    state_map = byte_map(minis['state'],2);state = bytes(state_map[n] for n in range(5))
    need(state == struct.pack('<HHB',512,0,0) and linked.program_image[336:341] == state and
         linked.program_image[283] == linked.program_image[341] == 0, 'actual five state bytes and two real linker-emitted gaps')
    for executable in (target,candidate):
        need(executable.program_image[0x19A3] == executable.program_image[DS*16+0x5B5] == 0, 'matching contextual target gap bytes')
    for name,off in (('bbufsiz',0x5B0),('pferrno',0x5B2),('pfkey',0x5B4)):
        need(address(table,name) == address(table,'_'+name) == (DS,off) and
             address(mini_map,name) == address(mini_map,'_'+name) == (21,off-0x5B0), 'both sets of state aliases')
    return state,dict(reader_native_bytes=175,reader_external_field_offset=158,reader_external_symbol='BGETC',
        source_explicit_zero_removed=True,independent_source=GETC,source_pointer_width=2,
        gaps=[dict(kind='CODE',mini_offset=283,target_segment=0,target_offset=0x19A3,size=1),
              dict(kind='DATA',mini_offset=341,target_segment=DS,target_offset=0x5B5,size=1)],
        gap_source_byte_credit=0,source_padding_added=False,whole_product_link_layout_recovered=False)


def verify(root,work,target,candidate,graph,files):
    raw,minis,report,report_sha = selected_pair(root,work,files)
    _,description = root_native(raw)
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
         [bytes((20,255,9,255,2)),bytes((21,255,7,255,6,255,5,255,4,255,3))], 'actual root DGROUP/CODE membership')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'],row['wrapper'],row['kind'],row['game'],row['binary']) == (WRAPPER,WRAPPER,'tasm',3,'L'), 'actual containing root producer')
    for name in {p[2] for p in PROCEDURES}:
        src = source(name);old = ('th03/formats/pfopen.asm' if name == 'pfopen' else 'libs/master.lib/'+src.rsplit('/',1)[1])
        need(files[WRAPPER].count(('include '+src).encode()) == 1 and src in description['dependency_paths'] and
             files[src] == (work/src).read_bytes() and files[src].replace(b'\r\n',b'\n') == (root/src).read_bytes().replace(b'\r\n',b'\n') and
             statements(files[src]) == statements(files[old]), 'complete source and original library/game origin: '+src)
    types = (root/TYPES).read_text();bfile = packed(types,'BFILE',BFILE);pfile = packed(types,'PFILE',PFILE)
    table = (work/'obj/th03/mainl.map').read_text()
    for cls,base,size,name,seg,group in (('CODE',CODE_BASE,10944,'_TEXT',0,'(none)'),('DATA',DATA_BASE,2036,'_DATA',DS,'DGROUP'),('BSS',0x13F6,5108,'_BSS',DS,'DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$',table)) == 1, 'complete containing native MAP layout')
    state,gap_review = mini_layout(minis,table,target,candidate)
    decoder = Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail = True
    owners,native,all_ins = [],[],[]
    for unit,name,provider,off,size,pop,ret,count in PROCEDURES:
        image,fields = resolve(raw,off,size);extent((target,candidate),image,0,off,[])
        ins = list(decoder.disasm(image,off));all_ins += ins
        need(len(fields) == count and sum(i.size for i in ins) == size and ins[-1].mnemonic == ret and
             (int(ins[-1].op_str,0) if ins[-1].op_str else 0) == pop and
             (off-CODE_BASE,name) in code_publics(raw,1) and address(table,name) == (0,off), 'complete native body/public/near-far cleanup: '+name)
        bounds = {i.address for i in ins}
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):
                need(i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds, 'all local branch destinations enter instructions')
        origin = 'authored' if unit == 'pfopen' else 'library'
        o = owner(PREFIX+unit,source(provider),0,off,image,size,0,[dict(name=name,offset=0,size=size,callee_pop_bytes=pop,return_kind=ret)],origin,report)
        if o['unit_id'] in GETC_UNITS:
            o.update(maintained_native_object=report['mini_rounds'][0]['outputs']['getc']['path'],maintained_native_source=GETC)
        owners.append(o);native.append(dict(unit_id=PREFIX+unit,fields=fields,ordered_relocations=[]))
    for name,provider,off in EVENS:
        image,fields = resolve(raw,off,1)
        need(image == b'\x90' and not fields, 'original macro/outer EVEN byte')
        extent((target,candidate),image,0,off,[])
        owners.append(owner(PREFIX+'root-tail-'+name,source(provider),0,off,image,1,0,[],'library',report))
    extent((target,candidate),state,DS,0x5B0,[])
    owners.append(owner(DATA_UNIT,DATA_SOURCE,DS,0x5B0,state,0,5,[],'library',report))
    owners[-1].update(maintained_native_object=report['mini_rounds'][0]['outputs']['state']['path'])
    dispatch = [f for f in native[-1]['fields'] if f['target'] == 1]
    need([f['value'] for f in dispatch] == [0x1952,0x1996,0x1904], 'plain/keyed/RLE native dispatch destinations')
    indirect = [dict(site=i.address,slot=i.operands[0].mem.disp) for i in all_ins if i.mnemonic == 'call' and
                i.operands[0].type == X86_OP_MEM and i.operands[0].mem.segment == X86_REG_ES]
    need(len(indirect) == 5 and {i['slot'] for i in indirect} == {2,4}, 'five actual near PFILE dispatch consumers')
    return dict(owners=owners,source_CODE_bytes=sum(o['code_bytes'] for o in owners),source_initialized_DATA_bytes=5,procedures=17,
        authored_CODE_bytes=281,library_CODE_bytes=sum(o['code_bytes'] for o in owners if o['origin'] == 'library'),library_initialized_DATA_bytes=5,native_scopes=native,
        packed_BFILE_bytes=9,packed_PFILE_bytes=31,BFILE_fields=bfile,PFILE_fields=pfile,
        near_dispatch_consumers=indirect,independent_native_module_layout=gap_review,
        source_paths=sorted({source(p[2]) for p in PROCEDURES})+[TYPES,GETC,DATA_SOURCE],
        selected_build_report_sha256=report_sha,selected_assembly_link_rounds=2,independent_module_rounds=2,
        original_cold_rebuilt=False,context_project_objects_reused=35,BSS_file_byte_credit=0,
        physical_DOS_or_heap_execution_claimed=False,runtime_matrix_required=False,whole_product_accepted=False)


def owner(unit,src,seg,off,image,code,data,procs,origin,report):
    return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=src,object=OBJECT,origin=origin,
        segment=seg,offset=off,start=seg*16+off,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],code_bytes=code,initialized_data_bytes=data,
        procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
        abi='native16-bit Pascal public file APIs; register-ES near PFILE reader dispatch; unchecked original state')


if __name__ == '__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['archive_native'],indent=2))
