# Japanese MAINL original `constrea`: full 3,241-byte C++ console stream boss

The selected original Borland 16-bit large-model CRT member is **340**
`constrea`, covering **3,241 CODE bytes, 92 initialized DATA bytes, and zero
BSS bytes**. Its full Borland C++ ABI includes **17 CODE publics**, among
them the complete `conbuf` construction, `overflow`, `makeActive`,
`makeInactive`, `swap`, the `constream` constructor, manipulators `clreol`,
`highvideo`, `lowvideo`, `normvideo`, `delline`, `insline`, and cursor,
attribute, position, background and color methods. The original DATA also
exports **`@conbuf@current` at +0** and **`@constream@isCon_` at +4**.
These are part of source ownership and are separately verified, not inferred
from the linked result.

`src/mainl/crt/constrea.asm` contains original 8086 source instructions,
all **35 original ordered C++ EXTDEF dependencies**, and real type-structured
Borland RTTI/vtable metadata in CODE and DATA. CODE has method instructions
through +2650, RTTI/class descriptors at +2651..2798, destructor functions
at +2799..3060, and further RTTI at +3061..3240. It retains class names
`conbuf`, `constream`, `ios`, `ostream`, `streambuf` as actual strings. Original
relocatable four-byte far vtable entries are symbolic `dd method`/`dd class`
declarations, not opaque executable-byte initializers. All 92 DATA bytes,
including the far callable vtable entries, are modeled as typed fields.

Important genuine TASM/8086 pitfalls resolved during recovery:

- Fourteen original **indirect far virtual calls** were initially emitted as
  near by untyped `call [bx+...]`. Explicit `call dword ptr [bx+...]` restores
  their original `FF /3` encoding instead of `FF /2` without patching bytes.
- Original `LES` through `ES:[bx+2]` requires explicit `dword ptr` memory
  in TASM. It is not equivalent to an immediate `ptr` expression.
- Type info and virtual methods stored in the CODE segment are referenced
  by DATA far pointers. A zero-byte `ASSUME CS:NOTHING` directive for the
  original DATA declarations preserves the valid CODE far relocation context.
- One original `conbuf` RTTI string ends in a genuine **double NUL** marker;
  its precise descriptor length and the virtual-pointer offsets were derived
  from the active original OMF rather than forcing a target byte count.

Native TASM `/m /mx /kh32768 /t` reconstructs **all 3,241/3,241 original
CODE bytes** (including typed RTTI), **92/92 original DATA bytes**, both DATA
publics, 17 original CODE public positions, ordered 35 original imports,
segment/group layout and **all 152/152 original native fixup sites, widths,
local/external targets, addends and even frame methods**. Of these, **134
fields are in CODE** and **18 far callable pointers are in DATA**. The
original BCC FIXUPP enumeration differs from TASM's, so literal record-stream
identity of the entire object is deliberately **not claimed**.

Product proof: `scripts/build_th03_mainl_after104_work.py constrea` inherits
the current source-bound **104-member Japanese MAINL CRT**, reconstructs this
real original slot and the unchanged **788 vendor CRT member programs**, and
runs **two independent normal TASM/TLIB/TLINK rounds**. Both exactly reproduce
the complete original **67,372-byte decoded Japanese MAINL EXE** and original
MAP, including all **677 MZ relocations**. Working CRT now contains **105
source-built members / 49,205 original-equal CODE bytes**. This is working
native source evidence only, *not* formally accepted ledger credit, and
no full cold replay ran.

Source-bound raw OBJ/LIB/EXE/MAP pairs, actual native tool phase logs, build
and review receipts remain under `.analysis/work/after104-constrea-*` and
`.analysis/work/mainl-after104-constrea-*`. Verify with
`review_th03_mainl_after104_work.py constrea` and
`tests.test_mainl_after104_work`.
