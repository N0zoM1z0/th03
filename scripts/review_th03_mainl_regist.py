#!/usr/bin/env python3
"""Complete MAINL registration/score-data candidate review, explicit interfaces."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, CS, DS, REVISION, sha

ROOT = Path(__file__).resolve().parents[1]
PROOF_SHA256 = "5a8afb0c78b4c2303258d8e0c8c152ccc5a62c1945807c89b227263cdc909ac4"
HI, HI_SIZE = 0x21ee, 206
RANGES = [("decode",0x17b9,60,""),("recreate",0x17f5,127,""),("sum_invalid",0x1874,42,""),
          ("load",0x189e,98,"2"),("encode",0x1900,188,"2"),("load_initial",0x19bc,145,""),
          ("insert",0x1a4d,330,""),("alphabet",0x1b97,56,""),("alphabet_putca",0x1bcf,55,"4"),
          ("unput",0x1c06,183,"4"),("regi_put",0x1cbd,66,"8"),("row_at",0x1cff,314,"6"),
          ("rows",0x1e39,39,""),("row",0x1e60,27,"2"),("name",0x1e7b,739,""),
          ("default_name",0x215e,132,""),("menu",0x21e2,348,"")]
# segment, offset -> name, argument bytes, callee cleanup bytes.
IMPORTS = {(0,0x896):("exist",4,4),(0,0x856):("create",4,4),(0,0x846):("close",0,0),
           (0,0x966):("open",4,4),(0,0x9a2):("seek",6,6),(0,0x8b2):("read",6,6),
           (0,0x786):("append",4,4),(0,0x9f2):("write",6,6),(0,0x1a3e):("irand",0,0),
           (0,0x17d0):("palette_show",0,0),(0,0xfec):("pi_free",8,8),
           (0,0x24e2):("bfnt",4,4),(0,0xeac):("copy_page",2,2),(0,0x25bc):("super_put",6,6),
           (0,0x306c):("scopy",8,8),(0,0x536):("fade_in",2,2),(0,0x57a):("fade_out",2,2),
           (0,0x237e):("super_free",0,0),(0xc7e,0xdc2):("input",0,0),
           (0xc7e,0x372):("frame",2,2),(0xc7e,0x9b7):("font",10,10),
           (0xc7e,0xa0):("music_load",6,0),(0xc7e,0x6e2):("music_interrupt",2,2),
           (0xc7e,0xee5):("wait",2,2),(0xc7e,0xccb):("pi_load",6,6),
           (0xc7e,0x529):("pi_palette",2,2),(0xc7e,0x52a):("pi_palette",2,2),
           (0xc7e,0x54e):("pi_put",6,6),(0xc7e,0x54f):("pi_put",6,6),
           (0xc7e,0x73e):("cdg_single",8,8),(0xc7e,0x1f4):("cdg_put",6,6),
           (0xc7e,0x950):("cdg_free",2,2),(0xc7e,0x84e):("cdg_all",6,6),
           (0xc7e,0x84):("volume_wait",2,0)}
PROVIDERS = ["th03/regist.cpp","th03/hiscore/regist.cpp","th03/hiscore/regist.hpp",
             "th03/scoredat.cpp","th03/formats/scoredat.cpp","th03/formats/scoredat.hpp",
             "th03/formats/score_ld.cpp","th03/formats/score_es.cpp","th03/formats/scorecry.hpp",
             "th03/sprites/regi.h","th03/score.hpp","th02/score.h","th03/resident.hpp",
             "th03/playchar.hpp","th03/common.h","th03/shiftjis/regist.hpp","game/input.hpp",
             "th03/hardware/input.h","th01/hardware/grppsafx.h","th02/hardware/frmdelay.h",
             "th03/formats/cdg.h","th03/formats/pi.hpp","th03/snd/snd.h","libs/master.lib/func.hpp",
             "platform.h","th03_mainl.asm"]


def decode(image):
    cs = Cs(CS_ARCH_X86,CS_MODE_16)
    cs.detail = True
    entries, boundaries, rows = {s for _,s,_,_ in RANGES}, set(), []
    for name,start,size,cleanup in RANGES:
        body = image[CS*16+start:CS*16+start+size]
        instructions = list(cs.disasm(body,start))
        if sum(i.size for i in instructions)!=size or not instructions or instructions[-1].mnemonic!="ret" or instructions[-1].op_str!=cleanup:
            raise ValueError("registration complete body/near cleanup differs")
        boundaries.update(i.address for i in instructions)
        edges=[]
        for i in instructions:
            if i.mnemonic.startswith(("j","loop")) or i.mnemonic in ("call","lcall"):
                if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):
                    raise ValueError("unexpected indirect registration edge")
                dest=tuple(o.imm for o in i.operands) if i.mnemonic=="lcall" else (CS,i.operands[0].imm)
                edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,sha256=sha(body),instruction_count=len(instructions),cleanup=cleanup,edges=edges))
    for row in rows:
        for edge in row["edges"]:
            segment, offset = edge["destination"]
            if edge["kind"]=="lcall":
                if (segment,offset) not in IMPORTS:
                    raise ValueError("registration unknown foreign interface")
            elif edge["kind"]=="call":
                if segment!=CS or offset not in entries:
                    raise ValueError("registration near call enters unowned/interior code")
            elif offset not in boundaries or not row["offset"]<=offset<row["offset"]+row["size"]:
                raise ValueError("registration branch enters data/operand/another body")
    return rows


def rotate(byte):
    return (byte>>3)|((byte&7)<<5)


def encrypted(section):
    """Mathematical byte-feedback specification; keys stay plaintext."""
    data=bytearray(section)
    key1,key2=data[204:206]
    feedback=key2
    for i in range(203,-1,-1):
        data[i]=(data[i]-key1-feedback)&255
        feedback=rotate(data[i])^key2
    return bytes(data)


def checksum(section):
    data=bytearray(section)
    struct.pack_into("<H",data,0,sum(data[2:])&65535)
    return bytes(data)


def section():
    data=bytearray(HI_SIZE)
    for place in range(10):
        data[2+place*8:10+place*8]=bytes((place+i)%49 for i in range(8))
        data[84+place*10:94+place*10]=bytes([32]*10)
        digits=number_digits(1000-place*100)
        data[85+place*10:93+place*10]=bytes(d+32 for d in digits)
        data[84+place*10+9]=33+place  # constructed reserved digit, deliberately nonzero
        data[184+place]=place%9+1
        data[194+place]=33+place
    data[82:84]=bytes([18,71])
    data[204:206]=bytes([23,197])
    return checksum(data)


def number_digits(value):
    return [(value//(10**i))%10 for i in range(8)]


class RegistrationProbe(Probe):
    """Actual root functions; all foreign library/file/input/render calls modeled."""
    def __init__(self,mz,*,keys=(0,),random_words=(0x1234,0x00ff,0x80),file_exists=True,
                 read_bytes=None,io_result=1):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg
        self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset
            struct.pack_into("<H",image,at,(struct.unpack_from("<H",image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image))
        self.code,self.data,self.stack=(0x2000+CS)*16,(0x2000+DS)*16,0x40000
        for name,value in (("CS",0x2000+CS),("DS",0x2000+DS),("SS",0x4000),("ES",0x3333),
                           ("BP",0x7777),("SI",0x1357),("DI",0x2468),("EFLAGS",0x202)):
            self.set(name,value)
        self.events,self.ports,self.writes,self.errors,self.frames=[],[],[],[],[]
        self.stop=False
        self.key_index,self.random_index=0,0
        self.files=[]
        self.uc.mem_write(self.data+0x21ea,struct.pack("<HH",0,0x5000))
        self.uc.mem_write(0x50000,b"\0"*256)
        for i,segment in enumerate((0xa800,0xb000,0xb800,0xe000)):
            self.uc.mem_write(self.data+0x1c60+i*4,struct.pack("<HH",0,segment))
        self.set_hi(section())
        self.resident(packed=1,credits=3,stage=5,rank=0)
        self.word(0x22bc,0)
        models={(0x2000+s)*16+o:(s,name,count,cleanup) for (s,o),(name,count,cleanup) in IMPORTS.items()}

        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as error:
                    self.errors.append(str(error));self.uc.emu_stop()
            return invoke

        def code(uc,address,size,user):
            if address==self.code+0xff00:
                self.stop=True;uc.emu_stop();return
            if address in models:
                segment,name,count,cleanup=models[address]
                if self.get("CS")!=0x2000+segment:raise ValueError("registration import segment alias")
                sp=self.get("SP")
                words=list(struct.unpack("<"+"H"*((count+4)//2),uc.mem_read(self.stack+sp,count+4)))
                args=words[2:]
                event=dict(name=name,args=args)
                if name in ("exist","create","open","append","bfnt"):
                    event["filename_hex"]=self.cstring(*args[:2]).hex()
                if name=="exist":self.set("AX",int(file_exists))
                elif name=="irand":
                    value=random_words[self.random_index%len(random_words)]
                    self.random_index+=1;self.set("AX",value&65535);event["returned_word"]=value&65535
                elif name=="read":
                    if read_bytes is not None:
                        uc.mem_write(args[2]*16+args[1],read_bytes[:args[0]])
                    self.set("AX",io_result)
                    event["supplied_count"]=0 if read_bytes is None else min(len(read_bytes),args[0])
                elif name=="write":
                    data=bytes(uc.mem_read(args[2]*16+args[1],args[0]))
                    self.files.append(data);event["bytes_sha256"]=sha(data)
                    self.set("AX",io_result)
                elif name=="seek":
                    event["offset"]=args[1]+(args[2]<<16);self.set("AX",io_result)
                elif name=="scopy":
                    length=self.get("CX")
                    if length!=8:raise ValueError("registration struct-copy count differs")
                    uc.mem_write(args[3]*16+args[2],bytes(uc.mem_read(args[1]*16+args[0],length)))
                    event["length"]=length
                elif name=="input":
                    key=keys[min(self.key_index,len(keys)-1)]
                    self.word(0x1d0c,key);self.key_index+=1;event["key"]=key
                elif name=="frame":
                    bp=self.get("BP")
                    state=bytes(uc.mem_read(self.stack+bp-16,16))
                    self.frames.append(dict(regi=struct.unpack_from("<H",state,14)[0],cursor=state[2],done=state[5],
                                            holds=list(struct.unpack_from("<4H",state,6))))
                elif name=="cdg_single":event["filename_hex"]=self.cstring(args[1],args[2]).hex()
                elif name in ("music_load","pi_load","cdg_all"):
                    # Pascal arguments reverse declaration order; filename is first.
                    pointer=args[:2]
                    event["filename_hex"]=self.cstring(*pointer).hex();self.set("AX",io_result)
                elif name=="font":
                    event["text_hex"]=self.cstring(*args[:2]).hex()
                elif name in ("create","close","open","append"):
                    self.set("AX",io_result)
                self.events.append(event)
                self.set("SP",sp+4+cleanup);self.set("CS",words[1]);self.set("IP",words[0]);return
            offset=address-self.code
            if self.get("CS")!=0x2000+CS or not any(start<=offset<start+length for _,start,length,_ in RANGES):
                raise ValueError("CPU escaped registration reviewed bodies/interfaces")

        def write(uc,access,address,size,value,user):
            if self.data+HI<=address<self.data+0x2400:self.writes.append([address-self.data,size,value])

        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1:raise ValueError("unexpected registration port/width")
            self.ports.append([port,value])

        def interrupt(uc,number,user):raise ValueError("unexpected registration interrupt")

        def input_port(uc,port,width,user):
            self.errors.append("unexpected registration input port");uc.emu_stop();return 0

        self.uc.hook_add(UC_HOOK_CODE,guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write))
        self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN,input_port,None,1,0,reg.UC_X86_INS_IN)

    def cstring(self,offset,segment):
        result=bytearray()
        for i in range(256):
            byte=bytes(self.uc.mem_read(segment*16+((offset+i)&65535),1))[0]
            if not byte:return bytes(result)
            result.append(byte)
        raise ValueError("registration interface string exceeds bounded model")

    def hi(self):return bytes(self.uc.mem_read(self.data+HI,HI_SIZE))

    def set_hi(self,data):
        if len(data)!=HI_SIZE:raise ValueError("score section size differs")
        self.uc.mem_write(self.data+HI,bytes(data))

    def resident(self,*,packed=1,credits=3,stage=5,rank=0,digits=None):
        for offset,value in ((0xc,packed),(0x36,credits),(0x33,stage),(0xb,rank)):
            self.uc.mem_write(0x50000+offset,bytes([value&255]))
        if digits is not None:self.uc.mem_write(0x50018,bytes(digits))
        self.uc.mem_write(0x50010,struct.pack("<I",0x12345678))

    def run(self,entry,args=(),budget=2000000,*,terminal=True):
        self.stop=False;self.errors.clear()
        self.set("SP",0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack("<"+"H"*(1+len(args)),0xff00,*args))
        self.uc.emu_start(self.code+entry,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError("registration terminal/budget observation differs")
        if self.stop and (self.get("SP")!=0xffd2+len(args)*2 or [self.get(r) for r in ("BP","SI","DI")]!=[0x7777,0x1357,0x2468]):
            raise ValueError("registration near cleanup/callee-saved contract differs")


def insert_expected(before,digits,credits,stage,packed):
    data=bytearray(before)
    place=next((p for p in range(10) if tuple(d+32 for d in reversed(digits))>
                tuple(reversed(data[85+p*10:93+p*10]))),-1)
    if place<0:return place,bytes(data)
    for p in range(8,place-1,-1):
        data[2+(p+1)*8:10+(p+1)*8]=data[2+p*8:10+p*8]
        data[84+(p+1)*10:94+(p+1)*10]=data[84+p*10:94+p*10]
        data[184+p+1],data[194+p+1]=data[184+p],data[194+p]
    data[2+place*8:10+place*8]=bytes([14]*8)
    data[85+place*10:93+place*10]=bytes((d+32)&255 for d in digits)
    data[84+place*10]=(35-credits)&255
    data[194+place]=48 if stage==99 else (32+stage)&255
    char=int((packed-1)/2)
    data[184+place]=(char+1)&255
    return place,bytes(data)


def matrix(mz):
    sorts=[]
    for value in [1001-p*100 for p in range(10)]+[1000-p*100 for p in range(10)]+[0]:
        for credits in (0,3):
            p=RegistrationProbe(mz);digits=number_digits(value)
            p.resident(digits=digits,credits=credits,stage=99 if value==1001 else 5)
            before=p.hi();expected,after=insert_expected(before,digits,credits,99 if value==1001 else 5,1)
            p.run(0x1a4d)
            if p.get("AX")!=(expected&65535) or p.hi()!=after:raise ValueError("score lexicographic insertion/shift/layout differs")
            sorts.append(dict(value=value,credits=credits,place=expected,after_sha256=sha(after)))
    p=RegistrationProbe(mz);digits=[255]*8;p.resident(digits=digits,credits=200,stage=255,packed=0)
    expected,after=insert_expected(p.hi(),digits,200,255,0);p.run(0x1a4d)
    if p.get("AX")!=expected or p.hi()!=after:raise ValueError("insertion wide compare/byte stores differ")
    sorts.append(dict(constructed_invalid_digits=digits,place=expected,after_sha256=sha(after)))
    names=[]
    for packed in (0,1,2,3,18,19,255):
        for content in (bytes([14]*8),bytes([3]*8),bytes(range(8))):
            p=RegistrationProbe(mz);p.resident(packed=packed)
            data=bytearray(p.hi());data[2:10]=content;p.set_hi(data)
            char=int((packed-1)/2)
            expected=bytes(p.uc.mem_read(p.data+0x92e+char*8,8))[::-1] if len(set(content))==1 else content
            p.run(0x215e)
            if p.hi()[2:10]!=expected:raise ValueError("default-name backwards/all-identical condition differs")
            names.append(dict(packed=packed,initial=list(content),final=list(expected),default_index=char))
    presses=(0x2000,0)*7+(0x2000,)
    sequences=[("eight-A",presses,0),("held-enter",(0x2000,)*40+(0,)+(0x2000,0)*6+(0x2000,),0),
               ("held-right",(8,)*40+(0,)+presses,3),
               ("backspace-bomb",(0x2000,0,0x10,0)+presses,0),
               ("END",(4,0,2,0,2,0,0x2000),None)]
    entries=[]
    for name,keys,letter in sequences:
        p=RegistrationProbe(mz,keys=keys);data=bytearray(p.hi());data[2:10]=bytes([14]*8);p.set_hi(data)
        before=p.hi();p.run(0x1e7b)
        if p.key_index!=len(keys) or len(p.frames)!=len(keys):raise ValueError("name menu input lock/repeat/termination differs")
        outside=[w for w in p.writes if not HI<=w[0]<HI+HI_SIZE and w[0]!=0x22bc]
        if letter is not None:
            if p.hi()[2:10]!=bytes([letter]*8) or not any(w==[0x22ef,1,14] for w in outside) or p.frames[-1]["cursor"]!=255:
                raise ValueError("eighth character cursor underflow/out-of-section write differs")
        elif p.hi()[2:10]!=bytes([14]*8) or p.frames[-1]["cursor"]!=7 or outside:
            raise ValueError("END selection/name preservation differs")
        if name=="held-right" and [p.frames[i]["regi"] for i in (0,31,32,35,36,39)]!=[1,1,2,2,3,3]:
            raise ValueError("direction first/repeat32/36 thresholds differ")
        entries.append(dict(name=name,input_calls=p.key_index,final_name=list(p.hi()[2:10]),frames=p.frames,
                            outside_score_writes=outside,ports_count=len(p.ports),render_requests=len([e for e in p.events if e['name']=='super_put'])))
    p=RegistrationProbe(mz,keys=(0x2000,));p.run(0x1e7b,budget=100000,terminal=False)
    nonterminal=dict(held_enter=True,input_calls=p.key_index,terminal=False,final_name=list(p.hi()[2:10]))
    p=RegistrationProbe(mz);p.resident(rank=2)
    p.run(0x19bc);p.run(0x19bc)
    filenames=[bytes.fromhex(e['filename_hex']).decode('ascii') for e in p.events if e['name']=='cdg_single']
    if filenames!=['rft2.cdg','rft4.cdg']:raise ValueError('initial loader rank filename accumulates differently')
    loader=dict(calls=2,rank=2,rank_images=filenames)
    crypto=[]
    for random_words in ((0,0,0),(0x1234,0xabcd,0xff),(0xffff,0xfffe,0x1200),(0x18,0xfe,0x80)):
        for rank in (0,3,0xffff,319):
            p=RegistrationProbe(mz,random_words=random_words,io_result=0);p.resident(stage=99,credits=3)
            plain=bytearray(p.hi());plain[204],plain[205],plain[83]=(v&255 for v in random_words);plain[82]=99
            plain=checksum(plain);expected=encrypted(plain);p.run(0x1900,(rank,))
            if p.hi()!=expected or p.files!=[expected] or next(e for e in p.events if e['name']=='seek')['offset']!=rank*206&65535:
                raise ValueError("encryption/checksum/seek/ignored-write contract differs")
            p.run(0x17b9)
            if p.hi()!=plain:raise ValueError("actual decode roundtrip differs")
            p.run(0x1874)
            if p.get("AX")&255:raise ValueError("decoded checksum unexpectedly invalid")
            bad=bytearray(plain);bad[0]^=1;p.set_hi(bad);p.run(0x1874)
            if p.get("AX")&255!=1:raise ValueError("checksum mutation not detected")
            crypto.append(dict(random_words=random_words,rank_word=rank,seek=rank*206&65535,encoded_sha256=sha(expected),plain_sha256=sha(plain)))
    loads=[]
    for exists,corrupt,stale in ((False,False,False),(True,False,False),(True,True,False),(True,False,True)):
        plain=section();encoded=bytearray(encrypted(plain))
        if corrupt:encoded[0]^=1
        p=RegistrationProbe(mz,file_exists=exists,read_bytes=None if stale else bytes(encoded),io_result=0)
        p.resident(stage=99,credits=3);p.set_hi(bytes(encoded) if stale else bytes([0xa5]*206));p.run(0x189e,(2,))
        recreated=not exists or corrupt
        if len(p.files)!=(4 if recreated else 0) or (not recreated and p.hi()!=plain):raise ValueError("load/recreate/stale-data contract differs")
        if recreated:
            saved_clear=[]
            for data in p.files:
                q=RegistrationProbe(mz);q.set_hi(data);q.run(0x17b9);saved_clear.append(q.hi()[82])
            if saved_clear!=[99]*4:raise ValueError("recreation all-rank unlock contract differs")
        else:saved_clear=[]
        loads.append(dict(exists=exists,corrupt=corrupt,stale_preexisting=stale,events=p.events,
                          saved_files=[sha(d) for d in p.files],saved_clear_flags=saved_clear,final_hi_sha256=sha(p.hi())))
    menus=[]
    for stage,credits in ((255,3),(255,0),(99,3),(5,3)):
        p=RegistrationProbe(mz,keys=presses,read_bytes=encrypted(section()))
        p.resident(stage=stage,credits=credits,digits=number_digits(1001),rank=2)
        p.run(0x21e2)
        sound=[e['args'][0] for e in p.events if e['name']=='music_interrupt']
        expected_sound=[0]+([0x210] if not credits or stage==99 else [])+([0x100] if not credits or stage==99 else [])
        if sound!=expected_sound or len(p.files)!=1 or p.word(0x22bc)!=(0xffff if stage==255 else 0) or bytes(p.uc.mem_read(p.data+0x5b6,4))!=struct.pack('<I',0x12345678):
            raise ValueError("full menu view/insert/fade/save/RNG-seed contract differs")
        if (stage==255 and any(e['name']=='input' for e in p.events)) or (stage!=255 and len(p.frames)!=15):
            raise ValueError("menu name-entry/view path differs")
        pictures=[bytes.fromhex(e['filename_hex']).decode('ascii') for e in p.events if e['name']=='pi_load']
        sprites=[bytes.fromhex(e['filename_hex']).decode('ascii') for e in p.events if e['name']=='cdg_all']
        expected_final='conti.pi' if credits and stage!=99 else 'over.pi'
        if pictures!=['regib.pi',expected_final] or sprites!=(['conti.cd2'] if credits and stage!=99 else []):
            raise ValueError('menu picture/continue sprite filename/ABI differs')
        menus.append(dict(stage=stage,credits=credits,entered_place=p.word(0x22bc),sound_requests=sound,
                          input_calls=p.key_index,events=p.events,ports=p.ports,final_hi_sha256=sha(p.hi()),
                          outside_score_writes=[w for w in p.writes if not HI<=w[0]<HI+HI_SIZE and w[0]!=0x22bc]))
    return dict(insertion_cases=sorts,default_name_cases=names,name_menu_cases=entries,name_nonterminal=nonterminal,
                crypto_cases=crypto,load_cases=loads,menu_cases=menus,initial_loader=loader,
                top_level_calls_per_image=152,terminal_calls_per_image=151,budget_cases_per_image=1,
                scope='Actual complete root/dependency functions; foreign files/RNG/struct-copy/input/render/timing/sound modeled, flat planes/page logs only')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/'.analysis/sol-mainl-cutscene-review-20261006.json').read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('registration requires pinned decoded lineage proof')
    proof=json.loads(raw)
    inputs={**proof['inputs'],'.analysis/sol-mainl-cutscene-review-20261006.json':sha(raw)}
    inputs['scripts/review_th03_mainl_regist.py']=sha(Path(__file__).read_bytes())
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError(f'registration input changed: {p}')
    verify()
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl')
    stored=read_verified_artifact(ROOT,artifact)
    if sha(stored)!=proof['stored_sha256']:raise ValueError('canonical MAINL differs from decoded lineage')
    paths=[p for p in inputs if p.endswith('mainl.exe')];target=parse_mz((ROOT/paths[0]).read_bytes())
    if len(paths)!=3 or not target.valid:raise ValueError('registration target/two candidate images absent')
    analysis,runtime=decode(target.program_image),matrix(target)
    rounds=[]
    for path in paths[1:]:
        candidate=parse_mz((ROOT/path).read_bytes());tree=Path(path).parents[2]
        if not candidate.valid:raise ValueError('invalid cached registration MZ')
        for source,original in providers.items():
            cache_path=str(tree/source);cached=(ROOT/cache_path).read_bytes()
            if cached!=(original.replace(b'\n',b'\r\n') if source.endswith('.asm') else original):
                raise ValueError(f'registration source association differs: {source}')
            inputs[cache_path]=sha(cached)
        map_path=next(p for p in inputs if str(tree) in p and p.endswith('mainl.map'))
        rows=[r for r in code_rows((ROOT/map_path).read_text(encoding='ascii'),len(candidate.program_image)) if r['module'] in ('th03/regist.cpp','th03/scoredat.cpp') and r['size']]
        if sorted((r['module'],r['segment'],r['offset'],r['size']) for r in rows)!=[('th03/regist.cpp',CS,0x189e,2720),('th03/scoredat.cpp',CS,0x17b9,229)]:
            raise ValueError('complete registration/scoredat CODE contributions differ')
        extents=[extent_observation(target,candidate,r) for r in rows]
        differences=[at for at in range(0x17b9,0x233e) if target.program_image[CS*16+at]!=candidate.program_image[CS*16+at]]
        if differences!=[0x19e2,0x19ec,0x22d8,0x22e2,0x230f,0x2319] or not all(e['ordered_relocations_equal'] for e in extents):
            raise ValueError('registration raw/ordered-relocation diagnostic differs')
        objects=[]
        for module in ('regist','scoredat'):
            obj_path=str(tree/f'obj/th03/{module}.obj');obj=describe_omf((ROOT/obj_path).read_bytes());inputs[obj_path]=sha((ROOT/obj_path).read_bytes())
            if not obj['valid'] or obj['module_name']!=f'th03/{module}.cpp' or obj['translator_comments']!=['TC86 Borland C++ 4.02']:
                raise ValueError('registration cached OMF association differs')
            objects.append(obj)
        observed=matrix(candidate)
        if observed!=runtime:raise ValueError('registration target/candidate CPU/model observations differ')
        rounds.append(dict(path=path,analysis=decode(candidate.program_image),runtime=observed,extents=extents,differences=differences,objects=objects))
    if any(rounds[0]['objects'][i]['dependency_timestamp_normalized_sha256']!=rounds[1]['objects'][i]['dependency_timestamp_normalized_sha256'] for i in range(2)):
        raise ValueError('cached registration OMF differs beyond dependency timestamps')
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('canonical MAINL changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('frozen registration provider changed')
    result=dict(kind='th03-mainl-complete-registration-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),
                inputs=inputs,providers={p:sha(d) for p,d in providers.items()},analysis=analysis,runtime=runtime,rounds=rounds,
                root_bytes=2720,scoredat_dependency_bytes=229,tools=dict(capstone_distribution=version('capstone'),unicorn_distribution=version('unicorn')),
                diagnostic_checks_pass=True,root_raw_equal=False,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS whole registration2720/scoredat229 candidate analysis and CPU/interface cases: {args.output}')


if __name__=='__main__':main()
