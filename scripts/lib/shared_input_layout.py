"""Complete native ownership of the shared nine-function input producer.

OP and MAINL use the same maintained source with independently reviewed target
addresses. Native far calls are relaxed by TLINK; no object is rewritten here.
This physical proof alone grants no source/behavior or canonical-file acceptance.
"""
import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

SOURCE = 'src/shared/hardware/input_modes.cpp'
WRAPPER = 'th03/inp_m_w.cpp'
OBJECT = 'obj/th03/inp_m_w.obj'
FUNCTIONS = (
    ('input-interface', 'input_mode_interface', 0, 36),
    ('input-key-key', 'input_mode_key_vs_key', 36, 10),
    ('input-joy-key', 'input_mode_joy_vs_key', 46, 34),
    ('input-key-joy', 'input_mode_key_vs_joy', 80, 34),
    ('input-one-cpu', 'input_mode_1p_vs_cpu', 114, 42),
    ('input-cpu-one', 'input_mode_cpu_vs_1p', 156, 45),
    ('input-cpu-cpu', 'input_mode_cpu_vs_cpu', 201, 42),
    ('input-attract', 'input_mode_attract', 243, 48),
    ('input-change', 'input_wait_for_change', 291, 76),
)
EXTERNALS = ('_js_bexist', '_js_stat', 'JS_SENSE', '@FRAME_DELAY$QI',
             '_input_mp_p1', '_input_mp_p2', '_input_sp', '@input_reset_sense_key_held$qv')
PROFILES = {
    'op': dict(artifact='th03-op', folder='TH03OP', code_segment=0xBEB, start=0xAD6,
               data_segment=0xD7F, empty_data=0x5F2, empty_bss=0x1F70,
               presence=0x2CC, joystick=0x11B4, player1=0x1AA2, player2=0x1AA4,
               single=0x1AA6, sense=0x304, delay=0x2EE, js=0x2DF4),
    'mainl': dict(artifact='th03-mainl', folder='TH03ML', code_segment=0xC7E, start=0xDC2,
                  data_segment=0xE3F, empty_data=0x906, empty_bss=0x27EA,
                  presence=0x570, joystick=0x141A, player1=0x1D08, player2=0x1D0A,
                  single=0x1D0C, sense=0x388, delay=0x372, js=0x2AEA),
}
# Ordered native (offset, width, external-index) fields are independent of load
# addresses. The native emitter orders fields backwards; the six MZ relocation
# records follow its actual JS_SENSE pointer order, rather than sorted sites.
FIXUPS = (
    (345,4,4),(336,2,7),(315,4,4),(307,2,7),(285,2,6),(279,2,5),
    (275,2,7),(271,2,5),(268,2,7),(264,2,2),(259,4,3),(253,2,1),
    (247,4,8),(237,2,6),(231,2,5),(225,2,7),(218,2,7),(211,2,7),
    (205,4,8),(195,2,5),(191,2,6),(187,2,2),(182,4,3),(176,2,1),
    (172,2,6),(169,2,5),(165,2,7),(160,4,8),(150,2,6),(146,2,5),
    (142,2,2),(137,4,3),(131,2,1),(127,2,5),(123,2,7),(118,4,8),
    (110,2,5),(107,2,7),(104,2,6),(101,2,2),(96,4,3),(90,2,1),
    (84,4,8),(76,2,6),(73,2,7),(70,2,5),(67,2,2),(62,4,3),
    (56,2,1),(50,4,8),(40,4,8),(32,2,7),(28,2,5),(25,2,7),
    (21,2,2),(16,4,3),(10,2,1),(4,4,8),
)


def need(value, message):
    if not value: raise ValueError('shared input layout: ' + message)


def external_addresses(profile):
    p = PROFILES[profile]
    return dict(zip(EXTERNALS, ((p['data_segment'],p['presence']),
        (p['data_segment'],p['joystick']), (0,p['js']), (p['code_segment'],p['delay']),
        (p['data_segment'],p['player1']), (p['data_segment'],p['player2']),
        (p['data_segment'],p['single']), (p['code_segment'],p['sense']))))


def native_image(raw, profile):
    """Resolve all real OMF fields into a comparison buffer, never a product."""
    p = PROFILES[profile]
    records = parse_omf(raw)
    description=describe_omf(raw)
    need(description['translator_comments'] == ['TC86 Borland C++ 4.02'], 'native TC4 translator')
    need(description['module_name']==WRAPPER and description['record_counts']==dict(COMENT=17,EXTDEF=1,FIXUPP=1,
         GRPDEF=1,LEDATA=1,LNAMES=1,MODEND=1,PUBDEF=9,SEGDEF=3,THEADR=1)
         and records[-1].name=='MODEND' and records[-1].data==b'\0','complete reviewed native module/record closure')
    need(segment_definitions(raw) == [dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=367),
        dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),
        dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)], 'whole CODE and zero private DATA/BSS')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x28,0x48,0x48], 'BYTE CODE and WORD DATA/BSS USE16')
    names=[None]
    for rec in records:
        if rec.name!='LNAMES': continue
        at=0
        while at<len(rec.data):
            n=rec.data[at];at+=1;names.append(rec.data[at:at+n].decode('ascii'));at+=n
    groups=[r.data for r in records if r.name=='GRPDEF']
    need(len(groups)==1 and names[groups[0][0]]=='DGROUP' and groups[0][1:]==b'\xff\x02\xff\x03','complete DATA/BSS group')
    externals=[]
    for rec in records:
        if rec.name!='EXTDEF':continue
        at=0
        while at<len(rec.data):
            n=rec.data[at];at+=1;externals.append(rec.data[at:at+n].decode('ascii'));at+=n
            need(rec.data[at]==0,'untyped native external');at+=1
    need(tuple(externals)==EXTERNALS,'complete symbolic external order')
    need(code_publics(raw,1)==[(off,'@'+name.upper()+('$QI' if off==291 else '$QV')) for _,name,off,_ in FUNCTIONS], 'nine whole OMF public procedures')
    body,blocks=code_bytes(raw,1)
    need(len(body)==367 and [(b['offset'],b['size']) for b in blocks]==[(0,367)],'single complete native CODE record')
    image=bytearray(body); fields=[];relaxed=[];addresses=external_addresses(profile)
    for rec in records:
        if rec.name!='FIXUPP':continue
        at=0
        while at<len(rec.data):
            need(at+4<=len(rec.data),'complete native fixup field')
            loc,low,fd=rec.data[at:at+3];at+=3
            kind=loc>>2&15
            need(loc&0xC0==0xC0 and kind in (1,3) and fd in (0x16,0x56),'literal WORD/pointer external fixup')
            if fd==0x16:need(rec.data[at]==1,'DGROUP frame');at+=1
            index=rec.data[at];at+=1
            need(1<=index<=len(externals),'bounded external index')
            width=2 if kind==1 else 4;site=(loc&3)*256+low
            need(site+width<=367 and not any(site<f[0]+f[1] and f[0]<site+width for f in fields),'whole nonoverlapping native fields')
            addend=int.from_bytes(body[site:site+width],'little')
            need(addend==(1 if site in (211,218) else 0),'literal native external addend')
            name=externals[index-1];segment,offset=addresses[name]
            if width==2:
                need(fd==0x16 and segment==p['data_segment'],'WORD external belongs to DGROUP')
                image[site:site+2]=(offset+addend).to_bytes(2,'little')
            else:
                need(fd==0x56 and site>0 and body[site-1]==0x9A,'actual far CALL pointer')
                if segment==p['code_segment']:
                    delta=(offset-(p['start']+site+4))&65535
                    image[site-1:site+4]=b'\x90\x0E\xE8'+delta.to_bytes(2,'little');relaxed.append(site-1)
                else:image[site:site+4]=offset.to_bytes(2,'little')+segment.to_bytes(2,'little')
            fields.append((site,width,index))
    need(tuple(fields)==FIXUPS,'all 58 ordered native fields')
    need(len(relaxed)==10,'eight reset and two frame-delay far-call relaxations')
    return bytes(image),fields,relaxed


def verify(work, target, candidate, profile):
    p=PROFILES[profile];raw=(work/OBJECT).read_bytes();description=describe_omf(raw)
    dependencies=[n.replace(chr(92),'/') for n in description['dependency_paths']]
    need(description['valid'] and SOURCE in dependencies and WRAPPER in dependencies,'actual maintained producer/source closure')
    need((work/WRAPPER).read_text().replace('\r\n','\n')=='#include "'+SOURCE+'"\n','actual complete shared wrapper')
    image,fields,relaxed=native_image(raw,profile)
    start=p['code_segment']*16+p['start'];end=start+367
    need(image==target.program_image[start:end]==candidate.program_image[start:end],'complete naturally resolved native target equality')
    text=(work/f'obj/th03/{profile}.map').read_text().replace(chr(92),'/')
    for segment,offset,size,cls,name,group,attr in ((p['code_segment'],p['start'],367,'CODE','SHARED',r'\(none\)',0x28),
        (p['data_segment'],p['empty_data'],0,'DATA','_DATA','DGROUP',0x48),
        (p['data_segment'],p['empty_bss'],0,'BSS','_BSS','DGROUP',0x48)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={group}\s+M=th03/inp_m_w\.cpp\s+ACBP={attr:02X}\s*$',text))==1,'complete literal MAP allocation')
    for name,(seg,off) in external_addresses(profile).items():
        symbol=('@input_reset_sense_key_held$qv' if name=='@input_reset_sense_key_held$qv' else name)
        symbol={'@input_reset_sense_key_held$qv':'input_reset_sense_key_held()','@FRAME_DELAY$QI':'frame_delay(int)','JS_SENSE':'JS_SENSE'}.get(symbol,symbol)
        # Master's assembly exports both decorated/undecorated data names; bind
        # the exact underscore spelling used by native EXTDEF.
        need(len(re.findall(rf'(?mi)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,'external in both MAP tables: '+symbol)
    expected_pairs=[[p['code_segment'],p['start']+site+2] for site,width,index in FIXUPS if index==3]
    pairs=[]
    for mz in (target,candidate):
        need(not any(r.linear<end and r.linear+2>start and not start<=r.linear<=end-2 for r in mz.relocations),'no relocation straddles producer')
        pairs.append([[r.segment,r.offset] for r in mz.relocations if start<=r.linear<end])
    need(pairs==[expected_pairs,expected_pairs],'six literal ordered JS far-call relocation records')
    owners=[]
    for suffix,name,offset,size in FUNCTIONS:
        entry=p['start']+offset;address=start+offset
        need(len(re.findall(rf'(?m)^\s*{p["code_segment"]:04X}:{entry:04X}\s+(?:idle\s+)?{re.escape(name)}\({"int" if offset==291 else ""}\)\s*$',text))==2,'both whole function MAP publics')
        chunk=image[offset:offset+size];digest=hashlib.sha256(chunk).hexdigest()
        owners.append(dict(unit_id=p['artifact']+'-decoded-'+suffix,name=name,source=SOURCE,object=OBJECT,
            segment=p['code_segment'],offset=entry,start=address,size=size,coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=digest,candidate_sha256=digest,
            ordered_relocations=[pair for pair in expected_pairs if address<=pair[0]*16+pair[1]<address+size],
            abi='far Pascal; RETF 2' if offset==291 else 'far Pascal; no arguments; RETF',private_data_bytes=0,private_bss_bytes=0))
    return dict(owners=owners,functions=9,code_bytes=367,private_data_bytes=0,private_bss_bytes=0,
        ordered_native_fields=[dict(offset=s,width=w,external=EXTERNALS[i-1]) for s,w,i in fields],
        ordered_relocations=expected_pairs,normal_tlink_relaxed_calls=relaxed,
        native_ownership_reviewed=True,acceptance_requires_current_publication=True,whole_product_accepted=False)


def unit_ids(profile):
    return {PROFILES[profile]["artifact"]+"-decoded-"+suffix for suffix,_,_,_ in FUNCTIONS}
