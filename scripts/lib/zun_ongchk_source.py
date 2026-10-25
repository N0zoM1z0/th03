"""Native source-presence proof for ONGCHK; no exact acceptance is granted.

The complete 926-byte image is emitted by ordinary TASM/TLINK. The declared
42-byte BSS begins at 049E and is not a binary input or file-backed filler.
"""
import hashlib,re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf,describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

SOURCE='src/zun/ongchk.asm'
CODE_PUBLICS=((0x100,'start'),(0x127,'probe_hardware'),(0x1A0,'probe_type3'),(0x247,'probe_type2'),
 (0x2C2,'probe_found'),(0x2DD,'probe_failed'),(0x2E4,'adpcm_check'),(0x2FB,'adpcm_write'),
 (0x3A8,'adpcm_read'),(0x428,'adpcm_dummy_read'),(0x449,'adpcm_compare'),(0x455,'adpcm_register_write'),
 (0x47C,'ram_pattern'),(0x49C,'port_override'),(0x49D,'probe_result'))
BSS_PUBLICS=((0,'fm_address_port'),(2,'fm_data_port'),(4,'adpcm_address_port'),(6,'adpcm_data_port'),
 (8,'has_board_rom'),(9,'type2_first'),(10,'ram_buffer'))
FIELDS=((265,'type2_first'),(282,'type2_first'),(291,'probe_result'),(297,'type2_first'),
 (314,'type2_first'),(326,'probe_result'),(336,'port_override'),(343,'port_override'),
 (399,'probe_result'),(411,'probe_result'),(418,'probe_result'),(423,'has_board_rom'),
 (442,'has_board_rom'),(479,'port_override'),(486,'port_override'),(570,'has_board_rom'),
 (585,'probe_result'),(590,'has_board_rom'),(609,'has_board_rom'),(640,'port_override'),
 (647,'port_override'),(708,'fm_address_port'),(715,'fm_data_port'),(722,'adpcm_address_port'),
 (729,'adpcm_data_port'),(735,'probe_result'),(833,'ram_pattern'),(840,'adpcm_address_port'),
 (844,'adpcm_data_port'),(1015,'ram_buffer'),(1019,'adpcm_address_port'),(1044,'adpcm_data_port'),
 (1067,'adpcm_address_port'),(1086,'adpcm_data_port'),(1098,'ram_pattern'),(1101,'ram_buffer'),
 (1116,'adpcm_address_port'),(1138,'adpcm_data_port'))

def need(value,message):
    if not value:raise ValueError('ONGCHK native source: '+message)

def verify_outputs(obj,linked,mapping,target=None):
    records=parse_omf(obj);d=describe_omf(obj)
    need(d['valid'] and d['module_name']=='ongchk.asm'
         and d['translator_comments']==['Turbo Assembler  Version 5.0']
         and d['dependency_paths']==['ongchk.asm'],'actual self-contained TASM producer')
    need(d['record_counts']==dict(COMENT=5,FIXUPP=1,GRPDEF=1,LEDATA=1,LNAMES=5,MODEND=1,PUBDEF=22,SEGDEF=3,THEADR=1),
         'complete self-contained native record closure; no binary includes or external symbols')
    need(segment_definitions(obj)==[
        dict(index=1,name='_TEXT',**{'class':'CODE'},overlay='',size=0x49E),
        dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),
        dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=42)],'ORG100 CODE/DATA and meaningful uninitialized workspace')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x48]*3,'WORD PUBLIC USE16 native segments')
    need([r.data for r in records if r.name=='GRPDEF']==[b'\x08\xFF\x03\xFF\x02\xFF\x01']
         and [r.data for r in records if r.name=='MODEND']==[b'\xC1\x10\x01\x01\0\x01'],
         'actual tiny DGROUP and 0100 entry')
    need(code_publics(obj,1)==list(CODE_PUBLICS) and code_publics(obj,2)==[]
         and code_publics(obj,3)==list(BSS_PUBLICS),'all complete native code/data/BSS publics')
    le,=[r.data for r in records if r.name=='LEDATA']
    need(le[:3]==b'\x01\0\x01' and len(le)==929,'one complete 926-byte initialized contribution, no BSS emission')
    resolved=bytearray(le[3:]);fields=[]
    addresses={n:(1,a) for a,n in CODE_PUBLICS};addresses.update({n:(3,a+0x49E) for a,n in BSS_PUBLICS})
    fix,=[r.data for r in records if r.name=='FIXUPP']
    need(len(fix)==5*len(FIELDS),'all thirty-eight native WORD fields')
    for at,(site,symbol) in zip(range(0,len(fix),5),FIELDS):
        loc,low,fd,frame,segment=fix[at:at+5]
        need(0x100+(loc&3)*256+low==site and loc&0xFC==0xC4 and fd==0x14 and frame==1,
             'literal own-segment absolute WORD with DGROUP frame')
        want_segment,want=addresses[symbol]
        add=int.from_bytes(resolved[site-0x100:site-0xFE],'little')
        value=add+(0x49E if segment==3 else 0)
        need(segment==want_segment and value==want,'native symbolic target: '+symbol)
        fields.append(dict(site=site,bytes=2,target=symbol,target_segment=segment,addend=add,resolved=value))
        resolved[site-0x100:site-0xFE]=value.to_bytes(2,'little')
    need(bytes(resolved)==linked and len(linked)==926,'complete resolved native COM bytes')
    if target is not None:need(linked==target,'complete attested target payload equality')
    text=mapping.decode('ascii')
    for offset,size,kind,name in ((0,0x49E,'CODE','_TEXT'),(0x49E,0,'DATA','_DATA'),(0x49E,42,'BSS','_BSS')):
        need(len(re.findall(rf'(?m)^\s*0000:{offset:04X}\s+{size:04X} C={kind}\s+S={name}\s+G=DGROUP\s+M=ongchk.asm ACBP=48\s*$',text))==1,
             'literal complete native MAP allocation')
    for name,(_,address) in addresses.items():
        need(len(re.findall(rf'(?m)^\s*0000:{address:05X}\s+(?:idle\s+)?{name}\s*$',text))==2,'both MAP public tables: '+name)
    instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(linked[:892],0x100))
    need(sum(i.size for i in instructions)==892 and instructions[-1].mnemonic=='ret','complete instruction-only code partition')
    need(linked[892:]==b'*+=-PMD ADPCM RAM Check Data-=+*\xFF\0','semantic 32-byte test vector and two mutable defaults')
    return dict(source=SOURCE,code_bytes=892,initialized_data_bytes=34,bss_bytes=42,
        native_fields=fields,initialized_publics=[list(p) for p in CODE_PUBLICS],
        bss_publics=[list(p) for p in BSS_PUBLICS],file_bytes=926,file_sha256=hashlib.sha256(linked).hexdigest(),
        binary_seed_consumed=False,original_source_identity_attested=False,original_assembler_identity_attested=False,
        exact_acceptance=False,canonical_unit_credit_changed=False,whole_product_accepted=False)
