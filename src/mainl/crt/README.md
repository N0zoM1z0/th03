# MAINL CRT reconstruction

The accepted normal893-member library has28 source providers. Natural
`new.cpp`,`xalloc.cpp` and `xmsg.cpp` are accepted through the scoped BCC4.5 -O1
route;their six owners total2258 bytes. See the
[C++ native review](../../../docs/MAINL_EXCEPTION_CPP_REVIEW.md),
[current handoff](../../../docs/RE_HANDOFF.md) and current publication in
`config/mainl_work/scoped_acceptance.json` for authoritative scope and limits.
Earlier unmatched C++ trials are historical controls.

`xx.cpp` composes the complete DOS exception/RTTI graph in one TU. It is a
separate,unaccepted29th provider in the normal-library candidate. That route
uses actual native BCC `-c -y` output followed by TLIB/TLINK;separate `-S` output
supplies names only. The retained S/TASM miniatures have their own codegen and
field order. See the [xx product review](../../../docs/MAINL_XX_PRODUCT_REVIEW.md).
Whole xx and whole-product source exactness remain open.

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
