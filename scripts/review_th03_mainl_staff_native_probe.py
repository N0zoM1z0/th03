#!/usr/bin/env python3
"""Review a uniquely staged, complete native MAINL staff source probe."""
import argparse
import json
import re
import build_th03_mainl_staff_after575_work as build
from review_th03_mainl_staff_after575_work import review

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', required=True)
stage = parser.parse_args().stage
if not re.fullmatch(r'af[0-9]+s', stage):
    parser.error('stage must be an afNNNs identifier')
build.STAGE = stage
build.PREFIX = f'.analysis/work/mainl-staff-{stage}-native-'
build.REPORT = build.PREFIX + 'build.json'
build.SCRATCH = build.WORK / ('probe/' + stage)
build.DRIVER = 'scripts/build_th03_mainl_staff_native_probe.py'
result = review()
path = build.ROOT / (build.PREFIX + 'review.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, sort_keys=True))
