# Original Japanese C++ `fstream` destructor and its three far adjustors

Recovered selected Borland 16-bit CRT member **735** `iofsdtr` in complete
symbolic source `src/mainl/crt/iofsdtr.asm`: **735 original CODE bytes**,
**36 initialized DATA bytes**, zero BSS, original far C++ public
`@fstream@$bdtr$qv` at CODE+0, nine ordered imports, and original
`_TEXTA/_DATA/_BSS` plus DGROUP layout.

The native source implements the full `fstream` far destructor (145-byte
executable body) including original exception/reference destructor counts,
`iostream`, `fstreambase`, and `ios` destruction, conditional far object
release, and the **three real multiple-inheritance adjustor thunks** at
CODE+145/+157/+169. Each thunk is expressed with real 8086 operations
`mov bx,sp`, `add word ptr ss:[bx+4],...`, and **`jmp far ptr`**, not copied
executable CODE bytes. The remaining `_TEXTA` region contains typed Borland
class RTTI/destructor metadata and eight actual class-name strings; the
36-byte DATA section carries the original five far C++ unwind pointers.

A meaningful 16-bit C++ ABI issue was discovered and resolved: unlike the
four *constructor* modules where each adjustment thunk jumps to an external
`fstream` destructor, this destructor module itself defines the public far
target. TASM optimized `jmp far ptr @fstream@$bdtr$qv` into **near `E9`**
and changed CODE size, relocation sites and linked behavior. Scoping the
thunks with `ASSUME CS:NOTHING` forces the **original far `EA`** even when
the target is local. No `db 0EAh` machine-code injection, byte patching or
OBJ metadata editing was used. All three original thunk targets preserve
the exact original native code frame, sites and selected far public.

Standalone TASM `/m /mx /kh32768 /t` reconstructs **735/735 whole CODE
bytes**, **36/36 whole DATA bytes**, original public/extern/segment structure
and **all 36/36 original OMF relocation sites, target methods, addends,
widths and frame methods**. The original BCC FIXUPP *record order* remains
different; complete original native OBJ byte identity is not claimed.

`scripts/build_th03_mainl_after173_work.py fstream-destructor` starts from
the fully source-bound **173-source original Japanese CRT** and replaces
only actual selected CRT slot 735 in two independent normal TASM/TLIB/TLINK
rounds. Both reconstruct the entire **67,372-byte decoded Japanese MAINL
EXE and original MAP byte-for-byte**, including **677 original ordered MZ
relocations** and **719 untouched vendor CRT program records**. Working
source reaches **174 members / 76,670 original-equal CODE bytes**. This is
working evidence, not accepted-ledger credit; no full cold replay ran.

Proof: `review_th03_mainl_after173_work.py fstream-destructor`,
`tests.test_mainl_after173_work`, the raw native OBJ/LIB/EXE/MAP pairs,
source-bound receipts, and tool writer logs under `.analysis/work/after173-*`
and `.analysis/work/mainl-after173-*`.
