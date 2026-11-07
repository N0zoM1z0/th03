#!/usr/bin/env python3
"""Two exact native TC4 compilations of large original MAIN round loop."""
import build_th03_main_core_after593_work as parent
from lib.native_main_cpp_layer import NativeMainCPP

RUN=NativeMainCPP(parent,
    "config/main_work/entry_after594.json",
    "scripts/build_th03_main_entry_after594_work.py",
    "af594e",".analysis/work/main-entry-after594-native-")
ROOT,WORK,REPORT,STAGE,SCRATCH=RUN.ROOT,RUN.WORK,RUN.REPORT,RUN.STAGE,RUN.SCRATCH

def response(n):
    c,_,_=RUN.inputs()
    return RUN.response(c,n)

def read_pin(pin):
    return RUN.read_pin(pin)

if __name__=="__main__":
    RUN.run()
