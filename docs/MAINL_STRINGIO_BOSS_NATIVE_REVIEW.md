# Complete original Borland C++ string I/O boss: 11 APIs, typed RTTI

`src/mainl/crt/stringio.asm` is a complete source transcription of the
**original Japanese CL.LIB member 427** (`stringio`). Unlike a helper-only
or partial member, it reconstructs **1,466 original CODE bytes**, 50 original
relocation fields, 20 original external references, 11 far public C++ APIs,
and two complete compiler segments: `_TEXT` **110 bytes** and `_TEXTC`
**1,356 bytes**. The native `_DATA` and `_BSS` are empty and the original
DGROUP order is preserved. All executable instruction sequences are real
8086 source. After the last method, the native code segment contains typed
Borland `xalloc` and `xmsg` exception RTTI at `_TEXTC+1234` and `+1300`;
these are named symbolic declarations rather than embedded executable bytes.

The eleven original entry points, including exact offsets, are:

| `_TEXTC` offset | Original exported API | Coverage |
| ---: | --- | --- |
| 0 | `string::read_file` | far stream string read / delimiter delegation |
| 69 | `string::read_string` | stream to referenced string read |
| 138 | `string::read_line` | newline, optional whitespace and `__ctype` handling |
| 292 | `string::read_to_delim` | delimiter-mode scan and shared-reference clone |
| 361 | `string::read_token` | token-mode scan and shared-reference clone |
| 427 | `operator>>(istream&, string&)` | native extraction adapter |
| 455 | `operator<<(ostream&, string const&)` | native format and output |
| 517 | `getline(istream&, string&)` | first getline wrapper |
| 545 | `getline(istream&, string&, char)` | delimiter overload |
| 576 | `TStringRef::read_to_delim` | full buffer growth, delimiter, exception logic |
| 805 | `TStringRef::read_token` | full 429-byte token/buffer/ctype boss |

The 110-byte `_TEXT` region is likewise fully owned: an original exception
unwind thunk, two genuine exception-state descriptor records, and the
nonexported far xalloc destructor including its reference decrement and
conditional deallocation. The source calls the actual original Borland
constructors, I/O and string helpers, with the original 16-bit ABI.

## Verification issues resolved from the actual original OMF

The original compiler uses immediate **FAR `9A`** calls to locally defined
`TStringRef` methods, even though both methods share `_TEXTC`. Native TASM
otherwise converts these into `PUSH CS` and near calls. The source retains
that one literal x86 far-call opcode followed by a **symbolic, relocatable
far target**, not an opaque CODE-byte array. Five original local far-call
relocations occur at `_TEXTC+52,121,273,344,410` (four to `+576`, one to
`+805`). Imported Borland `__ctype`, `string::skip_white` and
`string::resize_inc` use explicit group-framed DATA references as in the
original program. The two exception frame state references at `_TEXTC+588`
and `+817` point to `_TEXT+13` and `+27`, not simply their descriptor bases.

The original `_TEXTC+1264` far RTTI destructor points to `_TEXT+33` and
`_TEXTC+1280` points to the `xmsg` RTTI at `+1300`. The entire 50-field
relocation population matches **segment, location, width, target, addend and
frame**, and every original materialized `_TEXT`/`_TEXTC` byte agrees.

`scripts/build_th03_mainl_after331_work.py stringio-boss` extends the
source/receipt-bound **342-member** CRT carrier, runs two independent
serialized native TASM/TLIB/TLINK rounds, and preserves all 893 member
programs. Both rounds independently reproduce the full original decoded
Japanese MAINL **67,372-byte EXE and MAP**, with all **677 ordered DOS MZ
relocations**. The resulting CRT has **342 source-backed programs**,
**550 unchanged contextual original programs**, and **113,505 original-equal
CRT CODE bytes**, an increase of **1,466**. Raw OBJ/LIB/EXE/MAP and writer
logs are retained under `.analysis/work/after331-*`, SHA-bound to the live
source and inherited evidence and rechecked by the reviewer and
`tests.test_mainl_after331_work` without a new full cold replay.

The **literal original OMF FIXUPP record order and whole Borland OBJ program
serialization still differ** from the TASM program. This link-exact
working-source expansion does not create any Factory-accepted source extent
or canonical packed-file unit credit.

## Reconciliation of two independent source-bound additions

The earlier `gpt-web: recover all thirteen locale isctype APIs and exact
native link` checkpoint already owned the `after330` source-bound driver,
its `locale-isctype-family` receipts and the full 333-byte `is` CRT member.
The first stringio publication accidentally reused that exact driver and
test filename, which made the prior locale receipt non-reviewable even
though its raw native rounds and `is.asm` source remained correct. This was
a genuine integration defect, not a failure of either reconstructed module.

The original `scripts/{build,review}_th03_mainl_after330_work.py` and
`tests/test_mainl_after330_work.py` have therefore been **restored
byte-for-byte from their existing commit**. The existing original
`locale-isctype-family` native receipts were validated without replay.
The unchanged 1,466-byte `stringio.asm` is now built and source-bound in
**after331**, taking both parent native rounds as its complete inherited
library and retaining the new pair of OBJ/LIB/EXE/MAP/link logs. The
combined **343-member** source chain has been confirmed by both independent
Japanese EXE/MAP native rounds and the exact source/reviewer hash DAG.
This reconciliation preserves both complete source units, rather than
silently displacing the earlier 13-API member with a later one.
