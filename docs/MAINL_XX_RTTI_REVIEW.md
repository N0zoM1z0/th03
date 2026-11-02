# MAINL complete DOS xx source graph and RTTI

`src/mainl/crt/xx.cpp` now composes the original exception/RTTI TU in source
order. New bounded includes recover front580D..583D,49 bytes,and tail8294..895A,
1735 bytes. The latter contains1599 instruction bytes in14 complete procedures
and136 compiler-generated RTTI/vtable bytes. `__GetTypeInfo` is131 bytes;the
following582 bytes are a separate private near recursive search. `__DynamicCast`
is357 bytes;its trailing descriptors are data,not instructions.

This closes natural source presence for all12,622 original CODE bytes,
18 initialized DATA bytes and10 reviewed BSS bytes. The ordinary BCC
-c -y normal-library product now reproduces the **entire12,622-byte original
CODE payload,all187 literal ordered fields and the whole decoded Japanese
MAINL EXE/MAP exactly**. Its actual native RTTI tail is1,735 bytes with
136 metadata bytes and one optional zero in dense LEDATA. All50 complete
linked xx function bodies agree. This is a source-exact working carrier,
not yet a formal accepted211-owner ledger promotion.

The independent BCC -S/TASM diagnostic miniature remains different:
CODE12,619,181 fields,DATA18/BSS10,RTTI tail1,734 and metadata135.
It has no LIDATA zero;the native product emits the real optional zero
inside dense LEDATA. Do not normalize or conflate these two producers.
See [normal product review](MAINL_XX_PRODUCT_REVIEW.md).

## Source and native ownership

The current full-TU review also checks the recovered catch local storage and its
remaining instruction forms. initCatchArg now has the original24-byte frame;
exceptionHandled uses the original second descriptor slot at BP-8. See
[catch storage review](MAINL_XX_CATCH_REVIEW.md#current-catch-local-storage-recovery)
for the one remaining diagnostic S/TASM class-guard branch form. Native
initCatchArg678 and exceptionHandled216 are both object-exact;the S/TASM
miniature retains its own field order. The normal-library
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
The original and native BCC -c object retain the same single far strcmp
field at+96 and literal EXTDEF8. The ordinary linked body now matches all
120 bytes and that field at its original address. Earlier unequal call
displacements belonged to the incomplete preceding translation-unit layout;
the independent S/TASM miniature remains a different diagnostic producer.
The complete native xx source carrier agrees raw,while its formal published
acceptance ownership remains a separate gate.

The complete18-entry import vector now agrees in native order after restoring
the explicit far DOS declarations in xx_abi.h. Both the full-TU and normal-library
reviewers compare the literal vectors. The import-only S/TASM checkpoint
retained its prior EXE/MAP bytes;the current native product has its own full raw
comparison. Neither vector sorting nor object rewriting is involved.

Previous scoped reset experiments omitted -Z-. Restoring -O2-pg,-Os,-O-i and
-Z- after before preserves all following function lengths;GetTypeInfo131,private
search582 and DynamicCast357 remain. No optimizer option push/pop is needed.

Compiler-produced tail storage is reviewed completely:Bad_cast20,
Bad_typeid22,far pointer descriptor21,the optional compiler zero,vtable12,
and typeinfo descriptor/terminated lists60. The original and actual native
BCC -c product both have1,735 tail bytes/136 metadata and now agree raw,
including their real CODE-record locations and literal relocation vectors.
The diagnostic S/TASM path instead has1,734/135 with no optional zero,
which is preserved as an explicit negative comparison,not repaired
by adding a fake byte. The native header retains size8,mask3,
class flags1073h,base/virtual/member offsets48/52/56,
WORD destructor counts1/1 and mask5. Internal far pointers resolve
through the actual native library and final MAP.

The earlier assumption that final-label parity proves storage was wrong.
The scoped reviewer now checks actual LEDATA/LIDATA records and complete
payloads separately for native and S/TASM output.

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
288 procedures/36946 bytes. Publication/verifier inputs remain unchanged. The full normal-library link now recovers RaiseException1151/1151 bytes,
390/390-byte frames and the FF10 saved-EFLAGS80h/80h observation. The complete native xx CODE,all50 linked bodies and raw Japanese decoded EXE/MAP now agree;the formal accepted-source publication remains a distinct step. Whole-game completion remains unknown.
