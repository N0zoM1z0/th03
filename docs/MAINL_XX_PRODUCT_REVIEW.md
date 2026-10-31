# MAINL xx normal-library integration

The complete maintained DOS xx.cpp now builds under its real `xx` module name,
replaces the original xx member in the normal893-member library,and links the
actual MAINL project. This is a **raw-different diagnostic candidate**,with no
new source-exact credit or published product acceptance.

Two real BCC4.5/TASM/TLIB/TLINK rounds repeat complete raw ASM,OBJ,LIB,EXE and MAP
vectors. The full candidate EXE is67324 bytes;the fixed Japanese decoded target
is67372. Both headers are4096 bytes and have677 relocation entries;the complete
ordered vectors remain separate and different. Equal counts are not exactness.

## Native source and unchanged inputs

`build_th03_mainl_xx_work.py` reuses the current reviewed28-provider normal
library pair. It checks the entire retained raw pair and phase logs,then asks
native TLIB to extract its893 members. Every extracted member's program records
must match that retained library. The only newly compiled producer is xx.cpp.
No original object code is spliced into the recovered TU.

The maintained TU keeps its source order. Include names alone are shortened for
DOS transport,as in the earlier miniature. Actual BCC compilation uses xx.cpp,
actual TASM uses xx.asm,and native TLIB receives the real xx.obj. There is no
THEADR or object patch to manufacture the member identity. Complete initialized
payload,ordered181 fields,segments,22 public symbols and18 imports agree with
the previously reviewed miniature despite the different input filename.

Both normal-library rebuilds retain all893 positions and all892 surrounding
member program records. Those include28 current source providers and864 vendor
context members;xx becomes the29th source provider in this candidate. The
accepted28-provider baseline files and its published211 owners remain unchanged.
The candidate's moved addresses are not substituted into that publication.

All36 existing project objects are reused. The real pinned TC4 C0L startup,
EMU.LIB and MATHL.LIB complete the39 unchanged binary link inputs. Their paths
are explicit in the candidate response,so the link does not depend on an
unbound startup/library search. No project object,ancestor producer or full cold/
DIET chain is rebuilt. All938 retained cold outputs remain current and unchanged.
The shared miniature recipe and prior source/receipt bindings also stay current.

## Whole-product field and ABI review

The actual MAP allocates xx CODE at0000:580D,size12567;original size is12622.
DATA18 remains at DGROUP:1172 and BSS10 at DGROUP:2876. The candidate DGROUP is
0E3C rather than original0E3F. The CODE length difference and ordinary paragraph
layout produce the48-byte file-size difference;no source padding is introduced.
All18 initialized DATA bytes agree with the compiler output,and BSS has no
invented initializers or file-byte credit.

The reviewer resolves **every source CODE byte** from actual native OMF payload
and all181 fields through the real whole-product MAP. All18 interfaces resolve
to their library providers,with no trap implementation in this executable.
Four arithmetic near-call fields use TASM's explicit CODE frame;their literal
records stay intact and are checked against the real N_LXMUL/N_LUDIV targets.
The20 xx MZ segment words match the actual whole EXE in emitted order. Each of
the22 original public interfaces also binds its real current MAP address.
Current compiler ASM emits no optional zero before the vtable,and no LIDATA
record supplies one. The reviewer checks the emitted directive and actual record
rather than inferring an initializer from final address parity. Current RTTI
tail length1734 differs from original1735;complete raw tail equality remains open.

All50 procedures retain complete raw byte comparisons. The dispatcher remains
a complete140-byte raw match. Raise now has the original direct-indexed argument
loop:all71 count/index/copy bytes agree in the actual linked executable. Local
-O-v eliminates two extra WORD induction pointers;FS/GS writes,the16-bit zero
chain,direct SS assignment and CX/ES/BX resume addressing follow native order.
The current Raise body1081 differs from1151,and its342-byte frame still lacks
an unproved48-byte original region. No placeholder storage or flag adjustment
is added to close that gap.

A scoped -O1 profile recovers all120 raw **unlinked object bytes** of
`typeinfo::before`. Its one original/current far strcmp field at+96 is retained
literally,including different EXTDEF indices8/18. The linked body remains
different because its call displacement follows the current carrier layout.
Previous reset trials omitted -Z-;restoring it with -O2-pg,-Os,-O-i leaves
all following function lengths unchanged. Earlier NOSMART/single-pass TASM
experiments still do not yield equality and are not adopted. Net CODE length55
is not a differing-byte count.

Local -O-v now recovers dtorCleanup's original32-byte stack frame and1035-byte
body. Its complete unlinked object differs in only3 bytes,two internal CALL
operands;all1025 bytes outside the five local CALL operands agree. Every CALL
resolves to the corresponding real source helper. The literal OMF field order
still differs:original function offsets40/996/932,current40/932/996. The linked
body also differs,so no exact credit follows. Recovering destroyVariable's local
declaration/initialization order matches its72-byte member/array-count search.
See the [destruction findings](MAINL_XX_DESTRUCTION_REVIEW.md#current-full-tu-codegen).

compatibleType now has its original372-byte extent and four-byte stack frame.
Local -O-m removes an extra common-mask WORD;the CV subset,count OR and positive
base-return expressions recover the complete native branch layout. Its unlinked
body differs at only two CALL operand bytes. All368 bytes outside those operands
agree,and both helpers resolve by their actual compiler identities. Original and
candidate native field vectors are empty. The linked body still differs;see the
[type findings](MAINL_XX_TYPES_REVIEW.md#current-compatibility-loop-recovery).

Five focused target/source pairs execute routines from the linked product:
virtual-address merging,distinct-address ambiguity,downcast source containment,
secondary-vtable typeinfo update,and register catch jump. They preserve the
selected far frames and DS/SS/BP/SI/DI values.

A sixth observation exercises the linked RaiseException/dispatcher path with
the unchanged actual TASM handler fixture. Both memcpy calls now enter the real
normal-library implementation directly;there is **no import redirection or
memory-helper model**. The handler's DEADBEEFh EAX change resumes correctly,and
other full registers/segments agree with the original. At entry SP=FF00 the
complete tested record/register/context pair now agrees,including EFLAGS84h.
One alternate entry SP=FF10 yields original80h/source84h while every other
observed field agrees. Both use the actual linked memcpy twice. The remaining
390/342 allocation gap therefore remains observable despite default-sample
agreement. These observations do not claim a DOS boot or ending playthrough.

## Current receipts and next work

Keep `.analysis/work/mainl-xx-product-build.json`,
`mainl-xx-product-review.json`,both `xx-product-roundN-xx.asm/.obj/.lst`,
`xx-product-roundN-xxcrt.lib`, `xx-product-roundN-xxfull.exe/.map`,the exact
transported source/header inputs,maintained xx.cpp snapshot,native extraction/
library/link responses and phase logs. Temporary extraction objects are removed;
the retained current library and native phase record remain their provenance.

```sh
PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_xx_work.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_work.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_work
```

Source presence remains250 extents/60028 gross bytes. Accepted MAINL remains211
owners/288 procedures/36946 bytes,with whole-game completion unknown. The full
source graph now has a repeatable normal-library/whole-program route. Next close
the complete xx CODE/field/layout differences,including the RaiseException frame
and its unproved local region,and require raw target EXE/MAP equality before promotion.
