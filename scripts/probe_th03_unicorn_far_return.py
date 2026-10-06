#!/usr/bin/env python3
"""Reproduce Unicorn's read-hook/RETF interaction on the attested OP POLAR body."""
import argparse
from importlib.metadata import version
import json
from pathlib import Path
import struct
from lib.pc98 import parse_mz
from review_th03_mainl_cutscene import sha

ROOT=Path(__file__).resolve().parents[1]
TARGET='.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe'
TARGET_SHA='efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'


def probe():
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ
    from unicorn import x86_const as reg
    raw=(ROOT/TARGET).read_bytes()
    if sha(raw)!=TARGET_SHA:raise ValueError('RETF probe decoded target differs')
    body=parse_mz(raw).program_image[0xbeb0+0x155:0xbeb0+0x16f];rows=[]
    for hooked in (False,True):
        u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000);u.mem_write(0x2c005,body)
        u.mem_write(0x4ffd0,struct.pack('<5H',0xff00,0x2990,32767,96,256))
        for n,v in [('CS',0x2beb),('SS',0x4000),('SP',0xffd0),('BP',0x7777)]:u.reg_write(getattr(reg,'UC_X86_REG_'+n),v)
        positions=[]
        def code(uc,address,size,user):
            positions.append(address)
            if len(positions)==10:uc.emu_stop()
        def read(*args):pass
        u.hook_add(UC_HOOK_CODE,code)
        # Even an empty callback restricted away from the stack reproduces it.
        if hooked:u.hook_add(UC_HOOK_MEM_READ,read,None,0x50000,0xeffff)
        u.emu_start(0x2c005,0x100000,count=12)
        rows.append(dict(read_hook=hooked,positions=positions,terminal=positions[-1]==0x39800,
                         registers={n:u.reg_read(getattr(reg,'UC_X86_REG_'+n)) for n in ('CS','SP','AX','BP')}))
    if not rows[0]['terminal'] or rows[0]['registers']!=dict(CS=0x2990,SP=0xffd4,AX=32863,BP=0x7777):raise ValueError('Unhooked original POLAR control failed')
    return dict(kind='unicorn-memory-read-hook-retf-control',unicorn=version('unicorn'),inputs={TARGET:sha(raw)},
                polar_sha256=sha(body),observations=rows,read_hook_changes_terminal=rows[0]['terminal']!=rows[1]['terminal'],
                notes='Compiler/runtime tool observation only. Music Room executes original far returns without read hooks; bulk load operands are traced at attested code boundaries. No emulated-return replacement or target modification.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=probe();a.output.write_text(json.dumps(r,indent=2)+'\n');print('RETF read-hook discrepancy:',r['read_hook_changes_terminal'])


if __name__=='__main__':main()
