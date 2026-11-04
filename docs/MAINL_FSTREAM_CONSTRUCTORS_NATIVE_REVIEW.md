# Original Japanese C++ `fstream`: four full constructors and their native RTTI

Four actual selected Borland large-model CRT members have been completely
recovered in genuine symbolic 8086 assembly, with the four distinct far C++
`fstream` constructor overloads and their original multiple inheritance
layout:

| Original CRT slot | Module | CODE | DATA | Original far exported constructor |
| ---: | --- | ---: | ---: | --- |
| 731 | `iofsctr1` | 772 | 36 | `@fstream@$bctr$qv` |
| 732 | `iofsctr2` | 787 | 36 | `@fstream@$bctr$qnxcii` |
| 733 | `iofsctr3` | 775 | 36 | `@fstream@$bctr$qi` |
| 734 | `iofsctr4` | 787 | 36 | `@fstream@$bctr$qinci` |

`src/mainl/crt/iofsctr*.asm` reconstructs all four real far constructor
bodies, their `ios`, `iostream`, `fstreambase`, and `filebuf` base
initialization, allocation/exception destructor bookkeeping and exact
per-object virtual pointer offsets. The `_TEXTA` CODE sections also contain
**three executable 12-byte original multiple-inheritance destructor-adjustor
thunks per module**, expressed as genuine `mov bx,sp`, `add word ptr
ss:[bx+4],...`, `jmp far ptr` instructions—not opaque machine-byte tables.
Following these thunks is the actual typed Borland RTTI with eight original
`fstream`, `ios`, `iostream`, `fstreambase`, `filebuf`, `ostream`, `istream`,
`streambuf` class names and symbolic relocated far pointers. Each 36-byte
initialized DATA section is the native unwind/class pointer table with five
far relocatable entries. No patched OBJ records, machine-CODE arrays, size
padding or original object metadata forgery was used.

Independent TASM 5.0 `/m /mx /kh32768 /t` reproduces **all 3,121 original
CODE bytes and 144 initialized DATA bytes**, four original C++ public
entrypoints, 13 original ordered dependencies per member, segment/group
layout and **144/144 original OMF fixup sites, targets, widths, addends and
frame methods**. Only the literal original BCC-vs-TASM FIXUPP record order
remains different; whole original OMF object-program byte identity is not
claimed where false.

`scripts/build_th03_mainl_after169_work.py fstream-constructors` inherits the
source/driver/parent-hash-bound **169-source** Japanese CRT and assembles all
four at the true original selected member slots in **two independent normal
TASM/TLIB/TLINK rounds**. Both reconstruct the complete **67,372-byte decoded
Japanese MAINL EXE and original MAP byte-for-byte**, including all **677
original ordered DOS MZ relocations** and leaving **720 unchanged vendor CRT
program records**. Working CRT now has **173 source-built members and 75,935
original-equal CODE bytes**. This is working-source evidence, not formal
accepted-ledger credit. No full cold replay was run.

Review with `review_th03_mainl_after169_work.py fstream-constructors`,
`tests.test_mainl_after169_work`, and the retained two raw OBJ/LIB/EXE/MAP
native rounds and actual writer logs under `.analysis/work/after169-*` and
`.analysis/work/mainl-after169-*`.
