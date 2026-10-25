"""Complete native staff roll; static equality alone grants no runtime acceptance."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS,DS,SOURCE,WRAPPER,OBJECT,verify as enclosing_layout

START,SIZE,NATIVE=0x2E1D,980,2715
DATA=dict(seed=0x5B6,vsync=0x144E,tone=0x578,resident=0x21EA,score=0x27DC,
          page=0x27C4,enabled=0x27D7,requested=0x27C5,frame=0x27C2,cap=0x22C0,
          adapt=0x27C6,speed=0x27CC,duration=0x27CE,limit=0x27D0,height=0x27D4,
          secondary=0x27D6,playchar=0x27E7,rank=0x27E6,skill=0x27E8,input=0x1D0C)
BINDINGS={2:('_random_seed',DS,DATA['seed']),3:('_vsync_Count1',DS,DATA['vsync']),
 7:('GRCG_SETCOLOR',0,0xC36),8:('GRCG_OFF',0,0xC60),9:('GRCG_BYTEBOXFILL_X',0,0xB9E),
 10:('PALETTE_SHOW',0,0x17D0),11:('_PaletteTone',DS,DATA['tone']),12:('PALETTE_ENTRY_RGB',0,0x1A68),
 13:('PALETTE_BLACK_OUT',0,0x57A),16:('_resident',DS,DATA['resident']),17:('CDG_FREE',0xC7E,0x950),
 20:('@FRAME_DELAY$QI',0xC7E,0x372),28:('_page_back',DS,DATA['page']),30:('_score',DS,DATA['score']),
 32:('_mainl_dissolve_alpha_enabled',DS,DATA['enabled']),33:('_mainl_dissolve_alpha_requested',DS,DATA['requested']),
 37:('_mainl_snow_frame',DS,DATA['frame']),38:('_mainl_snow_slot_limit',DS,DATA['cap']),
 42:('SND_KAJA_INTERRUPT',0xC7E,0x6E2),43:('_snd_delay_until_volume',0xC7E,0x84),44:('_snd_load',0xC7E,0xA0),
 45:('_mainl_snow_auto_adjust',DS,DATA['adapt']),46:('_mainl_staff_speed',DS,DATA['speed']),
 47:('_mainl_staff_duration',DS,DATA['duration']),48:('_mainl_staff_center_limit',DS,DATA['limit']),
 49:('_mainl_staff_height_offset',DS,DATA['height']),50:('_mainl_staff_secondary_slot',DS,DATA['secondary']),
 54:('_mainl_verdict_playchar',DS,DATA['playchar']),55:('_mainl_verdict_rank',DS,DATA['rank']),56:('_mainl_verdict_skill',DS,DATA['skill']),
 57:('_input_sp',DS,DATA['input']),58:('@INPUT_MODE_INTERFACE$QV',0xC7E,0xDC2),
 59:('CDG_LOAD_SINGLE',0xC7E,0x73E),60:('CDG_LOAD_SINGLE_NOALPHA',0xC7E,0x7C8),
 61:('_mainl_staff_music',DS,0xC28),62:('_mainl_staff_palette',DS,0xC2D)}
FILES=((63,'_mainl_stf1',0xC37),(64,'_mainl_stf11',0xC40),(65,'_mainl_stf3',0xC4A),
       (66,'_mainl_stf4',0xC53),(67,'_mainl_stf5',0xC5C),(68,'_mainl_stf6',0xC65),
       (69,'_mainl_stf7',0xC6E),(70,'_mainl_stf8',0xC77),(71,'_mainl_stf9',0xC80),
       (72,'_mainl_stf10',0xC89),(73,'_mainl_stf2',0xC93),(74,'_mainl_stf12',0xC9C))
BINDINGS.update({index:(name,DS,offset) for index,name,offset in FILES})
MAP_NAMES={20:'frame_delay(int)',58:'input_mode_interface()'}
NEAR_CALLS=((0x3023,0x2576),(0x3067,0x2561),(0x306A,0x26E5),(0x3077,0x26B5),
 (0x30A5,0x29C2),(0x30C1,0x29C2),(0x30D8,0x2C0D),(0x30F4,0x2AA7),
 (0x3110,0x29C2),(0x311B,0x29C2),(0x3126,0x29C2),(0x3131,0x29C2),(0x313C,0x29C2),
 (0x3145,0x2561),(0x3150,0x298E),(0x315B,0x298E),(0x315E,0x26E5),(0x316B,0x26B5),
 (0x317C,0x2C98),(0x3186,0x2C98),(0x3196,0x2561),(0x3199,0x26E5))
FIELDS=((3062, 207, 86, None, 9, 0),
 (3039, 207, 86, None, 9, 0),
 (3016, 207, 86, None, 7, 0),
 (3005, 207, 86, None, 9, 0),
 (2985, 207, 86, None, 9, 0),
 (2965, 207, 86, None, 7, 0),
 (2954, 207, 86, None, 10, 0),
 (2949, 207, 86, None, 12, 0),
 (2946, 199, 22, 2, 62, 0),
 (2940, 207, 86, None, 10, 0),
 (2935, 199, 22, 2, 11, 0),
 (2926, 207, 86, None, 44, 0),
 (2923, 199, 22, 2, 61, 0),
 (2915, 199, 22, 2, 56, 0),
 (2908, 199, 22, 2, 56, 0),
 (2903, 199, 22, 2, 56, 0),
 (2896, 199, 22, 2, 30, 8),
 (2892, 199, 22, 2, 56, 0),
 (2887, 199, 22, 2, 56, 0),
 (2881, 199, 22, 2, 30, 7),
 (2877, 199, 22, 2, 56, 0),
 (2872, 199, 22, 2, 56, 0),
 (2861, 199, 22, 2, 30, 6),
 (2858, 199, 22, 2, 56, 0),
 (2853, 199, 22, 2, 56, 0),
 (2842, 199, 22, 2, 30, 6),
 (2825, 199, 22, 2, 30, 7),
 (2822, 199, 22, 2, 56, 0),
 (2815, 199, 22, 2, 55, 0),
 (2808, 198, 22, 2, 54, 0),
 (2793, 198, 22, 2, 30, 0),
 (2784, 198, 22, 2, 16, 0),
 (2774, 198, 22, 2, 30, 0),
 (2764, 198, 22, 2, 16, 0),
 (2754, 198, 22, 2, 38, 0),
 (2748, 206, 86, None, 42, 0),
 (2739, 206, 86, None, 43, 0),
 (2731, 206, 86, None, 13, 0),
 (2724, 206, 86, None, 42, 0),
 (3681, 206, 86, None, 17, 0),
 (3669, 198, 22, 2, 37, 0),
 (3660, 206, 86, None, 42, 0),
 (3650, 198, 22, 2, 37, 0),
 (3643, 198, 22, 2, 57, 0),
 (3629, 198, 22, 2, 37, 0),
 (3623, 206, 86, None, 10, 0),
 (3620, 198, 22, 2, 11, 0),
 (3612, 198, 22, 2, 37, 0),
 (3600, 206, 86, None, 58, 0),
 (3593, 198, 22, 2, 37, 0),
 (3585, 198, 22, 2, 28, 0),
 (3572, 197, 22, 2, 28, 0),
 (3553, 197, 22, 2, 37, 0),
 (3519, 197, 22, 2, 37, 0),
 (3458, 197, 22, 2, 49, 0),
 (3452, 197, 22, 2, 48, 0),
 (3447, 197, 22, 2, 50, 0),
 (3430, 197, 22, 2, 49, 0),
 (3424, 197, 22, 2, 48, 0),
 (3419, 197, 22, 2, 50, 0),
 (3402, 197, 22, 2, 48, 0),
 (3396, 197, 22, 2, 49, 0),
 (3380, 197, 22, 2, 45, 0),
 (3374, 197, 22, 2, 47, 0),
 (3368, 197, 22, 2, 46, 0),
 (3355, 197, 22, 2, 50, 0),
 (3349, 197, 22, 2, 47, 0),
 (3343, 197, 22, 2, 46, 0),
 (3337, 197, 22, 2, 48, 0),
 (3331, 197, 22, 2, 49, 0),
 (3326, 197, 22, 2, 32, 0),
 (3309, 196, 22, 2, 37, 0),
 (3297, 196, 22, 2, 3, 0),
 (3291, 204, 86, None, 20, 0),
 (3285, 196, 22, 2, 33, 0),
 (3280, 196, 22, 2, 45, 0),
 (3274, 204, 86, None, 42, 0),
 (3267, 204, 86, None, 10, 0),
 (3262, 196, 22, 2, 11, 0),
 (3257, 196, 22, 2, 28, 0),
 (3253, 196, 22, 2, 2, 0),
 (3244, 196, 22, 2, 16, 0),
 (3238, 196, 22, 2, 37, 0),
 (3229, 204, 86, None, 60, 0),
 (3224, 196, 22, 2, 74, 0),
 (3216, 204, 86, None, 60, 0),
 (3211, 196, 22, 2, 73, 0),
 (3203, 204, 86, None, 60, 0),
 (3198, 196, 22, 2, 72, 0),
 (3190, 204, 86, None, 60, 0),
 (3185, 196, 22, 2, 71, 0),
 (3177, 204, 86, None, 60, 0),
 (3172, 196, 22, 2, 70, 0),
 (3164, 204, 86, None, 60, 0),
 (3159, 196, 22, 2, 69, 0),
 (3151, 204, 86, None, 60, 0),
 (3146, 196, 22, 2, 68, 0),
 (3138, 204, 86, None, 60, 0),
 (3133, 196, 22, 2, 67, 0),
 (3125, 204, 86, None, 59, 0),
 (3120, 196, 22, 2, 66, 0),
 (3112, 204, 86, None, 59, 0),
 (3107, 196, 22, 2, 65, 0),
 (3099, 204, 86, None, 60, 0),
 (3094, 196, 22, 2, 64, 0),
 (3086, 204, 86, None, 60, 0),
 (3081, 196, 22, 2, 63, 0),
 (3067, 204, 86, None, 8, 0))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff roll layout: '+str(message))


def native_image(raw):
    code,_=code_bytes(raw,1)
    image=bytearray(code[NATIVE:NATIVE+SIZE])
    fields=[]
    report=[]
    names=[]
    block=None
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at]
                names.append(rec.data[at+1:at+n+1].decode())
                at+=n+2
        if rec.name=='LEDATA':
            block=rec.data[0],int.from_bytes(rec.data[1:3],'little')
        if rec.name!='FIXUPP' or block[0]!=1:
            continue
        at=0
        while at<len(rec.data):
            loc,low,method=rec.data[at:at+3]
            at+=3
            frame=rec.data[at] if method in (0x14,0x16) else None
            at+=int(frame is not None)
            index=rec.data[at]
            at+=1
            site=block[1]+(loc&3)*256+low
            if not NATIVE<=site<NATIVE+SIZE:
                continue
            width=4 if loc&0xFC==0xCC else 2
            need(site+width<=NATIVE+SIZE,'entire native field')
            addend=int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            name,segment,offset=BINDINGS[index]
            need(names[index-1]==name,'literal EXTDEF identity')
            if width==4:
                need((loc&0xFC,method,frame,addend)==(0xCC,0x56,None,0),'literal zero-addend far CODE field')
                value=offset|(segment<<16)
            else:
                need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'external DGROUP displacement WORD')
                need(addend==0 or index==30 and addend in (6,7,8),'only declared score-member addends')
                value=offset+addend
            image[site-NATIVE:site-NATIVE+width]=value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native roll fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields=native_image((work/OBJECT).read_bytes())
    start=CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'entire independently linked native roll')
    ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in ins)==SIZE and (ins[-1].mnemonic,ins[-1].op_str)==('ret',''),'entire near/noargs procedure')
    need(tuple((i.address,int(i.op_str,16)) for i in ins if i.mnemonic=='call')==NEAR_CALLS,'all22 internal near calls')
    far=[(i.address,tuple(int(v.strip(),16) for v in i.op_str.split(','))) for i in ins if i.mnemonic=='lcall']
    expected_far=[(0x2382+f['offset']-1,BINDINGS[f['target']][1:]) for f in fields if f['width']==4]
    need(sorted(far)==sorted(expected_far),'all34 native far calls')
    text=(work/'obj/th03/mainl.map').read_text()
    for index,(name,segment,offset) in BINDINGS.items():
        symbol=MAP_NAMES.get(index,name)
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,'both external MAP tables: '+symbol)
    need(len(re.findall(r'(?m)^\s*095F:2E1D\s+_mainl_staff_roll\s*$',text))==2,'both native owner publics')
    relocations=[(CS,0x2382+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==relocations,'complete literal ordered MZ vector')
    digest=hashlib.sha256(image).hexdigest()
    owner=dict(unit_id='th03-mainl-decoded-staff-staff',name='_mainl_staff_roll',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in relocations],
        argument_bytes=0,callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
        abi='near noargs; saved BP/SI/DI; far Pascal helpers and explicit cdecl load/volume cleanup')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=34,
        internal_near_calls=[dict(offset=at,callee=dest) for at,dest in NEAR_CALLS],
        far_calls=[dict(offset=at,segment=s,callee=ip) for at,(s,ip) in far],
        enclosing_DATA_or_other_CODE_newly_accepted=False,whole_product_accepted=False)
