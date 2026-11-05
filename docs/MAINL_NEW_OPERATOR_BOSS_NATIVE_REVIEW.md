# Complete original Borland C++ operator new, handlers and INIT/EXIT runtime

`src/mainl/crt/new.asm` reconstructs the **entire** original Japanese
Borland CL.LIB member **90**: 754 original CODE bytes, a 24-byte DATA
segment, empty BSS, six-byte `_INIT_` and six-byte `_EXIT_` records, and
**49 original relocation fields**. This member is a complete C++ runtime
module, not merely an allocation leaf. Its three original public far entry
points are `@xnew_handler$qv` at CODE+28,
`@set_new_handler$qnqv$v` at CODE+135, and `@$bnew$qui` at CODE+181.

The CODE also contains the native xmsg copy helper at +262, typed Borland
exception descriptors at +0..27 and +329..366, original initialization
function at +367, exit handler at +458, full `string`, `xalloc`, `xmsg`
RTTI records at +497,+555,+698 and the native exception object destructor
at +621. All executable paths are real 8086 instructions; exception state
and class RTTI are genuine named `dw`/`dd` declarations with relocatable
far pointers, rather than raw machine-code arrays.

The original DATA word/dword program is **sparse**: CODE references the
six-byte `___xalloc` object at DATA+0, but those first six bytes are truly
uninitialized in the original OMF LEDATA, even though DATA's declared size
is 24. The four bytes at DATA+6 hold the original far `__new_handler`
address (CODE+28), and the remaining 14 are the real `Out of memory` NUL
string. The `_INIT_` and `_EXIT_` records carry original `2001h` priority
and far pointer relocations to actual CODE+367 and CODE+458 respectively.
This is not an invented BSS region or a synthetic init/exit program.

## Three source/assembler parity corrections

First, TASM requires explicit `word ptr` for the six direct handler word
loads and stores; the exact original 8086 instructions remain the same.
Second, the exception catch metadata at CODE+335 refers to `___xalloc`
using **DGROUP frame1**, while TASM defaults to TARGET frame5. Writing the
typed source `dd DGROUP:___xalloc` restores the exact original frame,
location and addend. No binary postprocessing is involved.

Third, the actual original BCC object has a single large `_TEXT` LEDATA
block followed by its **descending-location FIXUPP record**. Ordinary
forward source produces every original CODE/DATA/INIT/EXIT byte and all 49
logical fields, but the complete Japanese EXE differs in **13 MZ relocation
entries**. The final source emits the original 8086 and typed RTTI
statements at their original locations using `ORG` at real
relocation-bearing instruction/metadata boundaries in descending order.
This retains natural code semantics and literal **all 49 ordered original
FIXUPP fields**. Neither executable bytes nor OMF records were patched or
synthesized to manufacture the final image. The complete original Borland
OMF member program remains different from TASM's nonsemantic record
serialization, despite the ordered FIXUPPs and exact linked image.

## Two-round native Japanese link proof

`scripts/build_th03_mainl_after347_work.py new-operator-exception-boss`
uses the verified **389-source** inherited original CRT chain (including
heap break and 10 MBCS classes). It reassembles the entire `new` source,
rebuilds the 893-slot CRT and links **twice** through original native
TASM/TLIB/TLINK. Both retained OBJ/LIB/EXE/MAP output vectors and writer
logs are SHA-bound to source, original library programs and parent receipts.
They are byte-for-byte equal to the original Japanese decoded **67,372-byte
MAINL EXE/MAP**, including all **677 ordered DOS MZ relocations**. The
working CRT source chain now contains **390 complete source producers**,
**503 unchanged contextual originals**, and **126,150 original-equal
logical CODE bytes** (+754), plus the restored DATA/INIT/EXIT above.

Review with `scripts/review_th03_mainl_after347_work.py` and
`tests/test_mainl_after347_work.py`. This is a working-source gain, **not**
formal Factory acceptance, canonical packed-file credit or a complete
game source ownership claim. No full cold replay was run.
