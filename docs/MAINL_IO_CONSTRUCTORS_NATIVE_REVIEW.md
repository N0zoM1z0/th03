# Japanese TH03 C++ `istream` / `ostream` constructors: complete RTTI ownership

Two genuinely selected Borland large-model CRT members have been restored as
complete **symbolic 8086 code and typed C++ exception/RTTI metadata**:

| Original member slot | Module | CODE | DATA | Far C++ constructor PUBLIC offsets |
| ---: | --- | ---: | ---: | --- |
| 788 | `istx` | 971 | 20 | `istream` constructor variants +36 and +329 |
| 824 | `ostx` | 927 | 20 | `ostream` constructor variants +36 and +306 |

`src/mainl/crt/istx.asm` and `src/mainl/crt/ostx.asm` reproduce **both complete
original far constructor bodies in each member**, including original
exception block setup/exit, ownership of near/far dynamically allocated
`strstreambuf` and `filebuf`, `ios` initialization/destruction and `istream`
tie/skip handling. The 185 and 168 true 8086 instructions have symbolic
branches; CODE carries separately decoded exception frames at +0/+293
(`istx`) or +0/+270 (`ostx`) and separate C++ class RTTI/exception descriptors
at +596 (`istx`) and +552 (`ostx`). These non-executable sections are typed
`dw`/`dd` pointer/descriptor fields and genuine `filebuf`, `strstreambuf`,
`streambuf`, `istream`/`ostream`, and `ios` class-name strings—**not copied
executable CODE arrays or patched object bytes**. The real 20-byte DATA
section in each contains three far destructor/type pointers and original
exception unwind fields.

**Selected member and native TASM proof:** `/m /mx /kh32768 /t` reproduces
**971/971 + 927/927 complete original CODE bytes**, both **20/20 DATA**
sections, empty BSS, all original PUBLIC locations and 15/13 ordered
imports, the `_TEXTA/_DATA/_BSS` structure and original DGROUP
`08ff02ff03`. All **47 + 44 = 91 OMF relocated fields** match the genuine
original CRT at the same segment and site, with their exact type, target,
addend, width and **frame method**. Borland BCC and TASM differ in the
literal ordered FIXUPP *record sequence*, so whole original OBJ identity
is **not** claimed. No artificial executable padding or object editing.

`scripts/build_th03_mainl_after149_work.py constructors` begins from the
complete source-bound 149-source original Japanese CRT and rebuilds the
two actual member slots in **two independent normal TASM/TLIB/TLINK rounds**.
Both reconstruct the **entire original 67,372-byte decoded Japanese MAINL
EXE and original MAP byte-for-byte**, including all **677 ordered MZ
relocations**, leaving the other **742 original vendor member programs
unchanged**. Working-source CRT is now **151 source-built members / 67,906
original-equal CODE bytes**. There is no formal accepted-ledger promotion;
**no full cold replay** was performed.

Provenance: `review_th03_mainl_after149_work.py constructors`,
`tests.test_mainl_after149_work`, raw OBJ/LIB/EXE/MAP pairs, source-hash-bound
receipts and actual Borland writer logs under `.analysis/work/after149-*`
and `.analysis/work/mainl-after149-*`.
