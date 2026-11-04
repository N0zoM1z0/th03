# Original Japanese MAINL: 18 complete multibyte and JIS CRT algorithms

Eighteen **distinct selected** original Japanese Borland 16-bit large-model
CRT members have now been recovered as whole symbolic 8086 sources. They
implement the PC-98 Japanese multibyte character and JIS/JMS conversion
semantics, not just forwarder wrappers:

| Original CRT slot | Module | Original CODE | Purpose |
| ---: | --- | ---: | --- |
| 673 | `FMBSNBSE` | 143 | Far multibyte counted byte set |
| 617 | `MBSNBSET` | 143 | Multibyte counted byte set |
| 685 | `FMBSSET` | 127 | Far multibyte string set |
| 629 | `MBSSET` | 127 | Multibyte string set |
| 600 | `MBJMSJIS` | 64 | Japanese machine-set to JIS conversion |
| 599 | `MBJISJMS` | 48 | JIS to machine-set conversion |
| 635 | `MBTOHIRA` | 40 | Multibyte to hiragana |
| 636 | `MBTOKATA` | 31 | Multibyte to katakana |
| 640 | `JISALPHA` | 39 | JIS alphabet classification |
| 644 | `JISUPPER` | 29 | JIS uppercase classification |
| 642 | `JISLOWER` | 29 | JIS lowercase classification |
| 641 | `JISDIGIT` | 29 | JIS digit classification |
| 643 | `JISSPACE` | 23 | JIS space classification |
| 650 | `JTOLOWER` | 33 | Japanese character lowercase conversion |
| 651 | `JTOUPPER` | 33 | Japanese character uppercase conversion |
| 597 | `MBISSYM` | 34 | Multibyte symbol classification |
| 589 | `MBISKATA` | 34 | Multibyte katakana classification |
| 588 | `MBISHIRA` | 29 | Multibyte hiragana classification |

Each `src/mainl/crt/*.asm` source contains genuine **semantic 8086
instructions with symbolic control flow**, including the original near/far
memory and 16-bit value behavior, rather than a copied executable CODE byte
array, artificial padding or post-assembled object manipulation. Sources
preserve the actual original CRT PUBLIC/EXTDEF inventories and the original
DGROUP ordering for each member; `MBJMSJIS`/`MBJISJMS` use a different
original group order from most JIS classification members.

Each distinct actual original CRT slot was checked, not inferred from filenames
or older notes. Native TASM 5.0 `/m /mx /kh32768 /t` reconstructs **all
1,035/1,035 original CODE bytes**, empty DATA/BSS, original public offsets,
empty imports, and each selected original member's **literally empty OMF
FIXUPP inventory**. This proves zero missing relocations, not byte-identical
unexamined OMF record classes.

`scripts/build_th03_mainl_after214_work.py jis-multibyte-leaves` reuses the
source/parent/driver-hash-bound original **214-source Japanese CRT** and
recompiles the 18 actual selected slots in **two independent normal
TASM/TLIB/TLINK rounds**. Both reproduce the **complete original 67,372-byte
decoded Japanese MAINL EXE and original MAP byte-for-byte**, including all
**677 original ordered DOS MZ relocations**; **661 original vendor CRT program
records remain unchanged**. Working-source CRT reaches **232 genuine
source-compiled members / 91,904 original-equal CODE bytes**. No full cold
replay was run and no new formally accepted-ledger credit is claimed.

Review with `review_th03_mainl_after214_work.py jis-multibyte-leaves` and
`tests.test_mainl_after214_work`. Retained source-bound native OBJ/LIB/EXE/MAP
vectors, their hashes and the actual native writer logs are under
`.analysis/work/after214-*` and `.analysis/work/mainl-after214-*`.
