#!/usr/bin/env python3
"""Original 16-bit player movement/shot/hit/stuff: two TC4/TLINK rounds."""
import build_th03_main_character_after592_work as parent
from lib.native_main_cpp_layer import NativeMainCPP

RUN=NativeMainCPP(parent,
    "config/main_work/core_after593.json",
    "scripts/build_th03_main_core_after593_work.py",
    "af593p",".analysis/work/main-core-after593-native-")
ROOT,WORK,REPORT,STAGE,SCRATCH=RUN.ROOT,RUN.WORK,RUN.REPORT,RUN.STAGE,RUN.SCRATCH

def response(n):
    c,_,_=RUN.inputs()
    return RUN.response(c,n)

def read_pin(pin):
    return RUN.read_pin(pin)

if __name__=="__main__":
    RUN.run()
