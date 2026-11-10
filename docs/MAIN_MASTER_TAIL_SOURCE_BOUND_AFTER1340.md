# Original TH03 MAIN master tail: initialized DATA / BSS provenance

The 35 KB symbolic assembler carrier now tracked at
`config/main_work/data_carriers/mst_tail.asm` reconstructs the original
`obj/th03/mst_tail.obj` physical state contribution. This is build-only
composition: it includes both original ReC98 data declarations and
TH03-specific global game state, not a claimed decompiled function.

The original physical object has **zero executable CODE bytes**. Its
initialized `_DATA` records contain **1,566 real bytes**, within a
**1,606-byte DATA segment**; its `_BSS` segment spans **22,250 bytes**
of reserved globals. All **414 PUBLIC symbols** and their addresses,
segment definitions, initialized bytes and order-sensitive OMF fields
match the current native output. It carries no literal fixup fields.
These large storage byte counts must **not** be added to the 88,373-byte
selected physical CODE total, nor equated to newly authored gameplay.

Two generated sprite text inputs `score.asp` and `pellet.asp` are saved
in `config/main_work/generated_sprites/` (respectively 2,053 and 7,207
source bytes). The build's required include graph is recursively checked
against tracked maintained sources and the retained ReC98 reference,
**including** the matching original BMP source images. The special
`th03/math/randring.inc` actually consumed by the build is byte-for-byte
identical to the maintained `src/main/math/randring_getters.inl`, rather
than the older vendor version, and is explicitly bound as such. All
63 recursive/sheet/image dependencies are recorded by source hashes.
The retained reference library is not independently vendored by this
commit, and canonical packed-file/whole-product source acceptance remains
open.

Native source-bound stage `af1340d` reassembles only `mst_tail` in two
independent original TASM 5.0 rounds. Replacing the true historical
physical slot in the unchanged 99-object TLINK 6.10 response yields
both **byte-identical Japanese MAIN executables**, full normalized
MAP and ordered MZ relocation vectors. Its original object is checked
across all DATA/BSS/CODE segments and symbol offsets, not only the
executable bytes.

Negative control `af1340e` changed `_snd_active`'s initialized value
from `0` to `1` **in an isolated input**, with all other contents the
same. TASM compiled successfully but the complete original payload
comparison correctly rejected the wrong DATA. The tracked source and
original target were never modified. No full cold replay occurred.

Read-only current input and native output review:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_master_tail_storage.py --stage af1340d --check
```
