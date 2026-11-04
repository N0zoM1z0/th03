# Original Japanese MAINL DOS wildcard / startup-argument source recovery

The selected original Borland CRT member **151** (`wild`) exports the DOS
wildcard startup entry `__wildargv` at **CODE+7**, in the native 16-bit
large-model startup environment. The recovered `src/mainl/crt/wild.asm`
contains the original argument/environment and PSP processing, DBCS path
recognition and wildcard file enumeration, far DOS error and allocation
paths, and final restoration of the original argc/argv/stack interface.
It does not use original executable byte arrays or post-assembly OBJ patches.

The original two-segment OMF is unusual: its **795-byte CODE extent** includes
**two uninitialized scratch bytes** at CODE+0/+1 before a far abort jump and
`__wildargv` at +7. All **793 materialized CODE bytes** match the original
selected member exactly. Its **10-byte DATA extent is entirely uninitialized**
(`saved_return_offset`, `saved_return_segment`, original `DS`, `SI`, `DI`).
Both segments retain the original absence/presence pattern of LEDATA bytes;
zero-filling them and claiming 795+10 materialized original bytes would be
incorrect. The only DGROUP member is `_DATA`, with original literal `06ff02`.

The source preserves all eleven original EXTDEF imports: startup globals
`__C0argc`/`__C0argv`, PSP and environment, DOS version, far abort/DBCS
helper, published `__argc`/`__argv`, and far `_sbrk`. TASM's register operand
order for `xchg dx,si`, the original `SS:LODSB` (wildcard name buffer) and
three `ES`-prefixed writes to DGROUP argc/argv must be expressed explicitly;
otherwise the program can assemble successfully yet differ from the selected
native CODE and relocation frames.

Reconstruction and full native checks establish **38/38 original relocation
sites, target methods, targets, addends, location types and frame methods**.
The original compiler orders the FIXUPP records differently from TASM, so
literal complete OBJ serialization is **not** claimed. Data/public ownership
and all other source-visible ABI details are checked separately from link
identity.

`scripts/build_th03_mainl_after97_work.py lsetlocl-wild` retains the
source-bound original 97-member Japanese MAINL carrier and compiles both
`lsetlocl` and `wild` from source at their genuine library indices. In two
independent TASM/TLIB/TLINK rounds, all other **794 vendor CRT program
records** are unchanged; the **whole 67,372-byte decoded Japanese MAINL EXE**
and original **MAP** are byte-identical, including all **677 MZ relocations**.
The working CRT now has **99 source-compiled members** spanning **44,010
original-equivalent CODE segment bytes**, with the `wild` two-byte
unmaterialized scratch counted as span, not executable instructions. No new
formal accepted ledger credit or whole-product source ownership is claimed.

Scoped review `review_th03_mainl_after97_work.py lsetlocl-wild` plus
`tests.test_mainl_after97_work`. Both raw native OBJ/LIB/EXE/MAP vectors,
compiler/link phase logs and source-bound receipts are retained under
`.analysis/work/after97-lsetlocl-wild-*` and
`.analysis/work/mainl-after97-lsetlocl-wild-*`. The original cold pair was
reused, **not rebuilt**.
