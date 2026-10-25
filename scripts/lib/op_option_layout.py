"""Complete menu movement and option caller; the main caller stays separate."""
import hashlib,re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf,describe_omf
from lib.op_cfg_layout import OBJECT,WRAPPER,SEGMENT,OFFSET,DATA_SEGMENT,DATA_OFFSET,verify as containing_layout
from lib.op_render_layout import verify as renderer_layout
from lib.op_vs_layout import verify as vs_layout
from probe_th03_main_boss_marisa_cpp import code_bytes
SOURCE='src/op/menu/menu_state.inl'
FUNCTIONS=(('th03-op-decoded-menu-move','move',1945,63,'menu_sel_update_and_render(char,char)',4),
 ('th03-op-decoded-menu-option','option',2299,532,'option_update_and_render()',0))
ENTRIES={name:(SEGMENT*16+OFFSET+off,size) for _,name,off,size,_,_ in FUNCTIONS}
EXTERNALS={10:('TEXT_CLEAR',0,0x21F4),15:('_resident',DATA_SEGMENT,0x2464),16:('_input_sp',DATA_SEGMENT,0x1AA6),
 31:('_snd_active',DATA_SEGMENT,0x5DC),32:('_snd_determine_mode',0xBEB,0x4A),33:('SND_KAJA_INTERRUPT',0xBEB,0x553),
 35:('@box_main_to_submenu_animate$qv',SEGMENT,0x17AF)}
FIELDS=(
 (2002, 2, 199, 20, 2, 3, 4),
 (1993, 2, 199, 20, 2, 2, 209),
 (1989, 2, 199, 20, 2, 2, 209),
 (1980, 2, 199, 20, 2, 2, 209),
 (1977, 2, 199, 20, 2, 2, 209),
 (1968, 2, 199, 20, 2, 2, 209),
 (1964, 2, 199, 20, 2, 2, 209),
 (1957, 2, 199, 20, 2, 3, 4),
 (1949, 2, 199, 20, 2, 2, 209),
 (2825, 2, 199, 20, 2, 3, 1),
 (2818, 2, 199, 22, 2, 16, 0),
 (2813, 2, 199, 20, 2, 3, 2),
 (2808, 2, 198, 20, 2, 2, 209),
 (2803, 2, 198, 20, 2, 2, 213),
 (2796, 2, 198, 22, 2, 16, 1),
 (2791, 2, 198, 20, 2, 3, 2),
 (2786, 2, 198, 20, 2, 2, 209),
 (2781, 2, 198, 20, 2, 2, 213),
 (2771, 2, 198, 20, 2, 2, 209),
 (2765, 2, 198, 22, 2, 16, 0),
 (2758, 2, 198, 22, 2, 16, 1),
 (2746, 2, 198, 20, 2, 2, 209),
 (2739, 2, 198, 22, 2, 15, 0),
 (2721, 2, 198, 22, 2, 15, 0),
 (2707, 2, 198, 20, 2, 2, 209),
 (2703, 2, 198, 22, 2, 31, 0),
 (2697, 4, 206, 86, None, 33, 0),
 (2686, 2, 198, 22, 2, 15, 0),
 (2678, 4, 206, 86, None, 33, 0),
 (2671, 4, 206, 86, None, 32, 0),
 (2666, 4, 206, 86, None, 33, 0),
 (2648, 2, 198, 22, 2, 15, 0),
 (2641, 2, 198, 20, 2, 2, 0),
 (2631, 2, 198, 22, 2, 15, 0),
 (2613, 2, 198, 22, 2, 15, 0),
 (2591, 2, 198, 20, 2, 2, 209),
 (2583, 2, 198, 22, 2, 16, 0),
 (2571, 2, 198, 20, 2, 2, 209),
 (2552, 2, 197, 22, 2, 15, 0),
 (2538, 2, 197, 20, 2, 2, 209),
 (2534, 2, 197, 22, 2, 31, 0),
 (2528, 4, 205, 86, None, 33, 0),
 (2517, 2, 197, 22, 2, 15, 0),
 (2509, 4, 205, 86, None, 33, 0),
 (2502, 4, 205, 86, None, 32, 0),
 (2497, 4, 205, 86, None, 33, 0),
 (2479, 2, 197, 22, 2, 15, 0),
 (2472, 2, 197, 20, 2, 2, 0),
 (2450, 2, 197, 22, 2, 15, 0),
 (2429, 2, 197, 20, 2, 2, 209),
 (2421, 2, 197, 22, 2, 16, 0),
 (2407, 2, 197, 22, 2, 16, 0),
 (2393, 2, 197, 22, 2, 16, 0),
 (2384, 2, 197, 20, 2, 3, 1),
 (2379, 2, 197, 20, 2, 3, 1),
 (2372, 2, 197, 22, 2, 16, 0),
 (2367, 2, 197, 20, 2, 3, 1),
 (2362, 2, 197, 20, 2, 2, 213),
 (2358, 2, 197, 20, 1, 1, 1615),
 (2356, 2, 197, 20, 2, 3, 4),
 (2329, 2, 197, 20, 2, 2, 209),
 (2320, 2, 197, 20, 2, 3, 1),
 (2316, 2, 133, 22, 1, 35, 0),
 (2311, 4, 205, 86, None, 10, 0),
 (2305, 2, 197, 20, 2, 2, 213),
)

def need(v,m):
    if not v:raise ValueError('OP option layout: '+str(m))

def native_image(raw,functions=FUNCTIONS,fields_expected=FIELDS,externals=EXTERNALS):
    code=code_bytes(raw,1)[0];image=bytearray(code);fields=[];names=[];block=None
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at];at+=1;names.append(rec.data[at:at+n].decode());at+=n
                need(rec.data[at]==0,'untyped native external');at+=1
        elif rec.name=='LEDATA':block=rec.data[0],int.from_bytes(rec.data[1:3],'little')
        elif rec.name=='FIXUPP' and block[0]==1:
            at=0
            while at<len(rec.data):
                loc,lo,fd=rec.data[at:at+3];at+=3;frame=None
                need(fd in (20,22,86),'literal native field form')
                if fd in (20,22):frame=rec.data[at];at+=1
                target=rec.data[at];at+=1;s=block[1]+(loc&3)*256+lo;w=4 if loc>>2&15==3 else 2
                if not any(off<=s<off+size for _,_,off,size,_,_ in functions):continue
                need(any(off<=s and s+w<=off+size for _,_,off,size,_,_ in functions),'whole scoped native field')
                addend=int.from_bytes(code[s:s+w],'little');fields.append((s,w,loc,fd,frame,target,addend))
                if fd==20:
                    need(w==2 and loc&64 and (frame,target) in ((1,1),(2,2),(2,3)),'own CODE/DATA/BSS group offset')
                    value=addend+{1:OFFSET,2:DATA_OFFSET,3:0x118A}[target]
                else:
                    need(target in externals,'scoped symbolic external');_,seg,address=externals[target]
                    if fd==86:
                        need(w==4 and code[s-1]==0x9A,'real far CALL');value=(seg<<16)+address+addend
                    elif w==4:
                        need(loc&64 and frame==1 and seg==SEGMENT and code[s-1]==0x9A and addend==0,'normal same-CS symbolic far CALL')
                        # Comparison buffer only: TLINK's native same-CS relaxation.
                        # The object and executable remain untouched.
                        image[s-1:s+4]=bytes((0x90,0x0E,0xE8))+((address-(OFFSET+s+4))&65535).to_bytes(2,'little')
                        continue
                    elif loc&64:
                        need(w==2 and frame==2 and seg==DATA_SEGMENT,'external DGROUP WORD');value=address+addend
                    else:
                        need(w==2 and frame==1 and seg==SEGMENT,'relative near group CALL');value=(address+addend-(OFFSET+s+2))&65535
                image[s:s+w]=value.to_bytes(w,'little')
    need(tuple(fields)==fields_expected and all(names[i-1]==n for i,(n,_,_) in externals.items()),'all literal ordered fields and external identities')
    return bytes(image)

def verify(work,target,candidate):
    containing_layout(work,target,candidate);renderer_layout(work,target,candidate);vs_layout(work,target,candidate)
    raw=(work/OBJECT).read_bytes();image=native_image(raw);text=(work/'obj/th03/op.map').read_text()
    need(SOURCE in describe_omf(raw)['dependency_paths'] and WRAPPER in describe_omf(raw)['dependency_paths'],'maintained bounded include in actual native producer')
    owners=[]
    for unit,name,off,size,public,args in FUNCTIONS:
        start=SEGMENT*16+OFFSET+off;body=image[off:off+size]
        need(body==target.program_image[start:start+size]==candidate.program_image[start:start+size],'complete resolved native function bytes')
        rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,start));need(sum(i.size for i in rows)==size and rows[-1].mnemonic=='ret' and rows[-1].op_str==('4' if args else ''),'complete instruction body and actual cleanup')
        need(len(re.findall(rf'(?m)^\s*0990:{OFFSET+off:04X}\s+(?:idle\s+)?{re.escape(public)}\s*$',text))==2,'both function MAP public tables: '+public)
        pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4 and off<=s<off+size]
        for mz in (target,candidate):
            need([[r.segment,r.offset] for r in mz.relocations if start<=r.linear<start+size]==pairs,'complete literal ordered MZ vector')
            need(not any(r.linear<start+size and r.linear+2>start and not start<=r.linear<=start+size-2 for r in mz.relocations),'no straddling MZ fields')
        h=hashlib.sha256(body).hexdigest();owners.append(dict(unit_id=unit,name=name,source=SOURCE,object=OBJECT,segment=SEGMENT,offset=OFFSET+off,start=start,size=size,coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=pairs,argument_bytes=args,callee_pop_bytes=args,private_data_bytes=0,private_bss_bytes=0,abi='near Pascal signed BYTE parameters in WORD slots; RET 4' if args else 'near no-argument entry; BP/SI/DI preserved; RET'))
    pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4]
    for mz in (target,candidate):need([[r.segment,r.offset] for r in mz.relocations if any(o['start']<=r.linear<o['start']+o['size'] for o in owners)]==pairs,'cross-function literal relocation order')
    for name,seg,off in EXTERNALS.values():
        if name=='@box_main_to_submenu_animate$qv':name='box_main_to_submenu_animate()'
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both external MAP tables: '+name)
    return dict(owners=owners,functions=2,code_bytes=595,instruction_bytes=595,ordered_native_fields=[list(f) for f in FIELDS],ordered_relocations=pairs,private_data_bytes=0,private_bss_bytes=0,containing_producer_accepted=False,main_caller_accepted=False,whole_product_accepted=False)
