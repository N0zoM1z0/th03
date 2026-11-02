# Native DOS memset and setmem: cumulative five-source MAINL CRT link

The new maintained src/mainl/crt/memset.asm reconstructs the original
large-model DOS memset library member at zero-based index263. It has
two genuine far cdecl public entries, _setmem at CODE offset0 and _memset
at CODE offset38. The former writes the actual byte value via original
word-aligned DI and REP STOSW, preserving the one-byte leading and trailing
cases and all original arguments/16-bit wrapping. The latter pushes its
parameters in the original near-call ABI order, explicitly saves CS and
calls _setmem with the exact original displacement, then returns the far
destination pointer through DX:AX. The source contains ordinary 8086
mnemonics and labels,not original function-byte arrays or object patches.

Two real TASM native assemblies emitted **the complete original72 CODE
bytes**, no literal fixups, the two original public symbol identities and
offsets, the original _TEXT/DATA/BSS extents (72/0/0), and exact original
BSS-before-DATA GRPDEF 08ff03ff02. There is no extra alignment filler,
initializer or memory-model substitution.

The cumulative scoped builder includes the four previously recovered
natural source members memchr37,memcmp40,memcpy36,strcmp48, plus this
memset72 member, totalling **233 source-present CODE bytes**. It retains
all893 original TLIB positions; only source members at indices
259/260/261/263/292 differ,and the other888 original member program
records are preserved. Two serialized TASM/TLIB/TLINK rounds repeat the
entire raw native object/library/EXE/MAP vectors and both rebuild the
actual **67,372-byte decoded Japanese MAINL EXE and complete original MAP
byte-for-byte**, with all677 MZ relocations. The accepted original
28-provider CRT library and211-owner publication are untouched.
This is a verified source-only working carrier,not automatic newly
published ledger credit.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_growth_work.py memchr-memset
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_growth_work.py memchr-memset
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_growth_work

The retained receipts and complete native vectors are under
.analysis/work/mainl-crt-growth-memchr-memset-{build,review}.json
and crt-growth-memchr-memset-roundN-*. No original cold/DIET or ancestor
runtime chain was rerun.
