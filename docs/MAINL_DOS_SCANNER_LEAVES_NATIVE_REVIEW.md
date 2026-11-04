# Japanese MAINL original vscanf, DOS vectors, date/time leaf recovery

Six **distinct selected** CRT members have been recovered as complete
Borland 8086 native source and linked into the original Japanese 893-member
CRT, complementing the existing `scanner`, `scanf`, `sscanf`, `signal` and
`utime` source units:

| Original slot | Member | CODE | Original exports |
| ---: | --- | ---: | --- |
| 330 | `vscanf` | 40 | far `_vscanf` at +0 |
| 328 | `vfscanf` | 41 | far `_vfscanf` at +0 |
| 38 | `dosvect` | 40 | `__dos_getvect` +0, `__dos_setvect` +19 |
| 64 | `getvect` | 40 | `_getvect` +0, `_setvect` +19 |
| 57 | `getdate` | 46 | `_getdate` +0, `_gettime` +23 |
| 113 | `setdate` | 46 | `_setdate` +0, `_settime` +23 |

The source modules use normal symbolic 8086 far procedure declarations,
register saving, DOS `INT 21h` services 25h/35h and 2Ah/2Bh/2Ch/2Dh,
`LES`/`LDS` far caller-struct pointer handling and the original near scanner
callbacks. No executable machine-code byte arrays, artificial padding or
post-assembled OBJ edits were used. Both scanner wrappers preserve the
original `__scanner`, `__Nfgetc`, `__Nungetc`, stdout stream and `va_list`
calling conventions. All six independently reassemble to their **253/253
original CODE bytes**, zero DATA/BSS, exact original public/extern ABI and
original DGROUP membership (including the different group order for vectors
and setter functions).

The native OMF comparison checks all original site, width, target, addend and
segment conventions. Only two `__scanner` external near calls (CODE+31 in
`vscanf`, +32 in `vfscanf`) differ in frame metadata: BCC TARGET frame5
versus TASM CODE frame0; Borland/TASM FIXUPP record ordering also differs
for these wrappers. The four DOS leaf objects have no relocation entries.
Full original OBJ record-stream identity is not claimed where false.

`scripts/build_th03_mainl_after106_work.py scan-vectors-time` inherits the
source-bound, full-original Japanese **106-member** CRT carrier and assembles
these six at their actual selected native library indices. Two independent
TASM/TLIB/TLINK rounds reproduce the **entire 67,372-byte decoded Japanese
MAINL EXE and original MAP** and all **677 ordered MZ relocations**, with
**781 unchanged contextual vendor member program records**. The working
source CRT reaches **112 members and 51,546 original-equal CODE bytes**.

Proofs: `review_th03_mainl_after106_work.py scan-vectors-time`,
`tests.test_mainl_after106_work`, two raw OBJ/LIB/EXE/MAP vectors and tool
phase logs under `.analysis/work/after106-scan-vectors-time-*` plus
source-hash-bound receipts in `.analysis/work/mainl-after106-*`. This is
working source reconstruction, not formal accepted-ledger credit. **No full
cold replay** was run.
