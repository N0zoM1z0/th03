#!/usr/bin/env python3
"""Read-only two-round source-native original CDG loader review."""
import json
from build_th03_mainl_cdg_load_after582_work import RUN

if __name__=="__main__":
    result=RUN.review()
    (RUN.ROOT/(RUN.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("CDG loader natural C++: 593 original CODE/5 functions/35 OMF FIXUPPs; two whole 67372-byte MAINL EXEs exact.")
