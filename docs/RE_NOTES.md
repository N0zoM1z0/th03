# TH03 reconstruction findings

Read the [current handoff](RE_HANDOFF.md) first. It owns current sizes,accepted
counts and open work. This file retains ABI findings and input relationships;
it is not another verification gate. Detailed native reviews retain bounded
proofs and qualified historical observations.

## Current source and build routes

The accepted MAINL library has28 source providers,including natural new/xalloc/
xmsg. Their six owners total2258 bytes:1563 CODE,659 inline DATA,30 other
initialized DATA and6 genuinely uninitialized file-storage bytes. The scoped
producer is BCC4.5 -O1 with pinned TC4 headers. Keep its profile separate from xx.
See [C++ native review](MAINL_EXCEPTION_CPP_REVIEW.md).

The complete xx TU is a separate,unaccepted29th provider. The normal product
uses BCC4.5 native `-c -y` objects followed by TLIB/TLINK. Separate `-S` output
supplies mangled names/return declarations only. Native source-file/LINNUM
records bind all50 bodies to actual transported definitions. Earlier S/TASM
miniatures remain separate diagnostics with different codegen/field order.
See [product review](MAINL_XX_PRODUCT_REVIEW.md) for complete current metrics.

Useful current recoveries include the complete1495-byte call-adapter bank and
88 literal ordered fields within the matching2822-byte native prefix;the
715/129-byte destruction bodies;the157-byte comparator;and handler880/frame56
with both argument-cleanup pairs. These are bounded observations within xx,
not additional accepted bytes. The remaining catch and Raise gaps stay open.

The native386 instruction intrinsics express individual unsupported operations.
Addresses retain compiler symbols and offsetof-derived offsets. BCC's native
local-member arithmetic requires the checked minus-offset spelling;the default
S/TASM path retains member syntax. Do not substitute an object patch or an
instruction-byte array for source. The native objects'187 fields retain emitted
1024-byte CODE-block order and descending sites inside each block. The handler's
changed field order follows its movement across0x2000;do not sort it away.

## Stable xx ABI observations

- Registration chain/runtime pointers are at SS:14/16. Registration DS/SI are
  at14/16 and its initial destructor count at26 is a DWORD. Descriptor free DS
  is at24 and the far callback at26. These are used prefixes,not proof of every
  original allocation size. Native and S/TASM ES callback operands have their
  own maintained spellings.
- Far toss takes32 argument bytes. Public C++ wrappers retain four far void
  pointers,three WORDs and a far filename;rethrow preserves SS-relative argument
  promotion. Name/file/line borrow runtime slots+1C/+16/+1A;the name points at
  runtime+28h and destination writes cap at127. Link the descriptor before
  copying;save/restore the DWORD count for construction;non-rethrow destroys
  the original temporary. The DOS exception code is0EEFFACEh.
- Global unwind with a null record initializes only code26h,flags2 and count0.
  Dispatch stops before the requested registration and treats every nonzero
  handler result as continue. Both five-byte empty hooks are actual procedures.
- Raise uses __saveregs,the used context prefix is204 bytes,and resume frames
  are48/26. ES:BX must retain the destination while the overlapping return frame
  is written. Default FF00 observations agree;alternate FF10 still exposes
  original80h/source84h. The390/342-byte frame difference and original
  BP[-134,-86) ownership are unproved. The16-bit resume path and full lifecycle
  have not been executed by the focused probes. See [throw review](MAINL_XX_THROW_REVIEW.md).
- Catch uses type at descriptor+4,payload+58,and copy/buffer flags+57/+56.
  Original-buffer destruction restores the saved DWORD SS:10 counter. Cleanup
  updates the head/context,returns far cdecl and leaves SS:14 unchanged. Catch
  arguments use wrapped SS:newBP+offset;near-pointer flag1000 supplies DS.
- Type matching retains public access3 through each base link,skips virtual
  entry flag8,and follows virtual entry4 through a segment-preserving WORD
  address. Friends are passed through rather than dereferenced;fspec is unused.
  Near-to-far fallback can succeed without comparing pointees;void fallback
  requires equal CV. The emergency far slot at runtime+20 is not new owned
  storage;free clears only WORD flag0001 at+4.
- Callback DS comes from runtime+6;incoming DS is restored on return. The
  16-bit fastcall this-argument is last:virtual-base copy(0,source,destination)
  uses AX0/BXsource/DXdestination for near pointers. Pascal this-last100 gates
  the relevant paths;fastthis80 uses SI or DS:SI. The four virtual-base SI
  transfers use register variables;nonvirtual ASM transfers preserve the final
  branch shape. Do not generalize one source spelling to every branch.
- Destruction's empty-table check compares offsetFFFF only. Global/initial
  counts are DWORDs;class counts+1A/+1C are WORDs. RETCTX20 remains active and
  DTCADJ100 returns the nonvirtual count. Base/member/DTT strides are8/6/10.
  Virtual-base offsets retain their segment;FAR_VPTR1000 selects a far vtable.
  The backward member loop reuses its search count,and virtual destruction
  leaves the release allocation pointer unchanged.
- GetTypeInfo131,private recursive search582 and DynamicCast357 have separate
  boundaries. Search virtual lists first;equal actual addresses merge public
  access and distinct addresses remain ambiguous. Downcast checks the actual
  source subobject without adding the cross-cast public-path condition.
  Typeinfo copy throws a null typeinfo pointer;assignment is a no-op. The two
  empty exception values share packed BSS+8/+9. _CurrExcContext has no later
  imported-jump-table fallback. Tail descriptors/vtables are data.

Keep original unchecked behavior. The focused callbacks and actual linked
memcpy observations resolve selected ABI questions;they do not establish a DOS
boot or ending playthrough. Do not import later Win32/Delphi/WITHVT/NEWXX,
friend or exception-specification behavior from reference RTL.

## Compiler findings and rejected routes

Local -O-v/-Ov restores induction behavior;the spelling -Ov- and option push/
pop are rejected. Local -O-m/-Om removes unwanted cached masks in the type
routines. Scoped -O1 for before must restore -Z- along with the common options;
an earlier failed-reset conclusion omitted it. The handler's filter declaration
after Global_unwind ends delayed argument popping without an optimizer change.

Retained controls distinguish failed alternatives from current source. TASM
NOSMART/JWasm/old compiler trials are not the normal product route. Ordinary
48-byte structure-return and class-constructor probes have the wrong argument
ABI for the empty hook. Reaching678 bytes with a catch switch still gives wrong
instructions. A private frame-object control reaches390 allocated bytes but
1156 CODE bytes,not1151,and does not prove the missing object's type. Concrete
class-pointer and assignment-local -Z controls still leave cleanup223.
None is adopted. See the current reviews and
`.analysis/work/xx-raise-storage-followup.json` for the latest bounded records.

## Other retained findings

New preserves zero-to-one size,retry through the installed far handler and
null-handler return. Xalloc keeps its static out-of-memory value,deep copies,
throw by value and delete-before-new assignment. Initialized DATA2607 and
uninitialized file DATA6 remain separate in MAINL's2613-byte DATA total.

DOS constructors return with near RET12. The null-first-entry DOSENV branch
counts one byte,writes two and returns aligned-offset+1;do not generalize it to
null-vector or first-empty-string branches. Exec933 includes671 CODE/262 CS
storage,a97-byte copied continuation and257 uninitialized work bytes;its
executor takes near12-byte arguments. Farheap1115 separates1103 CODE/12 CS
state and retains three genuine scratch WORDs. Joystick103 excludes the two
following zeros. Palette EQU aliases XOR immediate18B8;VSync's CS vector remains
DW?. MAIN still has EC2D90 versus00 and MZ header/layout differences despite
1553 agreeing relocation entries. Old cutscene3195/regist2720/root2488 aggregate
rows overlap accepted functions and must not be counted again.

## Inputs and continuation

Use the [handoff](RE_HANDOFF.md) and [working-file rules](RE_WORKFLOW.md#working-files)
for current inputs and cleanup. Preserve fixed Japanese targets/assets,installed
tools,the local Wine prefix,Ghidra/JDK,.venv,ReC98 and one working build per
product. The old-named
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar` is an
actual OP/MAINL source input. Re-attest a Ghidra database before using it;earlier
attestations are historical evidence,not permission to trust a changed DB.

Keep current build/review JSON and complete raw pairs,the exact transported
sources/wrappers/context fixtures,responses and native phase logs. This includes
accepted28-provider exception-native and its reused CRT pairs,plus all current
xx bank/full-TU miniatures and the normal xx product pair. Native xx product
has five output kinds and no TASM listing;S/TASM miniatures still need listings.
Actual reviewers,not a report's explicit path keys alone,define the live set.

Historical codegen records may survive removal of their duplicate code and
binaries. They are not extra acceptance gates or commands to rerun every turn.
Do not rewrite frozen historical runtime hashes or scripts/lib/zun.py's MAIN
binding. Native output/source changes need affected rebuilds;documentation and
cleanup need retained-input validation rather than full cold or ancestor replay.
