#!/usr/bin/env python3
"""Stage only original OP scanner source and forwarding slots. No native execution."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OWNER='src/op/hardware/input_sense.cpp'
INPUT_HASHES={'compat/rec98/libs/master.lib/master.hpp': '8e279919734d76e7b9b4012255fa19b969733338a69d4aed32d6f2cdc081a7a1', 'compat/rec98/platform/x86real/flags.hpp': '410756ddb266e8a4a51767fffcf9724c5b6967c02901481a26335da0c20dfba2', 'compat/rec98/platform/x86real/pc98/keyboard.hpp': 'dcb649e854e438a69679f79381e0af5da78f2ffb242a724bd6daced0b08e281b', 'compat/rec98/th03/hardware/input.h': '84b0ca85929d0de82bc4ada8503fb226806f87869d473c4c865bf81509c1b18e', 'src/op/hardware/input_sense.cpp': '852cbd97be885063d93aa37135429b6b62fcf771658724fa608e8d61ac84521e'}
INPUTS=tuple(INPUT_HASHES)
ORIGINAL_PROVIDER_SHA='6ae7cf8c133164d4572186f1623888f9843b7bb709b9167ecd46c1e2215a1467'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read_inputs(root):
 result={}
 for n,digest in INPUT_HASHES.items():
  p=Path(root)/n;need(not any(x.is_symlink() for x in (p,*p.parents)),'symlink input');raw=p.read_bytes();need(sha(raw)==digest,'reviewed source differs '+n);result[n]=raw
 source=result[OWNER];body=source[source.index(b'#pragma option'):].replace(b'compat/rec98/',b'')
 need(sha(body)==ORIGINAL_PROVIDER_SHA,'literal original source provenance')
 need(source.endswith(b'#pragma codestring "\\x90"\n') and source.count(b'#pragma codestring')==1,'original trailing NOP context')
 return result
def payload(root):
 result=read_inputs(root);result['th03/input_s.cpp']=b'#include "th03/hardware/input_s.cpp"\n';result['th03/hardware/input_s.cpp']=b'#include "src/op/hardware/input_sense.cpp"\n';return result
def stage(root,output):
 data=payload(root);output=Path(output);need(not any(x.is_symlink() for x in (output,*output.parents)),'symlink output');need(not output.exists(),'fresh output required');output.mkdir()
 for n,raw in data.items():
  p=output/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 report=dict(schema='th03-op-keyboard-source-overlay-v1',files={n:dict(sha256=sha(raw),bytes=len(raw)) for n,raw in data.items()},scanner_bytes=417,carrier_context_bytes=418,nop_source_credit=0,compiler_invocations=0,source_acceptance=False,exact_acceptance=False)
 (output/'source_inventory.json').write_text(json.dumps(report,indent=2)+'\n');return report
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(stage(a.root,a.output),indent=2))
if __name__=='__main__':main()
