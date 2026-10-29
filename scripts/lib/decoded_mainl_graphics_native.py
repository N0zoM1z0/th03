"""Complete graphics/heap providers, semantic masks and natural native far calls."""
import hashlib
import json
import re
import struct
import tomllib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_CS
from build_th03_mainl_graphics_work import STATE, COPY, DRIVER, REPORT, wrapper, response, mini_wrappers, mini_response
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
DATA = (('graphics-clip-data',0x522,16,STATE[0][1]),('graphics-edge-masks',0x532,34,STATE[1][1]),
        ('graphics-byte-masks',0x84A,8,STATE[2][1]),('heap-initialized-data',0x852,8,STATE[3][1]))
DATA_SOURCES = {PREFIX+unit:src for unit,_,_,src in DATA}
# Public/private procedure bodies exclude outer EVEN and borrowed entry exits.
P = lambda name,off,size,ret='retf',pop=0,public=True:(name,off,size,ret,pop,public)
SCOPES = (
 ('grcg-box-library',0xAC8,366,['display_hardware/grcg_boxfill.asm','display_hardware/grcg_byteboxfill_x.asm'],
  [P('GRCG_BOXFILL',0xACE,207,pop=8),P('GRCG_BYTEBOXFILL_X',0xB9E,151,pop=8)],[(0xAC8,6)],[0xB9D,0xC35],10),
 ('draw-pack',0x162C,212,['resources/graph_pack_put_8.asm'],[P('GRAPH_PACK_PUT_8',0x1632,206,pop=10)],[(0x162C,6)],[],11),
 ('draw-noclip',0x2C68,202,['resources/graph_pack_put_8_noclip.asm'],[P('GRAPH_PACK_PUT_8_NOCLIP',0x2C6E,196,pop=10)],[(0x2C68,6)],[],9),
 ('draw-gaiji',0xF58,148,['resources/graph_gaiji_putc.asm'],[P('GRAPH_GAIJI_PUTC',0xF58,147,pop=8)],[],[0xFEB],1),
 ('draw-scroll',0x1700,88,['resources/graph_scrollup.asm'],[P('GRAPH_SCROLLUP',0x1700,88,pop=2)],[],[],2),
 ('draw-show',0x1758,6,['resources/graph_show.asm'],[P('GRAPH_SHOW',0x1758,5)],[],[0x175D],0),
 ('gdc-outpw',0xC66,11,['resources/gdc_outpw.asm'],[P('gdc_outpw',0xC66,11,'ret')],[],[],0),
 ('screen-mode',0xE24,78,['display_hardware/graph_400line.asm'],[P('GRAPH_400LINE',0xE24,77)],[],[0xE71],12),
 ('screen-clear',0xE72,36,['display_hardware/graph_clear.asm'],[P('GRAPH_CLEAR',0xE72,35)],[],[0xE95],2),
 ('screen-copy',0xE96,108,['display_hardware/graph_copy_page.asm'],[P('copy_plane',0xE96,21,'ret',public=False),P('GRAPH_COPY_PAGE',0xEAC,85,pop=2)],[],[0xEAB,0xF01],1),
 ('graph-extmode',0xF02,86,['display_hardware/graph_extmode.asm'],[P('GRAPH_EXTMODE',0xF02,86,pop=4)],[],[],1),
 ('egc-library',0x724,98,['display_hardware/egc.asm'],[P('EGC_ON',0x724,21),P('EGC_OFF',0x73A,31),P('EGC_START',0x75A,43)],[],[0x739,0x759,0x785],0),
 ('heap-manager',0x210A,628,['memory/heap.inl'],[P('HMEM_LALLOCATE',0x210A,52,pop=4),P('MEM_ASSIGN_DOS',0x213E,33,pop=2),
  P('MEM_ASSIGN',0x2160,38,pop=4),P('MEM_ASSIGN_ALL',0x2186,39),P('HMEM_ALLOCBYTE',0x21AE,20,'jmp'),P('HMEM_ALLOC',0x21C2,240,pop=2),
  P('HMEM_FREE',0x22B2,168,pop=2),P('MEM_UNASSIGN',0x235A,35)],[],[0x215F,0x21AD,0x237D],39),
 ('stack-memory',0x1EAA,76,['resources/smem_release.asm','resources/smem_wget.asm'],[P('SMEM_RELEASE',0x1EAA,15,pop=2),P('SMEM_WGET',0x1EC0,53,pop=2)],[(0x1EBA,6)],[0x1EB9,0x1EF5],5),
)


def need(value,message):
    if not value:
        raise ValueError('MAINL graphics native: '+str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_pair(root, work, files):
    report_raw = (root / REPORT).read_bytes()
    report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == {n: sha((root / n).read_bytes()) for n in [COPY]+[n for _, n in STATE]}, 'complete maintained state/recipe/cold context binding')
    generated, link = wrapper(files), response(files)
    need(report['wrapper_sha256'] == sha(generated) and report['response_sha256'] == sha(link) and
         (root / '.analysis/work/graphics-root.asm').read_bytes() == generated and
         (root / '.analysis/work/graphics-root.lnk').read_bytes() == link, 'actual include and unchanged link position')
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    prefix = root / config['paths']['wine_prefix']
    tasm = ['/usr/bin/wine-stable', str(prefix/'drive_c/TASM50/bin/TASM32.EXE'), '/m','/mx','/kh32768','/t','/dGAME=3']
    dos = ['/usr/bin/wine-stable', str(root/config['paths']['msdos_player']), '-e','-x','tlink']
    commands = []
    for n in (1,2):
        commands += [(f'round{n}-assemble',tasm+[WRAPPER,r'probe\gfxroot.obj'],0),
                     (f'round{n}-link',dos+[r'@probe\gfxroot.lnk'],0)]
        commands += [(f'round{n}-mini-{name}',tasm+[rf'probe\gfx-{name}.asm',rf'probe\gfx-{name}.obj'],0) for name in mini_wrappers()]
        commands += [(f'round{n}-mini-link',dos+[r'@probe\gfxmini.lnk'],0)]
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
    need(native_records(raw) == native_records(baseline) and public_records(raw) == public_records(baseline),
         'literal native payload/fixup order and complete public identity')
    description = describe_omf(raw)
    replacements = dict(STATE)
    need(description['valid'] and description['module_name'] == WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['dependency_paths'] == [replacements.get(n, n) for n in describe_omf(baseline)['dependency_paths']],
         'actual three maintained state includes and complete native dependency closure')
    for old,new in (STATE[0],STATE[3],STATE[4]):
        need(statements(files[old]) == statements((root/new).read_bytes()), 'complete original typed state declarations')
    need(tuple((b'call',*row[1:]) if row[0] == b'nopcall' else row for row in statements(files['src/mainl/display_hardware/graph_copy_page.asm'])) ==
         statements((root/COPY).read_bytes()), 'ordinary external far calls replace exactly two compatibility nopcall macros')
    need(all((root/f'.analysis/work/graphics-mini-{name}.asm').read_bytes() == content for name,content in mini_wrappers().items()) and
         (root/'.analysis/work/graphics-mini.lnk').read_bytes() == mini_response(), 'actual preserved standalone native source and response inputs')
    need([r['round'] for r in report['mini_rounds']] == [1,2], 'two independent far-call module vectors')
    vectors = []
    for row in report['mini_rounds']:
        need(set(row['outputs']) == {'memory','copy','exe','map'}, 'complete real memory/copy mini outputs')
        vector = {}
        for name,meta in row['outputs'].items():
            data = (root/meta['path']).read_bytes()
            need((len(data),sha(data)) == (meta['bytes'],meta['sha256']), 'current raw mini output')
            vector[name] = data
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'whole native mini OBJ/EXE/MAP repetition')
    common = ['ReC98.inc','libs/master.lib/func.inc','libs/master.lib/super.inc','libs/master.lib/bgm.inc','libs/master.lib/pf.inc',
              'libs/master.lib/clip.inc','libs/master.lib/macros.inc','libs/kaja/kaja.inc','twobyte.inc','pc98.inc','th01/hardware/egc.inc','th02/formats/pi_slots.inc']
    extras = {'memory':['src/mainl/memory/heap.inl','src/mainl/resources/smem_release.asm','src/mainl/resources/smem_wget.asm',STATE[3][1],
                        'libs/master.lib/grp[data].asm',STATE[4][1]],'copy':[COPY]}
    for name in mini_wrappers():
        d = describe_omf(vectors[0][name]);module = rf'probe\gfx-{name}.asm'
        need(d['valid'] and d['module_name'] == module and d['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
             d['dependency_paths'] == [module,*common,*extras[name]], 'actual complete native mini dependency closure')
    return raw,vectors[0],report,sha(report_raw)


def native_copy(root,raw,minis,table,target,candidate):
    memory,copy = minis['memory'],minis['copy']
    mr,cr = list(parse_omf(memory)),list(parse_omf(copy))
    need([r.data for r in mr if r.name == 'SEGDEF'] == [bytes.fromhex(n) for n in ('48c002020301','481400040501','742000060701','480800080901')] and
         [r.data for r in cr if r.name == 'SEGDEF'] == [bytes.fromhex(n) for n in ('486c00020301','480000040501')], 'complete mini segment lengths/WORD code and real stack/BSS')
    need([r.data for r in mr if r.name == 'GRPDEF'] == [bytes.fromhex('0aff04ff03ff02')] and
         [r.data for r in cr if r.name == 'GRPDEF'] == [bytes.fromhex('06ff02')], 'literal native mini DGROUP membership')
    need([r.data for r in cr if r.name == 'EXTDEF'] == [b'\x0fgraph_VramWords\0\x09SMEM_WGET\0\x0cSMEM_RELEASE\0'] and
         [r.data for r in cr if r.name == 'FIXUPP'] == [bytes.fromhex('c41a160101cc225602cc615603')], 'literal external WORD and two external FAR-pointer fixups')
    linked = parse_mz(minis['exe']);need(linked.valid and not linked.relocations and len(linked.program_image) == 836, 'complete native mini MZ and consumed far-call segment fields')
    mt = minis['map'].decode()
    for module,seg,off,size,cls,part,group,acbp in (('memory',0,0,704,'CODE','_TEXT','(none)',0x48),('copy',0,704,108,'CODE','_TEXT','(none)',0x48),
            ('memory',0x33,0,20,'DATA','_DATA','DGROUP',0x48),('memory',0x33,0x20,32,'STACK','STACK','DGROUP',0x74),('memory',0x33,0x40,8,'BSS','_BSS','DGROUP',0x48)):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{size:04X}\s+C={cls}\s+S={part}\s+G={re.escape(group)}\s+M=probe\\gfx-{module}\.asm\s+ACBP={acbp:02X}\s*$',mt)) == 1, 'actual complete mini module allocation')
    m = byte_map(memory,1);need(set(m) == set(range(704)) and not byte_map(memory,3) and not byte_map(memory,4), 'complete real memory CODE and uninitialized stack/BSS')
    image = bytearray(m[n] for n in range(704));fields = []
    records, = [r.data for r in mr if r.name == 'FIXUPP']
    for i in range(0,len(records),5):
        loc,low,method,frame,index = records[i:i+5]
        site = (loc&3)*256+low
        need(loc&0xFC == 0xC4 and (method,frame) == (0x14,1) and index in (2,4) and site+2 <= 704, 'literal complete native mini memory WORD field')
        addend = int.from_bytes(image[site:site+2],'little');value = {2:0,4:0x40}[index]+addend
        image[site:site+2] = value.to_bytes(2,'little');fields.append(dict(site=site,target=index,value=value))
    need(len(fields) == 44 and bytes(image) == linked.program_image[:704], 'independently resolved complete native memory provider')
    c = byte_map(copy,1);need(set(c) == set(range(108)) and not byte_map(copy,2), 'complete copy source without missing native bytes')
    original = bytes(c[n] for n in range(108))
    for base,words,release,get in ((704,10,0x274,0x28A),(0xE96,0x566,0x1EAA,0x1EC0)):
        image = bytearray(original)
        need(image[26:28] == b'\0\0', 'native graph_VramWords external addend')
        image[26:28] = words.to_bytes(2,'little')
        for off,dest in ((0x21,get),(0x60,release)):
            need(image[off:off+5] == b'\x9a\0\0\0\0', 'ordinary native five-byte far CALL, no source NOP')
            image[off:off+5] = b'\x90\x0e\xe8'+((dest-(base+off+5))&65535).to_bytes(2,'little')
        if base == 704:
            need(bytes(image) == linked.program_image[704:812], 'real TLINK same-CS far calls naturally emit NOP/PUSH CS/near CALL')
        else:
            extent((target,candidate),bytes(image),0,base,[])
    for name,mini_off,root_off in (('SMEM_RELEASE',0x274,0x1EAA),('SMEM_WGET',0x28A,0x1EC0),('GRAPH_COPY_PAGE',0x2D6,0xEAC)):
        need(address(mt,name) == (0,mini_off) and address(table,name) == (0,root_off), 'real callee/public identities in both MAP tables')
    return dict(native_copy_bytes=108,native_far_call_sites=[0x21,0x60],literal_far_pointer_fixups=2,consumed_segment_MZ_entries=0,
        naturally_relaxed_instruction_bytes=2,source_NOP_added=False,source=COPY,memory_native_fields=fields,mini_CODE_bytes=812,
        mini_context_DATA_bytes=20,mini_uninitialized_STACK_bytes=32,mini_uninitialized_BSS_bytes=8,runtime_execution_claimed=False)


def verify(root,work,target,candidate,graph,files):
    raw,minis,report,report_sha = selected_pair(root,work,files)
    _,description = root_native(raw)
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
         [bytes((20,255,9,255,2)),bytes((21,255,7,255,6,255,5,255,4,255,3))], 'literal root DGROUP/CODE member identities')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'],row['wrapper'],row['kind'],row['game'],row['binary']) == (WRAPPER,WRAPPER,'tasm',3,'L'), 'actual GAME3 large-model root producer')
    for name in {n for scope in SCOPES for n in scope[3]}:
        src = 'src/mainl/'+name
        need(files[WRAPPER].count(('include '+src).encode()) == 1 and src in description['dependency_paths'] and
             files[src] == (work/src).read_bytes() and files[src].replace(b'\r\n',b'\n') == (root/src).read_bytes().replace(b'\r\n',b'\n'), 'complete actual maintained source transport: '+src)
        if name != 'memory/heap.inl':
            need(statements(files[src]) == statements(files['libs/master.lib/'+name.rsplit('/',1)[1]]), 'complete original symbolic provider')
    table = (work/'obj/th03/mainl.map').read_text()
    for cls,base,size,name,seg,group in (('CODE',CODE_BASE,10944,'_TEXT',0,'(none)'),('DATA',DATA_BASE,2036,'_DATA',DS,'DGROUP'),('BSS',0x13F6,5108,'_BSS',DS,'DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$',table)) == 1, 'whole native containing MAP allocation')
    call_review = native_copy(root,raw,minis,table,target,candidate)
    decoder = Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail = True
    owners,native,all_ins = [],[],[]
    for unit,start,size,sources,procs,borrowed,evens,count in SCOPES:
        image,fields = resolve(raw,start,size);extent((target,candidate),image,0,start,[])
        ins = list(decoder.disasm(image,start));all_ins += ins;bounds = {i.address for i in ins}
        need(sum(i.size for i in ins) == size and len(fields) == count, 'complete CODE and literal native field stream: '+unit)
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):
                need(i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds, 'all local branch/continuation entries enter owned instructions')
        procedures = []
        for name,off,length,ret,pop,public in procs:
            body = [i for i in ins if off <= i.address < off+length]
            need(sum(i.size for i in body) == length and body[-1].mnemonic == ret and
                 (ret == 'jmp' or (int(body[-1].op_str,0) if body[-1].op_str else 0) == pop), 'complete body and native near/far cleanup: '+name)
            if public:
                need((off-CODE_BASE,name) in code_publics(raw,1) and address(table,name) == (0,off), 'actual native and both MAP public tables: '+name)
            procedures.append(dict(name=name,offset=off-start,size=length,return_kind=ret,callee_pop_bytes=pop,public=public))
        need(sum(p['size'] for p in procedures)+sum(n for _,n in borrowed)+len(evens) == size and
             all(next(i for i in ins if i.address == a).mnemonic == 'nop' for a in evens), 'complete procedure/borrowed-continuation/outer-EVEN partition')
        origin = 'authored' if unit == 'draw-noclip' else 'library'
        o = owner(PREFIX+unit,'src/mainl/'+sources[0],0,start,image,size,0,procedures,origin,report)
        if unit == 'screen-copy':
            o.update(maintained_native_object=report['mini_rounds'][0]['outputs']['copy']['path'],maintained_native_source=COPY)
        owners.append(o);native.append(dict(unit_id=PREFIX+unit,fields=fields,ordered_relocations=[],borrowed_extents=[list(b) for b in borrowed],ordinary_outer_EVEN_bytes=evens))
    need(address(table,'EGC_END') == address(table,'EGC_START') == (0,0x75A) and
         (0x75A-CODE_BASE,'EGC_END') in code_publics(raw,1), 'EGC_END is the same native public body as EGC_START')
    lookup_fields = [f for scope in native for f in scope['fields'] if f['target'] == 1]
    for f in lookup_fields:
        instruction = next(i for i in all_ins if i.address <= f['site'] < i.address+i.size)
        operand, = [o for o in instruction.operands if o.type == X86_OP_MEM and o.mem.segment == X86_REG_CS]
        need(f['value'] in (0x1AAA,0x1AAC) and operand.mem.disp == f['value'] and operand.size == 2 and
             instruction.mnemonic in ('mov','or'), 'actual WORD lookup into previously accepted semantic RotTbl')
    need(len(lookup_fields) == 16, 'all sixteen packed-pixel table operand fields')
    edges = b''.join(((0xFFFF << (16-n))&65535).to_bytes(2,'big') for n in range(17))
    masks = bytes(255 >> n for n in range(8))
    edge_source = (root/STATE[1][1]).read_text();mask_source = (root/STATE[2][1]).read_text()
    need('REPT 17' in edge_source and 'DW ((edge_bits AND 0ffh) SHL 8) OR (edge_bits SHR 8)' in edge_source and
         'REPT 8' in mask_source and 'DB byte_mask_bits' in mask_source and
         not re.search(r'(?im)^\s*(?:ORG|DW\s+[0-9]|DB\s+[0-9])\b',edge_source+'\n'+mask_source), 'semantic mask generation without literal target tables/fill')
    payload = byte_map(raw,2)
    expected = [struct.pack('<6h2H',0,639,639,0,399,399,0xA800,399*80),edges,masks,struct.pack('<4H',0,0,0,256)]
    for (unit,off,size,src),semantic in zip(DATA,expected):
        data = bytes(payload[i] for i in range(off-DATA_BASE,off-DATA_BASE+size))
        need(data == semantic, 'complete independent initialized state/table: '+unit)
        extent((target,candidate),data,DS,off,[])
        owners.append(owner(PREFIX+unit,src,DS,off,data,0,size,[],'library',report))
    constants_block = False
    for r in parse_omf(raw):
        if r.name == 'LEDATA':
            first = int.from_bytes(r.data[1:3],'little');last = first+len(r.data)-3
            constants_block = r.data[0] == 2 and any(first <= off-DATA_BASE < last for _,off,_,_ in DATA)
        elif r.name == 'FIXUPP':
            need(not constants_block, 'complete literal initialized-constant LEDATA has no native fixups')
    for name,off in [('ClipXL',0x522),('ClipXW',0x524),('ClipXR',0x526),('ClipYT',0x528),('ClipYH',0x52A),('ClipYB',0x52C),('ClipYT_seg',0x52E),('ClipYB_adr',0x530),
                     ('mem_TopSeg',0x852),('mem_MyOwn',0x854),('mem_AllocID',0x856),('mem_Reserve',0x858),
                     ('mem_OutSeg',0x1458),('mem_TopHeap',0x145A),('mem_FirstHole',0x145C),('mem_EndMark',0x145E)]:
        need(address(table,name) == address(table,'_'+name) == (DS,off), 'both original state aliases in both MAP tables')
    need(address(table,'EDGES') == (DS,0x532) and address(table,'BYTE_MASK') == (DS,0x84A) and not byte_map(raw,9), 'native generated table identities and no BSS initializers')
    return dict(owners=owners,source_CODE_bytes=sum(o['code_bytes'] for o in owners),source_initialized_DATA_bytes=sum(o['initialized_data_bytes'] for o in owners),
        procedures=sum(o['procedure_count'] for o in owners),authored_CODE_bytes=202,native_scopes=native,
        packed_pixel_table_operand_fields=lookup_fields,generated_edge_WORDs=17,generated_BYTE_masks=8,EGC_END_START_same_body=True,
        native_far_call_review=call_review,heap_BSS_bytes=8,BSS_file_byte_credit=0,source_paths=sorted({'src/mainl/'+n for s in SCOPES for n in s[3]})+[n for _,n in STATE]+[COPY],
        selected_build_report_sha256=report_sha,selected_assembly_link_rounds=2,independent_far_call_module_rounds=2,context_project_objects_reused=35,
        original_cold_rebuilt=False,runtime_matrix_required=False,physical_graphics_or_heap_execution_claimed=False,whole_product_accepted=False)


def owner(unit,src,seg,off,image,code,data,procs,origin,report):
    return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=src,object=OBJECT,origin=origin,
        segment=seg,offset=off,start=seg*16+off,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],code_bytes=code,initialized_data_bytes=data,
        procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],abi='native16-bit far Pascal graphics/heap; private near helpers and shared borrowed continuations')


if __name__ == '__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['graphics_native'],indent=2))
