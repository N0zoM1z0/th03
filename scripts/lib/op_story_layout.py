"""Complete story caller, with separate static-table and library dependencies."""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.op_cfg_layout import OBJECT,SEGMENT,OFFSET,DATA_SEGMENT,verify as containing_layout
from lib.op_vs_layout import resolve

START,SIZE=0x9A17,390
RANDOM,RANDOM_SIZE=0x1D12,42
FIELDS=((649,4,206,86,None,46,0),(646,2,198,20,2,2,223),(642,2,198,20,2,2,223),
 (633,4,206,86,None,12,0),(628,4,206,86,None,33,0),(620,4,206,86,None,3,0),
 (589,2,198,22,2,15,0),(572,2,198,22,2,15,0),(537,2,198,22,2,15,0),
 (513,2,198,22,2,15,0),(474,2,197,22,2,15,0),(442,2,197,22,2,15,0),
 (429,2,197,22,2,15,0),(415,2,197,20,2,2,9),(400,2,197,20,2,2,9),
 (382,4,205,86,None,20,0),(375,2,197,22,2,19,0),(366,2,197,22,2,15,0),
 (357,2,197,20,2,2,16),(339,2,197,22,2,15,0),(326,2,133,22,1,44,0),(278,2,197,22,2,15,0))
EXTERNALS={3:('GAIJI_RESTORE',0,0xF1A),12:('@game_exit$qv',0xBEB,0x112),
 15:('_resident',DATA_SEGMENT,0x2464),19:('_random_seed',DATA_SEGMENT,0x312),
 20:('IRAND',0,RANDOM),33:('SND_KAJA_INTERRUPT',0xBEB,0x553),
 44:('@select_story_menu$qv',SEGMENT,0x249A),46:('_execl',0,0x9119)}

def need(v,m):
    if not v:raise ValueError('OP story layout: '+m)

def verify(work,target,candidate):
    containing_layout(work,target,candidate)
    image,fields=resolve((work/OBJECT).read_bytes(),271,661,OFFSET,EXTERNALS)
    need(tuple(fields)==FIELDS and image==target.program_image[START:START+SIZE]
         ==candidate.program_image[START:START+SIZE],'complete source producer and all 22 native fields')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    ins={i.address:i for i in decoder.disasm(image,START)}
    need(sum(i.size for i in ins.values())==SIZE and ins[START+SIZE-1].mnemonic=='ret','complete near function')
    text=(work/'obj/th03/op.map').read_text()
    for seg,off,name in ((SEGMENT,0x117,'story_menu()'),(0,RANDOM,'IRAND'),(DATA_SEGMENT,0x312,'_random_seed'),
                         (SEGMENT,0x249A,'select_story_menu()')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both literal MAP publics: '+name)
    pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START<=r.linear<START+SIZE]==pairs,'five ordered MZ relocations')
        need(not any(r.linear<START+SIZE and r.linear+2>START and not START<=r.linear<=START+SIZE-2 for r in mz.relocations),'no straddling relocation')
        body=mz.program_image[RANDOM:RANDOM+RANDOM_SIZE]
        need(hashlib.sha256(body).hexdigest()=='f359b845e844a9dc8207e6037c0e5a46d14932ea09958949f4c805c0b27f94ea','actual 42-byte library random helper')
        need(not any(RANDOM<=r.linear<RANDOM+RANDOM_SIZE for r in mz.relocations),'no random helper MZ relocations')
        data=mz.program_image[DATA_SEGMENT*16:]
        need(data[0x99:0xA0]==bytes(7) and data[0xA0:0xA9]==bytes((1,0,0,2,0,3,5,4,6)),'source static defaults and nine-row table dependency')
    # A full blocked candidate domain closes this loop independently of an
    # emulator instruction budget. IRAND returns 0..32767, then signed IDIV 7
    # leaves a candidate 0..6. Each seen/excluded candidate returns to the call.
    expected={0x9A85:('lcall','0, 0x1d12'),0x9A8A:('mov','bx, 7'),0x9A8D:('cdq',''),
      0x9A8E:('idiv','bx'),0x9A90:('mov','word ptr [bp - 2], dx'),
      0x9A93:('mov','bx, word ptr [bp - 2]'),0x9A96:('cmp','byte ptr [bx + 0x99], 0'),
      0x9A9B:('jne','0x9a85'),0x9A9D:('mov','ax, word ptr [bp - 4]'),
      0x9AA0:('cmp','ax, word ptr [bp - 2]'),0x9AA3:('je','0x9a85')}
    need(all((ins[a].mnemonic,ins[a].op_str)==v for a,v in expected.items()),'closed blocked-candidate native CFG')
    h=hashlib.sha256(image).hexdigest()
    owner=dict(unit_id='th03-op-decoded-entry-screens',name='story_menu',source='src/op/entry.cpp',object=OBJECT,
        segment=SEGMENT,offset=0x117,start=START,size=SIZE,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=h,candidate_sha256=h,ordered_relocations=pairs,argument_bytes=0,callee_pop_bytes=0,
        private_data_bytes=0,private_bss_bytes=0,abi='near no-argument entry; AL bool; preserved BP/SI/DI; static seen state persists after failed exec')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=[list(f) for f in FIELDS],ordered_relocations=pairs,
        reviewed_initialized_dependency_bytes=139,dependency_ranges=[[0x99,7],[0xA0,128],[0x312,4]],
        blocked_candidate_CFG=sorted(expected),library_random_dependency_bytes=42,library_random_source_credit_added=False,
        character_selection_procedure_owned=False,containing_producer_accepted=False,whole_product_accepted=False)
