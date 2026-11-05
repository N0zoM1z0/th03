#!/usr/bin/env python3
"""Read-only Intel OMF FIXUPP decoding for large original Borland CRT members.

Unlike the historical MAINL literal_fields() helper, this parser accepts
original OMF frame method 4 (frame of the fixup location) as well as
methods 0/1/5. It does not rewrite or normalize any original record,
construct an object, build a target, or relax source acceptance criteria.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from lib.borland_library import library_members
from lib.omf import parse_omf
from build_th03_mainl_display_work import payload
from lib.decoded_mainl_display_native import externs
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics


def original_literal_fixups(raw: bytes) -> list[dict]:
    fields = []
    active = None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            assert len(record.data) >= 3, 'truncated original 16-bit LEDATA'
            segment = record.data[0]
            offset = int.from_bytes(record.data[1:3], 'little')
            active = (segment, offset, record.data[3:])
        if record.name != 'FIXUPP':
            continue
        data = record.data
        cursor = 0

        def omf_index() -> int:
            nonlocal cursor
            assert cursor < len(data), 'missing OMF FIXUPP index'
            result = data[cursor]
            cursor += 1
            if result & 0x80:
                assert cursor < len(data), 'truncated OMF two-byte index'
                result = ((result & 0x7F) << 8) | data[cursor]
                cursor += 1
            return result

        while cursor < len(data):
            assert cursor + 3 <= len(data), 'truncated original FIXUPP field'
            loc, low, method = data[cursor:cursor+3]
            cursor += 3
            fm, tm = (method >> 4) & 7, method & 3
            assert loc & 0x80, 'not an explicit original location record'
            assert method & 0x8C == 4, 'unsupported original OMF method flags'
            assert fm in (0, 1, 4, 5), 'unsupported original OMF frame mode'
            assert tm in (0, 1, 2), 'unsupported original target mode'
            frame = omf_index() if fm in (0, 1) else None
            target = omf_index()
            offset = ((loc & 3) << 8) | low
            kind = (loc >> 2) & 15
            assert kind in (1, 2, 3), 'unsupported original 16-bit location type'
            width = {1:2, 2:2, 3:4}[kind]
            assert active is not None and offset+width <= len(active[2]), (
                'FIXUPP outside preceding LEDATA',offset,width)
            fields.append(dict(
                segment=active[0],site=active[1]+offset,location_type=kind,
                width=width,segment_relative=bool(loc & 0x40),
                frame_method=fm,frame=frame,
                target_method=tm,target=target,
                addend=int.from_bytes(active[2][offset:offset+width],'little')))
    return fields


def original_member(members, name):
    choices = [m for m in members if m.name == name]
    if len(choices) != 1:
        raise ValueError('ambiguous or absent ORIGINAL member: '+name)
    return b'\x80\x02\x00\x00\x7e' + choices[0].program_records


def inspect(name, raw):
    refs = original_literal_fixups(raw)
    p=payload(raw)
    data_size=next((s['size'] for s in segment_definitions(raw) if
                    s['name']=='_DATA' and s['class']=='DATA'),0)
    data_implicit=sorted(set(range(data_size))-
                         {i for seg,i in p if seg==2})
    return dict(member=name, original_segments=[
        (s['name'],s['class'],s['size']) for s in segment_definitions(raw)],
        original_code_publics=code_publics(raw,1),
        original_imports=externs(raw),
        fixup_count=len(refs),
        original_DATA_implicit_sites=data_implicit,
        frame_methods=dict(sorted(Counter(f['frame_method'] for f in refs).items())),
        fixup_segments=dict(sorted(Counter(f['segment'] for f in refs).items())),
        original_location_frames=[
            f for f in refs if f['frame_method']==4],
        original_initdata_fixups=[
            f for f in refs if f['segment']==4])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('members',nargs='+',help='exact original Japanese CL.LIB member names')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    vendor=root/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB'
    originals=library_members(vendor.read_bytes())
    for name in args.members:
        r=inspect(name,original_member(originals,name))
        r['original_location_frames_count']=len(r.pop('original_location_frames'))
        print(json.dumps(r,ensure_ascii=False,sort_keys=True))


if __name__=='__main__':
    main()
