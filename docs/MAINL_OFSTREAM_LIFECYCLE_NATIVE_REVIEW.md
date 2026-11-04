# Original Japanese Borland `ofstream`: four constructors and full destructor

Five distinct actual selected original large-model CRT members now have
complete symbolic 8086 sources, preserving the original C++ multiple-
inheritance ABI and typed exception/RTTI records:

| Original CRT slot | Member | CODE | DATA | Original far public |
| ---: | --- | ---: | ---: | --- |
| 795 | `ofsctr1` | 596 | 28 | `@ofstream@$bctr$qv` |
| 796 | `ofsctr2` | 612 | 28 | `@ofstream@$bctr$qnxcii` |
| 797 | `ofsctr3` | 599 | 28 | `@ofstream@$bctr$qi` |
| 798 | `ofsctr4` | 608 | 28 | `@ofstream@$bctr$qinci` |
| 799 | `ofsdtr` | 569 | 28 | `@ofstream@$bdtr$qv` |

The source implements all original `ofstream`, `fstreambase`, `ostream`,
`ios` and `filebuf` construction/destruction, including object ownership,
far calls, original heap and exception cleanup behavior, and correct virtual
function table positions. Between each real C++ procedure and the class
RTTI lie **two genuinely executable 12-byte far destructor-adjustor
thunks**, expressed as normal 8086 `mov`, stack-pointer `add`, and `jmp far
ptr` instructions—not copied machine-code byte strings. Following those
thunks are the authentic six class-name strings and symbolic `dw`/`dd` RTTI
and destructor descriptors. The 28-byte DATA per member likewise contains
the real far-pointer unwind table, not fabricated target padding.

The self-referencing `ofsdtr` adjustor thunks exposed a compiler/codegen
trap: TASM optimized jumps to the destructor defined in the same CODE
segment into near `E9`. The original object uses **far `EA`**, so
`ASSUME CS:NOTHING` immediately before those thunks restores the actual
far semantics and bytes without modifying the produced OBJ.

Native TASM 5.0 `/m /mx /kh32768 /t` reconstructs **2,984/2,984 original
CODE bytes and 140/140 initialized DATA bytes**, all five original public
names/offsets, 11/7 ordered original imports, exact segment/group layout
and **135/135 original OMF fixup sites, kinds, targets, addends and frame
methods**. The BCC and TASM FIXUPP record *sequence* differs; we do **not**
claim byte-identical full original OBJ serialization.

`scripts/build_th03_mainl_after209_work.py ofstream-lifecycle` inherits the
fully verified source-bound **209-source Japanese MAINL CRT**, replacing
only these five selected original member slots in **two independent normal
TASM/TLIB/TLINK rounds**. Both reproduce the entire original **67,372-byte
decoded Japanese MAINL EXE and original MAP byte-for-byte**, including
**all 677 original MZ relocations** and **679 original contextual CRT member
programs unchanged**. The working source CRT reaches **214 members and
90,869 original-equal CODE bytes**. This is source-bound working evidence,
not formal accepted-ledger promotion; no full cold replay was run.

Proof: `review_th03_mainl_after209_work.py ofstream-lifecycle`,
`tests.test_mainl_after209_work`, source-bound raw OBJ/LIB/EXE/MAP pairs,
real Borland writer logs and receipts under `.analysis/work/after209-*` and
`.analysis/work/mainl-after209-*`.
