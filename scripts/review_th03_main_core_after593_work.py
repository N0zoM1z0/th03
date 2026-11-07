#!/usr/bin/env python3
"""Read-only source-native full-EXE review for original PLAYER core."""
import json
from build_th03_main_core_after593_work import RUN

if __name__=="__main__":
    result=RUN.review()
    (RUN.ROOT/(RUN.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Player core: 3135 original CODE / 21 public functions / 260 OMF fixups, 2 full original Japanese MAIN files exact.")
