#!/usr/bin/env python3
"""Independent OP/MAINL complete text carrier with native GRCG and scalar effects."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed
from review_th03_mainl_text import PROVIDERS, HEADERS, INITIAL, font_byte, weight_row

ROOT = Path(__file__).resolve().parents[1]
PARENT = '.analysis/th03-shared-cdg-draw/sol-shared-cdg-draw-source-20261006/receipt.json'
PARENT_SHA = '3af43ad7435658807c9bab066d99c2e324dda825627d287be37c087e7abca2b9'
PROFILES = {
    'op': dict(cs=0xbeb, ds=0xd7f, start=0x82b, color=0xec6, off=0xef0, converter=0x9561, mbctype=0x103d, graph=0xd51),
    'mainl': dict(cs=0xc7e, ds=0xe3f, start=0x9b7, color=0xc36, off=0xc60, converter=0x924c, mbctype=0x11ef, graph=0xf05),
}


def ranges(p):
    return [('text', p['cs'], p['start'], 613, 10), ('color', 0, p['color'], 41, 4), ('off', 0, p['off'], 5, 0)]


def analyze(image, p):
    decoder = Cs(CS_ARCH_X86, CS_MODE_16); decoder.detail = True
    rows = []
    for name, seg, start, size, cleanup in ranges(p):
        body = image[seg*16+start:seg*16+start+size]
        ins = list(decoder.disasm(body, start)); bounds = {i.address for i in ins}
        wanted = ('retf', hex(cleanup) if cleanup == 10 else str(cleanup) if cleanup else '')
        if len(body) != size or not ins or sum(i.size for i in ins) != size or (ins[-1].mnemonic, ins[-1].op_str) != wanted:
            raise ValueError('text complete body/far cleanup differs')
        edges = []
        for i in ins:
            if i.mnemonic in ('ret', 'retf') and (i.mnemonic, i.op_str) != wanted: raise ValueError('text interior return differs')
            if i.mnemonic == 'int': raise ValueError('text unknown interrupt')
            if i.mnemonic in ('in', 'out'):
                allowed = [('out', 'dx, al'), ('in', 'al, dx')] if name == 'text' else [('out', '0x7c, al'), ('out', 'dx, al')]
                if (i.mnemonic, i.op_str) not in allowed: raise ValueError('text port encoding differs')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall')): continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands): raise ValueError('text indirect edge')
            dest = tuple(o.imm for o in i.operands) if i.mnemonic == 'lcall' else (seg, i.operands[0].imm)
            if i.mnemonic in ('call', 'lcall'):
                expected = {0x2b: (0, p['color']), 0x7f: (0, p['converter']), 0x25a: (0, p['off'])}
                if name != 'text' or i.mnemonic != 'lcall' or expected.get(i.address-start) != dest: raise ValueError('text complete caller binding differs')
            elif dest[1] not in bounds: raise ValueError('text branch enters operand/neighbor')
            edges.append(dict(position=i.address-start, kind=i.mnemonic, destination=dest))
        if name == 'text':
            by = {i.address-start: i for i in ins}
            for at, base, mask in [(0x65,p['mbctype'],4),(0x98,p['mbctype'],3),(0xb5,p['graph'],0x5e)]:
                if (by[at].mnemonic, by[at].op_str) != ('test', f'byte ptr [bx + {hex(base)}], {hex(mask) if mask > 9 else mask}'):
                    raise ValueError('text actual classifier binding differs')
            if set(e['position'] for e in edges if e['kind']=='lcall') != {0x2b,0x7f,0x25a}: raise ValueError('text complete call set differs')
        rows.append(dict(name=name, segment=seg, offset=start, size=size, instructions=len(ins), positions=sorted(i.address-start for i in ins), sha256=sha(body), edges=edges))
    return dict(bodies=rows, body_bytes=613, contextual_bytes=46)


class TextSpec:
    """Source-level event generator; actual synthetic physical tables/string/ROM."""
    def __init__(self, before, p, s):
        self.memory = bytearray(before); self.p = p; self.s = s
        self.position = u16(s.get('offset',0xfff8)); self.glyphs = []

    def events(self):
        p,s = self.p,self.s; ds=(p['ds']+0x2000)*16; string=s.get('segment',0x5000)*16
        left=signed(u16(s.get('left',0))); top=signed(u16(s.get('top',0))); fx=u16(s.get('fx',0))
        yield ['out',0x7c,1,0xc0]
        for plane in range(4): yield ['out',0x7e,1,255 if fx&(1<<plane) else 0]
        yield ['out',0x68,1,0xb]
        for _ in range(65536):
            byte=self.memory[string+self.position]
            if not byte: break
            quotient=(abs(left)//8)*(-1 if left<0 else 1); remainder=left-quotient*8; vram=u16(top*80+quotient)
            if self.memory[ds+p['mbctype']+byte]&4:
                arg=u16(((byte if byte<128 else byte-256)<<8)+self.memory[string+u16(self.position+1)])
                codepoint=u16(s.get('jis',0x2121)); self.position=u16(self.position+2)
                yield ['convert',arg,codepoint]
            elif self.memory[ds+p['mbctype']+byte]&3:
                codepoint=byte+0x2980; self.position=u16(self.position+1)
            elif self.memory[ds+u16(p['graph']+(byte if byte<128 else byte-256))]&0x5e:
                codepoint=byte+0x2900; self.position=u16(self.position+1)
            else: codepoint=0x2b21; self.position=u16(self.position+1)
            yield ['out',0xa1,1,codepoint&255]; yield ['out',0xa3,1,((codepoint>>8)-32)&255]
            half=0x2921<=codepoint<=0x2b7e
            self.glyphs.append(dict(codepoint=codepoint,left=left,half=half,clipped=left>(632 if half else 624)))
            if self.glyphs[-1]['clipped']: break
            glyph=[]
            for line in range(16):
                yield ['out',0xa5,1,line|32]; high=font_byte(codepoint,line|32); yield ['in',0xa9,1,high]; row=high<<8
                if not half:
                    yield ['out',0xa5,1,line]; low=font_byte(codepoint,line); yield ['in',0xa9,1,low]; row+=low
                glyph.append(row)
            for row in glyph:
                row=weight_row(row,(fx>>4)&3)
                values=[(row>>((remainder+8)&31))&255,(row>>(remainder&31))&255,((row&255)<<((8-remainder)&31))&255] if remainder else [row>>8,row&255]
                for j,value in enumerate(values):
                    at=0xa8000+u16(vram+j); self.memory[at]=value; yield ['store',at-0xa8000,1,value]
                vram=u16(vram+80)
            left=signed(u16(left+((fx>>6)&7)+(8 if half else 16)))
        else: raise ValueError('text scalar exhausted word glyph bound')
        yield ['out',0x68,1,0xa]; yield ['out',0x7c,1,0]


class TextProbe(Probe):
    def __init__(self,mz,p):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg; self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset; struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image)); self.uc.mem_write(0xa8000,INITIAL)
        self.p=p; self.code=(p['cs']+0x2000)*16; self.data=(p['ds']+0x2000)*16; self.stack=0x40000
        meta=analyze(mz.program_image,p)
        self.allowed={(seg+0x2000,at+position) for row,(_,seg,at,_,_) in zip(meta['bodies'],ranges(p)) for position in row['positions']}
        self.errors=[]; self.trace=[]; self.visited=set(); self.calls=[]; self.stop=False; self.s={}
        self.low=self.high=self.selector=None
        def guard(fn,default=None):
            def invoke(*args):
                try: return fn(*args)
                except Exception as e: self.errors.append(str(e)); self.uc.emu_stop(); return default
            return invoke
        def code(uc,address,size,user):
            cs=self.get('CS'); ip=address-cs*16
            if address==self.code+0xff00:
                if (cs,ip)!=(p['cs']+0x2000,0xff00): raise ValueError('text terminal segment alias')
                self.stop=True; uc.emu_stop(); return
            if address==0x20000+p['converter']:
                sp=self.get('SP'); frame=struct.unpack('<3H',uc.mem_read(self.stack+sp,6))
                if cs!=0x2000 or sp!=0xff82 or self.get('SS')!=0x4000 or self.get('BP')!=0xffbe or frame[:2]!=(p['start']+0x84,p['cs']+0x2000): raise ValueError('text converter cdecl frame differs')
                value=u16(self.s.get('jis',0x2121)); self.trace.append(['convert',frame[2],value]); self.calls.append(dict(name='convert',sp=sp,bp=self.get('BP'),argument=frame[2]))
                self.set('AX',value)
                if self.s.get('volatile'):
                    self.set('CX',0xffff); self.set('DX',0xffff); self.set('EFLAGS',self.get('EFLAGS')|1)
                self.set('SP',sp+4); self.set('CS',frame[1]); self.set('IP',frame[0]); return
            if (cs,ip) not in self.allowed: raise ValueError(f'CPU escaped text instruction boundaries {cs:04x}:{ip:04x} physical {address:05x}')
            if cs==p['cs']+0x2000: self.visited.add(('text',ip-p['start']))
            elif p['color']<=ip<p['color']+41: self.visited.add(('color',ip-p['color']))
            else: self.visited.add(('off',ip-p['off']))
            if (cs,ip) in ((0x2000,p['color']),(0x2000,p['off'])):
                name='color' if ip==p['color'] else 'off'; sp=self.get('SP'); n=4 if name=='color' else 2
                frame=struct.unpack('<'+str(n)+'H',uc.mem_read(self.stack+sp,2*n)); wanted=p['start']+(0x30 if name=='color' else 0x25f)
                if self.get('SS')!=0x4000 or self.get('BP')!=0xffbe or sp!=(0xff80 if name=='color' else 0xff84) or frame[:2]!=(wanted,p['cs']+0x2000) or name=='color' and frame[2:]!=(u16(self.s.get('fx',0))&15,0xc0): raise ValueError('text native GRCG frame differs')
                self.calls.append(dict(name=name,sp=sp,bp=self.get('BP'),arguments=list(frame[2:])))
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536: return
            if 0xa8000<=address and address+size<=0xb8000 and size==1: self.trace.append(['store',address-0xa8000,size,value]); return
            raise ValueError('text unexpected physical write/width')
        def output(uc,port,width,value,user):
            if width!=1 or port not in (0x7c,0x7e,0x68,0xa1,0xa3,0xa5): raise ValueError('text unknown output port/width')
            if port==0xa1: self.low=value
            elif port==0xa3: self.high=(value+32)&255
            elif port==0xa5:
                if value not in (*range(16),*range(32,48)): raise ValueError('text unknown ROM row')
                self.selector=value
            self.trace.append(['out',port,width,value])
        def inp(uc,port,width,user):
            if (port,width)!=(0xa9,1) or None in (self.low,self.high,self.selector): raise ValueError('text unknown ROM input/selection')
            value=font_byte((self.high<<8)|self.low,self.selector); self.trace.append(['in',port,width,value]); return value
        def intr(*args): raise ValueError('text unexpected interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code)); self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write)); self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT); self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,s,terminal=True):
        self.s=s; self.trace=[]; self.calls=[]; self.visited=set(); self.errors=[]; self.stop=False
        for name,value in [('CS',self.p['cs']+0x2000),('DS',self.p['ds']+0x2000),('SS',0x4000),('ES',0x3333),('FS',0x3456),('BP',0x7777),('SI',0x1357),('DI',0x2468),('SP',0xffc0),('EFLAGS',2|(0x200 if s.get('if',1) else 0)|(0x400 if s.get('df') else 0))]: self.set(name,value)
        string=bytearray(b'A'*65536 if s.get('unterminated') else b'\0'*65536); offset=u16(s.get('offset',0xfff8))
        for i,b in enumerate(s.get('string',[] if s.get('unterminated') else [65,0])): string[u16(offset+i)]=b
        seg=s.get('segment',0x5000)
        if seg in (0x4000,self.p['cs']+0x2000): raise ValueError('text string aliases stack/CODE fixture')
        self.uc.mem_write(seg*16,bytes(string))
        args=[0xff00,self.p['cs']+0x2000,offset,seg,u16(s.get('fx',0)),u16(s.get('top',0)),u16(s.get('left',0))]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<7H',*args))
        before=bytes(self.uc.mem_read(0,0x100000)); spec=TextSpec(before,self.p,s)
        self.uc.emu_start(self.code+self.p['start'],0x100000,count=50000 if terminal else 10000)
        if self.errors: raise ValueError(self.errors[0])
        if self.stop!=terminal: raise ValueError('text terminal/budget differs: '+str(s))
        expected=list(spec.events()) if terminal else list(itertools.islice(spec.events(),len(self.trace)))
        if self.trace!=expected: raise ValueError('text unified scalar trace differs: '+str(s))
        after=bytes(self.uc.mem_read(0,0x100000))
        if after[:self.stack]!=spec.memory[:self.stack] or after[self.stack+65536:]!=spec.memory[self.stack+65536:]: raise ValueError('text full physical memory differs')
        if terminal and (self.get('SP')!=0xffce or self.get('DS')!=self.p['ds']+0x2000 or [self.get(r) for r in ('BP','SI','DI','FS')]!=[0x7777,0x1357,0x2468,0x3456]): raise ValueError('text far cleanup/saved registers differ')
        if bool(self.get('EFLAGS')&0x400)!=bool(s.get('df')) or bool(self.get('EFLAGS')&0x200)!=bool(s.get('if',1)): raise ValueError('text IF/DF differs')
        endoffset=struct.unpack('<H',self.uc.mem_read(self.stack+0xffc4,2))[0]
        if terminal and endoffset!=spec.position: raise ValueError('text far pointer word increment differs')
        return dict(scenario=s,terminal=terminal,trace_events=len(self.trace),trace_sha256=sha(json.dumps(self.trace,separators=(',',':')).encode()),stores=sum(e[0]=='store' for e in self.trace),ports=sum(e[0] in ('in','out') for e in self.trace),conversions=sum(e[0]=='convert' for e in self.trace),calls=self.calls,string_offset=endoffset,visited=sorted(self.visited),es=self.get('ES'),fs=self.get('FS'),if_df=self.get('EFLAGS')&0x600,memory_before_sha256=sha(before),memory_after_sha256=sha(after))


def cases(mz,p):
    result=[(dict(string=[0]),True)]
    for byte in range(1,256): result.append((dict(string=[byte,0x40,0] if mz.program_image[p['ds']*16+p['mbctype']+byte]&4 else [byte,0],jis=0x2121),True))
    for df in (0,1):
        for weight in range(4):
            for left in range(8):
                for string in ([65,0],[0x81,0x40,0]): result.append((dict(df=df,fx=weight*0x10|15,left=left,string=string),True))
        for jis in (0,0x2920,0x2921,0x2b7e,0x2b7f,0x7fff,0xffff): result.append((dict(df=df,jis=jis,string=[0x81,0,90,0],offset=0xffff,left=1),True))
        for spacing in range(8):
            for left in (1,623): result.append((dict(df=df,fx=(spacing<<6)|0x30|5,string=[65,0x81,0x40,0xa1,9,90,0],left=left),True))
        for color in range(16): result.append((dict(df=df,fx=0xfff0|color,string=[65,0]),True))
        result.append((dict(df=df,left=-32768,unterminated=True),False))
    for left in (623,624,625,631,632,633,639,640,32767,-32768,-1,-7,-8,-9):
        for top in (-1,0,399,400,819,820,32767):
            for string in ([65,0],[0x81,0x40,0]): result.append((dict(left=left,top=top,string=string,fx=0x3f),True))
    for flags in [(0,0),(0,1),(1,0),(1,1)]:
        result.append((dict(if_=flags[0],df=flags[1],volatile=True,string=[0x81,0x40,0],fx=0x35),True))
        result[-1][0]['if']=result[-1][0].pop('if_')
    for segment in (0,p['ds']+0x2000,0xa800):
        for offset in (0,0xffff): result.append((dict(segment=segment,offset=offset,string=[0x81,0x40,0],left=1,fx=0x35),not (segment==0xa800 and offset==0xffff)))
    return result


def matrix(mz,p):
    rows=[TextProbe(mz,p).run(s,terminal) for s,terminal in cases(mz,p)]
    probe=TextProbe(mz,p)
    sequence=[dict(left=7,top=400,fx=0x3f,string=[65,0x81,0x40,0],df=1),dict(string=[0],df=0),dict(left=7,top=400,fx=0x3f,string=[65,0x81,0x40,0],df=1)]
    for index,s in enumerate(sequence):
        row=probe.run(s); row['persistent_sequence_index']=index; rows.append(row)
    return rows


def coverage(meta,rows):
    wanted={(b['name'],i) for b in meta['bodies'] for i in b['positions']}; seen={(name,i) for r in rows for name,i in r['visited']}
    if wanted!=seen: raise ValueError('text incomplete native coverage: '+str(sorted(wanted-seen)))
    return dict(positions=len(wanted),complete=True,invocations=len(rows),returns=sum(r['terminal'] for r in rows),prefixes=sum(not r['terminal'] for r in rows),trace_events=sum(r['trace_events'] for r in rows),stores=sum(r['stores'] for r in rows),ports=sum(r['ports'] for r in rows),conversions=sum(r['conversions'] for r in rows))


def semantic(rows):
    return [{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',required=True,type=Path); args=parser.parse_args()
    raw=(ROOT/PARENT).read_bytes()
    if sha(raw)!=PARENT_SHA: raise ValueError('text previous cold proof differs')
    parent=json.loads(raw); inputs={**parent['inputs'],PARENT:sha(raw)}
    paths=['scripts/review_th03_shared_text.py','scripts/review_th03_mainl_text.py',*HEADERS,
           '.analysis/sol-shared-input-op-ghidra-check-20261006.log','.analysis/sol-shared-text-mainl-ghidra-check-20261006.log']
    for path in paths: inputs[path]=sha((ROOT/path).read_bytes())
    def verify():
        for path,h in inputs.items():
            if sha((ROOT/path).read_bytes())!=h: raise ValueError('text prerequisite changed: '+path)
    verify(); providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    previous=json.loads((ROOT/'.analysis/sol-shared-cdg-draw-review-20261006.json').read_bytes()); observations={}
    for art,p in PROFILES.items():
        artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+art); stored=read_verified_artifact(ROOT,artifact)
        image_paths=[previous['observations'][art][0]['path']]+[f'.analysis/th03-shared-cdg-draw/sol-shared-cdg-draw-source-20261006/round{n}/source/bin/th03/{art}.exe' for n in (1,2)]
        observations[art]=[]; target=parse_mz((ROOT/image_paths[0]).read_bytes())
        for path in image_paths:
            inputs[path]=sha((ROOT/path).read_bytes()); mz=parse_mz((ROOT/path).read_bytes())
            if not mz.valid: raise ValueError('text invalid MZ')
            meta=analyze(mz.program_image,p); cpu=matrix(mz,p)
            tables={name:sha(mz.program_image[p['ds']*16+at:p['ds']*16+at+256]) for name,at in [('mbctype',p['mbctype']),('signed_graph',p['graph']-128)]}
            row=dict(path=path,analysis=meta,tables=tables,cpu=cpu,coverage=coverage(meta,cpu))
            if len(observations[art]):
                tree=Path(path).parents[2]; mp=tree/f'obj/th03/{art}.map'; op=tree/'obj/th03/grppsafx.obj'
                for consulted in (mp,op): inputs[str(consulted)]=sha((ROOT/consulted).read_bytes())
                linked=next(r for r in code_rows((ROOT/mp).read_text(),len(mz.program_image)) if r['module']=='th03/grppsafx.cpp' and r['size'])
                if (linked['segment'],linked['offset'],linked['size'])!=(p['cs'],p['start'],613): raise ValueError('text physical MAP carrier differs')
                row['comparison']=extent_observation(target,mz,linked)
                if not row['comparison']['raw_slice_equal'] or not row['comparison']['ordered_relocations_equal']: raise ValueError('text original raw/ordered relocations differ')
                for name,data in providers.items():
                    cp=tree/name; cached=(ROOT/cp).read_bytes(); inputs[str(cp)]=sha(cached)
                    if name.endswith(('.asm','.inc')): data=data.replace(b'\r\n',b'\n'); cached=cached.replace(b'\r\n',b'\n')
                    if cached!=data: raise ValueError('text actual frozen provider differs: '+name)
                first=observations[art][0]
                if meta!=first['analysis'] or tables!=first['tables'] or semantic(cpu)!=semantic(first['cpu']): raise ValueError('text independent artifact observations differ')
            observations[art].append(row)
        if read_verified_artifact(ROOT,artifact)!=stored: raise ValueError('text canonical target changed')
        print('PASS shared text',art,observations[art][0]['coverage'],flush=True)
    verify()
    report=dict(kind='th03-shared-text-complete-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__': main()
