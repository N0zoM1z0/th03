# MAINL CRT reconstruction

Current MAINL coverage is described by the [generated progress](../../../docs/PROGRESS.md)
and [current composition review](../../../docs/CURRENT_LINKED_BUILD_REVIEW.md).
The current project route has 29 source providers in its original-order
893-member library; the other members retain their compiler-supplier context.

Natural `new.cpp`, `xalloc.cpp` and `xmsg.cpp` use the reviewed BCC4.5 `-O1`
route. `xx.cpp` now provides the complete DOS exception/RTTI graph in one TU:
all 50 functions, complete CODE/DATA and ordered fields have independent native
proofs and participate in the current MAINL rebuild. It is the accepted 29th
provider, replacing the earlier unmatched working-source candidate. See the
[C++ native review](../../../docs/MAINL_EXCEPTION_CPP_REVIEW.md) and
[xx product review](../../../docs/MAINL_XX_PRODUCT_REVIEW.md).

The current shared runtime route freshly assembles all displayed CL contributors
across MAIN/OP/MAINL and composes them with the current project objects. It
retains the known `setvbuf` operand-field order gap; the composition review
contains its current commands and complete comparison scope.

Historical source-linked library totals describe earlier experiments, not the
current accepted owner inventory. Native OBJ identity also includes record
packing and field order; a target-equal final EXE alone cannot establish those
properties for an individual library member.

The accepted provider chain includes
[buffered I/O](../../../docs/MAINL_STDIO_NATIVE_REVIEW.md),
[DOS paths](../../../docs/MAINL_PATH_NATIVE_REVIEW.md),
[DOSCMD/DOSENV](../../../docs/MAINL_DOSCONSTRUCT_NATIVE_REVIEW.md),
[load preparation](../../../docs/MAINL_LOADPROG_NATIVE_REVIEW.md),
[overlay execution](../../../docs/MAINL_EXEC_NATIVE_REVIEW.md),
[far heap](../../../docs/MAINL_FARHEAP_NATIVE_REVIEW.md) and
[the original six providers](../../../docs/MAINL_CRT_NATIVE_REVIEW.md).
The full cold recipe retains its earlier six-provider graph;scoped links reuse
validated current pairs to compose the newer library. Do not replay the cold
chain solely to refresh documentation.

Preserve 16-bit widths,packing,segments,calling conventions and compile/link
order. The loader's near caller-pop12 executor and constructors' near RET12
are different ABIs. Keep the original unchecked behavior and intentional DOS
quirks,including FFFF resize collision and signed/wrapping arithmetic.

`fbrk.asm` is the maintained semantic ASM provider;`fbrk.c` is an unmatched
high-level candidate. Link one FBRK implementation. No original library object,
opcode array,padding or OMF patch supplies implementation bytes. The old
`provenance.json` and early replay reports describe historical checkpoints;
they are not the current source-acceptance summary.

Run affected reviews and validate unchanged raw pairs. Historical CPU scenario
counts and failed native variants are supporting records,not new source progress
or per-change test requirements.
