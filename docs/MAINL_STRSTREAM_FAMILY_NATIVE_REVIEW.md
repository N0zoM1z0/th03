# Original Japanese C++ `strstream`: constructors, destructor, adjustors and RTTI

Three actual selected Borland CRT source members reconstruct the full
`strstream` lifecycle with genuine 8086 source and typed Borland class
metadata:

| Original slot | Member | CODE | initialized DATA | Original far C++ public |
| ---: | --- | ---: | ---: | --- |
| 736 | `iosrctr1` | 795 | 36 | `@strstream@$bctr$qv` |
| 737 | `iosrctr2` | 873 | 36 | `@strstream@$bctr$qncii` |
| 738 | `iosrdtr` | 745 | 36 | `@strstream@$bdtr$qv` |

Each complete module preserves the original far C++ constructor/destructor
body, original `ios`, `iostream`, and `strstreambase` object ownership,
exception destructor accounting, the `strstreambuf` connection and original
object layout. `iosrctr2` also implements the original string-length,
far virtual dispatch and initial capacity behavior. All **2,413/2,413
original CODE bytes and 108/108 DATA bytes** are genuine authored assembler
with exact original far PUBLIC/EXTDEF and `_TEXTA/_DATA/_BSS` structure.

**Executable CODE after each public return is not blindly interpreted as
RTTI data.** Each of the three CRT members contains three genuine native
12-byte multiple-inheritance destructor-adjustor thunks, expressed as real
`mov bx,sp`, `add word ptr ss:[bx+4],...`, and **`jmp far ptr`** 8086
instructions. Subsequent Borland RTTI is expressed as typed `dw`/`dd` class
metadata and original `strstream`, `ios`, `iostream`, `strstreambase`,
`strstreambuf`, `ostream`, `istream` and `streambuf` names. The 36-byte DATA
sections are true exception-unwind far-pointer tables, not code-size padding.
No output-byte patching or opaque original executable machine-code arrays.

Two real TASM traps were solved from original selected OMF rather than from
previous documentation: the `iosrctr2` virtual call at CODE+237 must use
**far indirect `FF 5F 1C`**, not near `FF 57 1C`; the `iosrdtr` self-referential
far thunks at +152/+164/+176 must not be collapsed into near jumps, so
`ASSUME CS:NOTHING` scopes the thunk region to preserve original `EA`.
TASM `/m /mx /kh32768 /t` now independently reproduces every original
CODE and DATA byte, all original PUBLICs, ordered imports and **109/109 OMF
relocation sites, kinds, targets, addends and frame methods**. BCC and TASM
serialize the FIXUPP records in different **order**, so literal original
whole-OBJ record identity is **not** claimed.

`scripts/build_th03_mainl_after174_work.py strstream-family` inherits the
verified actual original **174-source Japanese MAINL CRT** and normally
recompiles all three selected slots in **two independent normal TASM/TLIB/
TLINK rounds**. Both produce the **whole original 67,372-byte decoded
Japanese MAINL EXE and MAP byte-for-byte**, preserving **all 677 ordered MZ
relocations** and **716 unchanged contextual vendor CRT programs**. Working
source reaches **177 modules / 79,083 original-equal CODE bytes**. Formal
accepted-ledger credit remains unchanged; no full cold replay ran.

Verify with `review_th03_mainl_after174_work.py strstream-family` and
`tests.test_mainl_after174_work`; two raw OBJ/LIB/EXE/MAP vector pairs and
actual tool logs remain under `.analysis/work/after174-*` and
`.analysis/work/mainl-after174-*`.
