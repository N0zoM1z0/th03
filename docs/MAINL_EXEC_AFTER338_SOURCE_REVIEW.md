# Original 933-byte DOS overlay exec: source-bound literal OMF proof

**Original-input correction at after537:** the historical comparison below
used the 28-source carrier (`64b0a5…`), not the installed compiler CL.LIB
(`7d53ed…`). The real member initializes CODE+0..254 through LIDATA and uses
TARGET frame5 at +371,+397,+482,+560. The below uninitialized-storage and
original-program-identity claims are superseded by the
[shared exec / two-product proof](SHARED_EXEC_OP_RUNTIME_AFTER537_NATIVE_REVIEW.md).
All historical receipts and raw outputs remain intact. The current owner is
`src/shared/crt/dos_exec.asm`; the old TU remains a frozen ancestor input.

## Historical after338 report; original-input claims superseded above

The tracked `src/mainl/crt/exec.asm` is revalidated against the **actual
Japanese original CL.LIB member 345**, not accepted just because an
[older reconstruction note](MAINL_EXEC_NATIVE_REVIEW.md) exists. The
complete original **933-byte `_TEXT` CODE segment** is recovered as native
16-bit Borland source, including both work fields and executable instructions.

The original has **257 truly uninitialized CODE positions**, specifically
`_TEXT+0..254` (255 bytes) and `+356..357` (two-byte saved environment word).
Only **676 CODE bytes** are materialized in the OMF records. The first
255 bytes include a 143-byte copy-stack, PSP storage, 80-byte path/FCB,
MZ header and relocation parameters. The source preserves these as natural
`?` declarations; there is no synthesized initialized buffer or target-byte
array. A 97-byte copied native DOS load/transfer continuation starts at
`_TEXT+255`. The public near `__exec` body starts at original `_TEXT+359`;
it opens the input file, copies DOS command/FCB structures, computes the
COM/MZ load size, resizes the DOS memory block, copies the continuation and
environment, calls CRT cleanup, then transfers to the loaded code. Error
paths preserve original DOS and near Borland `__IOERROR` return conventions.

The original CRT group is `06ff02`; DATA is empty. All six original imports
(`__cexit`, `__IOERROR`, `__envseg`, `DGROUP@`, `__psp`, `__version`), the
original near public, all original CODE bytes and **21 original FIXUPP
records** match by site, frame, target, addend and literal ordered list.

## Important original provenance and stronger-than-code exactness

The separate historical `vendor/exec.obj` agrees with original CODE,
public/interface, segment geometry and relocation sites/targets, but has
**four non-identical BCC original frames** at CODE+371,+397,+482,+560:
the standalone version has TARGET frame5 and the real library member has
DGROUP frame1. The native `after338` builder explicitly checks those four
cases and chooses the pinned library program as primary evidence.

When the original stable native source timestamp is used, **both TASM
producer rounds reproduce the original complete CL.LIB member OMF
program records byte-for-byte**, not just the materialized 676 bytes or the
ordered 21 FIXUPPs. The blank CODE region is preserved as uninitialized
source declarations. There is no after-the-fact object or EXE patch.

`scripts/build_th03_mainl_after338_work.py dos-exec-overlay-boss` extends
the full **363-member** native source/receipt-bound parent (including
`loadprog`). All **893** CRT slots remain ordered and complete; there are
now **364** source-backed members, **529** unchanged original contextual
members and **119,828 original-equal logical CRT CODE bytes**. Two real
native TASM/TLIB/TLINK rounds produce the full original Japanese decoded
MAINL **67,372-byte EXE and MAP**, including the exact **677 ordered MZ
relocations**. Raw native OBJ/LIB/EXE/MAP producer outputs, logs, parent and
source hashes are retained under `.analysis/work/after338-*` and reviewed by
`scripts/review_th03_mainl_after338_work.py` and
`tests/test_mainl_after338_work.py`.

This is working CRT source verification, **not** formally accepted
Factory decoded extent, packed-file unit credit or whole-game ownership.
No full native cold replay was run.
