# Complete original `TRegexp`: two CODE segments, typed RTTI and maxpat DATA

The original Japanese Borland CL.LIB member **420** (`regexp`) has now been
recovered in natural, named `src/mainl/crt/regexp.asm`. This is the full
**649-byte CODE / 2-byte initialized DATA** C++ member, not a stub around
an exported function. It contains all **five far methods**:

| Original `_TEXTC` offset | Original far public | Reconstructed implementation |
| ---: | --- | --- |
| 0 | `@TRegexp@$bctr$qnxc` | Construct from character string; allocate six-byte object, generate pattern, maintain references |
| 81 | `@TRegexp@$bctr$qmx7TRegexp` | Copy construction with original pattern-copy call and refcount semantics |
| 162 | `@TRegexp@$bdtr$qv` | Release owned pattern and optional object deletion |
| 233 | `@TRegexp@copy_pattern$qmx7TRegexp` | Exception-framed 128-byte allocation, `memcpy`, capacity transfer |
| 332 | `@TRegexp@gen_pattern$qnxc` | Exception-framed 128-byte allocation and `@makepat` generation |

The separate `_TEXT` segment is **110 bytes**: a small exception unwind thunk,
**two complete typed Borland exception frame records**, and the real
out-of-memory exception destructor with reference-count and delete logic.
The `_TEXTC` segment includes the five methods followed by real typed `xalloc`
and `xmsg` RTTI descriptors (original starts at `_TEXTC+417` and `+483`).
The original initialized DATA is a `dw 128` exported as `@TRegexp@maxpat`.
The empty BSS, 9 imported far functions, public locations and the unusual
`DGROUP` order are preserved.

## Original codegen detail, not an object patch

TASM normally changes a direct far call **within the same CODE segment** into
`PUSH CS` plus near `CALL`. The pinned original Borland OBJ instead uses the
true x86 immediate far `CALL` (`9A`, followed by the relocation-backed far
pointer) at `_TEXTC+45` and `+126`. To preserve the original instruction
without manufacturing executable byte arrays, the source explicitly declares
that **single x86 opcode byte** (`db 09ah`) followed by the **symbolic far
function address** (`dd @TRegexp@gen_pattern...` and `dd
@TRegexp@copy_pattern...`). These typed `dd` declarations produce the
original OMF segment relocation target and remain linked naturally. There
are no raw CODE arrays, synthetic padding regions, OBJ modifications or
binary/link patches. Two compiler exception frame pointers at `_TEXTC+245`
and `+344` also require the *state-record* offsets `_TEXT+13` and `+27`,
not the descriptor-base labels `_TEXT+5` and `+19`.

## Scoped original native evidence

`scripts/build_th03_mainl_after329_work.py regexp-boss` extends the
**340-member** source/receipt-bound carrier. Two independent native
TASM/TLIB/TLINK rounds reproduce complete original `_TEXT` (110 bytes),
`_TEXTC` (539 bytes), DATA (2 bytes), all original 31 code relocation fields
including their **frames**, all public/import/segment/group identities, and
the exact original Japanese decoded MAINL **67,372-byte EXE and MAP** with
**677 ordered DOS relocations**. There are now **341 source-backed CRT
members**, **552** original contextual programs and **111,706 source-compiled
original-equal CRT CODE bytes**. The complete raw OBJ/LIB/EXE/MAP rounds and
writer logs are retained under `.analysis/work/after329-*` and bound to
original member program, source, parent receipt and builder hashes.

Literal original ordered **OMF FIXUPP record order and full member record
serialization still differ** from TASM (despite all 31 original fields and
the linked product matching). This is a working-source reconstruction, not a
new formally Factory-accepted extent or proof of whole-game ownership.
No full native cold replay was performed. Run the narrow source-bound review
`PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after329_work.py regexp-boss`
and its test `tests.test_mainl_after329_work`.
