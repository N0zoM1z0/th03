#!/usr/bin/env python3
"""Supplement frozen PI review with successful post-wrap borrowing and failed reads."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import review_th03_mainl_pi_decoder as pi

PROOF = '.analysis/sol-mainl-pi-decoder-review-20261006.json'
PROOF_SHA = 'b8df97fa69813085abf90a7d08fba4c0640614bf37b0c0449b64abda3192c584'


def require_success(p, ax, carry, required):
    """A allocation/error return cannot stand in for an intended decoder path."""
    if (ax, carry, p.get('AX'), p.get('EFLAGS') & 1) != (0, 0, 0, 0):
        raise ValueError('PI supplement requires successful decoder return')
    if not set(required) <= p.visited:
        raise ValueError('PI supplement required native branch was not executed')


def matrix(mz):
    rows, meta = [], pi.analyze(mz.program_image)
    scenarios = []
    for position in range(5):
        first = 1 if position == 2 else 2
        scenarios.append(('post-wrap-reference-borrow', dict(width=60000, height=2, heap=0x9000, out=0x9000,
                          bits='1011'+pi.copy_bits(first,5536)+pi.copy_bits(position,60000)),
                          [0x1459] if position == 0 else [0x13e1]))
    for ax in (0,65535):
        scenarios.append(('refill-failure-supplied-bytes', dict(comment=[65]*16384,
                          reads=[{},dict(cf=1,ax=ax,inject_on_failure=True)]),[0x161a]))
    for label,scenario,required in scenarios:
        p = pi.DecoderProbe(mz,scenario,meta)
        model = pi.Scalar(p)
        before = pi.sha(bytes(model.mem))
        ax, carry = model.run('load',pi.LOAD_ARGS)
        p.run('load',pi.LOAD_ARGS)
        pi.compare(p,model,ax,carry,label)
        require_success(p,ax,carry,required)
        rows.append(dict(label=label,scenario=scenario,required_instructions=required,top_level_calls=1,
                         ax=ax,cf=carry,visited=sorted(p.visited),native_entries=dict(p.native),events=p.events,
                         decode_steps=model.decode_steps,store_count=len(p.writes),stores_sha256=pi.trace_hash(p.writes),
                         memory_before_sha256=before,memory_after_sha256=pi.sha(bytes(model.mem))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    raw=(pi.ROOT/PROOF).read_bytes()
    if pi.sha(raw)!=PROOF_SHA:
        raise ValueError('PI supplement parent receipt differs')
    proof=json.loads(raw)
    inputs={**proof['inputs'],PROOF:pi.sha(raw),'scripts/review_th03_mainl_pi_decoder_borrow.py':pi.sha(Path(__file__).read_bytes()),
            'tests/test_mainl_pi_decoder_borrow_review.py':pi.sha((pi.ROOT/'tests/test_mainl_pi_decoder_borrow_review.py').read_bytes())}
    def verify():
        for path,digest in inputs.items():
            if pi.sha((pi.ROOT/path).read_bytes())!=digest:
                raise ValueError('PI supplement input changed: '+path)
    verify()
    observations=[]
    for prior in proof['observations']:
        mz=pi.parse_mz((pi.ROOT/prior['path']).read_bytes())
        if not mz.valid or json.loads(json.dumps(pi.analyze(mz.program_image)))!=prior['analysis']:
            raise ValueError('PI supplement image partition differs')
        cpu=matrix(mz)
        if observations:
            normalized=lambda rows:[{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]
            if normalized(cpu)!=normalized(observations[0]['cpu']):
                raise ValueError('PI supplement target/cold CPU differs')
        visited={a for r in prior['cpu']+prior['nonterminal']+cpu for a in r['visited']}
        own={a for a in prior['analysis']['bounds'] if 0xfec<=a<0x162c}
        coverage=dict(new_instructions=len(own),visited=len(own&visited),unvisited=sorted(own-visited))
        observations.append(dict(path=prior['path'],cpu=cpu,combined_instruction_coverage=coverage))
        print('Reviewed supplement',prior['path'],len(cpu),'successful calls',coverage,flush=True)
    verify()
    result=dict(kind='th03-mainl-pi-decoder-successful-borrow-refill-supplement',observed_utc=datetime.now(timezone.utc).isoformat(),
                inputs=inputs,parent=PROOF,parent_sha256=PROOF_SHA,observations=observations,diagnostic_checks_pass=True,
                new_build=False,new_owned_bytes=0,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS successful PI borrow/refill supplement:',args.output)


if __name__=='__main__':
    main()
