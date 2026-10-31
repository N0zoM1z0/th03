# MAINL xx local unwind and dispatch source candidate

This review describes a retained earlier miniature,not the current full-TU
link. The maintained xx.cpp now links through the normal library as an unaccepted
candidate;see [current product review](MAINL_XX_PRODUCT_REVIEW.md). Miniature
CODE/provider counts below remain specific to that diagnostic. Current overall
source presence is250 extents/60,028 gross bytes;accepted MAINL is unchanged.

`src/mainl/crt/xx_dispatch.inl` recovers a bounded bank from the original
monolithic `xx.cpp` TU. It is an include rather than a proposed new product TU.
The bank at0000:72B3 spans1565 bytes:1533 instruction bytes in five procedures
and32 bytes of actual inline tables/signature. It is source-present,with zero
new exact credit. MAINL acceptance stays211 extents/288 procedures/36,946 bytes.
With the later [destruction bank](MAINL_XX_DESTRUCTION_REVIEW.md),
[call adapters](MAINL_XX_CALLS_REVIEW.md),[catch/type bank](MAINL_XX_CATCH_REVIEW.md)
and [type matcher](MAINL_XX_TYPES_REVIEW.md),the then-source scope was246 extents/
55,702 gross bytes.

| Bank-relative offset | Procedure | Instruction bytes | Return |
| ---: | --- | ---: | --- |
| 0 | local_unwind | 447 | near cdecl |
| 459 | _Local_unwind | 32 | far cdecl |
| 491 | _Return_unwind | 42 | far cdecl |
| 533 | findMatchingHandler | 132 | near cdecl |
| 673 | _ExceptionHandler | 880 | far cdecl |

The complete xx module remains12622 CODE-class bytes,18 DATA bytes and10 BSS
bytes. Public-symbol gaps do not define function sizes: the880-byte handler
ends at78C4,followed by a12-byte switch table and further destruction helpers.
The bank's other table is12 bytes at7472; the semantic `**BCCxh1` tag occupies
754C..7553. Both six-entry switch tables enter actual instruction boundaries.
A native `#pragma codestring` emits the meaningful tag. No opcode array,padding
or target-derived product bytes are introduced.

The ABI header describes only the prefixes used by this bank. Native
`__InitExceptBlocks` and actual dispatcher accesses establish SS-relative
registration pointers,SS:0014 for the exception chain and SS:0016 for the far
runtime-info pointer. Registration fields are table+6,SP+10,context+12,DS+14,
SI+16,unwind flag+18,exception code+20,exception-info SS pointer+24 and a DWORD
destructor counter+26. The header's31-byte registration prefix does not prove
the size or tail padding of every original registration allocation.

Exception descriptors retain a WORD callback DS at+24 and a far free callback
at+26. Registration,matching handler and context are at+36,+38,+42; the used
prefix ends at58. Freeing a descriptor switches DS to the recorded callback
DS,then restores it. Destruction minima are signed16 values converted to the
callee's32-bit count. Near destructor-table offsets are paired with the context
table's segment,not left relative to DS. Compile-time offset/width constraints
check these concrete ABI questions against the actual16-bit compiler.

The local unwinder walks outer contexts before executing finally,catch cleanup
or destructor cleanup. Catch cleanup retains the original unchecked assumption
that its descriptor exists. The dispatcher preserves both saved DS and SI,
checks throw specifications while unwinding,and handles C++ catches plus C
filter forms. It preserves the original negative-filter rule: with the
noncontinuable flag set,it changes the registration context to the outer
context before returning continue-execution. No defensive product changes are
made. The later Win32 `_fpreset`,Delphi paths and flattened-pointer declarations
are not imported.

The later Borland [xx implementation](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/SOURCE/EXCEPT/XX.CPP)
and [internal header](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/RTLINC/XX.H)
were structural references. Their flat definitions and callback/environment
layout differ from the target. A new private Ghidra database of the fixed
67372-byte decoded Japanese MZ was independently attested against its existing
DIET declaration before observations were used. Complete original OMF fields,
MAP boundaries,linked bytes,body returns and branches were then checked directly;
Ghidra's inferred boundaries and parameter types are hypotheses.

The retained diagnostic profile uses the existing scoped BCC4.5 compiler with
`-O2-pg -Os -O-i -Z- -S`,then actual TASM5 and TLINK. Borland's
[optimizer documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_3.1_Users_Guide_1992.pdf)
explains the separate optimization controls; this profile's suitability is
limited to the observed output. Two native rounds repeat full generated ASM,
two-OBJ,mini-EXE and MAP vectors. The wrapper includes the maintained bank and
ABI header; all64 available active SDK headers match the pinned installation.
This is an inventory of all available headers,not an inferred consumed subset.

Candidate CODE is1566 bytes and BSS8. The three public entry offsets match the
original bank,but the complete native bank does not match. Seven surrounding
private/runtime interfaces are explicit trap imports in this isolated miniature.
Internal far calls become external five-byte calls; stack-cleanup grouping and field
streams differ. The diagnostic does not replace the original normal library
member or link the whole product. The later complete TU supplies those interfaces.
Exact ownership still requires closing its raw CODE/field/layout differences;do not normalize them away.

The subsequent destruction bank now provides static near dtorCleanup in a
combined same-TU miniature. The shared ABI header has expanded descriptor/list
prefixes; this isolated dispatch diagnostic supplies its external cleanup
declaration only in its wrapper. Its native pair and evidence receipts were
refreshed. The integrated result and remaining interfaces are reviewed separately.

A single targeted native probe runs the negative constant C-filter branch in
the real target and real mini-linked source. Both return0 through the far
cdecl caller frame,preserve DS/SS/BP/SI/DI,move context0010 to0006,retain the
existing exception-info pointer,and write the saved DS/SI runtime fields.
No imported helper is executed: the mini-link's explicit context providers are
unreachable traps,not behavior models. The miniature has a real uninitialized
stack segment; the focused runner supplies its own caller stack. Other branches,
real DOS execution and whole-game exception behavior are not established.

The original211 accepted owners,their publication and verifier inputs,and the
938-output cold pair remain unchanged and are validated. No full cold/DIET or
ancestor runtime chain is replayed. The later full-TU review directly proved
RaiseException1151,tossAnException815 and dtorCleanup1035 boundaries and their
metadata ownership. They are no longer merely Ghidra size suggestions. Complete
source codegen/frame/layout and literal relocation equality remain open;see the
current product review before selecting further work.

## Current full-TU handler recovery

The maintained `_ExceptionHandler` now has the original880-byte body and56-byte
stack frame. Its actual `int filter` declaration follows the Global_unwind call.
This declaration ends BCC's deferred argument-pop sequence,so both unwind calls
retain their own POP CX pairs. All13 raw bytes between the first call's operand
end and the second cleanup end match. Jump optimization remains enabled;no new
local,optimizer switch or padding is introduced.

The declaration-boundary hint in the pinned
[ReC98 notes](https://github.com/nmlgc/ReC98/blob/b6ba5b0a529edbb31efdf8c0e939263804f8ee47/Research/Borland%20C%2B%2B%20decompilation.md)
was checked with real BCC4.5/TASM output. A local -O- experiment first recovered
the size and cleanup. Moving only the real filter declaration reproduces the
entire initialized TU payload,ordered fields,segments,imports and publics of
that experiment. The maintained source adopts the declaration order.

The complete unlinked880-byte handler differs at six byte offsets:
248/249/372/529/585/610. These belong to four internal CALL operands and the
switch-table address. All854 bytes outside the seven near-CALL operands and
five real native fields agree literally. The seven calls resolve to the actual
local_unwind,typeIDcaught,findMatchingHandler,Global_unwind,initCatchArg and
JumpToCatch bodies,including both far-return PUSH CS frames. The unexpected
far interface and both DGROUP callback slots retain their real field shapes.

The adjacent12-byte switch table retains relative destinations
856/615/734/374/856/856,all actual instruction boundaries. Original/current
handler field emission order is372/294/724/703/700 versus294/372/700/703/724.
The original table fields run10/8/6/4/2/0;TASM emits0/2/4/6/8/10. Original/current
unexpected EXTDEF indices now agree at15/15 after import declaration recovery.
The remaining field-order differences are retained
without sorting or operand rewriting. Complete object/linked equality and exact
ownership remain open;there is no new exact credit.

The dispatch-only candidate is now1567 CODE bytes because two original internal
far calls are external in that miniature. The throw miniature resolves one of
those calls and has a1566-byte dispatch tail. The full TU resolves both and has
the original880-byte handler. Current xx CODE12569 and EXE67324 remain different
from original12622/67372. All affected native pairs were refreshed,while the
accepted211 owners/36946 bytes,892 surrounding library members,39 binary link
inputs and938 cold outputs remain unchanged. No full cold/DIET replay is needed.
