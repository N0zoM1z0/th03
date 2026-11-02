# Original 666-byte qsort recursion: verified native control-flow blueprint

This is a bounded roadmap for reconstructing the original DOS Borland
qsort recursive algorithm,not a replacement or accepted function.

The original Japanese vendor qsort.obj has CODE756,DATA0,BSS6,29
literal ordered OMF fields. It comprises the source-matched near
swap helper at offset0 (46 bytes),the **still-unrecovered private
666-byte near recursive sorting body** at offset0x2E (242 fully
decoded instructions),and the bounded source-matched far qsort
wrapper at offset0x2C8 (44 bytes). The recursion uses a24-byte local
frame and returns with near RET 6. The private swap uses RET 8.

Using the actual original instruction boundaries and literal
original OMF records, the recursive body has **25 fixups**:
four arithmetic helper calls (N_LXMUL@ twice and N_LDIV@ twice)
plus real BSS comparator/element-width references. The exact
call graph includes:

- Six genuine near calls to private swap at CODE offsets
  00CE,0119,012E,015E,01BF,0234.
- Two genuine recursive calls to core offset002E from
  CODE offsets0299 and02AE.
- Four original imported near arithmetic CALLs at
  offsets0085,00A0,0264,0287, with literal import fixups
  sites0086,00A1,0265,0288.
- Seven indirect far comparator callbacks through the
  original BSS far callback pointer at CODE offsets
  005D,00B7,00DD,0102,0181,019D,01EF.
- Thirty direct conditional/unconditional jump instructions,
  all bounded to actual instruction addresses within
  original core,not inferred source labels.

The full original far entry stores width at BSS+4, comparator at
BSS+0/+2 and passes the original three near argument words.
This is not a standard library qsort shape that can safely be
assumed from a modern algorithm. The median/partition arrangement,
pointer width arithmetic,comparator calling convention,overflow
behavior and near recursive RET 6 all need to be reconstructed
with the original Borland compiler/TASM code generation.

A maintained native 46-byte swap source and original44-byte public
wrapper source are already verified in separate scoped builds.
The far wrapper differs only in its two-byte symbolic CALL offset
because the complete666-byte recursive core is not present.
This blueprint is NOT claimed as generated qsort core bytes or
additional source exact credit: complete_qsort=false,
original_source_core_recovered=false and source_acceptance=false.
The complete original vendor object is never patched.

The next actual source work is to recover the recursion algorithm and
generate the original body,25 ordered fields,then integrate the full
qsort original member into the existing15-source native working
MAINL library and compare actual decoded EXE/MAP. Do not use
NOP/zero filler,a fabricated ret6 core or full cold replay.

Affected-only original structural check:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_qsort_core.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_qsort_core

Original instruction and FIXUPP evidence is retained in
.analysis/work/mainl-qsort-core-map-review.json.
