# OP PI and PFOPEN native source review

2026-10-29: four complete functions now have current OP source ownership:
PI243 plus PFOPEN281,524 CODE bytes/28 native fields/five literal ordered MZ
relocations. No private DATA/BSS, library bodies or external storage are added.

| Procedure | Segment:offset | CODE | Return cleanup |
| --- | --- | --- | --- |
| PI palette | 0BEB:04A6 | 37 | Far Pascal2 |
| PI draw | 0BEB:04CB | 136 | Far Pascal6 |
| PI load | 0BEB:0A90 | 70 | Far Pascal6 |
| PFOPEN | 0000:2EF2 | 281 | Far Pascal8 |

## Complete native PI producers

The current `pi_put.cpp`173 and `pi_load.cpp`70 TC4 producers consume literal
includes of maintained `src/shared/formats/pi_put.cpp` and `pi_load.cpp`.
Both have BYTE-aligned SHARED CODE and empty DATA/BSS, with only the listed
native publics. Every actual dependency is checked. The consumed `mem.h`,
`_defs.h` and `_null.h` copies also match the pinned installation.

The unchanged MAINL layout module supplies native field/name grammar only;
its resolved image is discarded. OP's own raw objects and both OP MAP public
tables resolve every field anew. All16 native fields and five MZ entries match
the target/candidate in emitted order. The full two producers and all three
function return boundaries/cleanup are checked; no object or executable is patched.

Palette apply copies the48-byte palette and calls palette_show. Drawing retains
the original row loop, packed-image width, one-step top wrap after each row and
far pointer normalization. Offset arithmetic truncates before the normalization
step; do not add a carry fix for artificial pointer inputs. Load retains the
GAME3 free-before-load branch and the original loader result. Slot accesses,
coordinates, allocations and library results remain unchecked. Palette/PI buffers,
headers, memcpy and graphics services remain external context.

## Actual PFOPEN carrier and source transport

The old notes name the unsplit `th03_op.asm` producer. The current native public
actually belongs to `th03_optail.asm`/`obj/th03/optail.obj`:1258 CODE bytes,
WORD-aligned _TEXT, and empty local DATA/BSS. PFOPEN begins at native offset920.
Its actual provider `th03/formats/pfopen.asm` is a byte-for-byte copy of maintained
`src/shared/formats/pfopen.asm`, including CRLF transport. The containing source
includes that provider exactly once, and the native dependency records confirm
consumption. This retained legacy provider path is a bounded include in the real
tail TU; it is not described as a new standalone assembler producer.

Every consumed tail source/include, native segment/public and complete MAP
allocation is bound. PFOPEN's281 bytes have explicit, nonoverlapping LEDATA
coverage. The verifier does not fill unrelated holes in the enclosing module
with zeros or claim ownership of the complete tail.

The12 native fields preserve their actual emitted order:five relative WORDs for
service calls,three absolute CODE WORDs for decoder pointers andfour DGROUP
WORDs. Each service call is already emitted as PUSH CS/CALL near to the same
_TEXT frame, keeping the far return stack without a segment relocation. The
decoder pointers are near offsets for PFGETX0/PFGETX1/PFGETC1. Both OP MAP tables
resolve all fields independently; the complete function matches the Japanese
target and current candidate, with an empty MZ vector.

The private near call to STR_IEQ targets300C after the separate alignment byte
at300B. The comparator, alignment byte, other tail functions and global data
remain contextual. All direct PFOPEN branches enter complete instructions
within its97-instruction body, which ends at the genuine RETF8.

## Preserve the game-specific archive behavior

PFOPEN uses the cached32-byte archive header table through FS:DI. It allocates
PFILE, opens BFILE and walks filenames with the private comparator. A zero
header type reaches seek_error, which falls through into seek in this version;
it is not repaired into an early failure return.

The selected physical file offset is copied to PFILE and passed to BSEEK_. Aux
selects the plain/encrypted byte reader; compression selects the plain/RLE
decoder. Preserve the transient ES=CX assignment and subsequent ES restoration.
The16-bit packed/original sizes are zero-extended into DWORD accounting fields.
The native error paths keep their different byte/word pferrno stores and original
close/free order. No new allocation/file-failure model or defensive product fix
is required to establish equal native source.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_asset_native
.venv/bin/python -m unittest tests.test_op_asset_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use one CPU, nice10 and empty displays. These scopes reuse the unchanged verified
native cold pair without compiling, linking or replaying runtime models. Focused
checks reject identical corrupt PI/PFOPEN images, reordered palette MZ entries
and invented PFOPEN segment relocations. Whole OP source ownership and the
scanner's separate legacy trailer remain open.
