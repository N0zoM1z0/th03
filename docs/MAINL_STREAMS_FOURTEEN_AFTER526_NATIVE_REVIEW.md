# Fourteen complete float/BCD/manipulator/stream members — after526

Fourteen original Japanese CRT members now have complete maintained native
source, with **1,604 executable CODE bytes and 2 initialized DATA bytes**:

| Slot / member | Scope | CODE bytes | Logical fields |
| --- | --- | ---: | ---: |
| 196 / [bcd2](../src/mainl/crt/bcd2.asm) | BCD stream insertion/extraction | 151 | 12 |
| 785 / [istskoff](../src/mainl/crt/istskoff.asm) | istream seekg(offset, direction) | 108 | 1 |
| 786 / [istskpos](../src/mainl/crt/istskpos.asm) | istream seekg(position) | 105 | 1 |
| 789 / [mnrstflg](../src/mainl/crt/mnrstflg.asm) | resetiosflags factory/callback | 143 | 4 |
| 791 / [mnsetflg](../src/mainl/crt/mnsetflg.asm) | setiosflags factory/callback | 143 | 4 |
| 792 / [mnsetw](../src/mainl/crt/mnsetw.asm) | setw factory/callback | 139 | 3 |
| 793 / [mnsfill](../src/mainl/crt/mnsfill.asm) | setfill factory/callback | 140 | 3 |
| 794 / [mnsprec](../src/mainl/crt/mnsprec.asm) | setprecision factory/callback | 139 | 3 |
| 803 / [ostasn1](../src/mainl/crt/ostasn1.asm) | ostream_withassign from ostream | 44 | 1 |
| 804 / [ostfloat](../src/mainl/crt/ostfloat.asm) | long-double insertion/formatting | 165 | 8 |
| 805 / [ostasn2](../src/mainl/crt/ostasn2.asm) | ostream_withassign from streambuf | 36 | 1 |
| 817 / [ostosfx](../src/mainl/crt/ostosfx.asm) | conditional suffix flushing | 78 | 5 |
| 820 / [ostskoff](../src/mainl/crt/ostskoff.asm) | ostream seekp(offset, direction) | 108 | 1 |
| 821 / [ostskpos](../src/mainl/crt/ostskpos.asm) | ostream seekp(position) | 105 | 1 |

All original CODE/DATA bytes match without exclusions. `ostfloat` retains
its empty `_TEXTA` followed by `_DATA`, `_BSS`, and executable `_TEXT`; its
two DATA bytes are the typed `"+"` string. Every segment's name, class, size
and native ACBP alignment/combination attributes match original. Original
GROUP layout, fifteen named public entries and import order are checked.

The source preserves x87 80-bit values and status-word operations, original
f/e/g format selection, the real near REALCVT call, and ostream outstr.
BCD retains real conversion calls, its original 5000 argument, near N_SCOPY
copy and both Pascal `retf 8` exits. Manipulators keep the original six- or
eight-byte object layout with symbolic far callback addresses; setfill
retains CBW and its original word store. Assignment and suffix wrappers
retain real ios initialization and conditional this/cout/clog flushes.
Seeks use the original virtual seekoff/seekpos calls and get/put mode flags.
Unchecked original behavior and allocation/return ABI are preserved.

Proved offset-seek, position-seek, flag-manipulator and word-manipulator
families expand through four bounded includes, separately in each original
TU. There are no inline target instruction arrays, padding, missing-byte
allowances, object patches or MAP rewrites.

All **48 ordered logical OMF fields** match sites, widths, kinds, symbolic
targets and addends. Twelve members additionally match literal ordered
FIXUPPs. Two FP members have precisely enumerated metadata differences:

- `ostfloat`: five Borland x87 frame-4 / TASM frame-5 fields, plus its near
  REALCVT call at CODE+126, original TARGET frame versus TASM CODE segment 4.
- `bcd2`: seven x87 frame-4 / frame-5 fields, plus N_SCOPY at CODE+135,
  original TARGET frame versus TASM CODE segment 1.

The verifier restricts these **12 x87 and 2 near-call frame differences**
to their actual symbols, sites, segments and PC-relative properties. The
receipt retains both raw symbolic field descriptions for every difference.
Two extra native EMUL declarations have the same FPU symbol names as the
original declarations and are explicitly bounded. These comparison rules
never rewrite an OBJ. Literal FIXUPP equality for the FP members and raw
original OBJ program-record identity remain **false**.

The [after526 producer](../scripts/build_th03_mainl_after526_work.py) extends
the unchanged after525 source-bound pair. Both TASM/TLIB/TLINK rounds reproduce
the complete **67,372-byte Japanese MAINL EXE and original MAP**, including
all **677 literal ordered MZ relocations**. All earlier 752 source members,
127 remaining vendor members and the original 893-member order are preserved.

The [independent reviewer](../scripts/review_th03_mainl_after526_work.py)
checks fourteen TUs, four includes, parent/recipe hashes, actual writer logs,
all complete OBJ/LIB/EXE/MAP vectors, and independently enumerates the exact
fourteen metadata differences. All raw evidence and scratch are retained.
No full cold replay or redundant runtime/test matrix was performed.

Current working-source CRT: **766/893 complete members, 202,502 original-equal
CODE-segment bytes**. Formal Factory canonical packed-file acceptance remains
**0/250**; whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after526-streams-float-bcd-manip-seek-fourteen-build.json`

SHA-256: `903d4a1b6bfdde709ca3b95c270e57ecfc42de7c9451905f5b859b5e1e3d6dab`.
