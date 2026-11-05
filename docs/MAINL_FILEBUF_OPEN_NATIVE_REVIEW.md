# MAINL `filebuf::open`: complete native Borland member and linked equality

This scope is the complete original Japanese Borland CRT `fsbopen` member
713, not merely one observed call site. The source
`src/mainl/crt/fsbopen.asm` reconstructs the full 346-byte `_TEXTA` CODE
segment, with no DATA or BSS. The original far C++ public is
`@filebuf@open$qnxcii`; the literal extern sequence is `_lseek`,
`_open`, `@streambuf@setp$qnct1`, `@streambuf@setg$qnct1t1`.
Original group bytes are `08ff02ff03`.

The recovered instructions translate the iostream input/output, append,
truncation, binary/text and other original flags to DOS `_open` flags.
They retain the early refusal to reopen an attached filebuf, descriptor
and offset fields, `_lseek` setup, buffer start adjustment and the
two far streambuf pointer resets. The return is the original far
`this` pointer on success and null on refusal/failure. 16-bit casts,
signed comparisons and wraparound are left as observed.

## Scoped proof and limitation

The independent native TASM/TLIB/TLINK driver
`scripts/build_th03_mainl_after320_work.py filebuf-open` consumes a
source-hash-bound and raw-output-hash-bound 320-source parent chain
without replaying historical cold native builds. Its two fresh runs:

- Produce 346 original-equal CODE bytes, matching all original section
  extents, public/extern interface and ordered MZ product relocations.
- Produce four far fixups at CODE+122, +176, +293, +327; each original
  site, target and frame matches after site sorting.
- Replace one more selected member of 893, reaching **321 genuine native
  source members**, 572 unchanged vendor members and **105,526 bytes**
  of original-equal CRT CODE.
- Link the entire decoded original Japanese MAINL EXE and MAP byte-for-byte
  equal in both rounds, preserving its 677 MZ relocation entries.

The original BCC vs TASM **literal FIXUPP record order** differs. This
does not establish original OMF serialization or change the accepted
canonical packed-unit ledger. `review_th03_mainl_after320_work.py` and
`tests.test_mainl_after320_work` enforce the bounded claim.
