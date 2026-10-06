#!/usr/bin/env python3
"""Complete MAINL root candidate CODE review with explicit foreign models."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import CS, DS, Probe, REVISION, sha
from review_th03_mainl_snow import u16

ROOT = Path(__file__).resolve().parents[1]
PROOF = '.analysis/sol-mainl-transitions-review-20261006.json'
PROOF_SHA256 = '16ab427299695eb78f08a999a044fa351068154e1c0e70dd99de8eacc3d884fd'
# Name, offset, size, return kind, Pascal cleanup.
RANGES = [('free_all',0x186,23,'ret',''),('win_animation',0x19d,250,'ret',''),
          ('story_dispatch',0x297,133,'ret',''),('next_load',0x31c,288,'ret',''),
          ('next_put',0x43c,627,'ret',''),('shot_pair',0x6c1,111,'ret','6'),
          ('shot_load',0x730,93,'ret','2'),('main',0x78d,528,'retf',''),
          ('continue_menu',0x99d,417,'ret','')]
TABLE, TABLE_WORDS = 0x6af, [0x5a7,0x5a7,0x5af,0x5b7,0x5af,0x5b7,0x5a7,0x5bf,0x5c7]
# Segment/offset -> model name, argument bytes, callee cleanup.
FAR = {(0,0xe72):('clear',0,0),(0,0x1758):('show',0,0),
       (0,0x17d0):('palette',0,0),(0,0x1a68):('rgb',4,4),
       (0,0x536):('black_in',2,2),(0,0x57a):('black_out',2,2),
       (0,0x208a):('white_in',2,2),(0,0x20ca):('white_out',2,2),
       (0,0xeac):('copy_page',2,2),(0,0xfec):('pi_free',8,8),
       (0,0x1f32):('text_fill',4,4),(0,0x2820):('respal_set',0,0),
       (0,0x276e):('respal_exist',0,0),(0,0xc72):('gaiji_backup',0,0),
       (0,0xcb2):('gaiji_load',4,4),(0,0xc96):('gaiji_restore',0,0),
       (0,0x1f20):('text_clear',0,0),(0,0x8e37):('exec',12,0),
       (0,0xc36):('grcg_color',4,4),(0,0xace):('grcg_box',8,8),
       (0,0xc60):('grcg_off',0,0),
       (0xc7e,0x1b0):('exit',0,0),(0xc7e,0x98f):('exit_to_main',0,0),
       (0xc7e,0x700):('init',4,4),(0xc7e,0x2c):('sound_mode',0,0),
       (0xc7e,0x65e):('se_reset',0,0),(0xc7e,0xfa4):('hflip',0,0),
       (0xc7e,0xf32):('cdg_put',6,6),(0xc7e,0x1f4):('cdg_alpha',6,6),
       (0xc7e,0x2a8):('cdg_hflip',6,6),(0xc7e,0x73e):('cdg_load',8,8),
       (0xc7e,0x950):('cdg_free',2,2),(0xc7e,0x372):('delay',2,2),
       (0xc7e,0xc1c):('measure_delay',4,4),(0xc7e,0xdc2):('input',0,0),
       (0xc7e,0x6e2):('music',2,2),(0xc7e,0xa0):('music_load',6,0),
       (0xc7e,0xccb):('pi_load',6,6),(0xc7e,0x9b7):('font',10,10),
       (0xc7e,0x52a):('pi_palette',2,2),(0xc7e,0x529):('pi_palette',2,2),
       (0xc7e,0x54f):('pi_put',6,6),(0xc7e,0x54e):('pi_put',6,6),
       (0xc7e,0x5d7):('pi_interlace',6,6),(0xc7e,0x5d6):('pi_interlace',6,6)}
NEAR = {3:('cfg',0,0),0x34:('win_load',0,0),0x14e:('win_text',0,0),
        0xb3e:('script_load',4,4),0xb84:('script_free',0,0),
        0x167e:('animate',0,0),0x21e2:('regist',0,0),
        0x233e:('ending',0,0),0x2382:('staff',0,0)}
PROVIDERS = ['th03_mainl.asm','th03/formats/cdg_free_all.asm','th03/formats/cdg.inc',
             'th03/formats/cdg.h','th03/resident.hpp','th03/playchar.hpp','th03/score.hpp',
             'th03/hardware/input.h','th03/th03.inc','th03/snd/snd.h','th02/snd/snd.h',
             'libs/kaja/kaja.h','libs/master.lib/func.hpp','th03/formats/pi.hpp',
             'th03/common.inc','th03/hardware/input.inc','th03/chars.inc',
             'th02/score.inc','th02/v_colors.inc']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    entries={a for _,a,_,_,_ in RANGES};rows=[]
    for name,start,size,kind,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size]
        instructions=list(decoder.disasm(body,start));bounds={i.address for i in instructions}
        if sum(i.size for i in instructions)!=size or not instructions or (instructions[-1].mnemonic,instructions[-1].op_str)!=(kind,cleanup):
            raise ValueError('root complete body/return contract differs')
        edges=[]
        for i in instructions:
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=(kind,cleanup):raise ValueError('root interior return contract differs')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if i.address==0x5a2:
                if i.mnemonic!='jmp' or len(i.operands)!=1 or i.operands[0].type!=X86_OP_MEM or i.op_str!='word ptr cs:[bx + 0x6af]':raise ValueError('root switch expression differs')
                edges.append(dict(instruction=i.address,kind='switch',table=TABLE));continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('unexpected root indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic=='lcall':
                if dest not in FAR:raise ValueError('root unknown far interface')
            elif i.mnemonic=='call':
                if dest[1] not in entries|set(NEAR):raise ValueError('root near call enters operand/unreviewed entry')
            elif dest[1] not in bounds:raise ValueError('root branch leaves body/enters operand')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,sha256=sha(body),instructions=len(instructions),return_kind=kind,cleanup=cleanup,edges=edges))
        if name=='next_put' and any(a not in bounds for a in TABLE_WORDS):raise ValueError('root switch destination enters operand')
    table=image[CS*16+TABLE:CS*16+TABLE+18]
    if list(struct.unpack('<9H',table))!=TABLE_WORDS:raise ValueError('root switch catalogue differs')
    coverage=sorted([(a,a+n) for _,a,n,_,_ in RANGES]+[(TABLE,TABLE+18)])
    if coverage[0][0]!=0x186 or coverage[-1][1]!=0xb3e or any(a[1]!=b[0] for a,b in zip(coverage,coverage[1:])):raise ValueError('root contribution partition differs')
    return dict(bodies=rows,table=dict(offset=TABLE,size=18,words=TABLE_WORDS,sha256=sha(table)),body_bytes=2470,contribution_bytes=2488)


class RootProbe(Probe):
    """Actual nine root bodies; external code, I/O, clock and exec are models."""
    def __init__(self,mz,*,keys=(0x20,),cfg=1,tick=97,exec_returns=True,io_result=0):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x295f0,0x2e3f0,0x40000
        for name,value in [('CS',0x295f),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202)]:self.set(name,value)
        self.events,self.ports,self.errors,self.entries=[],[],[],[];self.stop=False;self.exec_stop=False;self.inputs=0;self.polls=0;self.calls=0
        self.uc.mem_write(self.data+0x21ea,struct.pack('<HH',0,0x5000));self.uc.mem_write(0x50000,bytes(range(256)))
        self.uc.mem_write(0x50000+0x29,bytes([3]*10))  # Nine opponents plus a constructed out-of-array stage9 sentinel.
        self.resident();self.word(0x1d0c,0)
        models={(0x2000+s)*16+o:(s,o,name,count,clean,4) for (s,o),(name,count,clean) in FAR.items()}
        models.update({self.code+o:(CS,o,name,count,clean,2) for o,(name,count,clean) in NEAR.items()})
        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x295f:raise ValueError('root terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if self.get('CS')==0x295f and address-self.code in {a for _,a,_,_,_ in RANGES}:self.entries.append(address-self.code)
            if address==self.code+0x652 and tick is not None:
                self.polls+=1;self.word(0x144e,tick)
            if address in models:
                seg,off,name,count,clean,retbytes=models[address]
                if (self.get('CS'),address-self.get('CS')*16)!=(0x2000+seg,off):raise ValueError('root modeled interface segment alias')
                sp=self.get('SP');words=list(struct.unpack('<'+'H'*((count+retbytes)//2),uc.mem_read(self.stack+sp,count+retbytes)));args=words[retbytes//2:]
                event=dict(name=name,args=args)
                if name in ('rgb','music_load','pi_load','cdg_load','gaiji_load','init','script_load'):
                    index=1 if name=='cdg_load' else 0
                    event['filename_hex']=self.cstring(*args[index:index+2]).hex()
                if name=='font':event['text_hex']=self.cstring(*args[:2]).hex()
                if name=='input':
                    key=keys[min(self.inputs,len(keys)-1)];self.inputs+=1;self.word(0x1d0c,key);event['key']=key
                if name=='palette':event['tone']=self.word(0x578)
                if name=='cfg':self.set('AX',cfg)
                elif name=='exec':
                    event['path_hex']=self.cstring(*args[:2]).hex();event['argv0_hex']=self.cstring(*args[2:4]).hex()
                    if args[4:]!=[0,0]:raise ValueError('root execl null terminator differs')
                    self.set('AX',65535)
                    if not exec_returns:self.exec_stop=True;self.events.append(event);uc.emu_stop();return
                elif name in ('rgb','pi_load','cdg_load','gaiji_load','init','music_load'):self.set('AX',io_result)
                self.events.append(event);self.set('SP',sp+retbytes+clean);self.set('CS',words[1] if retbytes==4 else 0x295f);self.set('IP',words[0]);return
            off=address-self.code
            if self.get('CS')!=0x295f or not any(a<=off<a+n for _,a,n,_,_ in RANGES):raise ValueError('CPU escaped reviewed MAINL root bodies')
        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1:raise ValueError('unexpected root port/width')
            self.ports.append([port,value])
        def interrupt(uc,number,user):raise ValueError('unexpected root interrupt')
        def inp(uc,port,width,user):self.errors.append('unexpected root input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,inp,None,1,0,reg.UC_X86_INS_IN)

    def cstring(self,offset,segment):
        b=bytes(self.uc.mem_read(segment*16+offset,256))
        if b'\0' not in b:raise ValueError('root model string exceeds256')
        return b.split(b'\0',1)[0]

    def resident(self,*,mode=1,winner=0,stage=5,credits=3,p1=1,p2=3,menu=0,bgm=0):
        for at,value in [(0x28,mode),(0x17,winner),(0x33,stage),(0x36,credits),(0xc,p1),(0xd,p2),(0x35,menu),(0x15,bgm)]:self.uc.mem_write(0x50000+at,bytes([value]))

    def run(self,entry,args=(),*,terminal=True,exec_stop=False,budget=100000):
        self.stop=False;self.exec_stop=False;self.errors.clear();self.calls+=1
        far=entry==0x78d;frame=[0xff00,0x295f] if far else [0xff00]
        self.set('CS',0x295f);self.set('SP',0xffd0);self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(len(frame)+len(args)),*frame,*args))
        self.uc.emu_start(self.code+entry,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal or self.exec_stop!=exec_stop:raise ValueError('root terminal/exec/budget differs')
        cleanup={'shot_pair':6,'shot_load':2}.get(next(n for n,a,_,_,_ in RANGES if a==entry),0)
        if terminal and (self.get('SP')!=0xffd0+len(frame)*2+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('root return stack/callee-saved differs')

    def result(self):
        return dict(ax=self.get('AX'),resident_hex=bytes(self.uc.mem_read(0x50000,512)).hex(),events=self.events,ports=self.ports,inputs=self.inputs,polls=self.polls,entries=self.entries,calls=self.calls,
                    stage_filename_hex=self.cstring(self.word(0x114),0x2e3f).hex(),bgm_filename_hex=self.cstring(0x3a3,0x2e3f).hex(),script_filename_hex=self.cstring(self.word(0xc6),self.word(0xc8)).hex(),
                    playchar_hex=bytes(self.uc.mem_read(self.data+0x13f3,3)).hex(),credit_text_hex=self.cstring(0x8d8,0x2e3f).hex())


def matrix(mz):
    cases=[]
    def record(scope,p,params):cases.append(dict(scope=scope,params=params,result=p.result()))
    p=RootProbe(mz);p.run(0x186)
    if [e['args'] for e in p.events]!=[[i] for i in range(32)]:raise ValueError('free-all slot order differs')
    record('free_all',p,{})
    # Resident array deliberately has nonzero markers beyond its nine elements.
    for mode in (0,1,0x80,0x7f):
        for winner in (0,1):
            for stage in (0,5,6,7,8,9,10,255):
                for opponent in (0,1,14,15,18,255):
                    p=RootProbe(mz);p.resident(mode=mode,winner=winner,stage=stage)
                    address=0x50000+0x29+stage;p.uc.mem_write(address,bytes([opponent]));initial=bytes(p.uc.mem_read(0x50000,512))
                    p.run(0x297);expected=bytearray(initial)
                    answer=1
                    if initial[0x28]==1 and initial[0x17]==0:
                        value=initial[0x29+initial[0x33]];expected[0xd]=value
                        answer={7:3,8:4,9:5}.get(initial[0x33],0)
                        if not answer and int((value-1)/2)>=7:expected[0xd]=1
                    if p.get('AX')!=answer or bytes(p.uc.mem_read(0x50000,512))!=bytes(expected):raise ValueError('story dispatch scalar/far-array state differs')
                    record('dispatch',p,dict(mode=mode,winner=winner,stage=stage,opponent=opponent))
    for packed in (0,1,2,19,20,21,255):
        for pid in (0,1):
            p=RootProbe(mz);p.resident(p1=packed,p2=packed);original=bytes(p.uc.mem_read(p.data+0x116,12));p.run(0x730,(pid,))
            value=packed-1;filename=bytearray(original)
            if value>=10:filename[0]=(filename[0]+value//10)&255;value%=10
            filename[1]=(filename[1]+value)&255;first=bytes(filename).split(b'\0')[0];filename[2:4]=b'ex';second=bytes(filename).split(b'\0')[0]
            loads=[e for e in p.events if e['name']=='pi_load'];puts=[e['args'] for e in p.events if e['name']=='pi_interlace']
            if [bytes.fromhex(e['filename_hex']) for e in loads]!=[first,second] or puts!=[[0,200,pid*320],[0,208,pid*320]]:raise ValueError('shot mutable local filename/coordinates differ')
            if bytes(p.uc.mem_read(p.data+0x116,12))!=original:raise ValueError('shot source template unexpectedly modified')
            record('shot',p,dict(packed=packed,pid=pid))
    for mode,stage,p2 in [(1,5,3),(1,6,3),(1,5,15),(1,5,17),(0x80,5,3)]:
        p=RootProbe(mz);p.resident(mode=mode,stage=stage,p2=p2);p.uc.mem_write(p.data+0x13f3,b'\0');p.run(0x31c)
        loads=[e for e in p.events if e['name']=='cdg_load'];pis=[e for e in p.events if e['name']=='pi_load']
        adjustment=4 if mode!=1 else 2 if (p2-1)//2==7 else 1 if (p2-1)//2==8 else 3 if stage==6 else 0
        expected=('stnx'+str(1+adjustment)+'.pi').encode()
        if bytes.fromhex(pis[1]['filename_hex'])!=expected or len(loads)!=(2 if adjustment else 3):raise ValueError('next-load filename/stage request differs')
        record('next_load',p,dict(mode=mode,stage=stage,p2=p2))
    # Reusing a root context exposes the mutable global filename accumulation.
    p=RootProbe(mz);p.resident(mode=0x80);p.uc.mem_write(p.data+0x13f3,b'\0');p.run(0x31c);p.run(0x31c)
    if [bytes.fromhex(e['filename_hex']) for e in p.events if e['name']=='pi_load']!=[b'stnx0.pi',b'stnx5.pi',b'stnx0.pi',b'stnx9.pi']:raise ValueError('next-load cumulative filename differs')
    record('next_load_twice',p,{})
    for stage in (5,6):
        for packed in (1,3,15,17,21,255):
            p=RootProbe(mz,tick=97);p.resident(stage=stage,p2=packed);p.run(0x43c)
            music=[bytes.fromhex(e['filename_hex']) for e in p.events if e['name']=='music_load']
            char=(packed-1)//2;expected=bytes([(48+char//10)&255,48+char%10])+b'mm.m'
            if music!=[b'dec.m' if stage==6 else expected,b'YUME.EFC']:raise ValueError('next-put BGM decimal request differs')
            record('next_put',p,dict(stage=stage,packed=packed))
    for tick,keys,terminal in [(32,(0x20,),False),(33,(0x20,),True),(96,(0x20,),True),(97,(0,),True),(None,(0x20,),False)]:
        p=RootProbe(mz,tick=tick,keys=keys);p.run(0x43c,terminal=terminal,budget=10000)
        record('clock',p,dict(tick=tick,keys=keys,terminal=terminal))
    for credits in (0,1,3,255):
        for keys in [(0x20,),(0x1000,),(4,4,0,4,0x20),(4,4,0x20),(0x3020,)]:
            p=RootProbe(mz,keys=keys);p.resident(credits=credits,stage=0);initial=bytes(p.uc.mem_read(0x50000,256));p.run(0x99d)
            selected=1
            if credits:
                held=False
                for k in keys:
                    direction=bool(k&12)
                    if direction and not held:selected=1-selected
                    held=direction
                    if k&0x2020:break
                    if k&0x1000:selected=0;break
            expected=bytearray(initial);expected[0x18:0x28]=b'\0'*16
            if credits:
                expected[0x36]=(credits-selected)&255;expected[0x33]=255;expected[0x34]=2
            if p.get('AX')!=(selected if credits else 0) or bytes(p.uc.mem_read(0x50000,256))!=expected:raise ValueError('continue scalar resident effects differ')
            if p.cstring(0x8d8,0x2e3f)!=(bytes([(48+credits-selected)&255]) if credits else b'0'):raise ValueError('continue mutable credit digit differs')
            record('continue',p,dict(credits=credits,keys=keys))
    p=RootProbe(mz,keys=(0,));p.run(0x99d,terminal=False,budget=10000);record('continue_budget',p,{})
    for mode,winner,stage,menu,bgm,credits,key in [(1,0,0,0,0,3,0x20),(1,0,5,0,1,3,0x20),(1,0,7,0,0,3,0x20),(1,0,8,0,0,3,0x20),(1,0,9,0,0,3,0x20),(1,1,5,0,0,3,0x20),(0x80,0,5,0,0,3,0x20),(1,0,5,1,0,3,0x20),(1,0,9,0,0,0,0x20),(1,0,9,0,0,3,0x1000)]:
        p=RootProbe(mz,exec_returns=True,keys=(key,));p.resident(mode=mode,winner=winner,stage=stage,menu=menu,bgm=bgm,credits=credits);p.run(0x78d,(2,0x1234,0x4567,0x5678,0x6789))
        execs=[bytes.fromhex(e['path_hex']) for e in p.events if e['name']=='exec']
        expected=[b'op' if mode!=1 or (stage==9 and (not credits or key==0x1000)) else b'main']
        if menu:expected=[b'op']+expected
        if execs!=expected:raise ValueError('main returned-exec handoff path differs')
        names=[e['name'] for e in p.events]
        if (0x19d in p.entries)!=(stage not in (0,8)) or ('staff' in names)!=(stage==9) or ('animate' in names)!=(stage in (7,8)) or ('ending' in names)!=(stage==9 and (not credits or key==0x1000)):raise ValueError('main control-flow route differs')
        record('main',p,dict(mode=mode,winner=winner,stage=stage,menu=menu,bgm=bgm,credits=credits,key=key))
    p=RootProbe(mz,cfg=0);p.run(0x78d)
    if [e['name'] for e in p.events]!=['cfg']:raise ValueError('main absent-resident gate differs')
    record('main_cfg_absent',p,{})
    p=RootProbe(mz,exec_returns=False);p.resident(menu=1);p.run(0x78d,terminal=False,exec_stop=True)
    if [bytes.fromhex(e['path_hex']) for e in p.events if e['name']=='exec']!=[b'op']:raise ValueError('main modeled exec handoff differs')
    record('main_exec_stop',p,{})
    return cases


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('root prior proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_root.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('root input changed: '+p)
    verify();target=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl'));observations=[]
    maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('invalid root image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            tree=Path(path).parents[2]
            for p,data in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=(data.replace(b'\n',b'\r\n') if p.endswith('.asm') else data):raise ValueError('root provider association differs')
            mp=next(p for p in maps if str(tree) in p)
            row=next(r for r in code_rows((ROOT/mp).read_text(),len(mz.program_image)) if r['module']=='th03_mainl.asm' and r['name']=='CUTSCENE_TEXT')
            if (row['segment'],row['offset'],row['size'])!=(CS,0x186,2488):raise ValueError('root MAP contribution differs')
            decoded=parse_mz((ROOT/observations[0]['path']).read_bytes());observed['comparison']=extent_observation(decoded,mz,row)
            observed['body_comparisons']={name:extent_observation(decoded,mz,dict(start=CS*16+at,size=size)) for name,at,size,_,_ in RANGES}
            observed['raw_difference_offsets']=[at for at in range(0x186,0xb3e) if decoded.program_image[CS*16+at]!=mz.program_image[CS*16+at]]
            if observed['cpu']!=observations[0]['cpu']:raise ValueError('root target/cached CPU diagnostics differ')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl'))!=target:raise ValueError('root canonical target changed')
    for p,data in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=data:raise ValueError('root frozen provider changed')
    result=dict(kind='th03-mainl-complete-root-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS complete MAINL root CODE candidate and explicit CPU/interface scopes:',args.output)


if __name__=='__main__':main()
