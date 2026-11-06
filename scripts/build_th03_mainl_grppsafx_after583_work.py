#!/usr/bin/env python3
"""Two original first-use TC4J PC-98 CG-ROM text renderer build/link rounds."""
import build_th03_mainl_cdg_load_after582_work as parent
from lib.native_cpp_forward import NativeCPP

RUN=NativeCPP(parent,
    "config/mainl_work/grppsafx_after583.json",
    "scripts/build_th03_mainl_grppsafx_after583_work.py",
    "af583g",".analysis/work/mainl-grppsafx-after583-native-")

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
