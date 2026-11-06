#!/usr/bin/env python3
"""Read-only source-native whole-EXE review of original 613-byte text renderer."""
import json
from build_th03_mainl_grppsafx_after583_work import RUN

if __name__=="__main__":
    result=RUN.review()
    (RUN.ROOT/(RUN.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Natural CG-ROM text source 613 CODE / 1 complete function / 6 original fixups, 2 whole Japanese MAINL EXEs exact.")
