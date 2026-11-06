# Shared large-model startup after548

C0 now reproduces all 58 literal ordered relocation fields through MAINL
and OP, retaining original entry metadata, storage and public ownership.
Its 32 PUBLIC packets still differ in emitted order. That gap remains
explicit; complete original OMF identity and product source acceptance are
not claimed. This is supplier-derived source with zero authored-game credit.

Live owner: `src/shared/crt/startup_large.asm`. Historical
`src/mainl/startup/c0.asm` and the after535 producer remain frozen.

## Original object and complete storage

The independently opened installed original is TC4 `LIB/C0L.OBJ`, 2,438 bytes,
SHA-256 `09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2`.
Supplier C0.ASM, RULES.ASI and BUILD_C0.BAT identities remain pinned by
`config/th03_mainl_startup.json`. Japanese product targets retain
`candidate-local-attested` provenance; independent pristine-dump attestation
remains unknown. A reconstructed carrier is never the original.

| Original storage | Preserved |
| --- | --- |
| Segments | All 17, original order, widths, flags, classes and names |
| CODE extent / initialized | 625 / 623 bytes |
| CODE621–622 | Two genuine uninitialized DGROUP cache bytes |
| CODE623–624 | Original initialized large-model word C004h |
| DATA | All 144 bytes initialized, including null-check header and globals |
| STACK | All 128 bytes reserved and uninitialized |

Every initialized byte is written once. Actual LEDATA/LIDATA records are
checked with the established recursive initializer decoder, using read-only
record envelopes solely for inspection. No product object is patched.
Both cache holes and the entire STACK reservation remain absent from the
initialized-site vector. No padding or target instruction arrays fill them.

All original raw THEADR, LNAMES, SEGDEF, GRPDEF, EXTDEF, ALIAS and MODEND
records agree, including original reverse GROUP membership and the exact
entry frame/target. Imports remain in original order. The original source
filename `c0.ASM` is deliberately preserved in the native invocation.

## Ordered fields and retained PUBLIC gap

Complete geometry, segment-relative status, frame, target method/index and
addend agree directly for all 58 fields, without sorting. CODE sites are:

```text
6,23,27,31,35,41,72,87,137,141,144,179,182,185,201,210,246,
284,297,301,305,309,1,94,101,115,127,165,172,194,229,268,276,
287,290,316,322,334,337,361,372,437,313,329,356,384,388,397,
401,410,414,423,427,449,460,471,482; then DATA130
```

Ordinary instruction spans retain native record chronology; all real code
labels are bound first. The original PROC-dependent RET widths and scoped
local labels are made explicit, preserving call distances and branch bytes.
The SE structure retains its byte fields and six-byte near/far entry layout.

All 32 original public definitions and complete raw packets remain equal
as sets, including both absolute constants and shared-address DATA aliases.
Their actual ordered lists remain in the receipt with equality explicitly
false. Native TASM's emitted order is the same retained order as after535;
no new PUBLIC gap is introduced and no sorting claims to close the old one.
Complete original OMF-program identity remains false.

## ABI and native producer investigation

The supplier-derived code retains PSP entry state, environment scan and
16-bit sizing, minimum stack handling, DOS resize and interrupt-protected
SS:SP switch. It preserves BSS clearing, DOS file-handle setup, exception
initialization, main/exit arguments and cleanup paths. Initializers keep
ascending priority with first-entry ties; cleanup keeps descending priority
with last-entry ties. Near/far table calls, vector save/restore, divide-error
handling and unchecked runtime behavior remain unchanged.

af548a records rejection of unmodified TASM-specific syntax by JWasm.
af548b's syntax-compatible form reproduces all initialized bytes but changes
two nfile frames, GROUP encoding and entry MODEND; it is not adopted.
The installed native writer's MODEND implementation converts segment frames
to TARGET, so source scheduling alone cannot retain this original raw entry.
No assembler backend patch is used to bypass that limitation.

af548c–f retain native TASM default / tested `/kh` setting probes. None restores
the original PUBLIC order. af548g verifies the adopted source with native
TASM 5.0, flags `/m /mx /kh32768 /t`: all 58 ordered fields, all initialized
bytes and every other literal record scope above agree. Tool identity is
pinned; identity with the original assembler is not claimed. No emulator or
input-domain matrix is needed for this bounded source/codegen question.

## Affected two-product proof

Parent after547 root SHA-256 is
`5c834b1fd5f52c4af31f25c63a55edeaa9d6f59054db727f659e5e289c3ba68a`.
The after535 baseline root remains
`9a3592185b880d53d344cdd3f0cf0c0b13534d186833e7d739f673edd2e61d6b`.

Only C0 is assembled. All 893 library members and unchanged game objects
are reused; there is no TLIB or game compiler run. Each round retains five
fresh raw outputs: C0 OBJ, MAINL EXE/MAP and OP EXE/MAP. The actual unchanged
library round is retained by its parent receipt reference and validated
against both consumed native copies. It is not represented as fresh TLIB output.
Both complete fresh vectors repeat; six successful writer logs remain.

| Output | Result |
| --- | --- |
| MAINL EXE | 67,372 bytes; complete original equality; 677 ordered MZ entries |
| OP EXE | 63,866 bytes; complete original equality; 607 ordered MZ entries |
| MAINL MAP | 80,967 bytes; complete after547 equality |
| OP MAP | 68,078 bytes; complete after547 and historical cold MAP equality |

The independent reviewer passed, checking consumed new C0, unchanged source
library pair, tools, argv, independently reconstructed linker responses,
complete storage and selected material ownership. Earlier actual packed OP
proofs are reused through unchanged decoded bytes/tool identities. No new
DIET run is represented. The selected runtime diagnostic remains 75 equal
streams and setvbuf's one order-only stream. C0 PUBLIC order, formal MAINL
0/250 acceptance and the unknown whole-game denominator remain open.

Root: `.analysis/work/runtime-after548-build.json`, SHA-256 `b0bed460844c39c51a1496b312ac0b94120cfff2ccd7e202e6abdb01db9ed773`.
Producer/reviewer: `scripts/build_th03_runtime_after548_work.py` and
`scripts/review_th03_runtime_after548_work.py`; recipe:
`config/th03_startup_after548.json`.

All ten fresh raw outputs/six logs use `runtime-after548-*`. Actual inputs and
MAINL responses remain in `TH03ML/probe/af548h`; OP's consumed C0/library/
responses/outputs remain in `TH03OP/probe/af548h`. Independent review transcript
is `runtime-after548-independent-review.txt`. The 47-file af548a–g probe manifest
is `.analysis/work/probe/startup548/manifest.json`, SHA-256
`b601572bb87afa7c572302f2e5b75ed3bb90d2fd6e5d79a080810dfcfe18ffb9`.
Subsequent stages must reuse the actual startup pair from this root; the frozen
after535 startup pair remains historical baseline evidence. Displays were
empty, writers serialized, one CPU at nice10. No full CI, cold or ancestor
runtime replay, output cleanup or new authored-function acceptance occurred.
