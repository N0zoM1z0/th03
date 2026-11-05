# Five complete Borland C++ substring/find APIs: native Japanese MAINL

`src/mainl/crt/find1.asm` reconstructs the **entire original Japanese
CL.LIB member 398**, not only a wrapper, in semantic native 8086 source.
The member contains 83 bytes of original `_TEXT` CODE, 1,296 bytes of
`_TEXTC` CODE (**1,379 total**), zero initialized DATA and BSS, 14 original
imports and **52 original OMF relocation fields**. All five exported far C++
methods and their exact original entry offsets are preserved:

| `_TEXTC` offset | Exported C++ method | Full original behavior |
| ---: | --- | --- |
| 0 | `string::substring(const char *, unsigned)` | construct substring and delegate bounded range search |
| 181 | second `string::substring` overload | create bounded substring with exception state |
| 402 | `string::find(string &, unsigned)` | delegate to string find index |
| 473 | `string::find_index` | index-aware and case-policy-aware search |
| 684 | `string::find_case_index` | complete case-insensitive compare and long-index arithmetic |

The original `_TEXT+0` is an executable far exception-unwind thunk. The
remainder of that CODE segment contains **three actual 10-byte exception
cleanup frames** at +5, +15, +25, **three typed C++ catch records** at +35,
+45, +55 and a real exception-state record at +65..82. All original 16:16
references to the internal state words, including original interior offsets
**+9, +19, +29 and +69**, are represented using genuine named labels and
relocatable far addresses. The string RTTI is a genuine 58-byte typed
structure at `_TEXTC+1238`, including the original far destructor pointer.
There are no opaque machine CODE arrays, padding bytes or binary/OBJ patches.

## Verified original-codegen corrections

The original Borland exception-state pointers at four sites inside `_TEXTC`
refer to offsets +9,+19,+29,+69, **not** to the starts of their containing
records (+5,+15,+25,+65). The three private exception frame pointers at
`_TEXT+9,+19,+29` are genuine four-byte far OMF relocations, not paired
near offsets plus literal zeros. Both substring methods also require the
original sign-extended `CMP DX,-1` encoding; TASM's `byte -1` spelling
would materialize an incorrect immediate byte. Each case was corrected
against the original OMF relocation and original 8086 instructions, not
from historical notes or unverified assumptions.

The authoritative original Japanese BCC object emits `_TEXT` FIXUPPs in
**descending offset order**, then `_TEXTC` in the two original LEDATA
fragments 0..1023 and 1024..1295, with the fields **descending inside each
fragment**. The source therefore emits genuine instruction/typed-data blocks
at their original offsets in the original record-specific order. Native TASM
reproduces all **52 original FIXUPPs literally in site, order, frame, target
and addend**, and all **1,379 CODE bytes**. Full original Borland program
record equality is not claimed; unrelated OMF serialization differs.

`scripts/build_th03_mainl_after351_work.py string-find-boss` consumes the
**397-source** parent, reassembles this complete member, reconstructs the
893-position original library and performs **two independent serialized
native TASM/TLIB/TLINK rounds**, without a full cold replay. Both reproduce
the exact decoded Japanese **67,372-byte MAINL EXE and MAP**, including all
**677 DOS MZ relocations in original order**. The source-bound working CRT
now has **398 complete source members**, **495 unchanged contextual original
programs**, and **128,772 original-equal CRT CODE bytes** (+1,379). Every
native OBJ/LIB/EXE/MAP and writer log is retained under
`.analysis/work/after351-*`; the scoped reviewer and direct OMF/MZ tests are
`scripts/review_th03_mainl_after351_work.py` and
`tests/test_mainl_after351_work.py`.

This constitutes scoped **working-source** proof, not a new formal Factory
accepted extent, canonical packed-file ownership or whole-game exactness.
