# Original Japanese MAINL C++ standard iostream lifetime (ioststd)

Selected original Borland large-model CRT member **696**, `ioststd`, has five
native sections: **2,088 CODE** (`_TEXTA`), zero initialized DATA, **190 BSS**,
**12 INITDATA** and **12 EXITDATA** bytes. The original code public
`@Iostream_delete$qv` is at CODE+997. Seven BSS publics are `_cin` (+0),
`_cout` (+46), `_cerr` (+90), `_clog` (+134), and the three far streambuf
handles `___stdin_streambuf` (+178), `___stdout_streambuf` (+182),
`___stderr_streambuf` (+186); the 20 original ordered imports are preserved.

`src/mainl/crt/ioststd.asm` reconstructs all original standard stream
constructors, ownership, exception-cleanup dispatch, and destructors with
**real symbolic 8086 instructions** and typed Borland C++ metadata. CODE
contains four *non-executable* exception-tracking and class RTTI sections at
+0..215, +901..996, +1285..1342 and +1500..2087; these are original
`dw`/`dd` pointer and descriptor fields plus eleven genuine class-name
strings, **not instruction dumps or original executable byte arrays**.
Real code occupies +216..900, +997..1284 and +1343..1499. The two INITDATA
records call CODE+216 and +1343, and the two EXITDATA records call CODE+997
and +1436. Their Borland original priority bytes are preserved symbolically.

During source recovery, three original `FF /3` far indirect calls inside
`@Iostream_delete` initially assembled as `FF /2` near calls; explicitly
using `call dword ptr [bx]` restores the original bytes. Four original
GROUP-framed far pointers in the CODE exception descriptor at +1291/1301/
1311/1321 initially used TASM's TARGET frame. Writing the naturally
qualified `dd DGROUP:_cin` and corresponding stream object symbols produces
the **original GROUP frame**, without object editing. A zero-byte
`ASSUME CS:NOTHING` scope is required for seven BSS PUBLICs referenced
while CODE `_TEXTA` was previously assumed. The original `DGROUP` order
is `_BSS,_DATA` as expressed to TASM to recover the correct literal OMF
group membership `0cff02ff03`.

Native TASM 5.0 `/m /mx /kh32768 /t` now reproduces:

- **2,088/2,088 whole CODE bytes**, the 190-byte unmaterialized BSS and
  complete native BSS PUBLIC positions;
- all original **12/12 INITDATA** and **12/12 EXITDATA** bytes, including
  two far relocations in each, and original five-segment sizes/classes;
- **148/148 original OMF relocation sites, kinds, targets, addends and frame
  methods**, including 144 CODE fields and 2+2 startup/shutdown pointers.

The original compiler and TASM still serialize the FIXUPP records in
different **order**. The original complete native OBJ record stream is
**not** claimed byte-identical; the full CODE/INIT/EXIT byte and ordered
linked EXE/MAP evidence is independently established. No binary CODE
initializers, native object patches, linker patches or artificial padding.

`scripts/build_th03_mainl_after105_work.py ioststd` builds the actual CRT
slot 696 against the retained original Japanese 105-source carrier in **two
independent normal TASM/TLIB/TLINK rounds**. Both reproduce the **complete
67,372-byte decoded Japanese MAINL EXE and full original MAP byte-for-byte**
and all **677 ordered MZ relocations**, with the other **787 original vendor
member programs unchanged**. Working source CRT becomes **106 members and
51,293 original-equal CODE bytes**. The native builder/reviewer bind source
hashes, original selected OMF identities, both raw OBJ/LIB/EXE/MAP vectors,
actual writer phase logs, and the complete 62→105 receipt lineage.

Review with `scripts/review_th03_mainl_after105_work.py ioststd` and
`tests.test_mainl_after105_work`; raw native vectors and receipts are under
`.analysis/work/after105-ioststd-*` and
`.analysis/work/mainl-after105-ioststd-*`. This is working native source
reconstruction **not new accepted ledger credit** or full-source ownership;
**no full cold replay** was run.
