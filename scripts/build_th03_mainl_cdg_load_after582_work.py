#!/usr/bin/env python3
"""Two real first-use native Turbo CPP CDG loader compiles, whole MAINL links."""
import build_th03_mainl_root_controller_after580_work as parent
from lib.native_cpp_forward import NativeCPP

RUN=NativeCPP(parent,
    "config/mainl_work/cdg_load_after582.json",
    "scripts/build_th03_mainl_cdg_load_after582_work.py",
    "af582l",".analysis/work/mainl-cdg-load-after582-native-")

ROOT=RUN.ROOT
WORK=RUN.WORK
base=RUN.base
REPORT=RUN.REPORT
STAGE=RUN.STAGE
SCRATCH=RUN.SCRATCH

def response(n):
    c,_,_=RUN.inputs()
    return RUN.response(c,n)

if __name__=="__main__":
    RUN.run()
