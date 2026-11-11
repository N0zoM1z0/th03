#!/usr/bin/env python3
"""Compare selection, curve raster and story opponents with original OP code."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tomllib


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks',type=Path,required=True)
    parser.add_argument('--dos-root',type=Path,required=True)
    args=parser.parse_args()
    root=args.dos_root.resolve()
    sys.path.insert(0,str(root/'scripts'))
    from lib.pc98 import parse_mz
    from review_th03_op_select import SelectProbe,scenario
    from lib.op_story_runtime import Machine
    raw=(root/'.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/op.exe').read_bytes()
    config=tomllib.loads((root/'config/th03_diet.toml').read_text())
    expected=next(row['decoded_sha256'] for row in config['artifacts'] if row['id']=='th03-op')
    if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('original OP identity changed')
    mz=parse_mz(raw)
    executable=str(args.native_checks.resolve())
    vectors=[]
    for pid,mask,available,selected,confirmed,locked,paletted in [
        (0,1,7,[0,0],[0,0],[0,0],[1,1]),
        (0,2,9,[8,0],[0,0],[0,0],[1,1]),
        (0,3,7,[0,0],[0,0],[0,0],[1,1]),
        (0,32,7,[2,0],[0,0],[1,0],[1,1]),
        (0,0,7,[2,0],[0,0],[1,0],[1,1]),
        (0,32,7,[0,0],[0,1],[0,0],[1,1]),
        (1,16,7,[0,0],[1,0],[0,0],[2,1]),
        (0,48,7,[0,0],[0,1],[0,0],[1,2]),
        (1,32,7,[0,0],[1,0],[0,0],[1,1]),
        (0,32,9,[8,0],[0,0],[0,0],[1,1]),
        (0,32,7,[0,0],[1,0],[0,0],[1,1]),
    ]:
        s=scenario(sel=selected,confirmed=confirmed,locked=locked,paletted=paletted,available=available,fade=123)
        native=SelectProbe(mz,s);native.run('update',[pid,mask])
        dg=lambda at:int.from_bytes(native.uc.mem_read(native.data+at,1),'little')
        resident=0x60031
        result=[dg(0x2468),dg(0x2469),dg(0x246a),dg(0x246b),dg(0xa59),dg(0xa5a),
                *native.uc.mem_read(resident+12,2),int.from_bytes(native.uc.mem_read(native.data+0x2472,2),'little')]
        vectors.append(([pid,mask,available,*selected,*confirmed,*locked,*paletted,123],result))
    supplied=''.join(' '.join(map(str,row))+'\n' for row,_ in vectors)
    actual=subprocess.check_output([executable,'--selection'],input=supplied,text=True).splitlines()
    if len(actual)!=len(vectors):raise ValueError('selection result count differs')
    for line,(row,expected) in zip(actual,vectors):
        if list(map(int,line.split()))!=expected:raise ValueError(f'selection state differs: {row}: {line} != {expected}')
    for cycle,trails in [(0,8),(2,7),(128,7),(254,1)]:
        native=SelectProbe(mz,scenario(cycle=cycle,trail=trails));native.run('curves')
        pixels=bytearray(640*400);color=0
        for event in native.events:
            if event['name']=='grcg-color':color=event['args'][0]
            if event['name']=='pset':
                y,x=event['args'];x=x-65536 if x&32768 else x;y=y-65536 if y&32768 else y
                if 0<=x<640 and 0<=y<400:pixels[y*640+x]=color
        actual=subprocess.check_output([executable,'--curves',str(cycle),str(trails)])
        if actual!=pixels:raise ValueError(f'original curve raster differs: cycle={cycle},trails={trails}')
    for seed,paletted,rank in [(0,1,0),(1,5,1),(0x12345678,6,2),(0xffffffff,15,3),(500,18,0)]:
        native=Machine(mz,0x2000)
        native.run(selected_char=paletted,random_seed=seed,rank=rank)
        expected=list(native.uc.mem_read(native.resbase+0x29,9))
        expected+=[int.from_bytes(native.uc.mem_read(native.resbase+0x10,4),'little'),native.uc.mem_read(native.resbase+0x38,1)[0]]
        actual=list(map(int,subprocess.check_output([executable,'--opponents',str(seed),str(paletted),str(rank)],text=True).split()))
        if actual!=expected:raise ValueError(f'original story opponent/seed state differs: {seed,paletted,rank}')
    print('Original OP agrees: selection release/palette state, complete curve rasters and story opponent/seed handoff.')


if __name__=='__main__':main()
