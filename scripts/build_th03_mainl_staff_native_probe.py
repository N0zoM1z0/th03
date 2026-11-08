#!/usr/bin/env python3
"""Run a uniquely staged, two-round native MAINL staff source probe."""
import argparse
import re
import build_th03_mainl_staff_after575_work as build

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', required=True, help='fresh DOS-safe afNNNs stage')
stage = parser.parse_args().stage
if not re.fullmatch(r'af[0-9]+s', stage):
    parser.error('stage must be a unique afNNNs identifier')
build.STAGE = stage
build.PREFIX = f'.analysis/work/mainl-staff-{stage}-native-'
build.REPORT = build.PREFIX + 'build.json'
build.SCRATCH = build.WORK / ('probe/' + stage)
build.DRIVER = 'scripts/build_th03_mainl_staff_native_probe.py'
build.main()
