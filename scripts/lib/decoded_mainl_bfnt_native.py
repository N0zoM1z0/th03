"""Complete BFNT loader ownership, packed header and native operand writers."""
import hashlib
import json
import re
import tomllib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_CS
from build_th03_mainl_bfnt_work import STATE, TYPES, TYPES_OLD, DRIVER, REPORT, wrapper, response
from build_th03_mainl_resources_work import native_records, public_records
from lib.omf import parse_omf, describe_omf
from lib.decoded_mainl_resources_native import resolve
from lib.decoded_mainl_file_native import byte_map
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.mainl_staff_source import statements
from lib.decoded_mainl_root_helpers_layout import native as root_native, OBJECT, WRAPPER, CODE_BASE, DATA_BASE, DS
from probe_th03_main_boss_marisa_cpp import code_publics

BFNT_UNIT = 'th03-mainl-decoded-bfnt-library'
PALETTE_UNIT = 'th03-mainl-decoded-palette-bfnt'
DATA_UNIT = 'th03-mainl-decoded-bfnt-signature'
SELECTED_SOURCE = STATE[0][1]
SOURCES = ['src/mainl/resources/' + n + '.asm' for n in
           ('bfnt_entry_pat','bfnt_extend_header_skip','bfnt_header_read','bfnt_header_analysis','bfnt_palette_set')]
PROCEDURES = (('BFNT_ENTRY_PAT',0x286,302,8),('BFNT_EXTEND_HEADER_SKIP',0x3B4,34,6),
              ('BFNT_HEADER_READ',0x3D6,59,6),('BFNT_EXTEND_HEADER_ANALYSIS',0x412,95,6),
              ('BFNT_PALETTE_SET',0x4C6,64,6))
FIELDS = (('id',0,5),('col',5,1),('ver',6,1),('x00',7,1),('Xdots',8,2),('Ydots',10,2),
          ('START',12,2),('END_',14,2),('font_name',16,8),('time',24,4),('extSize',28,2),('hdrSize',30,2))
SMC = {0x36D:2,0x35F:2,0x2ED:2,0x309:1,0x364:2,0x307:1,0x302:2,0x2E8:2}


def need(value, message):
    if not value:
        raise ValueError('MAINL BFNT native: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_pair(root, work, files):
    report_raw = (root / REPORT).read_bytes()
    report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == {n: sha((root / n).read_bytes()) for n in [TYPES] + [n for _, n in STATE]}, 'complete maintained state/recipe/cold context binding')
    generated, link = wrapper(files), response(files)
    need(report['wrapper_sha256'] == sha(generated) and report['response_sha256'] == sha(link) and
         (root / '.analysis/work/bfnt-root.asm').read_bytes() == generated and
         (root / '.analysis/work/bfnt-root.lnk').read_bytes() == link, 'actual include and unchanged link position')
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    prefix = root / config['paths']['wine_prefix']
    commands = [ ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE'), '/m', '/mx', '/kh32768', '/t',
                  '/dGAME=3', WRAPPER, r'probe\bfntroot.obj'],
                 ['/usr/bin/wine-stable', str(root / config['paths']['msdos_player']), '-e', '-x', 'tlink', r'@probe\bfntroot.lnk'] ]
    need([(p['label'], p['command'], p['returncode']) for p in report['native_phases']] ==
         [(f'round{n}-{name}', commands[i], 0) for n in (1, 2) for i, name in enumerate(('assemble', 'link'))], 'two actual selected assembly/link rounds')
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
    expected_dependencies = []
    for n in describe_omf(baseline)['dependency_paths']:
        expected_dependencies.append(replacements.get(n, n))
        if n == TYPES_OLD:
            expected_dependencies.append(TYPES)
    need(description['valid'] and description['module_name'] == WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['dependency_paths'] == expected_dependencies,
         'actual maintained types/signature includes and complete native dependency closure')
    need(statements(files[TYPES_OLD]) == statements((root / TYPES).read_bytes()), 'complete original constants and packed structure')
    original, maintained = statements(files[STATE[0][0]]), statements((root / STATE[0][1]).read_bytes())
    need(tuple(b''.join(row).upper() for row in original) == tuple(b''.join(row).upper() for row in maintained),
         'complete signature declarations and aliases')
    return raw, report, sha(report_raw)


def verify(root, work, target, candidate, graph, files):
    raw, report, report_sha = selected_pair(root, work, files)
    _, description = root_native(raw)
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
         [bytes((20,255,9,255,2)), bytes((21,255,7,255,6,255,5,255,4,255,3))], 'literal DATA/BSS and CODE group membership')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'],row['wrapper'],row['kind'],row['game'],row['binary']) == (WRAPPER,WRAPPER,'tasm',3,'L'), 'actual root producer')
    for source in SOURCES:
        need(files[WRAPPER].count(('include '+source).encode()) == 1 and source in description['dependency_paths'] and
             files[source] == (work/source).read_bytes() and
             files[source].replace(b'\r\n',b'\n') == (root/source).read_bytes().replace(b'\r\n',b'\n') and
             statements(files[source]) == statements(files['libs/master.lib/'+source.rsplit('/',1)[1]]),
             'complete consumed original symbolic library source: '+source)
    text = (root/TYPES).read_text()
    structure, = re.findall(r'(?s)bfnt_header\s+STRUC\s*\n(.*?)bfnt_header\s+ENDS',text)
    fields, cursor = [], 0
    for name, dtype, count in re.findall(r'(?m)^(\w+)\s+(DB|DW|DD)\s+(?:(\d+) dup \(\?\)|\?)\s*$',structure):
        size = {'DB':1,'DW':2,'DD':4}[dtype]*int(count or '1')
        fields.append((name,cursor,size));cursor += size
    need(tuple(fields) == FIELDS and cursor == 32 and re.search(r'BFNT_HEADER_SIZE\s+EQU\s+32',text), 'complete packed32 header layout')
    table = (work/'obj/th03/mainl.map').read_text()
    for cls, base, size, name, seg, group in (('CODE',CODE_BASE,10944,'_TEXT',0,'(none)'),
            ('DATA',DATA_BASE,2036,'_DATA',DS,'DGROUP'),('BSS',0x13F6,5108,'_BSS',DS,'DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$',table)) == 1, 'containing native MAP allocation')
    need(address(table,'Palettes') == (DS,0x141E), 'actual48-byte palette BSS reference')
    decoder = Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail = True
    owners, native, instructions = [], [], []
    for unit, source, start, size, procs, evens, borrowed, field_count in (
        (BFNT_UNIT,SOURCES[0],0x272,512,PROCEDURES[:4],(0x411,0x471),(0x272,20),12),
        (PALETTE_UNIT,SOURCES[4],0x4C6,64,PROCEDURES[4:],(),None,1)):
        image, reloc_fields = resolve(raw,start,size)
        need(len(reloc_fields) == field_count, 'complete scoped native field stream')
        extent((target,candidate),image,0,start,[])
        ins = list(decoder.disasm(image,start));instructions += ins
        need(sum(i.size for i in ins) == size, 'complete instruction coverage, including ordinary EVEN')
        bounds = {i.address for i in ins}
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):
                need(i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds, 'complete local branch destinations')
        procedures = []
        for name,off,count,cleanup in procs:
            body = [i for i in ins if off <= i.address < off+count]
            need(sum(i.size for i in body) == count and body[-1].mnemonic == 'retf' and
                 int(body[-1].op_str,0) == cleanup and (off-CODE_BASE,name) in code_publics(raw,1) and
                 address(table,name) == (0,off), 'whole far Pascal body and both MAP public tables: '+name)
            procedures.append(dict(name=name,offset=off-start,size=count,callee_pop_bytes=cleanup,instruction_count=len(body)))
        need(sum(p['size'] for p in procedures)+len(evens)+(borrowed[1] if borrowed else 0) == size and
             all(next(i for i in ins if i.address == a).mnemonic == 'nop' for a in evens), 'complete body/shared-exit/outer-EVEN partition')
        owners.append(owner(unit,source,0,start,image,size,0,procedures,report))
        native.append(dict(unit_id=unit,fields=reloc_fields,ordered_relocations=[],ordinary_outer_EVEN_bytes=list(evens),
                           borrowed_error_extent=list(borrowed) if borrowed else None))
    insmap = {i.address:i for i in instructions}
    smc, reads = [], []
    for field in [f for f in native[0]['fields'] if f['target'] == 1]:
        instruction = next(i for i in instructions if i.address <= field['site'] < i.address+i.size)
        dest = field['value'];need(dest in SMC and instruction.mnemonic == 'mov', 'actual CS operand reference')
        operand, = [o for o in instruction.operands if o.type == X86_OP_MEM and o.mem.segment == X86_REG_CS]
        consumer = next(i for i in instructions if i.address <= dest < i.address+i.size)
        need(operand.mem.disp == dest and operand.size == SMC[dest] and consumer.mnemonic == 'mov' and
             consumer.imm_size == SMC[dest] and consumer.address+consumer.imm_offset == dest, 'complete real MOV operand slot')
        writer = instruction.operands[0].type == X86_OP_MEM
        (smc if writer else reads).append(dict(instruction=instruction.address,field=field['site'],destination=dest,width=operand.size))
    need(len(smc) == 8 and {s['destination'] for s in smc} == set(SMC) and len(reads) == 3 and
         {s['destination'] for s in reads} == {0x35F}, 'all8 writers/eight operand slots and3 saved-DS reads')
    need([(insmap[a].mnemonic,insmap[a].op_str) for a in (0x28A,0x28B,0x27F,0x280,0x281,0x282)] ==
         [('push','si'),('push','di'),('pop','si'),('pop','di'),('pop','ds'),('pop','bp')], 'original swapped SI/DI unwind, without ABI repair')
    data = byte_map(raw,2)
    signature = bytes(data[i] for i in range(0x51C-DATA_BASE,0x522-DATA_BASE))
    signature_block = False
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            begin = int.from_bytes(record.data[1:3],'little')
            signature_block = record.data[0] == 2 and begin <= 0x51C-DATA_BASE < begin+len(record.data)-3
        elif record.name == 'FIXUPP':
            need(not signature_block, 'literal signature-containing LEDATA has no native fields')
    need(signature == b'BFNT\x1a\0' and address(table,'BFNT_ID') == address(table,'_BFNT_ID') == (DS,0x51C), 'complete source signature/NUL and aliases')
    extent((target,candidate),signature,DS,0x51C,[])
    owners.append(owner(DATA_UNIT,SELECTED_SOURCE,DS,0x51C,signature,0,6,[],report))
    need(native[0]['fields'][-1]['value'] == 0x51C and native[0]['fields'][-1]['target'] == 2 and
         native[1]['fields'][0]['value'] == 0x141E and native[1]['fields'][0]['target'] == 9, 'actual signature DATA and palette BSS offsets')
    return dict(owners=owners,library_CODE_bytes=576,library_initialized_DATA_bytes=6,procedures=5,
        native_scopes=native,packed_header_fields=[dict(name=n,offset=o,size=s) for n,o,s in fields],packed_header_bytes=32,
        SMC_writers=smc,saved_DS_operand_reads=reads,borrowed_error_is_procedure=False,original_SI_DI_swap_preserved=True,
        selected_build_report_sha256=report_sha,selected_assembly_link_rounds=2,context_project_objects_reused=35,
        source_paths=SOURCES+[TYPES,SELECTED_SOURCE],original_cold_rebuilt=False,header_scratch_or_palette_BSS_credited=False,
        runtime_matrix_required=False,physical_DOS_or_palette_execution_claimed=False,whole_product_accepted=False)


def owner(unit,source,segment,offset,image,code,data,procedures,report):
    return dict(unit_id=unit,name=unit.removeprefix('th03-mainl-decoded-'),source=source,object=OBJECT,origin='library',
        segment=segment,offset=offset,start=segment*16+offset,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],code_bytes=code,initialized_data_bytes=data,
        procedure_count=len(procedures),procedures=procedures,private_data_bytes=0,private_bss_bytes=0,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
        abi='original16-bit far Pascal; shared borrowed entry unwind preserves original SI/DI swap' if procedures else 'six signature bytes and two public aliases')


if __name__ == '__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['bfnt_native'],indent=2))
