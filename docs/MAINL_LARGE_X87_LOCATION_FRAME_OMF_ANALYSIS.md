# Large original x87 bosses: location-frame OMF recovery

This investigation unblocks original **relocation inventory analysis** for
the previously unresolved large Japanese Borland CL.LIB members
isteldbl (index 765) and cplx2 (index 209). It is not a source
reconstruction claim for either function and grants no source credit.

The historical scripts/build_th03_mainl_display_work.py
literal_fields() helper intentionally accepts only OMF FIXUPP
frame methods 0, 1, and 5. It raises a parse exception when it
encounters original frame **method 4 (frame of the fixup location)**.
Both large members use this method extensively; the failure was
in the bounded old parser rather than in the original OMF records.

A new independent, read-only parser at
[scripts/probe_th03_mainl_large_fixups.py](../scripts/probe_th03_mainl_large_fixups.py)
now accepts 16-bit explicit unthreaded FIXUPP frame methods 0,1,4,5.
It preserves the **literal frame method**, original segment/site,
location width, target method/index and addend without replacing
method 4 with method 5. It does not modify the inherited small-member
scope rules, original objects, native build products or acceptance
ledger. Targeted tests prove backward exactness on original
bcd1, cplx1, dostimu and _pathops, whose frame methods were
already supported historically.

| Original CL.LIB member | Original CODE | Original DATA/INITDATA | All original FIXUPPs | Method 4 | Method 5 | Method 1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| isteldbl (765) | 1,947 | 14 / 0 | **112** | **85** | 11 | 16 |
| cplx2 (209) | 5,598 | 63 / 6 | **860** | **734** | 88 | 38 |

isteldbl exports the one complete far
istream extraction operator for an extended long double and imports
12 original symbols, including FIDRQQ, FIERQQ, FIWRQQ, the
original exception/float globals and the true 32-bit multiply helper.
All 112 original relocations affect CODE segment 1.

cplx2 exports **22 complete complex math/iostream procedures**
and imports 24 symbols including original trig/log/pow functions,
FPU emulation names and __turboFloat. Its 859 CODE fixups and one
_INIT_ fixup are now separately readable. The original
INITDATA segment is six bytes, with its original symbolic
relocation at INITDATA+2 -> CODE+5575.
Importantly, while _DATA SEGDEF size is **63**, the original Borland
LEDATA materializes only **47** bytes at DATA+16..62.
DATA+0..15 is an **implicit zero / unmaterialized region**.
Treating all 63 bytes as materialized DATA would have misreported
both original provenance and raw OMF equality. The new parser
reports the exact 16 missing byte sites without filling or patching
the original records.

These counts and all parsed location frames are directly checked
by tests/test_mainl_large_x87_location_frames.py, not copied
from a historical handoff. They are **original-member OMF observations**;
no TASM source has yet been demonstrated to reproduce the complete
location-framed FPU fields of these two large members. In particular,
the TASM EMUL work on bcd1 and cplx1 naturally produced their
original target-frame method 5 but does not, by itself, prove
method-4 equivalence in these larger modules. The next step is to
recover complete natural source and original location-frame
semantics, then run narrowly scoped native build/review. Do not
normalize all 734/85 original method-4 fields away or count these
members as maintained-source linked.

Focused reproduction (no cold replay):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_large_fixups.py isteldbl cplx2
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_large_x87_location_frames -v
