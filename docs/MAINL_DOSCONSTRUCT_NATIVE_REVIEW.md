# MAINL DOS command and environment constructors

The complete maintained `src/mainl/crt/doscmd.asm` and `dosenv.asm` own311 and365
CODE bytes at decoded0000:895B and0000:2DFB. Each exports one near entry,
`__DOSCMD` or `__DOSENV`, and ends in `RET12`. Each receives three far pointers;
the callee consumes their12 bytes. Neither contributes initialized DATA/BSS.
The earlier loader's lack of caller cleanup at these two calls is intentional.
Deferred argument cleanup elsewhere concerns the ordinary far C calls.

DOSCMD receives argv, an optional prefix and a far pointer whose presence enables
argv copying. Its third pointer is never dereferenced. It always counts argv
strings for allocation, including when copying is disabled. Size starts at3,
uses wrapping16-bit additions and optionally includes prefix length+1. The
output begins with a space; strings are copied using the real far stpcpy and
separated with spaces. The final space becomes CR, followed by NUL. The first
byte stores the low byte of cursor-minus-allocation-minus2. The constructor
has no command-length clamp; the loader's128-byte threshold remains separate.

DOSENV receives a far output pointer for the raw allocation, an optional program
name and an environment vector. It counts strings through a null far entry or
an empty string. Required bytes wrap16 bits before the8000h rejection; successful
allocation requests required+15. The original malloc pointer is stored through
the output pointer before alignment. Only the destination offset is rounded
with `(offset+15)&FFF0h`; the segment remains unchanged. Copies include each
string's NUL. An optional program name follows a WORD1 and has its own NUL.
Return subtracts required bytes from the final offset, retaining the segment.

The original distinguishes empty-environment representations: a null vector or
null first entry writes two NULs; a first entry pointing to an empty string writes
one. A null first entry also counts only one required byte but writes two;
subtracting required bytes therefore returns aligned-offset+1 in this case.
The maintained branch structure preserves both behaviors. One bounded actual-native
probe runs these three representations with a deterministic successful malloc
hook. It observes allocations17/16/16, two/two/one NULs in poisoned memory,
raw5000:0004, destination5000:0010, returns0010/0011/0010 and14 bytes removed
from the entry stack including the near return address. This resolves the
terminator/return/RET12 question without modelling DOS or allocator correctness.

Both original and fresh objects have BYTE CODE, empty WORD DATA/BSS and the
original literal DATA/BSS group order. Their entire initialized payloads match.
Each has five ordinary external far-call fields for malloc, strlen and stpcpy.
The old compiler emits fields in reverse site order; TASM emits another order.
Both literal streams are retained and complete field geometry compared by site.
All ten real TLINK far-call relaxations are independently resolved. Complete
source CODE matches linked output and both fixed target/current candidate;
complete scoped ordered MZ relocation vectors are empty. Dense instructions,
local branch destinations, public entries and the callee-pop12 returns are checked.

Two actual TASM/TLIB/TLINK rounds assemble both maintained TUs and compose eleven
source CRT providers in one normal893-member library. The existing natural
farheap, exec and loadprog pairs are validated and reused; the six original source
providers remain. All member positions and888 other current member payloads are
unchanged. Full two-OBJ/LIB/EXE/MAP vectors repeat; the entire decoded EXE and MAP
match the pinned Japanese target and retained MAP. The36 project objects and938
cold outputs/source/recipe/tools remain unchanged. No full cold/DIET or ancestor
runtime replay is needed. The frozen cold recipe still has six CRT replacements;
this bounded combined recipe establishes coexistence of all eleven providers.

The new scope adds2 library extents/procedures and676 CODE bytes. MAINL now accepts
187 extents,250 procedures or entries,29,715 CODE+1,886 DATA=31,601 bytes:
16,695 authored and14,906 library. All previous185 owner records and nested scopes
remain unchanged. Source presence becomes216 extents/42,043 bytes, including old
overlapping aggregate rows that receive no duplicate accepted credit. No padding,
object edits,defensive behavior changes,physical DOS execution or whole-product
source acceptance is claimed. Further CRT providers and remaining ownership are open.
