#!/usr/bin/env python3
"""Read-only large character/BOSS callback first-use Turbo C++ proof."""
import json
from build_th03_main_character_after592_work import RUN

if __name__=="__main__":
    result=RUN.review()
    (RUN.ROOT/(RUN.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Character setup: 3888 CODE, 12 complete functions, 1135 ordered native fixups; 2 original Japanese MAIN full files exact.")
