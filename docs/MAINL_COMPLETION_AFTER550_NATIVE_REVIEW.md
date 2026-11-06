# MAINL complete LUT generator, registration music and name pointers

After550 accepts three disjoint existing source owners: two complete procedures
with **98 CODE bytes / 37 instructions**, plus **40 initialized DATA bytes**.
This is newly established source ownership, not newly written implementation.

| Owner | Original address | Bytes | Maintained source |
| --- | --- | ---: | --- |
| `_hflip_lut_generate` | `0C7E:0FA4` | 30 CODE | `src/shared/formats/hfliplut.asm` |
| `_mainl_reg_music` | `095F:233E` | 68 CODE | `src/mainl/hiscore/regdata.cpp` |
| `_REGIST_PLAYCHARS` | `0E3F:0906` | 40 DATA | `src/mainl/hiscore/regdata.cpp` |

`scripts/lib/decoded_mainl_completion_native.py` independently resolves every
selected field and compares whole original decoded extents and literal ordered
MZ relocation vectors. It checks the complete unchanged regdata producer and
all188 fields before selecting eight music fields and ten pointer fields. The
LUT module has one actual offset field. All **19 selected fields** retain their
full frame/target/addend attributes and original order; the scoped MZ vectors
contain **17 relocations**, seven for music and ten for pointers. Nothing is
sorted for acceptance, masked or patched in a native output.

The LUT procedure has16 instructions, including its real entry jump and two
closed loop edges. It preserves DI and returns far without arguments. It writes
the existing256-byte LUT at DGROUP20D6; that storage is not a new owner. Music
has21 instructions, preserves the near BP frame, and calls the original
stop/load/play, fade-in, measure-delay, fade-out and stop providers. The far C
`snd_load` call retains its caller cleanup; the other far APIs retain Pascal
arguments. The table contains ten four-byte far pointers in original character
order, from none through Yumemi. Its actual registration-menu consumer and all
external name addresses agree. The strings and BSS are excluded.

## Reused native evidence

The unchanged current two-round **938-output** source-only cold graph is checked
in full, including all36 project producers, source/header/tool bindings and
actual output hashes. No native rebuild or historical emulator suite runs.
Target provenance remains `candidate-local-attested`; the pinned Japanese
decoded67372-byte image and all677 original MZ relocations remain equal.
Active shared runtime root remains **after548**.

Complete native objects:

- `obj/th03/hfliplut.obj`: SHA256
  `bb336bf20a26a4a0b74126e55b3b3342836e2537d5c7870e2146e92f098ca7c8`.
- `obj/th03/regdata.obj`: SHA256
  `007280d1c2e399e6d5d29f15549aa8ab3219cdd1ea41f578ef9f785d94c673e7`.

The direct review is
`PYTHONPATH=scripts .venv/bin/python -m lib.decoded_mainl_completion_native --current-cold`;
its saved result is `.analysis/work/mainl-completion-after550-review.json`.
The main decoded publication includes these owners and their eleven required
gates. Previous211 owners and historical reports remain available in
`.analysis/work/mainl-completion-after550-preserved/` and their original paths.

## Two pre-existing source provenance gaps

Refreshing the publication exposed old farheap and setupio verifiers comparing
later maintained source against earlier reports. Their existing later native
pairs are after332 `farheap-manager` and after493
`stdio-startup-stream-initdata-boss`. Both later sources emit **every earlier
non-comment OMF record identically, in literal order**, including segment/group
attributes, publics/imports, true holes, initialized bytes and full fixups.
The bridge validates each later source/driver, all retained writer logs, both
whole OBJ/LIB/EXE/MAP vectors and actual linked target equality. The new native
member also matches its actual library slot. It invokes no native writer.

Farheap's complete program-record stream is also equal. Setupio's debug/comment
records differ; complete program-record identity stays explicitly false.
Earlier source snapshots and report hashes remain unchanged. The publication
records the source successors rather than rewriting historical receipts.

## Remaining boundaries

The current ownership-gap audit drops project CODE outside published scopes
from905 to **807 bytes across11 contributions**. This is a queue of unowned
allocations, including tables and boundaries, not a missing-function count.
Vector alignment and the input candidate's adjacent NOP remain unaccepted.

An isolated sound-mode probe removes only its manual codestring, retains the
compiler's generated ASM unchanged, then runs native TASM. It emits29 CODE bytes
versus the retained30-byte contribution, so the trailing NOP's provenance is
still open. No padding or producer change is adopted. Preserve af550a and its
eight-file `.analysis/work/probe/completion550/manifest.json`.

No source/recipe input of the active native graph changes. No output cleanup,
canonical file-backed credit, Factory acceptance or whole-game percentage is
claimed. Focused review, publication/tracking/progress checks and
`git diff --check` are the affected validation; no full CI or cold replay.
