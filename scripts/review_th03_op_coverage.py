#!/usr/bin/env python3
"""Measure original OP decoded units against cold MAP coordinates, without acceptance."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows
from review_th03_mainl_cutscene import sha

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-op-configuration-review-20261006.json'
PROOF_SHA='ecb383f145486d9b978408c09e40b540c37f2aff6c335a3952cd28fec2ce3fe1'


def coverage(units,carriers,image_size):
    intervals=[]
    for row in units:
        if row['artifact']!='th03-op' or not row['segment'].startswith('decoded:'):continue
        if row['boundary_state']!='reviewed' or row['state'] not in ('boundary-reviewed','source-present'):continue
        segment=int(row['segment'].split(':',1)[1],16);offset=int(row['offset'],0);size=int(row['size'],0)
        start=segment*16+offset
        if not 0<=segment<=65535 or not 0<=offset<=65535 or size<0 or start+size>image_size:raise ValueError('OP decoded unit exceeds bounds')
        intervals.append((row['id'],start,start+size))
    result=[]
    for carrier in carriers:
        start=carrier['start'];size=carrier['size'];end=start+size
        if not size:continue
        if start<0 or size<0 or end>image_size:raise ValueError('OP MAP carrier exceeds bounds')
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
        result.append(dict(carrier=carrier,independent_unit_bytes=sum(bool(n) for n in counts),
                           overlapping_unit_bytes=sum(n>1 for n in counts),independent_unit_gaps=gaps,unit_intersections=intersections))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP coverage proof differs')
    proof=json.loads(raw);ip=proof['observations'][0]['path'];mp=str(Path(proof['observations'][1]['path']).parents[2]/'obj/th03/op.map')
    inputs={PROOF:sha(raw)}
    for p in (ip,mp,'config/units.csv','scripts/review_th03_op_coverage.py','tests/test_op_coverage_review.py','scripts/review_th03_decoded_code.py','scripts/lib/pc98.py','scripts/review_th03_mainl_cutscene.py'):
        inputs[p]=sha((ROOT/p).read_bytes())
    if any(inputs[p]!=proof['inputs'][p] for p in (ip,mp)):raise ValueError('OP coverage original image/MAP differs')
    mz=parse_mz((ROOT/ip).read_bytes())
    if not mz.valid:raise ValueError('OP coverage invalid MZ')
    units=list(csv.DictReader((ROOT/'config/units.csv').read_text().splitlines()))
    observed=coverage(units,code_rows((ROOT/mp).read_text(),len(mz.program_image)),len(mz.program_image))
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP coverage input changed: '+p)
    result=dict(kind='decoded-op-original-interval-vs-cold-map-coverage',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observed,
                source_acceptance=False,exact_acceptance=False,
                notes='Original target intervals versus compiler MAP coordinates only. Shifted init leaves a cold carrier leading gap and intersects the next cold carrier by one byte; this does not establish target carrier/source ownership. Native compiler/helper context is not independent unit credit. DATA/BSS/devices/canonical storage and complete product/Oracle ownership remain open.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS OP interval comparison:',len(observed),'nonzero CODE carriers;',sum(o['independent_unit_bytes'] for o in observed),'covered;',sum(o['overlapping_unit_bytes'] for o in observed),'overlap')


if __name__=='__main__':main()
