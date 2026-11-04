# TH03 original PC-98 extended serial subsystem: `pc98comx`

The **actually selected** Japanese Borland large-model CRT member **495**
`pc98comx` is a distinct extended PC-98 RS-232C driver; it is **not** the
previously recovered `pc98com` slot494. It contains complete **1,383 CODE,
35 initialized DATA and 70 uninitialized BSS bytes**. Ten original public
far entry points are at +672/+951/+1021/+1043/+1068/+1104/+1126/+1165/
+1202/+1268 for the respective init/terminate/send/receive/status/change/
buffer/break/reset/baud-check routines. It imports `_getvect`, `_setvect`,
`___nec_delay` and the separate near `N_SCOPY@` helper in original order.

`src/mainl/crt/pc98comx.asm` reconstructs the complete original 8086
hardware/BIOS detection, interrupt vector installation/restoration,
near-memory scanning, RS-232C status and ring state, and far API routines.
Executable CODE is **real 8086 instructions and symbolic branch labels**;
there are no original machine-CODE byte arrays, object patches or size-only
padding. Initialized DATA contains original state bytes, a BIOS/ROM-search
signature and original mode/baud lookup tables (the noninstruction signature
is deliberately retained as DATA). BSS remains completely uninitialized
and its native 70-byte extent is preserved.

The key native distinction is between displacement fields framed by DGROUP
and five search-signature offsets framed by TARGET in the original BCC OMF.
Symbolic `DGROUP:label` versus unqualified `offset label` produces the
appropriate original frame methods without object mutation. The one near
`N_SCOPY@` call uses original CODE frame0 and is reproduced with a genuinely
near EXTDEF, unlike the TARGET-frame5 near-call differences in some earlier
C++ modules. The source retains the original 55/35 DATA layout and all
original far/near register/segment ownership.

Normal TASM 5.0 `/m /mx /kh32768 /t` reproduces **1,383/1,383 CODE bytes**,
**35/35 DATA bytes**, all ten public offsets, four original imports, three
native segments and GROUP `08ff03ff02`. **All 58/58 OMF relocation fields,
including sites, widths, target methods/indices, addends and original frame
methods, agree when paired by native site.** The BCC and TASM FIXUPP record
ordering is different, so literal original object-record identity is
*not* claimed.

`scripts/build_th03_mainl_after128_work.py pc98comx` starts from the
complete source-bound original Japanese **128-member CRT**, recompiles this
actual slot and retains the other **764 original vendor member records**.
Two independent TASM/TLIB/TLINK rounds reproduce the entire original
**67,372-byte decoded Japanese MAINL EXE and original MAP byte-for-byte**,
including all **677 ordered MZ relocations**. Working source coverage now
reaches **129 members / 60,022 original-equal CODE bytes**; this does **not**
add formal accepted-ledger credit or imply complete whole-game ownership.
No full cold replay was performed.

Verify with `review_th03_mainl_after128_work.py pc98comx` and
`tests.test_mainl_after128_work`. Source-bound native receipts, actual tool
logs and two raw OBJ/LIB/EXE/MAP vectors are retained under
`.analysis/work/mainl-after128-pc98comx-*` and
`.analysis/work/after128-pc98comx-*`.
