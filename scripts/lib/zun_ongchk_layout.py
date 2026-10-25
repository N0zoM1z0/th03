"""One complete library COM source owner, including meaningful DATA and BSS.

The original source/assembler remain unidentified. Native producer identity,
ordered symbolic fields and decoded coordinates are independently checked.
"""
import hashlib
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86 import X86_OP_IMM
from lib.zun import parse_launcher
from lib.zun_ongchk_source import SOURCE,verify_outputs

def need(v,m):
    if not v:raise ValueError('ONGCHK exact layout: '+m)

def verify(work,target,candidate,files,maintained,cold):
    need(target==candidate and len(target)==22812,'complete current decoded product equality')
    child=parse_launcher(target,223)['payloads'][0]
    need(child['name']=='-1' and child['size']==926,'actual first payload directory slot')
    at=child['decoded_file_offset'];body=target[at:at+926]
    native=verify_outputs(*[(work/('ongchk/ongchk.'+ext)).read_bytes() for ext in ('obj','com','map')],body)
    need(native==cold['ongchk_source_candidate'],'current self-contained native source layout')
    root=Path(__file__).resolve().parents[2]
    need(SOURCE in maintained and maintained[SOURCE]==(root/SOURCE).read_bytes()
         and files['ongchk/ongchk.asm']==maintained[SOURCE].replace(b'\n',b'\r\n')
         and (work/'ongchk/ongchk.asm').read_bytes()==files['ongchk/ongchk.asm'],
         'actual maintained source transport')
    need('libs/kaja/ongchk.com' not in files and cold['source_context']['vendor_inputs'][0]['path']=='bin/masters.lib'
         and len(cold['source_context']['vendor_inputs'])==1,'no ONGCHK binary input')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    instructions={i.address:i for i in decoder.disasm(body[:892],0x100)}
    loops={
      'register':(0x461,(0x461,0x462,0x464),'or','js',16),
      'write_idle':(0x350,(0x350,0x351,0x353),'or','js',6),
      'dummy_idle':(0x42D,(0x42D,0x42E,0x430),'test','js',8),
      'read_idle':(0x3FE,(0x3FE,0x3FF,0x401),'test','js',6),
      'read_ready':(0x407,(0x407,0x408,0x40A),'test','je',6),
      'read_data':(0x40D,(0x40D,0x40E,0x410),'or','js',6)}
    cycles=[]
    for name,(entry,sites,test,jump,depth) in loops.items():
        rows=[instructions[s] for s in sites]
        need([i.mnemonic for i in rows]==['in',test,jump] and rows[0].op_str=='al, dx'
             and rows[-1].operands[0].type==X86_OP_IMM and rows[-1].operands[0].imm==entry,
             'closed IN/logic/conditional native polling cycle: '+name)
        need(rows[1].op_str==('al, 8' if name=='read_ready' else 'al, al'),'actual held condition')
        cycles.append(dict(name=name,entry=entry,instruction_starts=list(sites),stack_depth=depth,
            held_reply=0 if name=='read_ready' else 128,body_bytes=sum(i.size for i in rows),no_stores_or_stack_effects=True))
    rows=[instructions[s] for s in (0x377,0x378,0x37A,0x37C,0x37D)]
    need([i.mnemonic for i in rows]==['in','test','jns','in','jmp']
         and rows[2].operands[0].imm==0x37F and rows[-1].operands[0].imm==0x377
         and all(i.op_str=='al, dx' for i in (rows[0],rows[3])),'closed write-completion two-read cycle')
    cycles.append(dict(name='write_complete',entry=0x377,instruction_starts=[i.address for i in rows],stack_depth=6,
        held_reply=128,body_bytes=sum(i.size for i in rows),no_stores_or_stack_effects=True))
    h=hashlib.sha256(body).hexdigest()
    owner=dict(unit_id='th03-zun-decoded-ongchk',name='ONGCHK',source=SOURCE,object='ongchk/ongchk.obj',
        origin='library',segment='decoded:-1',start=0x100,size=926,code_bytes=892,data_bytes=34,bss_bytes=42,
        coordinate_space='decoded-payload-com',payload_option='-1',outer_decoded_file_offset=at,canonical_file_offset=None,
        target_sha256=h,candidate_sha256=h,ordered_relocations=[],ordered_native_fields=native['native_fields'],
        abi='COM startup at 0100; inherited SS and retained count WORD; terminal DOS 4C; nine real near helpers with two shared RET tails')
    return dict(owners=[owner],source_extents=1,entry_points=10,code_bytes=892,data_bytes=34,bss_bytes=42,
        native=native,ordered_relocations=[],polling_cycles=cycles,all_initialized_DATA_semantically_owned=True,
        original_source_attested=False,original_assembler_attested=False,whole_product_accepted=False)
