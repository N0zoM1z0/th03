#!/usr/bin/env python3
"""Run a fresh two-round native MAINL root-controller source probe."""
import argparse
import re
import build_th03_mainl_root_controller_after580_work as build
from build_th03_mainl_resources_work import need

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', required=True, help='fresh DOS-safe afNNNr stage')
stage = parser.parse_args().stage
if not re.fullmatch(r'af[0-9]+r', stage):
    parser.error('stage must be a unique afNNNr identifier')
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
build.main()
