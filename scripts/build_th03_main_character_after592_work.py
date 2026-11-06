#!/usr/bin/env python3
"""Two source-native 16-bit C++ character-resource/BOSS-callback rounds."""
import build_th03_main_collision_after591_work as parent
from lib.native_main_cpp_layer import NativeMainCPP

RUN=NativeMainCPP(
    parent,"config/main_work/character_setup_after592.json",
    "scripts/build_th03_main_character_after592_work.py",
    "af592p",".analysis/work/main-character-after592-native-")
ROOT,WORK,REPORT,STAGE,SCRATCH=RUN.ROOT,RUN.WORK,RUN.REPORT,RUN.STAGE,RUN.SCRATCH

def response(n):
    c,_,_=RUN.inputs()
    return RUN.response(c,n)

def read_pin(pin):
    return RUN.read_pin(pin)

if __name__=="__main__":
    RUN.run()
