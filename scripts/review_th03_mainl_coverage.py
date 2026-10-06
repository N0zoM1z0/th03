#!/usr/bin/env python3
"""Compare MAINL decoded unit intervals with independently pinned MAP carriers."""
import argparse
import csv
from datetime import datetime,timezone
import json
from pathlib import Path
from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows
from review_th03_mainl_cutscene import sha

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-graphics-review-20261006.json'
PROOF_SHA='3b6525b43cf3f75885987ba9c190d0cf70bb2329e42d7fe7808c999c47773bd1'


def coverage(units,carriers,image_size):
    intervals=[]
    for row in units:
        if row['artifact']!='th03-mainl' or not row['segment'].startswith('decoded:'):continue
        if row['boundary_state']!='reviewed' or row['state']!='boundary-reviewed':continue
        segment=int(row['segment'].split(':',1)[1],16);offset=int(row['offset'],0);size=int(row['size'],0);start=segment*16+offset
        if not 0<=segment<=65535 or offset<0 or offset>65535 or size<0 or start+size>image_size:raise ValueError('decoded unit exceeds image/offset bounds')
        intervals.append((row['id'],start,start+size))
    result=[]
    for row in carriers:
        start=row['start'];size=row['size'];end=start+size
        if size<=0:continue
        if start<0 or end>image_size:raise ValueError('MAP carrier exceeds image bounds')
        counts=[0]*size;intersections=[]
        for name,left,right in intervals:
            a=max(start,left);b=min(end,right)
            if a>=b:continue
            intersections.append(dict(unit=name,start=a,size=b-a))
            for i in range(a-start,b-start):counts[i]+=1
        gaps=[];i=0
        while i<size:
            if counts[i]:i+=1;continue
            a=i
            while i<size and not counts[i]:i+=1
            gaps.append(dict(start=start+a,size=i-a))
        result.append(dict(carrier=row,independent_unit_bytes=sum(bool(n) for n in counts),overlapping_unit_bytes=sum(n>1 for n in counts),independent_unit_gaps=gaps,unit_intersections=intersections))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('coverage graphics proof differs')
    proof=json.loads(raw);imagepath=proof['observations'][0]['path'];mappath=str(Path(proof['observations'][1]['path']).parents[2]/'obj/th03/mainl.map')
    inputs={PROOF:sha(raw),'scripts/review_th03_mainl_coverage.py':sha(Path(__file__).read_bytes()),'tests/test_mainl_coverage_review.py':sha((ROOT/'tests/test_mainl_coverage_review.py').read_bytes())}
    for p in (imagepath,mappath):
        inputs[p]=sha((ROOT/p).read_bytes())
        if inputs[p]!=proof['inputs'][p]:raise ValueError('coverage pinned image/MAP differs')
    units_raw=(ROOT/'config/units.csv').read_bytes();inputs['config/units.csv']=sha(units_raw)
    mz=parse_mz((ROOT/imagepath).read_bytes())
    if not mz.valid:raise ValueError('coverage invalid decoded MZ')
    rows=list(csv.DictReader(units_raw.decode().splitlines()));carriers=code_rows((ROOT/mappath).read_text(),len(mz.program_image))
    observations=coverage(rows,carriers,len(mz.program_image))
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('coverage input changed: '+p)
    result=dict(kind='decoded-mainl-independent-unit-coverage',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,source_acceptance=False,exact_acceptance=False,notes='Union of reviewed decoded unit intervals only. Gaps can contain already reviewed native context and producer alignment; this is not a count of unknown semantics. CRT/root/DATA/BSS/device/packaging and complete Oracle ownership remain separate.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    root=next(o for o in observations if o['carrier']['module']=='th03_mainl.asm' and o['carrier']['segment']==0)
    print('PASS',len(observations),'nonzero MAP carriers; root covered',root['independent_unit_bytes'],'gaps',sum(g['size'] for g in root['independent_unit_gaps']),'overlap',root['overlapping_unit_bytes'])


if __name__=='__main__':main()
