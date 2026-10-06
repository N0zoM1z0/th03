# MAINL CRT break and pointer substrate review

This reviews six linked Borland CRT CODE carriers, 628 decoded bytes, that
support the ending's allocation dependencies. It adds candidate evidence;
it does not migrate proprietary CRT source, accept a maintained MAINL owner,
or assign a canonical stored-file offset. The complete malloc/new/realloc,
startup, exception and artifact dependency scopes remain open.

Receipt: `.analysis/sol-mainl-crt-break-review-20261006.json`, SHA-256
`fb467a0a852767eba985dbb5ca76ad674cb3b65d165cab4d7ffa3d006af2fbd5`; 891 guarded inputs.

```sh
DISPLAY= WAYLAND_DISPLAY= python3 scripts/review_th03_mainl_crt_break.py \
  --output .analysis/NEW_CRT_BREAK_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_crt_break_review.py
```

## CODE, DATA and compiler lineage

| MAP carrier | Decoded CODE offset | Bytes | Complete contents |
| --- | ---: | ---: | --- |
| h_llsh | 315E | 33 | Near bridge and far long shift |
| h_padd | 317F | 96 | Near/far pointer addition/subtraction and shared tails |
| ioerror | 31DF | 82 | Near IOERROR and DOSERROR wrappers |
| n_pcmp | 357C | 33 | Normalized pointer comparison |
| fbrk | 3E70 | 352 | Private resize helper, public near brk and sbrk |
| setblock | 8E5A | 32 | Public far DOS setblock wrapper |

Thirteen instruction partitions have 277 instruction positions. The near
shift/add/sub bridges change an actual near return frame into a far frame;
far entries and real RETF/RET cleanup are checked separately. The resize
helper is private and executes only through complete public brk/sbrk callers.
Twelve public entry coordinates agree with both cold MAPs and the compiled
library's public definitions. The apparent bytes `04 00` at 3EFC are the
immediate operand of RET 4 at 3EFB, not alignment or another function.

All 628 CODE bytes and their empty ordered MZ relocations agree with both
fresh MAINL products from the existing complete MAIN cold replay. The 111
bounded initialized DATA bytes also agree: PSP 2, errno 2, heap pointers 12,
DOS errno/table 91, resize granule count 2 and system error count 2. Runtime
fixtures initialize mutable fields separately; these slice comparisons do
not establish complete CRT/DGROUP/DATA/BSS layout or ownership.

The current installed and active CL.LIB have SHA-256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
These are locally attested candidate compiler binaries, separate from frozen
ReC98 authored source. Six selected members are bounded by library page,
record, segment, CODE length and public definition checks. Their raw hashes
are recorded, without copying proprietary members into product source.

The library's six A3 librarian naming comments retain stale checksums.
The replay reports these narrow, observed exceptions and does not repair
them or call the members valid strict OMF object streams. All selected
CODE/DATA/fixup/other record checksums are checked. Library framing or a
changed non-comment record is rejected. The full library hash is pinned.

A bounded symbolic resolver reproduces all selected linked CODE using MAP
symbols and the original member LEDATA/FIXUPP records: 39 fixups, including
DGROUP offsets, same-CODE relative calls and one TLINK far-call relaxation.
The five-byte far call becomes NOP/PUSH CS/CALL with the same length and
real far return ABI. Unsupported methods, threads, displacement forms,
out-of-range/overlapping ownership and wrong relaxation targets are rejected.
No target-byte patch or compiler source is used to produce this comparison.
Library DATA for IOERROR and the resize granule count matches the respective
DGROUP MAP contributions and target data. The three fixup-free helper members
already match their target CODE directly.

Both archived MAINL link responses select `emu.lib mathl.lib cl.lib` and are
bound to the original, hashed cold command logs. Their six CODE carriers,
two DATA contributions and public symbols match both products. Existing
archived source/config hashes and previous MAIN-only forwarding changes are
preserved. No new build or complete ending-library acceptance is claimed.

The selected stored packed MAINL database was re-attested before this work.
The observations use the decoded image, without unpacked Ghidra function
credit. Japanese YUMEZIKU targets remain candidate-local-attested; independent
pristine-dump attestation is unknown.

## Independent native execution

Each image has 7,858 scenarios and 11,247 terminal calls, with 25,714 native
entries. Across the target and two cold products, all 33,741 calls return
and execute 77,142 native entries. All 277 instruction positions execute.
These are bounded diagnostic counts, separate from prior caller receipts.

Every public scope executes real target instructions, including compiler
register helpers, near/far bridge stack changes, shared pointer tails,
private resize, errno conversion and DOS wrappers. Return IP/CS, CS/SS/SP,
cleanup, BP/SI/DI/DS and IF/DF preservation are guarded. Integer/address
specifications independently compare declared results, pointer-order CF/ZF,
ordered CPU stores, native-entry counts, DOS events and the entire 1 MiB
physical memory outside the 64 KiB stack. No malloc or other target routine
is replaced inside this scope.

DOS INT21/AH4A returns are explicit AX/BX/Carry fixtures. Real DOS block
ownership, resizing, process lifetime and asynchronous interrupts remain
unobserved. Each image retains its unrelated executable/DGROUP contents;
cross-image comparison omits only complete memory hashes.

The matrix includes all 256 shift count bytes, six long-word seeds, pointer
word/segment extrema and signed displacement boundaries, normalized alias
ordering, all 89 DOS table indices and clamp/negative error boundaries,
synthetic high-bit error table values, negative system-error counts, near/far
entry pairs, resize granule equality/mismatch, success/failure and BXFFFF,
PSP/rounding wrap, noncanonical break pointers and connected state changes.
Eleven controls cover complete partitions, operands/neighbors/shared edges,
native calls/services, bridge/private entry/return frames, full store spans,
stale completion, segment aliases, library framing/checksums, symbolic
fixup ownership, signed errors and failure-state effects.

## Preserved behavior and limits

- Pointer arithmetic normalizes `(segment * 16 + offset +/- signed delta)`
  modulo 1 MiB. Comparison separately normalizes each word pair before
  comparing segment and low offset. This affects aliases and wrapped
  segment sums; it is not a host flat-pointer comparison.
- Long shifts with counts 0 through 31 agree with unsigned 32-bit shifts.
  Counts above 31 retain the emitted helper's branch and Unicorn count-mask
  behavior. Those observations do not establish unusual V30 shift semantics
  or valid language-level shifts. The resize caller supplies count 4.
- sbrk's high-word range check is signed. A negative 1 MiB increment can
  normalize to the current break, pass its bounds and return the prior
  pointer without changing it. Positive 1 MiB is rejected. Large negative
  increments do not receive a repaired host overflow policy.
- brk checks normalized bounds but stores the caller's original word pair.
  The resize helper rounds the raw segment, retaining its offset separately.
  PSP subtraction, the add-63 rounding and paragraph multiplication wrap
  at 16 bits. Equality of the recorded granule count bypasses the DOS call.
- DOS resize success is the wrapper's AXFFFF sentinel. Failure first runs
  native IOERROR, then returns the DOS BX largest-block value. The private
  helper updates the maximum heap pointer to `(PSP + BX):0` on ordinary
  failure without advancing the break or granule count.
- Failure with BXFFFF collides with the success sentinel: errno records
  the failure, yet the helper records the new break/granule and reports
  success. This is an emulator observation under a declared DOS reply,
  not evidence that real DOS will return that combination.
- Positive DOS codes 0..88 use the table; higher signed-positive values
  clamp to 87. Negative errors within the signed system-error count bypass
  the table and set doserrno to FFFF. INT_MIN retains the word NEG overflow
  and can store errno 8000. DOSERROR returns its original argument after
  the same conversion. Synthetic high-bit table values are sign-extended.

## Remaining artifact scope

The refreshed MAP/unit interval union is recorded separately after this review.

MAINL maintained source/exact counts remain zero. This candidate CRT substrate
does not accept complete malloc/free/realloc/new/delete, CRT startup/exception
handling, full DATA/BSS or process/DOS lifetime. Prior ReC98 caller receipts
retain their allocation interfaces and original scope. The 505-file intake,
69 scoped MAIN CODE paths, canonical DIET packaging and complete Oracle gates
remain separate unfinished work. Accepted MAIN ownership is unchanged.
