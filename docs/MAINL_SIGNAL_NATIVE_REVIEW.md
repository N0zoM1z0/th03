# TH03 Japanese MAINL original DOS signal boss: 88-source native CRT

**Recovered source:** `src/mainl/crt/signal.asm`, genuine selected Borland
large-model CRT member **180**, not an arbitrary standalone vendor object.
It has **769 CODE / 38 initialized DATA / 4 BSS** bytes and exports two far
entry points: `_signal` at original CODE+392 and `_raise` at CODE+618. The
unexported leading routines (CODE+0, +114, +228) handle DOS interrupt
trampolines with register saves, `IRET`, one-shot handlers, callbacks and
interrupt-vector interaction. `_signal` manages registration and `_raise`
handles the original signal dispatcher. The six original ordered imports are
`__exit`, `__abort`, `_errno`, `_getvect`, `_setvect`, `___SignalPtr`.

The 8086 source is symbolic, with real branch labels, far pointer slots,
DOS interrupt numbers, active signal flags and uninitialized saved-vector
state; no original executable byte arrays or post-assembly patches. DATA is
materialized as two flags, twelve explicit 16-bit handler words, eight
interrupt-number bytes and the original final state words. A first attempt
with `12 dup(0)` produced equal effective zero bytes but TASM represented
the array differently (LIDATA instead of original LEDATA coverage). Using
twelve ordinary explicit `dw 0` entries restores the original materialized
DATA inventory, not just its zero-filled values.

The original assembly uses indirect far calls through stack far pointers;
TASM's default `call [bp-4]` encoded a *near* call. Correctly using
`call dword ptr [...]` restores the four complete original far call
instructions. Explicit `DGROUP:`-qualified external signal pointer and
`_errno` references restore all three originally GROUP-framed FIXUPPs.

Verified against the **actual selected original CRT member**, and with two
independent complete TASM/TLIB/TLINK normal link rounds:

- All **769 CODE / 38 DATA / 4 BSS** original sizes and CODE/DATA bytes;
- both original public offsets, six ordered imports, all segment and group
  identities and all **55/55** relocation fields by original site, kind,
  target, addend **and frame method**;
- **entire original 67,372-byte decoded Japanese MAINL EXE and full original
  MAP**, including all 677 MZ relocation entries, byte-for-byte.

Original Borland and TASM FIXUPP **record order** differs, so original native
OBJ serialization identity is **not** claimed despite exact site-sorted
fields, bytes and normal linker output. The working CRT now includes **88
source-compiled members / 36,906 original-equal CODE bytes**, leaving **805**
contextual vendor program records unchanged. This is independent working
source evidence, **not** new formal accepted-ledger credit.

Scope producer: `build_th03_mainl_after87_work.py signal`. Source-bound
review: `review_th03_mainl_after87_work.py signal`, with
`tests.test_mainl_after87_work`. Two raw native output vectors, receipts and
writer phase logs are retained in `.analysis/work/after87-signal-*` and
`.analysis/work/mainl-after87-signal-*`. The 87-source carrier was inherited,
not cold-rebuilt.

**Rejected duplicate ownership:** the older `farheap.asm` source is already
covered by an independent, formally accepted native owner in the existing
selected CRT. Its standalone vendor `farheap.obj` program bytes differ from
the **active accepted** CRT member; merely recompiling the standalone object
must not be counted as a new working member. The attempted incremental
`farheap` probe correctly failed at the selected-member identity check and
was replaced with this genuine newly sourced `signal` member.
