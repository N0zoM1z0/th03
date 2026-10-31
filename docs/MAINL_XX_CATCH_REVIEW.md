# MAINL xx catch cleanup and argument initialization

The current storage findings below come from the full TU. The earlier miniature
is retained separately. The maintained xx.cpp links through the normal library
as an unaccepted candidate;see [current product review](MAINL_XX_PRODUCT_REVIEW.md).
Miniature CODE/provider counts remain specific to that diagnostic. Current overall
source presence is250 extents/60,028 gross bytes;accepted MAINL is unchanged.

## Current catch local storage recovery

The private comparator is now a complete raw match. Scoped -O-m suppresses the
compiler's extra cached-mask WORD:the original10-byte frame and all157 object
bytes agree. The profile restores -Om afterward. Both literal field vectors
are empty,and the normal MAINL link retains the same157 bytes at0000:583E with
no MZ words inside the function. The miniature and full-TU reviewers check this
independently;the complete xx member and product remain unaccepted.

The full TU now restores two declaration scopes under the unchanged BCC4.5
profile. In initCatchArg,the existing far `pointer` used for near-pointer
expansion is declared after `value`,before `keep_original`. The original frame
is24 bytes rather than20:handler_type/type/size/value occupy BP-4/-8/-10/-14,
pointer is BP-18,keep_original BP-20,and the nested old_value BP-24. No storage
was added beyond these existing variables. In exceptionHandled,the first type
pointer is declared at function scope. Its second descriptor consequently uses
BP-8,the earlier count slot,instead of reusing the first descriptor's BP-4.

`catch_storage_codegen` checks complete bodies,instruction alignment,the six/
two actual helper calls and all remaining branch destinations. The current
normal product uses native BCC output. initCatchArg is674 versus678,frame24.
Native compilation recovers the original short class-guard JE at+0x18C
(candidate+0x188). Two forms remain:original JE/JMP versus source JNE at+0xEB,
and the original JMP-to-next at+0x117. All other instructions agree outside
checked branch/CALL operands. The retained S/TASM full-TU diagnostic is676 bytes
and also differs at that class guard.

exceptionHandled remains223 versus216,frame8. The original10-byte LES/store
sequence at+0x35 becomes17-byte DX:AX load/store/reload;the rest agrees under
the same operand checks. No defensive product changes are introduced.

Literal native field order stays explicit. exceptionHandled sites are original
95/29 versus native102/29;initCatchArg sites are original611/544/206 versus
native607/540/206. The separate S/TASM sites remain29/102 and206/542/609.
Both producers now retain original full-TU memcpy/memset EXTDEF indices9/10.
No vector is sorted and no partial storage/codegen proof is counted as acceptance.

Earlier controls in `.analysis/work/catch-storage-codegen-experiments.json`
cover braces,old_value scopes,labels and optimizer profiles. The isolated674-byte
native result is now reproduced by the maintained full TU after expressing
unsupported386 operations in source. See [product review](MAINL_XX_PRODUCT_REVIEW.md).
Current native CODE12572/187 fields and67324-byte EXE remain raw-different.
The published211 owners/36946 bytes and accepted28-provider library stay unchanged.
Affected native pairs are refreshed without rebuilding the938 retained cold outputs.

## Retained catch miniature

`src/mainl/crt/xx_catch.inl` recovers six complete procedures and their preceding
compiler EH data from the original monolithic DOS `xx.cpp`. The contiguous bank
0000:6CEF..72B2 is1476 bytes:1434 instructions and42 inline EH bytes.
`xx_type_equal.inl` separately owns the157-byte private far comparator at583E.
Both are bounded includes,not new product TUs. With the later
[type/descriptor bank](MAINL_XX_TYPES_REVIEW.md),the then-source scope was246 extents/
55,702 gross bytes. Accepted MAINL stays211 extents/288 procedures/36,946 bytes;
there is zero new exact credit.

| Procedure | Original address | Instruction bytes | Return |
| --- | --- | ---: | --- |
| sameTypeID | 583E | 157 | far cdecl |
| destThrownValue | 6D19 | 80 | near cdecl |
| exceptionHandled | 6D69 | 216 | near cdecl |
| _CatchCleanup | 6E41 | 125 | far cdecl |
| findBaseAddress | 6EBE | 204 | near cdecl |
| adjustClassAddress | 6F8A | 131 | far cdecl |
| initCatchArg | 700D | 678 | near cdecl |

The42-byte prefix is a catch-all handler record and one try/catch context table.
The source uses an ordinary `try/catch` around thrown-value destruction and
retains the terminate callback. Resolving all13 original OMF fields,in literal
order,from the original normal-library MAP reproduces the entire1476-byte bank.
Its three MZ segment words retain their literal order. Every function is densely
decoded to its actual near/far return,and direct branches enter instructions.
The comparator has no native fields or MZ words. This review uses direct fixed
Japanese target/OMF evidence;no database observations are needed.

Thrown-value cleanup uses descriptor+4 for its type,descriptor+58 for its payload,
and cached class flags at+22. The DOS body saves the SS:10 DWORD destructor count,
calls the destructor and restores the entire count before clearing argument-buffer
presence. This preserves the counter outside the thrown object's destruction.
Argument-copy cleanup separately checks the handler's class/dtor flags,uses the
SS-relative catch-argument address and clears its own presence byte.

`_CatchCleanup` pops the exception descriptor,reads the outer context through the
registration's far table,and calls real exceptionHandled. The descriptor's free
DS at+24 and far callback at+26 are distinct. It switches to that DS for the free
call,then restores incoming DS and returns through the normal far cdecl frame.
The registration chain at SS:14 remains the caller's responsibility.

The catch initializer records the handler type even for unnamed/catch-all cases.
It forms the argument address by16-bit wrapping of new BP plus the table offset,
marks the copy,and handles zero-pointer values,classes by value,pointers,
references and near-to-far pointer conversion. A copy constructor calls the real
callCopyCtor adapter. Near pointer mask1000 supplies DS; pointer/ref class paths
adjust the object address and retain the original object when necessary. The
original final descriptor accesses remain unchecked. The unused registration
argument remains in its16-byte near-cdecl parameter list.

The private comparator first accepts identical far descriptor pointers. Otherwise
it compares mask,size and local-type flag80,then compares signed characters in
the far names. The base search walks8-byte entries and recursively searches
ordinary bases. A virtual-base WORD supplies a new offset while retaining the
object's segment. The target tests the computed base-list far pointer,rather than
testing only its relative descriptor offset. The address adjuster searches the
ordinary list followed by the virtual list and returns the resulting far pointer.

The scoped BCC4.5 recipe now uses `-O2-pg -Os -O-i -Z- -S`. Explicit `-O-i`
after the presets retains library calls instead of expanding memory operations.
The real source has two far memcpy sites and one memset site,matching the native
question established by the original fields. Borland's
[compiler guide](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_4.0_Users_Guide_Oct93.pdf)
documents intrinsic expansion separately from ordinary calls. Actual compiler,
assembler and linked outputs establish this recipe's observed effect. The later
[xx reference](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/SOURCE/EXCEPT/XX.CPP)
supplied structure; its flat pointer/layout,extra type/flags arguments and stack
restoration rules are not imported into the DOS implementation.

Private catch declarations have moved from the ABI header to incomplete diagnostic
wrappers. The complete source retains static linkage and the original C++
`_CatchCleanup` public. Two native rounds repeat complete generated ASM,two-OBJ,
EXE and MAP vectors. Timestamped listings are retained separately; all64 available
SDK headers are bound. The affected earlier three miniatures were refreshed for
the shared header/driver/profile. The latest earlier receipt and its full raw
pair are validated and reused,without replaying its ancestor runtime observations
inside each catch review. The211-owner publication/verifier inputs and938 unchanged
cold outputs remain valid;this miniature does not rebuild the full cold pair or
replace the normal-library member. The later full-TU candidate does the latter.

The current comparator is157 bytes and raw-equal. Candidate catch bodies are79/223/125/204/
131/676 bytes,plus42 EH bytes,total1480. Whole candidate CODE is7214 with empty
DATA and8 bytes of callback BSS. Fourteen interfaces remain unresolved. Original
covered ranges total7193 bytes in three separate spans; gaps are not claimed.
Complete catch-bank equality and full-TU acceptance remain open.

Three small actual target/source probes establish concrete paths. A const class
catch invokes the real copy adapter and actual TASM constructor callback once,
passes SS:3FF0 plus the original far payload,records the copy and retains the
thrown buffer. Catch exit updates the exception head and outer context,passes the
descriptor to its actual TASM free callback in saved DS,and preserves SS:14.
Virtual-base adjustment compares nonidentical equal-named descriptors,reads the
virtual offset and returns6500:0220. All preserve incoming DS/SS/BP/SI/DI and the
near/far cdecl stack. Callback code resides outside both immutable program images;
unresolved helpers stay traps. These observations do not close every exception
path or physical DOS execution.

The later type bank supplies real private typeIDcaught and its compatibility
helpers. Its independent profile no longer needs that diagnostic provider; it
adds the allocator library interfaces instead. This earlier catch miniature
retains14 explicit providers and was refreshed once for the common profile entry.
