# Overlap-safe original DOS movmem and memmove, both entry points exact

The maintained 8086 source src/mainl/crt/movmem.asm recovers the
original **119-byte** Borland large-model CRT object,not just a
simple memcpy. The object has _movmem at offset0 and _memmove
at offset82, both far-cdecl interfaces. The former calls the real
original near N_PCMP@ helper to order the incoming far source and
destination pointers. It switches CLD/STD copy direction for
overlap, aligns each scan to the destination,uses one odd leading
MOVSB, REP MOVSW and an odd final MOVSB, then restores DF to
the normal forward state. The far _memmove wrapper calls the
preceding function using PUSH CS and a genuine near CALL,and
returns the far destination pointer in DX:AX.

Every original CODE byte, including the 82+37 split and the
single original near N_PCMP@ relocation at source CODE offset19,
is produced by real TASM source. The OMF field retains its
CODE frame, non-segment-relative 16-bit displacement and target
EXTDEF without rewriting the object. The original GRPDEF
08ff03ff02, empty DATA/BSS and both public symbol offsets also
match. This is not an embedded target-byte array or source-side
padding for apparent equality.

The scoped library contains this exact source object and all
13 previous independent source modules (full xx/RTTI and twelve
string/memory/scanner sources, including newly recovered strncpy).
The original library member266 is replaced while all other
**879 of893 member program records** remain intact. Two real
TASM/TLIB/TLINK rounds generate the complete original 67,372-byte
Japanese decoded MAINL EXE and its full MAP byte-for-byte,
including all 677 original MZ relocations. The cumulative
normal-link CODE reconstructed from 14 source modules is
**13,951 bytes**.

The pinned cold pair, original target and accepted 28-provider CRT/
211-owner MAINL publication remain unchanged. No new accepted
ledger credit, full cold replay or DIET repack is claimed.

Affected scope only:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_expand_work.py strncpy-movmem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_expand_work.py strncpy-movmem
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_expand_work
