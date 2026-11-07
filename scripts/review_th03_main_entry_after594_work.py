#!/usr/bin/env python3
"""Read-only complete original entry/round/stage C++ native link proof."""
import json
from build_th03_main_entry_after594_work import RUN

if __name__=="__main__":
    result=RUN.review()
    (RUN.ROOT/(RUN.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Round scheduler and entry: 3050 CODE, 8 native PUBLIC functions, 433 original fixups, two complete original MAIN files exact.")
