# MAINL DOS xx throw and global-unwind bank

`src/mainl/crt/xx_throw.inl` recovers original CODE6313..6CEE in the
original xx.cpp TU. This is source-present,with **zero new exact bytes**.
The bank has2446 instruction bytes in eight complete far procedures and78
compiler-generated EH bytes. The review independently resolves all2524 original
bytes from the real xx.obj,24 literal ordered native fields and six ordered MZ
segment words. The fixed Japanese decoded target remains the oracle.

| Procedure | Original bytes | S/TASM miniature bytes |
| --- | ---: | ---: |
| tossAnException | 815 | 812 |
| _ThrowException | 89 | 89 |
| _ReThrowException | 170 | 170 |
| exceptionChainHook | 5 | 5 |
| dispatchException | 140 | 140 |
| _Global_unwind | 71 | 71 |
| exceptionContextHook | 5 | 5 |
| RaiseException | 1151 | 1081 |

Original coverage now forms the continuous583E..8293 range,10838 bytes.
The front49 bytes,tail1735 and DATA18/BSS10 are now recovered in the complete
TU and linked through the normal library;see [product review](MAINL_XX_PRODUCT_REVIEW.md).
This bounded miniature remains diagnostic context rather than a product link.

## Recovered source and ABI

`tossAnException` is far cdecl with32 argument bytes. It saves DS,sets the
runtime throw-name pointer to runtime+28h,and scans the entire descriptor name
while limiting destination writes to127 characters through a WORD offset check.
It stores file/line in borrowed runtime slots+16h/+1Ah. The new descriptor is
linked onto runtime.exceptions **before** copying its payload. Descriptor size
is58;the free callback carries DS at+24 and its far address at+26.

Copy construction saves/restores the full DWORD destructor count and catches
exceptions to terminate. A non-rethrow destroys the caller's original temporary
when class flag2 is set,also under a catch-to-terminate block. The two EH records
and context entries occupy78 original CS bytes. Later flat RTL source differs
in descriptor-list order and temporary destruction;it is not substituted.

Public compiler-generated throws retain the C++ signature with four far void
pointers,three WORDs and a far filename. Both wrappers save the actual far
caller PC from SS:BP+2 into a DWORD local before building the outgoing frame. Rethrow preserves the SS-relative argument-address
promotion when its buffer flag is clear. Their real outgoing toss frames are32
bytes,with no extra registration argument. The DOS exception code is0EEFFACEh.

The descriptor argument is cached in a typed local,restoring the original72-byte
toss frame. The name-source address is evaluated before the destination.

The private dispatcher calls handlers with a far exception record,a near SS
registration,a far context and zero DWORD argument. Zero means handled;all other
return values continue the chain. Flags6 select unwind chain updates,which stop
before the requested registration. A null `_Global_unwind` record creates only
code26h,flags2 and count0;other fields remain uninitialized. Both original
five-byte empty hooks are real far functions,not padding. Its registration alias
and handler-disposition locals recover the complete original140-byte dispatcher:
all raw linked bytes agree in both the miniature and real normal-library link.
This is a body comparison,not promotion of the larger source unit.

`RaiseException` uses the compiler's `__saveregs` ten-WORD prologue and far
return. A CPU byte at `__8086` selects the386 PUSHAD/PUSHFD path. The used204-byte
context prefix includes the112-byte x87 save area,segment DWORDs and full general
registers;the original's additional frame ownership is not inferred from these
accesses. PUSHF/POP AX/MOV saves the flags while also changing AX before PUSHAD,as in the
original;the previous POP-to-local skipped that register effect. Low register
WORDs come from the entry snapshot. Reserved exception
code bit10000000h is cleared;argument count caps at15. Noncontinuable handling
uses C0000025h. Resume writes a48-byte386 or26-byte16-bit frame and changes SS:SP
before the actual POP/RETF sequence. ES:BX must retain the destination address:
a spilled local far pointer can overwrite itself as the resume frame is written.
Natural field writes use Borland register pseudovariables for that address.
The failed-dispatch terminate block follows both destructive resume paths;the
explicit C returns after RETF recover that control-flow placement.

## Native evidence and remaining difference

Two real BCC4.5 -O2-pg -Os -O-i -Z- -S,TASM and miniature TLINK rounds repeat
whole raw generated ASM,two OBJ,EXE and MAP vectors. Original timestamped
listings are retained separately. All64 available pinned SDK headers are bound.
The independent profile leaves the shared recipe and previous miniatures
unchanged. The actual exception-handler call now resolves to the recovered
`_Global_unwind`,reducing that old dispatcher body by one byte. Fifteen callable
runtime/library imports plus one CPU DATA slot remain diagnostic context.
The CPU slot is not a new product storage owner.

Four focused target/source observations check the386 context/restore path,
stop-before-target unwind and the two wrapper frames. The386 handler records
all segment/general-register fields and changes EAX to DEADBEEFh;both actual
routines resume that value and preserve the other full caller registers. A17
DWORD input caps at15 and retains all15 values. The two memcpy calls execute the
entire actual36-byte,relocation-free original memcpy;the miniature trap entry
redirects to separate fixture memory without altering either image or object.
There is no modeled allocator,EH service or memory helper. The16-bit resume
branch and complete throw/catch lifecycle have not been executed by these probes.

The native argument-count/index/copy block6AC0..6B06 is now a complete raw71-byte
match. A function-local -O-v suppresses the two compiler-generated WORD induction
pointers that the original loop does not have. FS/GS high halves are zeroed before
the segment writes;the16-bit zero chain fills EBP first. Direct `_SS` assignment
and CX/ES/BX resume-address construction recover the original instruction order.
The remaining frame allocation is390 versus342,not the former390/346.

The raw default-SP observation now agrees completely,including EFLAGS84h/84h.
One additional entry SP,FF10 instead of FF00,retains original80h/source84h while
all other observed context/record/register values still agree. Thus agreement
in the default sample did not close the frame/PF question. Both raw observations
are retained;there is no flag correction or placeholder stack object.

The independently read original stack operands and current compiler output give:

| Local region | Original BP interval | Current BP interval |
| --- | --- | --- |
| Exception record76 | -86..-10 | -86..-10 |
| Unproved48-byte region | -134..-86 | absent |
| Used context204 | -338..-134 | -290..-86 |
| Entry WORD snapshot20 | -358..-338 | -310..-290 |
| PUSHAD DWORD snapshot32 | -390..-358 | -342..-310 |

Intervals are half-open and offsets are decimal. The empty hook receives BP-134
in the original and the context's end in current source. The original address
and allocation footprint are known;the missing region's type/purpose remains
unproved. Matching its length with an invented object would not recover source.

Candidate throw bank2451 and miniature CODE10787 remain raw-different from
original bank2524 and covered10838. Equal wrapper sizes89/170 do not establish
raw equality. Source presence is250 extents/60028 gross bytes;accepted MAINL
stays211 owners/288 procedures/36946 bytes. Publication/verifier inputs and all938
retained cold outputs are unchanged. Native boundaries and fields are checked
independently. No full cold/DIET replay or ancestor runtime chain was repeated.

## Current native compiler investigation

The48-byte frame gap is not a short exception-parameter array:the existing record
already has15 DWORD slots. Borland's preserved
[16-bit EXCPT.H](https://raw.githubusercontent.com/earthsiege2/borland-cpp-ide/602b99a9fcd8429387d4c54cb1f455854e513886/SOURCE/RTL/RTLAPI/EXCPT.H)
also gives the204-byte context layout used by the observed field accesses.
A small native ABI probe shows that an ordinary48-byte structure return passes
a far four-byte buffer pointer;the original empty hook receives only two bytes.
That hypothesis does not establish ownership of the missing region. Product
storage and the342-byte frame are unchanged.

A further native ABI probe gives an ordinary48-byte resume-frame class an empty,
out-of-line default constructor under the current large-model profile. Its
constructor has41 CODE bytes,including the allocation/return path,and receives
four this-pointer bytes;the __saveregs caller allocates48 and pushes SS plus
offset. This does not match the original five-byte hook and its two-byte
argument. It establishes no ownership for the missing48 bytes. The actual
source/ASM/native object and compiler commands are recorded in
`.analysis/work/raise-constructor-probe.json`;no such object is added to Raise.

The complete normal product now uses actual native BCC `-c -y` objects.
Named instruction intrinsics express individual unsupported386 operations;
FS/GS stores retain compiler-symbolic DW addresses with offsetof-derived member
offsets. Native ES callback syntax also lives in source. There are no target
function arrays,object patches or hardcoded BP local offsets.

Real-linked execution caught a native inline-assembler offset bug. Both
`context.field` and `context + enum_offset` generated reversed local-member
addition:EFLAGS at BP-482 instead of BP-98,and SS at BP-490 instead of BP-90.
The faulty native candidate returned to0000:0000. Using `context - enum_offset`
recovers the intended address. The current native compilation yields CODE12554,
187 fields and22 publics;all50 procedures bind actual source/LINNUM records.
The earlier12576-byte direct object remains only historical prefix evidence.

All18 imports and the first2822 bytes/92 ordered fields agree literally in
both current object and linked image. Native BCC preserves all six original
five-byte forward FAR CALLs. tossAnException815 and destThrownValue80 recover
original lengths;destroyBases129 and destroyVariable715 also match complete
linked bodies. Those lengths alone do not prove the throw routines raw-equal.
The retained S/TASM full-TU diagnostic now has12553 CODE/181 fields,with812/79
throw helper lengths. Four virtual-base SI assignments recover the complete
call-adapter bank1495/all88 fields in the native product;copy750 now agrees.

Corrected real-linked Raise/dispatcher probes pass with actual library memcpy
twice. Default entry FF00 agrees in record,registers,segments and flags84h;
alternate FF10 keeps only the known80h/84h difference. Raise is still1081 versus
1151 and its frame342 versus390. No new storage,flag correction or acceptance
follows. `.analysis/work/xx-native-compiler-recovery.json` records the failed
operand forms,correction and current raw product pair;see
[normal product review](MAINL_XX_PRODUCT_REVIEW.md).

Current private inputs/receipts use the `xx-throw-*` prefix under
`.analysis/work/`,plus `mainl-xx-throw-build.json` and
`mainl-xx-throw-review.json`. Reproduce the affected scope with:

```sh
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_throw.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_throw.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_throw
```

Next resolve the remaining full-TU source/codegen/frame/storage gaps using the
normal-library link. Do not turn
these diagnostic observations into source-exact or whole-game progress.
