# MAINL xx DOS type compatibility and descriptor allocation

This review describes a retained earlier miniature,not the current full-TU
link. The maintained xx.cpp now links through the normal library as an unaccepted
candidate;see [current product review](MAINL_XX_PRODUCT_REVIEW.md). Miniature
CODE/provider counts below remain specific to that diagnostic. Current overall
source presence is250 extents/60,028 gross bytes;accepted MAINL is unchanged.

`src/mainl/crt/xx_type_match.inl` recovers the contiguous58DB..5D3B bank of the
original DOS `xx.cpp`. It follows the private type comparator and precedes the
call adapters. Its1121 bytes are all instructions in five complete procedures;
there are no inline tables or MZ segment words. Three actual far library fields
resolve the whole original payload from OMF/MAP to the fixed Japanese target.
Source presence at that checkpoint was246 extents/55,702 gross bytes. Accepted MAINL remains211
extents/288 procedures/36,946 bytes,with zero new exact credit.

| Procedure | Original address | Instruction bytes | Return |
| --- | --- | ---: | --- |
| findBaseType | 58DB | 339 | near cdecl |
| compatibleType | 5A2E | 372 | near cdecl |
| allocExceptMem | 5BA2 | 92 | far cdecl |
| freeExceptMem | 5BFE | 57 | far cdecl |
| typeIDcaught | 5C37 | 261 | near cdecl |

Direct decoding verifies full returns and branches,without treating symbol gaps
as bodies. The three original fields retain literal emission order:abort,malloc,
free. No database observations are needed. The source has natural typed control
flow and explicit16-bit masks; it introduces no padding,opcode arrays or object
patches. All five procedures retain private linkage. Two actual near calls from
the handler matcher/dispatcher now enter the real typeIDcaught body.

Base lookup first walks the virtual list,skipping entry flag8,then the ordinary
list. It follows8-byte entries and requires low access bits3 on every link in
the path. Recursion retains the accumulated accessibility. The friend-list
argument is passed onward but never dereferenced by these helpers. A private
link therefore remains rejected even with a valid friend list containing the
destination. The source preserves that behavior.

Compatibility iterates through pointer/array descriptors,compares DWORD array
counts and uses exact matching after indirection. Pointer qualifiers use3300:
CV0300 plus near/far3000. A native width fallback returns success for a source
with near bit1000 without comparing its pointee with the destination's pointee.
The target/source probe confirms Base near* can match unrelated Middle far*
through this path,with zero calls to the name comparator. This behavior is
preserved rather than replaced by later language/runtime rules.

typeIDcaught handles references,pointer widths and the zero-pointer flag. Its
void-pointer fallback requires exactly equal CV bits. Equal CV succeeds; adding
const to the destination void pointer in the observed differing-pointee case
fails. The original fspec argument is not read,although its caller and16-byte
near-cdecl argument list remain intact. The older generic comment about special
throw-specification rules does not establish a DOS branch that is absent from
the actual instructions. The later [xx implementation](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/SOURCE/EXCEPT/XX.CPP)
is structural context; its broader CV fallback is not copied.

Allocation first calls the original malloc interface. Its existing failure path
uses a runtime-provided128-byte emergency buffer,with occupied flag0001 in the WORD
flags at runtime+4; oversized or already-occupied fallback aborts. Freeing that
same far pointer clears only that flag; other pointers call free. The
buffer pointer lives at runtime+20h. Only this observed slot is accessed; no
fields or padding are invented for the unknown intervening runtime storage,
and no emergency buffer storage is claimed by this bank. A native free probe
changes flagsA501 toA500 and restores the far-cdecl caller frame. No allocation
failure or heap behavior is modeled.

The miniature uses the existing scoped BCC4.5 `-O2-pg -Os -O-i -Z- -S`,actual
TASM5 and TLINK. An independent profile supplies the added source/wrapper and
records its own driver hash alongside the common builder hash. This extension
keeps future source profiles separate from the shared recipe. The common entry
change refreshed the earlier four affected miniatures once. Their current
receipt and whole raw pair are validated and reused without ancestor runtime
replay inside this review. The211-owner publication/verifier inputs and938 cold
outputs remain validated and unchanged; no full cold or normal-library rebuild
is performed.

Two rounds repeat complete generated ASM,two-OBJ,EXE and MAP vectors. Original
listing page clocks are retained separately; all64 available SDK headers are
bound. Candidate bank is1119 bytes with341/368/92/57/261-byte bodies. Whole
candidate CODE is8352,empty DATA and8 existing callback BSS bytes. Its16 remaining
interfaces are unresolved surrounding library/runtime providers in this
miniature. Original covered ranges now total8314 bytes in two separate spans,
583E..6312 and6CEF..8293. Throw/unwind and RTTI/front code are excluded from this miniature;they are
recovered in the later complete TU. Its normal-library candidate is linked,while
complete raw equality and ordered whole-TU layout remain open.

Focused native probes establish public/private nested base matching,that width
shortcut,void CV behavior,and emergency-slot release. Every target/source pair
agrees on return value,actual name-comparison calls and DS/SS/BP/SI/DI with
SPFF02 for near matching orFF04 for far free. All unresolved providers remain
traps and are never executed. These observations are not an exhaustive type
matrix or a physical DOS execution claim.

## Current compatibility-loop recovery

The maintained compatibleType now has the original372 instruction bytes and
four-byte stack frame. Local `-O-m`,restored with `-Om` afterward,removes the
extra invariant WORD that cached the common source/destination mask bits.
The native loop recomputes those bits for the array test.

The source tests the masked CV subset on both operands. Its near-pointer width
shortcut uses explicit success/failure returns,and array wildcard checking uses
bitwise OR of both DWORD counts. Both descriptors are read even when the first
count is nonzero,as in the target. The final class/base path returns the helper
result inside a positive condition,then falls through to the shared failure
return. These natural expressions recover the original instruction and branch
layout without additional storage or object editing.

The complete unlinked372-byte body differs at only two bytes,+12Ah and+165h,
inside the calls at+129h and+164h. All368 bytes outside the four CALL operand
bytes agree literally. Both calls resolve independently to the actual source
sameTypeID and findBaseType procedures;the first retains its PUSH CS/far-return
ABI. Original and candidate literal field vectors are both empty. The full-TU
review repeats this comparison against its real compiler procedure identities.
Complete raw object and linked-body equality remain open because helper layout
differs;there is no new exact credit.

The updated type miniature retains341/372/92/57/261-byte procedures and a1123-byte
bank,versus original339/372/92/57/261 and1121. The type-loop change reused the
earlier catch/call/destruction baseline;the later handler declaration recovery
refreshed all affected xx producers. The accepted211-owner publication and cold
pair remain separate and unchanged.
