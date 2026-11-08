#!/usr/bin/env python3
"""Review a fresh two-round native MAINL root-controller source probe."""
import argparse
import json
import re
import build_th03_mainl_root_controller_after580_work as build
from build_th03_mainl_resources_work import need
from review_th03_mainl_root_controller_after580_work import review

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', required=True)
stage = parser.parse_args().stage
if not re.fullmatch(r'af[0-9]+r', stage):
    parser.error('stage must be an afNNNr identifier')
build.STAGE = stage
build.PREFIX = f'.analysis/work/mainl-root-{stage}-native-'
build.REPORT = build.PREFIX + 'build.json'
build.SCRATCH = build.WORK / ('probe/' + stage)
build.DRIVER = 'scripts/build_th03_mainl_root_native_probe.py'

def current_sources(cfg):
    code = (build.ROOT / cfg['source']).read_bytes()
    wrapper = (build.ROOT / cfg['wrapper']).read_bytes()
    need(code and b'\r' not in code and wrapper and b'\r' not in wrapper and
         wrapper.endswith(b'#include "src/mainl/root/complete_data.cpp"\n') and
         wrapper.count(b'#include "src/mainl/root/complete_data.cpp"') == 1 and
         b'mainl_win_animate' in code and b'mainl_story_dispatch' in code and
         b'mainl_stage_intro' in code,
         'actual current root controller source and producer wrapper')
    return code, wrapper

build.sources = current_sources
result = review()
path = build.ROOT / (build.PREFIX + 'review.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, sort_keys=True))
