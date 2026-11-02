# MAINL original DOS xx complete native source-and-link review

The maintained source graph rooted at src/mainl/crt/xx.cpp now builds one
native Borland C++ 4.5 exception/RTTI runtime member under its real DOS name.
The ordinary BCC -c -y output, inserted at the original xx slot in the
normal893-member CRT library, links a decoded Japanese MAINL that is
**byte-for-byte equal to the entire 67,372-byte fixed target**, with an
**identical original MAP and all677 original MZ relocations**. Two complete
independent BCC/TLIB/TLINK rounds repeat the unmodified raw ASM/OBJ/LIB/EXE/MAP
vectors. This is a successful natural-source linked reconstruction,not a
normalized comparison or patched binary. The target retains
candidate-local-attested provenance.

## Native source, relocations and ownership

| Property | Japanese original | Actual native BCC source |
| --- | ---: | ---: |
| xx CODE at 0000:580D | 12,622 | **12,622 (raw equal)** |
| Ordered native CODE fields | 187 | **187 (literal equal)** |
| Emitted xx MZ segment words | 20 | **20 (same order)** |
| xx DATA / used BSS | 18 / 10 | **18 / 10** |
| RTTI tail / metadata | 1,735 / 136 | **1,735 / 136** |
| Complete linked xx function bodies | 50 | **50 raw equal** |
| Original full decoded EXE | 67,372 | **67,372 raw equal** |
| Original full MAP | exact | **raw equal** |

The native compiler emits twelve contiguous1024-byte CODE LEDATA records
followed by334 bytes,with the same literal descending FIXUPP sites in every
record as the original. All187 fields agree literally,including each location,
type,target and addend;no vector is sorted. All18 EXTDEF names/indices are in
their original order. The original22 public definitions are independently
resolved through the actual MAP. All18 initialized DATA bytes also agree and
the original10 used BSS bytes retain their native extent. The full RTTI tail
has its original optional zero through dense native LEDATA (not a fake object
patch);the compiler-generated descriptors,virtual table and terminators remain
correct. The complete linked CODE/DATA,all MZ relocations and actual EXE/MAP
are checked without requiring a source-identical OMF comment/header wrapper.

The source member replaces only xx in the 893-member normal library.
The other892 complete member program records are unchanged,as are all36
project objects and the original three startup/EMU/MATHL binary inputs.
The accepted28-provider CRT library and the retained938-output cold pair
are validated and reused. No source cold/DIET replay or ancestor runtime
chain is performed. Source candidate xx is provider29 only in this isolated
working library;the old published211-owner / 36,946-byte MAINL accepted
ledger has **not yet been promoted** and is not falsely counted here.

## Important original codegen recoveries

The first2822 CODE bytes,including the complete1495-byte copy/destructor/
member-call adapter bank and92 ordered native fields,remain exact. The
157-byte private type comparator,339/372-byte type helpers,six genuine
forward FAR CALL forms and complete destruction bodies remain unchanged.

The 1,151-byte RaiseException recovers its meaningful48-byte SS resume-frame
local,original390-byte frame and five literal fields;real linked entry
SP=FF00 and SP=FF10 exception/context/register/flags probes agree against
the Japanese target with the actual memcpy. The216-byte exceptionHandled
retains its direct descriptor LES and the typed ES:BX far mask argument.
The public89/170-byte throw/rethrow wrappers retain original local slot order.

The complete678-byte initCatchArg was the remaining control-flow layout
blocker. Its original24-byte frame and literal fields at relative offsets
611/544/206 are recovered by retaining the pointer mask in Borland's _CX
pseudo-register,then expressing the actual semantic TEST/JE/JMP and
JMP-to-next edges with source inline assembler labels. A normal C if/else
collapsed those edges and removing a needed slot shifted subsequent calls;
an unqualified ASM branch spilled mask/base onto the stack. The restored
native BCC object now matches every initCatchArg byte and ordered field.
This also restores dependent call operands in the complete880-byte
_ExceptionHandler,1,035-byte dtorCleanup,447-byte local_unwind and the other
following code without editing those functions or their call displacements.

The final six operand-byte differences were in the582-byte recursive
searchBaseClass and357-byte __DynamicCast. Using the requested far address
as the left side of the base-address comparison preserves the original
argument-to-local instruction order;testing the incoming destination_id
far pointer for null instead of the equal cached local restores the original
BP+18/BP+20 parameter loads. These are semantics-preserving source
expressions,not constants inserted for byte matching. After both changes,
**all12,622 original native CODE bytes,187 literal fields and all50 linked
bodies agree**. No invented padding,raw function byte arrays or binary
object edits are involved.

The independent BCC -S/TASM diagnostic miniature remains intentionally
different in CODE lengths/metadata and branch relaxation. Its smaller
driver and trap-only imports are not mistaken for normal product output.
The real product is BCC -c -y followed by ordinary TLIB/TLINK;the separate
-S pass only supplies the genuine original50 mangled entry names and return
kinds. Native source-file COMENT/LINNUM records bind all50 function extents.
For optimized functions whose closing brace has no LINNUM, the boundary
reader uses a unique real final source statement within three lines and
requires an actual RET/RETF before the next native procedure;it never
slices at a guessed original-size boundary.

## Scoped tests and limits

Focused RTTI virtual-base,ambiguity,downcast and catch-register probes agree,
as do two real-linked Raise/dispatcher register/context/flag observations.
These are bounded execution observations,not a physical DOS game-play run.
The complete EXE/MAP equality is an independent much stronger raw artifact
result. It does not automatically add accepted ledger credit without the
formal publication and existing acceptance-verifier workflow.

Reproduce only the affected xx scope after changes:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_dispatch.py --with-catch
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_catch.py
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_types.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_types.py
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_throw.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_throw.py
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_rtti.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_rtti.py
    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_xx_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_work

Keep the two complete xx-product-roundN ASM/OBJ/LIB/EXE/MAP raw pairs,
the source transport,response and build/review receipts,phase logs and
original fixed Japanese target. The previous incomplete experiments are
historical controls,not current truth.
