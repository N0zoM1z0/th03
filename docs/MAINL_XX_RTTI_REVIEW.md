# MAINL complete DOS xx source graph and RTTI

`src/mainl/crt/xx.cpp` now composes the original exception/RTTI TU in source
order. New bounded includes recover front580D..583D,49 bytes,and tail8294..895A,
1735 bytes. The latter contains1599 instruction bytes in14 complete procedures
and136 compiler-generated RTTI/vtable bytes. `__GetTypeInfo` is131 bytes;the
following582 bytes are a separate private near recursive search. `__DynamicCast`
is357 bytes;its trailing descriptors are data,not instructions.

This closes source presence for all12622 original CODE bytes and18 initialized
DATA bytes,with reviewed used BSS10. **No new accepted credit.** This document's
full-TU miniature uses BCC -S/TASM:CODE12569,181 fields,DATA18,BSS10,metadata135
and tail1734. The current normal product instead uses actual BCC `-c -y`
objects:CODE12572,187 fields,metadata136 and tail1735,including one actual LEDATA
zero and no LIDATA. It remains raw-different;see [product review](MAINL_XX_PRODUCT_REVIEW.md).

## Source and native ownership

The current full-TU review also checks the recovered catch local storage and its
remaining instruction forms. initCatchArg now has the original24-byte frame;
exceptionHandled uses the original second descriptor slot at BP-8. See
[catch storage review](MAINL_XX_CATCH_REVIEW.md#current-catch-local-storage-recovery)
for the diagnostic three branch forms and current native two-form gap,plus
the load sequence and literal field-order differences. The normal-library
reviewer independently binds its actual native object payload and all50 source/
LINNUM boundaries;it does not equate that payload to this S/TASM miniature.

The full carrier has50 complete near/far procedures,12088 instruction bytes and
534 compiler/semantic CS storage bytes. All187 original literal native fields
independently reproduce the complete pinned Japanese CODE image. All20 original
MZ segment words retain their literal order. DATA18 matches both original OMF
and fixed target;the actual MAP owns it at0E3F:1172. BSS10 has no initializers
and the original MAP owns it at0E3F:2876.

The complete source has the same22 public C/C++ interfaces and18 external
runtime/library/CPU imports as original xx.obj. The existing private banks stay
in one TU. `__JumpToCatch__` is real source:BX selects SP,CX selects BP,and DX:AX
selects the far catch address. Its unreachable compiler SI/DI pops remain part
of the12-byte body. The private37-byte typeIDname returns `<notype>` for a null
descriptor. `_CurrExcContext` checks eight bytes before the handler for
`**BCCxh1`;the later RTL imported-jump-table fallback is absent here.

The two source strings are the original18 DATA bytes. The empty Bad_typeid and
Bad_cast throw values occupy adjacent BSS bytes+8/+9. A packed pair of actual
exception objects recovers that shared storage without adding WORD slots or
stack temporaries. The two earlier four-byte callback slots precede them.
This is a source storage recovery,not a claim about original variable spelling.

The pinned TC4 typeinfo.h supplies the original huge class and low vptr ABI.
Its unsupported copy constructor throws a null typeinfo pointer;assignment is
a no-op returning this. The empty virtual destructor naturally generates vptr
restoration and conditional delete. Equality calls sameTypeID;inequality negates
it. `before` returns false for null this-type,true for a null other-type,and
otherwise compares names. A local -O1 profile recovers the complete original
120-byte **unlinked object body**,including its two far expression temporaries.
The original and candidate retain their actual single far strcmp field at+96,
with literal EXTDEF8 now retained in both objects. Linked body bytes still differ
because the surrounding carrier layout changes the call displacement. This is
not whole-TU acceptance or relocation-record equality.

The complete18-entry import vector now agrees in native order after restoring
the explicit far DOS declarations in xx_abi.h. Both the full-TU and normal-library
reviewers compare the literal vectors. The import-only S/TASM checkpoint
retained its prior EXE/MAP bytes;the current native product has its own full raw
comparison. Neither vector sorting nor object rewriting is involved.

Previous scoped reset experiments omitted -Z-. Restoring -O2-pg,-Os,-O-i and
-Z- after before preserves all following function lengths;GetTypeInfo131,private
search582 and DynamicCast357 remain. No optimizer option push/pop is needed.

Compiler-produced tail storage is reviewed completely:Bad_cast20 bytes,
Bad_typeid22,far typeinfo-pointer descriptor21,optional compiler zero,vtable12 and
typeinfo descriptor/terminated lists60. The retained S/TASM tail is1734 bytes,including
1599 instructions and135 metadata bytes;the original has1735/136. Complete raw tail
equality remains open. The generated header retains size8,mask3,class flags1073h,
base/virtual/member offsets48/52/56,WORD destructor counts1/1 and destructor mask5.
All four internal far pointers bind the real typeinfo descriptor/destructor.

The earlier reviewer inferred the zero from final vtable-label parity. That
assumption fails when compiler output and TASM relaxation have different offset
estimates. After the comparator recovery,the retained S/TASM BCC ASM emits neither the
optional zero nor LIDATA;the previous catch-storage checkpoint emitted both. The reviewer checks
actual directive/record presence and every resulting byte in either case.
It does not require final-address alignment or insert a missing initializer.

## RTTI behavior and focused observations

`__GetTypeInfo` retains four far void-pointer parameters. A missing object
throws the shared Bad_typeid value. Otherwise the secondary-vtable WORD at-2
selects the complete vtable;its far type descriptor at-8 replaces only tpp,+4,
in the caller-supplied typeinfo object. The third parameter remains unused.

The recursive search visits virtual lists before ordinary lists,skips entry
flag8,and follows a WORD virtual-base address through flag4 while retaining the
object segment. Public access3 must survive the current path. Equal matches at
the same actual address merge public access;different addresses remain ambiguous.
The passed virtual-type value is forwarded,not used for an added filter.
Downcast verifies the actual source subobject address through a nested search;
this DOS containment path does not impose the cross-cast public-path condition.
Do not import later C++ access/RTTI behavior as a defensive fix.

Five target/source native pairs execute the complete real helpers:

- Shared virtual Base reached privately and publicly resolves once at6500:0500.
- Two distinct Base addresses are ambiguous and return null.
- Downcast verifies source6500:0128 and returns6500:0120 through private links.
- Secondary-vtable adjustment updates tpp while preserving the existing vptr.
- Register catch jump transfers to SP=E000/BP=2222 with the far destination.

All selected far frames and DS/SS/BP/SI/DI values agree. There is no modeled
search,allocator,EH service or memory helper. Failure throws and a complete
exception lifecycle are not executed by these probes.

## Reproducibility and remaining work

Two actual BCC4.5 -O2-pg -Os -O-i -Z- -S,TASM and miniature TLINK rounds repeat
whole raw generated ASM,two OBJ,EXE and MAP vectors. Listings retain page clocks.
All64 available pinned SDK headers are bound. The independent profile reads the
maintained xx.cpp and changes include filenames only for DOS transport. The shared
builder stays unchanged;source edits refresh affected miniatures before receipt
reuse. The candidate retains181 literal
fields and20 ordered MZ words. Current and original fields/vectors remain separate;
no byte or relocation normalization is used to claim equality.

Existing reviewed throw receipts and the unchanged938 cold outputs are reused,
without ancestor runtime or full cold/DIET replay. The fixed decoded Ghidra DB
was independently re-attested before the supporting tail/private-search reads.
The native carrier,fields and data ownership are checked independently.

Current receipts are `.analysis/work/mainl-xx-rtti-build.json` and
`mainl-xx-rtti-review.json`;retain both `xx-rtti-roundN-*` raw pairs,actual
wrapper/transported sources/context/link response and phase logs. Affected work:

```sh
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_rtti.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_rtti.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_rtti
```

Source presence is250 extents/60028 gross bytes;accepted MAINL remains211 owners/
288 procedures/36946 bytes. Publication/verifier inputs remain unchanged. Next
resolve the full TU codegen differences,including RaiseException390/342-byte
frames and alternate-entry-SP saved EFLAGS80h/84h,using the current normal-library link and
checking affected whole-product outputs. Whole-game completion remains unknown.
