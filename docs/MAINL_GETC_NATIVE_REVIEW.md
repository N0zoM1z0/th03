# Complete native DOS getc/fgetc: four-entry 485-byte original source

The original Borland DOS large-model CRT getc member at index237
is now a complete maintained 8086 mnemonic/label source TU:
src/mainl/crt/getc.asm. The object is **485 original CODE
bytes** over 193 genuine instructions, with four original public
entry addresses: __fgetc far entry at192, __Nfgetc near
stack-conversion shim at217, _fgetc far entry at220, and
_fgetchar far entry at469. The earlier two near helpers
at offsets0 and69 handle flushing outbound streams and refilling
the input buffer. These are real original DOS near/far entry points,
not four wrappers invented around modern fgetc semantics.

The source reproduces stream flags, buffered byte counts,
stream buffer pointers, actual far ___read fallback and
_eof verification, input/EOF/error flag changes and
the genuine 1-byte BSS lookahead cursor. It preserves the
private near RET and callee-clean RET 4, the far RETFs,
and the original three-byte __Nfgetc near-to-far
POP AX / PUSH CS / PUSH AX stack adapter. The four
EXTDEF names/indices match exactly: __streams, _fflush,
_eof, ___read. Real TASM5 assembles **all485 original
CODE bytes**, original DATA=0/BSS=1, literal
BSS-before-DATA GRPDEF 08ff03ff02 and all four PUBLICs.

Original BCC emits **nine OMF FIXUPPs in a nonmonotonic writer
order**: CODE sites 359,437,461,19,43,119,372,393,473.
The first three refer to the one-byte BSS object, followed by
group-framed __streams and far _fflush/___read/_eof
imports. A straightforward forward TASM source had identical
485 CODE bytes and correct field values but different
FIXUPP writer sequence. The maintained source instead emits
ten non-overlapping original instruction intervals in actual
FIXUPP writer order using typed ORG segment positioning.
**Every CODE byte belongs to exactly one real instruction**;
no padding, target opcode arrays or binary postprocessing.
Real assembly proves all **nine original ordered relocations
literally identical** in site,type,frame,target,index and addend.

The scoped producer build_th03_mainl_getc_work.py
reuses the preceding 29-source CRT carrier (including the
complete fread/fwrite IO TUs, scanner, both qsort bosses,
and 12,622-byte xx). TASM assembles getc twice,
TLIB replaces original slot237 and retains all **863
other member program records** of893 intact. Both actual
TASM/TLIB/TLINK rounds reproduce the **complete 67,372-byte
decoded Japanese MAINL EXE**, original MAP and **677 DOS MZ
relocations** byte-for-byte. This produces **30 simultaneous
exact source members totaling 19,340 CODE bytes**.

The pinned Japanese target is candidate-local-attested.
The accepted28-provider CRT and published211-owner MAINL ledger
remain unchanged. Source-only working-link exactness is not
automatic formal accepted credit; no full cold replay,
DIET pack or ancestor chain is performed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_getc_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_getc_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_getc_work

The two full native raw OBJ/LIB/EXE/MAP vectors,
source hashes and TASM/TLIB/TLINK phase logs are retained in
.analysis/work/mainl-getc-native-{build,review}.json
and .analysis/work/getc-full-*.
