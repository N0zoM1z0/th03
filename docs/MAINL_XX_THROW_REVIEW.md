# MAINL DOS xx throw and global-unwind bank

`src/mainl/crt/xx_throw.inl` recovers original CODE6313..6CEE in the
original xx.cpp TU. This is source-present,with **zero new exact bytes**.
The bank has2446 instruction bytes in eight complete far procedures and78
compiler-generated EH bytes. The review independently resolves all2524 original
bytes from the real xx.obj,24 literal ordered native fields and six ordered MZ
segment words. The fixed Japanese decoded target remains the oracle.

| Procedure | Original bytes | Current candidate bytes |
| --- | ---: | ---: |
| tossAnException | 815 | 800 |
| _ThrowException | 89 | 77 |
| _ReThrowException | 170 | 158 |
| exceptionChainHook | 5 | 5 |
| dispatchException | 140 | 132 |
| _Global_unwind | 71 | 71 |
| exceptionContextHook | 5 | 5 |
| RaiseException | 1151 | 1099 |

Original coverage now forms the continuous583E..8293 range,10838 bytes.
The front49 bytes and tail1735 bytes of xx CODE,and DATA18/BSS10 ownership,
remain open. This is not a complete TU or a normal-library replacement.

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
pointers,three WORDs and a far filename. Both wrappers obtain the actual far
caller PC from SS:BP+2. Rethrow preserves the SS-relative argument-address
promotion when its buffer flag is clear. Their real outgoing toss frames are32
bytes,with no extra registration argument. The DOS exception code is0EEFFACEh.

The private dispatcher calls handlers with a far exception record,a near SS
registration,a far context and zero DWORD argument. Zero means handled;all other
return values continue the chain. Flags6 select unwind chain updates,which stop
before the requested registration. A null `_Global_unwind` record creates only
code26h,flags2 and count0;other fields remain uninitialized. Both original
five-byte empty hooks are real far functions,not padding.

`RaiseException` uses the compiler's `__saveregs` ten-WORD prologue and far
return. A CPU byte at `__8086` selects the386 PUSHAD/PUSHFD path. The used204-byte
context prefix includes the112-byte x87 save area,segment DWORDs and full general
registers;the original's additional frame ownership is not inferred from these
accesses. Low register WORDs come from the entry snapshot. Reserved exception
code bit10000000h is cleared;argument count caps at15. Noncontinuable handling
uses C0000025h. Resume writes a48-byte386 or26-byte16-bit frame and changes SS:SP
before the actual POP/RETF sequence. ES:BX must retain the destination address:
a spilled local far pointer can overwrite itself as the resume frame is written.
Natural field writes use Borland register pseudovariables for that address.

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

**Saved EFLAGS are still different:** original84h,candidate80h in this probe.
The original stack allocation is390 bytes,current candidate346;the arithmetic
before the snapshot changes PF. Both full raw context observations are retained.
The review compares the tested record/register ABI while reporting this flag gap
explicitly. No flag adjustment or padding is added to manufacture equality.

Candidate throw bank2425 and whole CODE10776 remain raw-different from original
bank2524 and covered10838. Source presence is247 extents/58226 gross bytes;
accepted MAINL stays211 owners/288 procedures/36946 bytes. Publication/verifier
inputs and all938 retained cold outputs are unchanged. Ghidra's fixed decoded
DB was re-attested before the six supporting decompiles;native boundaries and
fields are checked independently. No full cold/DIET replay or ancestor runtime
chain was repeated.

Current private inputs/receipts use the `xx-throw-*` prefix under
`.analysis/work/`,plus `mainl-xx-throw-build.json` and
`mainl-xx-throw-review.json`. Reproduce the affected scope with:

```sh
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_xx_throw.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_throw.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_throw
```

Next recover the front jump/name and tail RTTI functions,then integrate the full
TU and resolve the remaining source/codegen/frame/storage gaps. Do not turn
these diagnostic observations into source-exact or whole-game progress.
