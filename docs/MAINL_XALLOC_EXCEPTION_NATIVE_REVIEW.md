# Complete original xalloc C++ exception boss and ordered Japanese MZ

`src/mainl/crt/xalloc.asm` is a **new source reconstruction** from the
original Japanese CL.LIB member **336**, not a mechanically included vendor
OBJ or a pre-existing accepted source. The member contains **513 complete
original CODE bytes**, no DATA/BSS, **two public far C++ APIs**, eight far
imports and 24 original logical relocations. The original CODE is restored
using actual 8086 instructions, typed Borland C++ exception records and
symbolic relocatable pointers, never opaque executable byte arrays.

| Original CODE offset | API / original content | Native source responsibility |
| ---: | --- | --- |
| 0 | `@xalloc@$bctr$qmx6stringui` | allocate/construct an xalloc and its owned xmsg; record its size and exception references |
| 91 | compiler exception metadata | two typed records and state pointers including `rtti_xalloc` |
| 127 | `@xalloc@raise$qv` | build a far C++ throw frame, invoke `xmsg` copy constructor, throw typed xalloc |
| 247 | private far xmsg copy thunk | copy object, keep derived size and increment reference count |
| 314 | `rtti_xalloc` | complete 66-byte typed derived class RTTI, destruct callback and base reference |
| 380 | private far destructor thunk | reference decrement, xmsg destructor, optional heap release |
| 457 | `rtti_xmsg` | complete 56-byte base class RTTI with original destructor import |

All original CODE and full relocation sites, widths, *frames*, targets and
addends match the pinned original OBJ in independent TASM comparison.
Literal **ordered OMF FIXUPP record order** and entire Borland OBJ record
serialization differ from TASM, and are explicitly **not** claimed exact.

## Why a byte-perfect OBJ can still link to a non-exact EXE

A forward-declared semantic source produced the correct complete CODE and
all 24 logical OMF fields. The complete executable body, MAP and unordered
677 DOS MZ relocations were also equal, but the **eight xalloc-associated
MZ relocation entries** were in the wrong sequence. Reversing seven large
original instruction/RTTI blocks helped but left the intra-block pairs and
triple in TASM's original forward order.

The final source uses `ORG` only at **eleven actual original executable or
typed metadata boundaries**, in descending-offset emission order:
`457,380,348,314,247,156,127,113,99,91,0`. No target CODE, filler or
binary modification is introduced. Those boundaries represent complete
exception descriptors, their saved state, one actual instruction boundary
inside the throw body and independently typed RTTI structures. Both native
TLINK rounds now emit the **exact original eight relocation entries** in
this literal order (each offset relative to the xalloc loaded-code base):

`489, 362, 346, 157, 136, 115, 101, 93`

All other 669 original entries remain in original order; the complete
Japanese 67,372-byte EXE and MAP are now byte-for-byte original.

## Two-round scoped native source evidence

`scripts/build_th03_mainl_after341_work.py xalloc-exception-boss` consumes
the existing **374-source** real Japanese CRT carrier, with all parent
source hashes and native OBJ/LIB/EXE/MAP receipts intact. It rebuilds only
this member from TASM source and produces the original 893-member library
with **375 complete source producers**, **518 unchanged contextual original
members**, and **121,362 original-equal logical CRT CODE bytes** (+513).
Two serialized normal TASM/TLIB/TLINK rounds are byte-identical and equal
to the original complete EXE/MAP, including all 677 ordered relocations.
Raw producer vectors and logs are retained under `.analysis/work/after341-*`,
reviewed by `scripts/review_th03_mainl_after341_work.py` and
`tests/test_mainl_after341_work.py`. No full cold replay was performed;
no Factory-accepted extent, packed-file credit or whole-game source exactness
is claimed from this working-only CRT evidence.
