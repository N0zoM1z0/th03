#!/usr/bin/env python3
"""Review MAINL CRT break/pointer substrate without product/source acceptance."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16
from review_th03_mainl_graphics import COLD, COLD_SHA
from review_th03_mainl_draw import return_cleanup, trace_hash

ROOT = Path(__file__).resolve().parents[1]
PROOF = '.analysis/sol-mainl-root-tail-review-20261006.json'
PROOF_SHA = 'a37eade687a70135c7a054420db3c38d8f7a4658854930e6e08b990e580f501a'
LIBRARY = '.analysis/toolchain/installed/tc40j/LIB/CL.LIB'
ACTIVE_LIBRARY = '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB'
LIBRARY_SHA = '7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7'
MEMBERS = {'h_llsh.asm': ('h_llsh', 0x315e, 33), 'h_padd.asm': ('h_padd', 0x317f, 96),
           'ioerror.cas': ('ioerror', 0x31df, 82), 'n_pcmp.asm': ('n_pcmp', 0x357c, 33),
           'fbrk.c': ('fbrk', 0x3e70, 352), 'setblock.cas': ('setblock', 0x8e5a, 32)}
RANGES = [('shift_near', 0x315e, 3, 'bridge'), ('shift_far', 0x3161, 30, 0),
          ('add_near', 0x317f, 3, 'bridge'), ('add_far', 0x3182, 44, 0),
          ('sub_near', 0x31ae, 3, 'bridge'), ('sub_far', 0x31b1, 46, 0),
          ('ioerror', 0x31df, 62, ('near', 2)), ('doserror', 0x321d, 20, ('near', 2)),
          ('compare', 0x357c, 33, ('near', 0)), ('grow', 0x3e70, 142, ('near', 4)),
          ('brk', 0x3efe, 67, ('near', 0)), ('sbrk', 0x3f41, 143, ('near', 0)),
          ('setblock', 0x8e5a, 32, 0)]
ENTRY = {n: a for n, a, _, _ in RANGES}
BRIDGES = {0x3161: 'shift_near', 0x3182: 'add_near', 0x31b1: 'sub_near'}
CROSS_BRANCHES = {0x3190: 0x31c1, 0x31bf: 0x3192}
PUBLIC = set(ENTRY) - {'grow'}
CALLS = {0x3225: 'ioerror', 0x3ebe: 'setblock', 0x3f11: 'compare', 0x3f24: 'compare',
         0x3f2f: 'grow', 0x3f50: 'shift_near', 0x3f79: 'add_near', 0x3f8a: 'compare',
         0x3f9d: 'compare', 0x3fb5: 'grow', 0x8e72: 'ioerror'}
PUBLICS = {'N_LXLSH@': 0x315e, 'F_LXLSH@': 0x3161, 'N_PADD@': 0x317f, 'F_PADD@': 0x3182,
           'N_PSUB@': 0x31ae, 'F_PSUB@': 0x31b1, '__IOERROR': 0x31df, '__DOSERROR': 0x321d,
           'N_PCMP@': 0x357c, '__brk': 0x3efe, '__sbrk': 0x3f41, '_setblock': 0x8e5a}
PSP, ERRNO, BASE, BREAK, TOP, DOSERR, TABLE, GRANULE, NERR = 0x7a, 0x7e, 0x84, 0x88, 0x8c, 0xe8e, 0xe90, 0x1130, 0x1170
DATA_RANGES = [('psp', PSP, 2), ('errno', ERRNO, 2), ('heap_pointers', BASE, 12),
               ('dos_error_table', DOSERR, 91), ('granule_count', GRANULE, 2), ('system_error_count', NERR, 2)]
DATA_PUBLICS = {'__psp': PSP, '_errno': ERRNO, '__heapbase': BASE, '__brklvl': BREAK, '__heaptop': TOP,
                '__doserrno': DOSERR, '__dosErrorToSV': TABLE, '__sys_nerr': NERR}


def signed16(v): return v - 65536 if v & 32768 else v
def normalized_pointer(offset, segment): return (u16(segment + (offset >> 4)), offset & 15)
def pointer_add(offset, segment, delta):
    physical = ((segment << 4) + offset + delta) & 0xfffff
    return physical & 15, physical >> 4


def library_members(data, emit=False):
    """Bound selected members; library A3 naming comments keep stale checksums."""
    if len(data) < 16 or data[0] != 0xf0: raise ValueError('CRT library header differs')
    page = int.from_bytes(data[1:3], 'little') + 3
    limit = int.from_bytes(data[3:7], 'little')
    if not 16 <= page <= 32768 or page & (page - 1) or not page <= limit < len(data):
        raise ValueError('CRT library page/dictionary bounds differ')
    result = {}; cursor = page
    while cursor < limit and data[cursor] != 0xf1:
        if data[cursor] != 0x80: raise ValueError('CRT library member lacks THEADR')
        start = cursor; records = []
        while True:
            if cursor + 3 > limit: raise ValueError('CRT library truncated record')
            kind = data[cursor]; length = int.from_bytes(data[cursor + 1:cursor + 3], 'little')
            end = cursor + 3 + length
            if length < 1 or end > limit: raise ValueError('CRT library record escapes member area')
            block = data[cursor:end]; records.append((kind, block[3:-1], block[-1], sum(block) & 255))
            cursor = end
            if kind in (0x8a, 0x8b): break
        header = records[0][1]
        if not header or header[0] + 1 != len(header): raise ValueError('CRT library THEADR name differs')
        name = header[1:].decode('ascii')
        if name in MEMBERS:
            if name in result: raise ValueError('CRT library duplicate selected member')
            exceptions = []
            for kind, payload, checksum, residual in records:
                if not residual: continue
                # TLIB's librarian name comment is observed separately. Do not
                # repair it or pass this stream to the strict object validator.
                stem = name.split('.')[0].encode()
                if kind != 0x88 or payload != b'\x00\xa3' + bytes([len(stem)]) + stem:
                    raise ValueError('CRT library selected non-comment checksum failed')
                exceptions.append(dict(record='COMENT A3',checksum=checksum,residual=residual,payload_hex=payload.hex()))
            segments = [r[1] for r in records if r[0] == 0x98]
            code = [r[1] for r in records if r[0] == 0xa0 and r[1][:3] == b'\x01\x00\x00']
            if not segments or len(code) != 1 or int.from_bytes(segments[0][1:3], 'little') != MEMBERS[name][2] or len(code[0]) - 3 != MEMBERS[name][2]:
                raise ValueError('CRT library selected CODE ownership differs')
            publics = {}
            for kind, payload, _, _ in records:
                if kind != 0x90 or payload[:2] != b'\x00\x01': continue
                at = 2
                while at < len(payload):
                    width=payload[at]; at+=1
                    if at+width+3>len(payload): raise ValueError('CRT selected public definition truncated')
                    symbol=payload[at:at+width].decode('ascii'); at+=width
                    offset=int.from_bytes(payload[at:at+2],'little'); at+=2
                    if payload[at] != 0 or symbol in publics: raise ValueError('CRT selected public type/duplicate differs')
                    at+=1; publics[symbol]=offset
            result[name] = dict(offset=start,size=cursor-start,sha256=sha(data[start:cursor]),publics=publics,
                                code_sha256=sha(code[0][3:]),code_size=len(code[0])-3,checksum_exceptions=exceptions,
                                fixup_records=sum(r[0] == 0x9c for r in records),
                                data_sha256=[sha(r[1][3:]) for r in records if r[0] == 0xa0 and r[1][:3] == b'\x02\x00\x00'])
            if emit: result[name]['records']=records
        cursor = ((cursor + page - 1) // page) * page
    if set(result) != set(MEMBERS): raise ValueError('CRT library selected members missing')
    return result


def linked_member(member, start, data_offset, symbols):
    """Replay this bounded OMF offset/far-call subset using reviewed MAP symbols."""
    records=member['records']; externals=[]; code=None; fixups=[]
    for kind,payload,_,_ in records:
        if kind==0x8c:
            at=0
            while at<len(payload):
                width=payload[at]; at+=1
                if at+width>=len(payload): raise ValueError('CRT external definition truncated')
                externals.append(payload[at:at+width].decode('ascii')); at+=width
                if payload[at]!=0: raise ValueError('CRT external type index differs')
                at+=1
        if kind==0xa0:
            if payload[:3]==b'\x01\x00\x00': code=bytearray(payload[3:])
            elif payload[:3]!=b'\x02\x00\x00': raise ValueError('CRT unsupported emitted segment')
        if kind==0x9c: fixups.append(payload)
    if code is None: raise ValueError('CRT member lacks emitted CODE')
    observed=[]; occupied=set()
    for payload in fixups:
        at=0
        while at<len(payload):
            if at+3>len(payload): raise ValueError('CRT truncated fixup')
            first,second,method=payload[at:at+3]; at+=3
            if not first&128 or method not in (0x06,0x14,0x16,0x56): raise ValueError('CRT unsupported fixup method/thread/displacement')
            location=((first&3)<<8)|second; kind=(first>>2)&15; relative=not bool(first&64)
            frame=method>>4; target=method&3
            if frame in (0,1):
                if at>=len(payload) or payload[at]!=1: raise ValueError('CRT fixup frame is not reviewed DGROUP')
                at+=1
            if at>=len(payload): raise ValueError('CRT truncated target index')
            index=payload[at]; at+=1
            if index&128 or index==0: raise ValueError('CRT unsupported target index')
            if target==0:
                if index!=2 or data_offset is None: raise ValueError('CRT unsupported segment target')
                segment,offset=0xe3f,data_offset; symbol='member _DATA'
            elif target==2:
                if index>len(externals) or externals[index-1] not in symbols: raise ValueError('CRT unresolved external symbol')
                symbol=externals[index-1]; segment,offset=symbols[symbol]
            else: raise ValueError('CRT unsupported target method')
            width=4 if kind==3 else 2
            if kind not in (1,3) or location+width>len(code): raise ValueError('CRT fixup exceeds declared CODE/location kind')
            owned=set(range(location-1 if kind==3 else location,location+width))
            if owned&occupied: raise ValueError('CRT overlapping fixup ownership')
            occupied.update(owned)
            if kind==3:
                if relative or segment!=0 or frame!=5 or not location or code[location-1]!=0x9a or code[location:location+4]!=b'\0'*4:
                    raise ValueError('CRT far-call relaxation precondition differs')
                # TLINK's same-CODE 9A -> NOP/PUSH CS/CALL preserves five bytes.
                code[location-1:location+4]=b'\x90\x0e\xe8'+struct.pack('<H',u16(offset-(start+location+4)))
                action='same-CODE far-call relaxation'
            else:
                addend=int.from_bytes(code[location:location+2],'little')
                if relative:
                    if segment!=0 or frame not in (0,5): raise ValueError('CRT relative target is not same CODE')
                    value=offset-(start+location+2)+addend
                else:
                    if segment!=0xe3f or frame!=1: raise ValueError('CRT absolute target is not DGROUP')
                    value=offset+addend
                code[location:location+2]=struct.pack('<H',u16(value)); action='self-relative CODE' if relative else 'DGROUP offset'
            observed.append(dict(location=location,kind=kind,relative=relative,frame=frame,target=symbol,coordinates=[segment,offset],action=action))
    return bytes(code),observed


def analyze(image):
    decoder = Cs(CS_ARCH_X86, CS_MODE_16); decoder.detail = True
    bounds = set(); decoded = []; returns = {}; rows = []
    for name, start, size, cleanup in RANGES:
        body = image[start:start+size]; ins = list(decoder.disasm(body, start))
        if len(body) != size or not ins or sum(i.size for i in ins) != size: raise ValueError('CRT complete body partition differs')
        if cleanup == 'bridge':
            if body != (b'\x5b\x0e\x53' if name == 'shift_near' else b'\x07\x0e\x06'): raise ValueError('CRT near/far bridge differs')
        elif isinstance(cleanup, tuple):
            if ins[-1].mnemonic != 'ret' or (int(ins[-1].op_str, 0) if ins[-1].op_str else 0) != cleanup[1]: raise ValueError('CRT near cleanup differs')
        elif return_cleanup(ins[-1]) != cleanup: raise ValueError('CRT far cleanup differs')
        bounds.update(i.address for i in ins); decoded.append((name,start,size,cleanup,ins))
    for name,start,size,cleanup,ins in decoded:
        edges = []
        for index,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                returns[i.address] = ('near', int(i.op_str,0) if i.op_str else 0) if i.mnemonic == 'ret' else ('far',int(i.op_str,0) if i.op_str else 0)
                expected = cleanup if isinstance(cleanup,tuple) else ('far',cleanup)
                if returns[i.address] != expected: raise ValueError('CRT interior return cleanup differs')
            if i.mnemonic in ('in','out'): raise ValueError('CRT unexpected port')
            if i.mnemonic == 'int' and (i.address != 0x8e67 or i.bytes != b'\xcd\x21'): raise ValueError('CRT unexpected interrupt')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')): continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands): raise ValueError('CRT indirect edge differs')
            if i.mnemonic in ('lcall','ljmp'): raise ValueError('CRT far edge differs')
            destination = i.operands[0].imm
            if i.mnemonic == 'call':
                if CALLS.get(i.address) not in ENTRY or ENTRY[CALLS[i.address]] != destination: raise ValueError('CRT native call differs')
                if i.address == 0x3ebe and (not index or ins[index-1].bytes != b'\x0e'): raise ValueError('CRT far call lacks PUSH CS')
            elif destination not in bounds or not (start<=destination<start+size or CROSS_BRANCHES.get(i.address)==destination):
                raise ValueError('CRT branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=destination))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),cleanup=cleanup,sha256=sha(image[start:start+size]),edges=edges))
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,owned_code_bytes=628)


class BreakProbe(Probe):
    def __init__(self,mz,scenario,meta=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg; self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset; struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image)); self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=scenario; self.meta=meta or analyze(mz.program_image); self.bounds=set(self.meta['bounds']); self.frames=[]; self.pending=None
        self.errors=[]; self.stop=False; self.events=[]; self.writes=[]; self.native=Counter(); self.visited=set(); self.reply_index=0
        for a,key,default in ((PSP,'psp',0x5000),(ERRNO,'errno',0xbeef),(DOSERR,'doserrno',0x1234),(GRANULE,'granule',0x45),(NERR,'nerr',48)):
            self.uc.mem_write(self.data+a,struct.pack('<H',scenario.get(key,default)))
        for a,key,default in ((BASE,'base',[0,0x6000]),(BREAK,'break',[0,0x6100]),(TOP,'top',[0,0x9000])):
            self.uc.mem_write(self.data+a,struct.pack('<2H',*scenario.get(key,default)))
        if 'table' in scenario:
            if len(scenario['table']) != 89: raise ValueError('CRT error table fixture width differs')
            self.uc.mem_write(self.data+TABLE,bytes(scenario['table']))
        def guard(fn,default=None):
            def invoke(*args):
                try: return fn(*args)
                except Exception as e: self.errors.append(str(e)); self.uc.emu_stop(); return default
            return invoke
        def code(uc,address,size,user):
            if self.get('CS') != 0x2000 or self.get('SS') != 0x4000: raise ValueError('CRT CODE/stack segment alias')
            if address == self.code+0xff00:
                if self.frames or self.pending: raise ValueError('CRT unfinished native frame')
                self.stop=True; uc.emu_stop(); return
            off=address-self.code
            if off not in self.bounds: raise ValueError('CPU escaped CRT instruction boundaries')
            self.visited.add(off)
            if off in BRIDGES and self.frames and self.frames[-1]['name'] == BRIDGES[off] and self.pending is None:
                frame=self.frames[-1]
                if frame['kind'] != 'near' or self.get('SP') != u16(frame['sp']-2): raise ValueError('CRT bridge stack differs')
                if tuple(struct.unpack('<2H',uc.mem_read(self.stack+self.get('SP'),4))) != (frame['ip'],0x2000): raise ValueError('CRT bridge far frame differs')
                frame.update(kind='far',sp=self.get('SP')); self.native[next(n for n,a,_,_ in RANGES if a==off)]+=1
            elif off in ENTRY.values():
                name=next(n for n,a,_,_ in RANGES if a==off)
                expected=self.pending
                if not expected or expected['name'] != name or self.get('SP') != expected['sp']: raise ValueError('CRT native entry frame differs')
                count=2 if expected['kind']=='far' else 1
                values=tuple(struct.unpack('<'+'H'*count,uc.mem_read(self.stack+self.get('SP'),2*count)))
                if values != ((expected['ip'],0x2000) if count==2 else (expected['ip'],)): raise ValueError('CRT native return address differs')
                self.frames.append(expected); self.pending=None; self.native[name]+=1
            if off in CALLS:
                name=CALLS[off]; kind='far' if name=='setblock' else 'near'
                if self.pending: raise ValueError('CRT overlapping native call')
                cleanup=next(c for n,_,_,c in RANGES if n==name)
                self.pending=dict(name=name,sp=u16(self.get('SP')-2),ip=off+3,kind=kind,cleanup=cleanup[1] if isinstance(cleanup,tuple) else 0)
            if off in self.meta['returns']:
                kind,cleanup=self.meta['returns'][off]
                if not self.frames: raise ValueError('CRT orphan native return')
                frame=self.frames.pop(); count=2 if kind=='far' else 1
                values=tuple(struct.unpack('<'+'H'*count,uc.mem_read(self.stack+self.get('SP'),2*count)))
                if frame['kind'] != kind or frame['cleanup'] != cleanup or self.get('SP') != frame['sp'] or values != ((frame['ip'],0x2000) if count==2 else (frame['ip'],)):
                    raise ValueError('CRT native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536: return
            if not any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((ERRNO,2),(BREAK,8),(DOSERR,2),(GRANULE,2))):
                raise ValueError('CRT write outside declared complete state span')
            self.writes.append([address,size,value])
        def intr(uc,number,user):
            if number!=0x21 or self.get('CS')!=0x2000 or self.get('IP')!=0x8e69 or self.get('AH')!=0x4a:
                raise ValueError('CRT unknown DOS request/site')
            replies=scenario.get('replies',[{}]); reply=replies[min(self.reply_index,len(replies)-1)]; self.reply_index+=1
            ax,cf,bx=reply.get('ax',8),reply.get('cf',0),reply.get('bx',self.get('BX'))
            self.events.append(dict(site=0x8e67,name='dos-setblock',segment=self.get('ES'),paragraphs=self.get('BX'),ax=ax,cf=cf,bx=bx))
            self.set('AX',ax); self.set('BX',bx); self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def port(*args): raise ValueError('CRT unexpected port interface')
        self.uc.hook_add(UC_HOOK_CODE,guard(code)); self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write)); self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(port),None,1,0,reg.UC_X86_INS_OUT); self.uc.hook_add(UC_HOOK_INSN,guard(port,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),registers=None,budget=10000):
        if name not in PUBLIC: raise ValueError('CRT private helper requires complete public caller')
        self.stop=False; self.errors.clear(); self.frames.clear(); self.pending=None
        defaults=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,
                      EFLAGS=2|self.s.get('flags',512)|(1024 if self.s.get('df') else 0))
        overrides=registers or {}
        if any(r not in ('AX','BX','CX','DX') for r in overrides): raise ValueError('CRT ABI register fixture differs')
        defaults.update(overrides)
        for r,v in defaults.items(): self.set(r,v)
        kind='far' if name.endswith('_far') or name=='setblock' else 'near'
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*((2 if kind=='far' else 1)+len(args)),0xff00,*([0x2000] if kind=='far' else []),*args))
        cleanup=2 if name in ('ioerror','doserror') else 0
        self.pending=dict(name=name,sp=0xffc0,ip=0xff00,kind=kind,cleanup=cleanup)
        self.uc.emu_start(self.code+ENTRY[name],0x100000,count=budget)
        if self.errors: raise ValueError(self.errors[0])
        if not self.stop: raise ValueError('CRT terminal/budget differs')
        if self.get('SP') != 0xffc0+(4 if kind=='far' else 2)+cleanup or any(self.get(r)!=defaults[r] for r in ('BP','SI','DI','DS','SS')):
            raise ValueError('CRT public cleanup/preserved registers differ')
        if self.get('EFLAGS') & 1536 != defaults['EFLAGS'] & 1536: raise ValueError('CRT IF/DF preservation differs')


class Scalar:
    """Integer/address specification; only DOS replies and data are fixtures."""
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000)); self.data=p.data; self.s=p.s; self.writes=[]; self.events=[]; self.native=Counter(); self.reply_index=0
    def word(self,a): return int.from_bytes(self.mem[self.data+a:self.data+a+2],'little')
    def put(self,a,v):
        v=u16(v); self.mem[self.data+a:self.data+a+2]=v.to_bytes(2,'little'); self.writes.append([self.data+a,2,v])
    def pointer(self,a): return self.word(a),self.word(a+2)
    def relation(self,left,right):
        self.native['compare']+=1
        a,b=normalized_pointer(*left),normalized_pointer(*right)
        return -1 if a<b else 1 if a>b else 0
    def error(self,code):
        self.native['ioerror']+=1; value=signed16(code)
        if value>=0:
            index=code if code<=88 else 87; self.put(DOSERR,index)
            value=signed16(self.mem[self.data+TABLE+index] | (0xff00 if self.mem[self.data+TABLE+index]&128 else 0))
        else:
            value=signed16(u16(-value))
            if value>signed16(self.word(NERR)):
                self.put(DOSERR,87); value=signed16(self.mem[self.data+TABLE+87] | (0xff00 if self.mem[self.data+TABLE+87]&128 else 0))
            else: self.put(DOSERR,65535)
        self.put(ERRNO,value); return 65535
    def setblock(self,segment,count):
        self.native['setblock']+=1
        replies=self.s.get('replies',[{}]); reply=replies[min(self.reply_index,len(replies)-1)]; self.reply_index+=1
        ax,cf,bx=reply.get('ax',8),reply.get('cf',0),reply.get('bx',count)
        self.events.append(dict(site=0x8e67,name='dos-setblock',segment=segment,paragraphs=count,ax=ax,cf=cf,bx=bx))
        if not cf: return 65535
        self.error(ax); return bx
    def grow(self,offset,segment):
        self.native['grow']+=1; psp=self.word(PSP)
        count=u16(u16(segment+1-psp)+63)>>6
        if count != self.word(GRANULE):
            paragraphs=u16(count<<6)
            if u16(psp+paragraphs)>self.word(TOP+2): paragraphs=u16(self.word(TOP+2)-psp)
            result=self.setblock(psp,paragraphs)
            if result!=65535:
                self.put(TOP+2,psp+result); self.put(TOP,0); return False
            self.put(GRANULE,paragraphs>>6)
        self.put(BREAK+2,segment); self.put(BREAK,offset); return True
    def run(self,name,args=(),registers=None):
        r=dict(AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444); r.update(registers or {})
        ax,bx,cx,dx=(r[k] for k in ('AX','BX','CX','DX'))
        if name=='setblock': return dict(ax=self.setblock(*args))
        if name=='ioerror': return dict(ax=self.error(args[0]))
        self.native[name]+=1
        if name=='doserror': self.error(args[0]); return dict(ax=args[0])
        if name.startswith('shift_'):
            if name.endswith('_near'): self.native['shift_far']+=1
            count=cx&255
            if count<16: result=(((dx<<16)|ax)<<count)&0xffffffff
            else: result=((ax<<((count-16)&31))&65535)<<16
            return dict(ax=result&65535,dx=result>>16)
        if name.startswith(('add_','sub_')):
            if name.endswith('_near'): self.native[name.replace('_near','_far')]+=1
            delta=(cx<<16)|bx
            if delta&0x80000000: delta-=0x100000000
            offset,segment=pointer_add(ax,dx,delta if name.startswith('add') else -delta)
            return dict(ax=offset,dx=segment)
        if name=='compare':
            a,b=normalized_pointer(ax,dx),normalized_pointer(bx,cx)
            return dict(cf=int(a<b),zf=int(a==b))
        if name=='brk':
            desired=tuple(args)
            if self.relation(desired,self.pointer(BASE))<0 or self.relation(desired,self.pointer(TOP))>0: return dict(ax=65535)
            return dict(ax=0 if self.grow(*desired) else 65535)
        if name=='sbrk':
            current=self.pointer(BREAK); inc=args[0]|(args[1]<<16)
            linear=((current[1]<<4)+current[0]+inc)&0xffffffff
            self.native['shift_near']+=1; self.native['shift_far']+=1
            if signed16(linear>>16)>15: return dict(ax=65535,dx=65535)
            delta=inc-0x100000000 if inc&0x80000000 else inc
            desired=pointer_add(*current,delta); self.native['add_near']+=1; self.native['add_far']+=1
            if self.relation(desired,self.pointer(BASE))<0 or self.relation(desired,self.pointer(TOP))>0: return dict(ax=65535,dx=65535)
            if not self.grow(*desired): return dict(ax=65535,dx=65535)
            return dict(ax=current[0],dx=current[1])
        raise ValueError('CRT scalar unsupported public entry')


def matrix(mz):
    meta=analyze(mz.program_image); rows=[]
    def observe(label,scenario,steps):
        p=BreakProbe(mz,scenario,meta); m=Scalar(p); before=sha(bytes(m.mem)); results=[]
        for name,args,registers in steps:
            expected=m.run(name,args,registers); p.run(name,args,registers)
            actual={'ax':p.get('AX'),'dx':p.get('DX'),'cf':p.get('EFLAGS')&1,'zf':int(bool(p.get('EFLAGS')&64))}
            if any(actual[k]!=v for k,v in expected.items()) or p.events!=m.events or p.writes!=m.writes or p.native!=m.native:
                raise ValueError('CRT independent return/events/stores/native entries differ: '+label+' '+str((expected,actual,p.native,m.native)))
            physical=bytes(p.uc.mem_read(0,0x100000)); expected_memory=bytes(m.mem)
            if physical[:p.stack]!=expected_memory[:p.stack] or physical[p.stack+65536:]!=expected_memory[p.stack+65536:]:
                raise ValueError('CRT whole physical memory outside stack differs: '+label)
            results.append(dict(function=name,args=args,registers=registers,result=expected))
        rows.append(dict(label=label,scenario=scenario,steps=results,top_level_calls=len(steps),native_entries=dict(p.native),visited=sorted(p.visited),
                         events=p.events,store_count=len(p.writes),stores_sha256=trace_hash(p.writes),memory_before_sha256=before,memory_after_sha256=sha(bytes(m.mem))))
    flags=[dict(df=df,flags=2|irq) for df in (False,True) for irq in (0,512)]
    word_values=(0,1,15,16,17,255,256,4095,4096,32767,32768,65534,65535)
    for count in range(256):
        for value in (0,1,0xffff,0x80000000,0xffffffff,0x12345678):
            observe('compiler-long-shift-counts',flags[count&3],[(n,[],dict(AX=value&65535,DX=value>>16,CX=0xa500|count)) for n in ('shift_near','shift_far')])
    for offset in word_values:
        for segment in (0,1,0x5000,0xffff):
            for delta in (0,1,15,16,65535,65536,0x7fffffff,0x80000000,0xffff0000,0xffffffff):
                observe('compiler-pointer-wrap-signed-offset',flags[offset&3],[(n,[],dict(AX=offset,DX=segment,BX=delta&65535,CX=delta>>16)) for n in ('add_near','add_far','sub_near','sub_far')])
    pointers=[(a,b) for a in word_values for b in (0,1,0x5000,0xffff)]
    for index,left in enumerate(pointers):
        for right in pointers: observe('normalized-pointer-order-aliases',flags[index&3],[('compare',[],dict(AX=left[0],DX=left[1],BX=right[0],CX=right[1]))])
    errors=list(range(0,96))+[127,128,255,256,32767,32768,65535,65534,65500,65488,65487]
    for error in errors:
        observe('DOS-error-sign-clamp-table',flags[error&3],[('ioerror',[error],{}),('doserror',[error],{}),('setblock',[0x5000,0x400],{})])
        observe('DOS-setblock-failure-largest-block',dict(flags[error&3],replies=[dict(ax=error,cf=1,bx=0x1234)]),[('setblock',[0x5000,0x400],{})])
    for error_count in (0,1,48,32767,32768,65535):
        for error in errors[-11:]: observe('signed-error-count-boundary',dict(nerr=error_count,table=[(i*17+129)&255 for i in range(89)]),[('ioerror',[error],{}),('doserror',[error],{})])
    requests=[(offset,segment) for offset in (0,1,15,16,65535) for segment in (0,0x4fff,0x5000,0x5fff,0x6000,0x603e,0x603f,0x6040,0x6100,0x8fff,0x9000,0xffff)]
    increments=[0,1,15,16,17,1023,1024,65535,65536,0x2ffff,0x30000,0x80000000,0xffffffff,0xfffffff0,0xffff0000,0xfff00000,0x100000,0x7fffffff]
    for base in flags:
        for granule in (0,0x45,65535):
            for reply in ({},{'cf':1,'ax':8,'bx':0x2000},{'cf':1,'ax':65535,'bx':65535}):
                scenario=dict(base,granule=granule,replies=[reply])
                for pointer in requests: observe('break-normalization-granule-DOS',scenario,[('brk',list(pointer),{})])
                for inc in increments: observe('sbrk-signed-wrap-DOS',scenario,[('sbrk',[inc&65535,inc>>16],{})])
    for psp in (0,1,0x5000,0xffc0,65535):
        observe('psp-rounding-wrap',dict(psp=psp,base=[0,0],top=[15,65535],granule=0),[('brk',[0,65535],{}),('sbrk',[0,0],{})])
    for current in ([65535,0x5100],[15,0x60ff],[16,0x60ff],[0,0xffff]):
        observe('noncanonical-existing-break',dict(base=[0,0],top=[15,65535],**{'break':current}),[('sbrk',[0,0],{}),('sbrk',[1,0],{})])
    observe('native-break-state-chain',{},[('sbrk',[1,0],{}),('sbrk',[1023,0],{}),('sbrk',[65535,65535],{}),('brk',[8,0x6100],{}),('sbrk',[0,0],{})])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes(); cold_raw=(ROOT/COLD).read_bytes()
    if sha(raw)!=PROOF_SHA or sha(cold_raw)!=COLD_SHA: raise ValueError('CRT prior/cold receipt differs')
    proof=json.loads(raw); cold=json.loads(cold_raw)
    inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_crt_break.py':sha(Path(__file__).read_bytes()),
            'tests/test_mainl_crt_break_review.py':sha((ROOT/'tests/test_mainl_crt_break_review.py').read_bytes())}
    for path in (LIBRARY,ACTIVE_LIBRARY,'config/toolchain.toml'):
        data=(ROOT/path).read_bytes(); inputs[path]=sha(data)
        if path.endswith('.LIB') and sha(data)!=LIBRARY_SHA: raise ValueError('CRT pinned local library differs')
    providers=library_members((ROOT/LIBRARY).read_bytes())
    emitted_members=library_members((ROOT/LIBRARY).read_bytes(),emit=True)
    def verify():
        for path,digest in inputs.items():
            if sha((ROOT/path).read_bytes())!=digest: raise ValueError('CRT input changed: '+path)
    verify(); artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl'); stored=read_verified_artifact(ROOT,artifact)
    observations=[]; target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    for name,member in providers.items():
        _,start,size=MEMBERS[name]
        if not member['fixup_records'] and member['code_sha256']!=sha(target.program_image[start:start+size]):
            raise ValueError('CRT fixup-free library CODE differs from target')
        for symbol,offset in PUBLICS.items():
            if start<=offset<start+size and member['publics'].get(symbol)!=offset-start:
                raise ValueError('CRT library public ownership differs: '+symbol)
    if providers['ioerror.cas']['data_sha256'] != [sha(target.program_image[0xe3f0+DOSERR:0xe3f0+DOSERR+91])] or providers['fbrk.c']['data_sha256'] != [sha(target.program_image[0xe3f0+GRANULE:0xe3f0+GRANULE+2])]:
        raise ValueError('CRT library initialized DATA differs from target')
    for index,prior in enumerate(proof['observations']):
        path=prior['path']; mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid: raise ValueError('CRT invalid MZ')
        observed=dict(path=path,analysis=analyze(mz.program_image))
        if index:
            tree=Path(path).parents[2]; mappath=str(tree/'obj/th03/mainl.map'); text=(ROOT/mappath).read_text(); inputs[mappath]=sha((ROOT/mappath).read_bytes())
            carriers=code_rows(text,len(mz.program_image)); selected=[]
            for module,start,size in MEMBERS.values():
                carrier=next(r for r in carriers if r['module']==module and r['start']==start and r['size']==size and r['segment']==0)
                selected.append(carrier)
            observed['carriers']=selected
            for name,offset in PUBLICS.items():
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.MULTILINE)}
                if coords!={(0,offset)}: raise ValueError('CRT public MAP entry differs: '+name)
            observed['public_entries']=PUBLICS
            symbols={n:(0,a) for n,a in PUBLICS.items()}
            for name,offset in DATA_PUBLICS.items():
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.MULTILINE)}
                if coords!={(0xe3f,offset)}: raise ValueError('CRT DATA public MAP entry differs: '+name)
                symbols[name]=(0xe3f,offset)
            data_carriers={}
            for module,offset,size in (('ioerror',DOSERR,91),('fbrk',GRANULE,2)):
                if len(re.findall(r'^\s*0E3F:'+f'{offset:04X}'+r'\s+'+f'{size:04X}'+r'\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M='+module+r'\s+ACBP=48\s*$',text,re.MULTILINE))!=1:
                    raise ValueError('CRT member DATA MAP contribution differs')
                data_carriers[module]=offset
            observed['library_linked_members']={}
            for name,member in emitted_members.items():
                module,start,size=MEMBERS[name]; linked,fixups=linked_member(member,start,data_carriers.get(module),symbols)
                if linked!=mz.program_image[start:start+size] or linked!=target.program_image[start:start+size]:
                    raise ValueError('CRT library symbolic fixup/link relaxation differs: '+name)
                observed['library_linked_members'][name]=dict(linked_code_sha256=sha(linked),fixups=fixups)
            logpath=str(tree.parent/'cold-build.log'); log=(ROOT/logpath).read_bytes(); inputs[logpath]=sha(log)
            if sha(log)!=cold['rounds'][index-1]['commands'][0]['log_sha256']: raise ValueError('CRT cold build command log differs')
            response_path=str(tree/'obj/th03/mainl.@l'); response=(ROOT/response_path).read_bytes(); inputs[response_path]=sha(response)
            command=response.decode().strip()
            if not command.startswith('-c -s -E c0l.obj ') or not command.endswith(', bin\\th03\\mainl.exe, obj\\th03\\mainl.map, emu.lib mathl.lib cl.lib') or command+'>'+'obj\\th03\\mainl.@l' not in log.decode():
                raise ValueError('CRT cold MAINL CL library/link response differs')
            observed['compiler_link_lineage']=dict(command_log=logpath,response=response_path,response_sha256=sha(response),new_build=False)
            observed['code_comparisons']={module:extent_observation(target,mz,dict(start=start,size=size,segment=0,offset=start)) for module,start,size in MEMBERS.values()}
            observed['data_comparisons']={name:extent_observation(target,mz,dict(start=0xe3f0+offset,size=size,segment=0xe3f,offset=offset)) for name,offset,size in DATA_RANGES}
            if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in list(observed['code_comparisons'].values())+list(observed['data_comparisons'].values())):
                raise ValueError('CRT cold raw/ordered relocations differ')
            if observed['analysis']!=observations[0]['analysis']: raise ValueError('CRT cold complete boundaries differ')
        observed['cpu']=matrix(mz)
        visited={a for row in observed['cpu'] for a in row['visited']}; bounds=set(observed['analysis']['bounds'])
        observed['instruction_coverage']=dict(instructions=len(bounds),visited=len(visited&bounds),unvisited=sorted(bounds-visited))
        normalized=lambda rows:[{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in rows]
        if index and normalized(observed['cpu'])!=normalized(observations[0]['cpu']): raise ValueError('CRT target/cold native CPU differs')
        observations.append(observed); print('Reviewed',path,len(observed['cpu']),'scenarios',observed['instruction_coverage'],flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored: raise ValueError('CRT canonical stored target changed')
    result=dict(kind='th03-mainl-crt-break-pointer-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                compiler_library=dict(path=LIBRARY,sha256=LIBRARY_SHA,selected_members=providers,provenance='candidate-local-attested',
                                      notes='Compiled Borland library, not frozen ReC98 authored source. A3 librarian comments retain stale checksums; code/data/fixup records checked without checksum repair. No copied proprietary objects/source or independent pristine attestation.'),
                cold_receipt_sha256=sha(cold_raw),tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),
                diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS MAINL CRT break substrate628 CODE/111 initialized DATA; source/exact open:',args.output)


if __name__=='__main__': main()
