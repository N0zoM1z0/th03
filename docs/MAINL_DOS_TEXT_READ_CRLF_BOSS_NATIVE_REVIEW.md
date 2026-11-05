# Original DOS text-mode read, Ctrl-Z and CRLF conversion — after470

The original Japanese Borland CL.LIB member read (index **276**) is
now maintained as actual [8086 source](../src/mainl/crt/read.asm).
This is the complete 207-byte FAR ___read function, not a wrapper:
it validates the DOS file descriptor against __nfile, invokes
the original near __IOERROR(6) for invalid descriptors, tests
__openfd state, reads with genuine FAR __rtl_read and translates
text-mode buffer bytes while preserving the native double-byte
read/seek behavior. The loop uses ES:SI to read from its far
buffer (the original ES segment override on LODS), skips CR
and translates Ctrl-Z into EOF, calls real __read when a
final CR needs lookahead and real _lseek to put back unread
bytes, and updates the same original descriptor flags.

All **207 original CODE bytes**, original _TEXT/_DATA/_BSS,
near and far external ABI, six ordered imports, and all
**eight literal ordered OMF FIXUPPs** match the Japanese
original, including _IOERROR CODE-framed near call at CODE+22
and far __rtl_read/__read/_lseek at +66/+142/+179.
An initial TASM candidate omitted the ES override on LODS
and mis-sized the routine by one byte; the source corrected
that with meaningful LODS byte ptr es:[si]. Strict original
OMF inspection also discovered that this module's GROUP is
BSS-before-DATA 08ff03ff02 rather than the initial TASM
DATA-first build, and that original layout was restored.
No target CODE bytes, NOP padding or object rewriting are used.

The after470 producer verifies the complete after469 677-source
carrier before two new native TASM/TLIB/TLINK rounds.
Both complete Japanese decoded MAINL EXE/MAP equal their
pinned targets (67,372 EXE bytes and 677 ordered MZ
relocations). Raw two-round OBJ/LIB/EXE/MAP, logs, source
hashes and original parent receipt are retained. The working
CRT reaches **678/893** source-linked members, **181,620
original-equal CODE bytes** with 215 contextual vendor
members. This proves source-bound working parity, not
full raw original Borland OBJ identity, Factory source
acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after470_work.py
(mode dos-text-file-read-crlf-boss).
Tests: tests.test_mainl_after470_work.
