# Full cplx2 source-linked Japanese MAINL parity — after514

The original Japanese Borland CL.LIB cplx2 member (slot **209**)
is now completely source-built in the working CRT carrier.
The [maintained original 8086/x87 source](../src/mainl/crt/cplx2.asm)
contains the entire original **5,598-byte CODE**, all **22 complete
FAR public functions**, the private CODE+5575 startup zero initializer,
all 63 DATA slots (16 genuinely unmaterialized, 47 initialized),
empty BSS, and all six INITDATA bytes including the genuine
symbolic CODE+5575 pointer.

**A real full native link now passes.** The [after514 producer](../scripts/build_th03_mainl_after514_work.py)
starts from the independently retained after513 source carrier
(721 complete source-linked members), verifies the original
threaded Borland OMF against its native source using a strict
860-field symbolic comparator, and produces two fresh
TASM/TLIB/TLINK native rounds replacing original cplx2 with
the maintained assembly source. Both complete decoded Japanese
MAINL EXE and MAP equal their original targets **byte-for-byte**:
67,372 EXE bytes, including all **677 ordered MZ relocations**.
Both complete raw OBJ/LIB/EXE/MAP vectors, all writer logs,
parent receipt, source/driver hashes and original vendor objects
are retained. Working CRT advances from **721/893 to 722/893**
complete source-linked original members, with **193,584 original-
equal CODE bytes**, leaving 171 unchanged contextual vendor members.

**Why the old two-byte gap vanished:** TASM 5 SMART code generation
automatically compresses two Borland same-CODE five-byte direct FAR
CALL instructions in acos at original CODE+799/+984 to PUSH CS plus
near CALL. Rather than hiding the gap, the source uses NOSMART
immediately before each actual FAR CALL and SMART immediately
afterward. Both genuine original direct FAR calls and their
symbolic original OMF sites are now emitted. No target opcode
arrays, artificial padding or post-assembly OBJ patches are used.

**Further original OMF issue caught and fixed:** earlier twenty-
function scoped checks did not cover GROUPDEF. The original has
BSS-before-DATA GROUPDEF value 0aff02ff03, while the first full
source used the reverse. This was corrected in natural source
before successful integration. Original CL.LIB also lists unused
__turboFloat among 24 external symbols; declaring that
original unused import reproduces all **24 original EXTDEF
symbol identities**, without adding an invented runtime call.

**Raw OBJ differences remain explicit.** Original Borland OMF
uses frame method 4 for 734 x87 helper references; TASM EMUL
emits target-frame method 5. At original CODE+5561 the near
N_SCOPY@ imported call uses Borland target-frame method 5,
whereas TASM emits CODE-frame method 0. The original packet/
EXTDEF chronology can also differ even when all symbolic
targets agree. The independently reviewed **860/860 logical
OMF fixup sites, symbolic targets, kinds, widths and addends**
match, but the raw Borland OBJ record stream does not.
Exact decoded full EXE/MAP is not a claim of literal original
OBJ or formal Factory/canonical packed-file acceptance.

Independent reviewer:
scripts/review_th03_mainl_after514_work.py
(mode cplx2-all-original-functions-and-initdata).
Tests: tests.test_mainl_after514_work,
tests.test_cplx2_full_code_exact_native.
The complete source-bound receipt is stored at
.analysis/work/mainl-after514-cplx2-all-original-functions-and-initdata-build.json.
No full cold replay was performed.
