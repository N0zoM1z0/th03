# Complete original `string` operator+ boss — 999 CODE and eight RTTI types

The pinned Japanese CL.LIB member **418** (`oprplus`) is now reconstructed in
natural 8086 source at `src/mainl/crt/oprplus.asm`. It is a full original C++
operator+ implementation, including the entire reference-counted string
concatenation path, length/capacity handling, allocation/constructor and
exception cleanup, **not** an API forwarding stub or an opaque CODE byte
array. The original `_TEXT` contains **253 bytes** of far exception-unwind,
compiler exception metadata and two complete far destructor/copy helpers.
The original `_TEXTC` contains **746 bytes**, including the complete far
`@$badd$qnxcmx6string` at +0 and eight original typed RTTI descriptors:
`TStringRef *` (+330), `string *` (+353), `string` (+372),
`string::lengtherror` (+430), `xalloc` (+508), `xmsg` (+574),
`TStringRef` (+630) and `TReference` (+700). Both DATA and BSS are empty.

The entire **999-byte original CODE payload**, the single original far C++
public, all 11 original imported function names, `_TEXT`/`_DATA`/`_BSS`/
`_TEXTC` segment geometry, DGROUP record `0aff02ff03`, and all **38 original
FIXUPP fields match literally**. This includes the original *record order*,
width, target, frame and addend — not just the sorted logical relocation set.
The original Japanese BCC emits 16 exception/cleanup FIXUPPs and 22 C++
method/RTTI fixups in descending position order in each respective CODE
LEDATA block. The source emits real 8086 and typed `dw`/`dd` statements at
their actual original positions using `ORG`, reproducing the original OMF
FIXUPP ordering without binary patches, synthetic executable padding or
literal machine CODE arrays. Full Borland OMF member record serialization
still differs in ancillary metadata and is **not** claimed byte-exact.

`scripts/build_th03_mainl_after365_work.py string-plus-exception-boss`
extends the already verified **431-source** Japanese MAINL carrier (including
PC-98 function keys and MBCS `strchr`). It compiles only the complete new
`oprplus` source, then rebuilds the original **893-slot** CRT library and
complete MAINL link in **two independent native TASM/TLIB/TLINK rounds**.
Both exactly reproduce the pinned original decoded Japanese **67,372-byte
EXE and complete MAP** byte-for-byte, including all **677 ordered DOS MZ
relocations**. The source-bound working carrier now includes **432 full
original-equal CRT members**, **461 unchanged contextual vendor members** and
**137,835 source-compiled original-equal CRT CODE bytes**, an increase of
**999**. Retained full original and native OBJ/LIB/EXE/MAP rounds, phase logs,
source/driver/parent hashes and reviewer checks live under
`.analysis/work/after365-*`, `scripts/review_th03_mainl_after365_work.py`
and `tests/test_mainl_after365_work.py`.

This is working-source verification, not a formal Factory accepted extent,
canonical packed-file unit credit or whole-game source exactness claim.
No full cold replay was run.
