#!/usr/bin/env python3
"""Review a uniquely staged, complete native MAINL staff source probe."""
import argparse
import json
import re
import build_th03_mainl_staff_after575_work as build
from review_th03_mainl_staff_after575_work import review

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--check', action='store_true', help='verify without writing a review report')
    args = parser.parse_args()
    if not re.fullmatch(r'af[0-9]+s', args.stage):
        parser.error('stage must be an afNNNs identifier')
    build.STAGE = args.stage
    build.PREFIX = f'.analysis/work/mainl-staff-{args.stage}-native-'
    build.REPORT = build.PREFIX + 'build.json'
    build.SCRATCH = build.WORK / ('probe/' + args.stage)
    build.DRIVER = 'scripts/build_th03_mainl_staff_native_probe.py'
    result = review()
    if not args.check:
        path = build.ROOT / (build.PREFIX + 'review.json')
        path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
