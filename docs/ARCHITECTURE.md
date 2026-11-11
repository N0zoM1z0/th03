# TH03 architecture

## Products and source

| Product | Role | Maintained source |
| --- | --- | --- |
| OP.EXE | Title, menus and game handoff | `src/op/` |
| MAIN.EXE | Main game | `src/main/` |
| MAINL.EXE | Ending and related menus | `src/mainl/` |
| ZUN.COM | Launcher and embedded payloads | `src/zun/` |

Proved common code belongs in `src/shared/`; dependencies are local or explicit
`compat/rec98/` forwarding. `.c`, `.cpp`, `.asm` are translation units; `.inl` is
a bounded include. Existing composer/provider paths are part of frozen native
recipes: consult the actual source graph before deleting or moving a file that
looks unused. Reference/compiler candidates are not automatically native owners.

`_reference/ReC98` supplies the pinned scaffold, headers and vendor context.
It remains reference material with its own authorship/license. Build wrappers
retain original first-use GAME/BINARY combinations and compile/link order;
a file shared by OP and MAINL has separate product-specific native proofs.

## Storage and coordinates

Japanese targets are pinned in `config/targets.toml`, with
`candidate-local-attested` provenance. Independent pristine-dump attestation is
unknown. Never substitute patched, translated or reference-game executables.

OP, MAINL and ZUN have DIET storage envelopes. Canonical stored-file coordinates,
decoded load addresses and native object offsets are different spaces.
`config/th03_diet.toml` pins the decoded identities. Current builders repeat
normal DIET `-B` packing/restore and compare complete decoded/stored files.
TH04's `-G` packing does not match TH03 OP.

A target-equal executable can still contain unowned reference/vendor code.
Complete product source acceptance additionally requires reviewed ownership,
layout, literal ordered relocations and native reproducibility. Unit
boundaries, inline compiler tables, unreachable instructions, initialized DATA,
BSS and linker gaps receive separate treatment. BSS is not file-backed; whole-game
source/function denominators remain unknown.

## Native builds

| Product | Cold/staging builder | Working tree in Wine `drive_c/` |
| --- | --- | --- |
| MAIN | `build_th03_main_work.py` / `replay_th03_main_native.py` | TH03WORK |
| OP | `build_th03_op_work.py` | TH03OP |
| MAINL | `build_th03_mainl_work.py` | TH03ML |
| ZUN | `build_th03_zun_work.py` | TH03ZUN |

These are the heavy **cold builders**: they recreate source inputs
and rebuild full game-object graphs in two independent rounds, when
that scope is actually needed. Routine TH03 MAIN C++ reconstruction
now uses the narrower
[`probe_th03_main_exatt_layout.py` source-native overlay](RE_HANDOFF.md)
and its independent reviewer: recompile only affected physical
translation units, compare their complete native OBJ/OMF, and reuse
unchanged original objects in the full normal TLINK response.
The frozen after596 link parent is retained, not repeated for
every source refactor.

MAIN's cold builder re-extracts its pinned VS vendor module with native
TLIB; installed CRT/runtime remain vendor context. Reports live in
`.analysis/work/`. The retained after596 parent supplies unchanged original
link inputs for current overlays. Its historical source snapshots must not
be overwritten with current source.

MAINL and OP retain a source-bound 893-slot library and shared startup/CRT
ancestry. The after554 MAINL link supplies root, picture and text-bank context;
current MAINL publication additionally uses the `af1055m` Staff/root refresh.
Native TLIB/TLINK preserve library member order. The current `af1369m` route
recompiles all 36 MAINL project objects and the complete maintained BCC4.5 xx
object in two rounds, reproducing the full decoded EXE and MAP with the
29-source-provider library. See the [current composition review](CURRENT_LINKED_BUILD_REVIEW.md)
and [xx source recovery](MAINL_XX_PRODUCT_REVIEW.md).

The shared startup still has a PUBLIC packet-order gap, and
`src/shared/crt/stdio_buffer.asm` retains two MOV operand pairs in the wrong
fixup order. The shared runtime's exact findings and these remaining limits
are recorded in the [DOS exec review](SHARED_EXEC_OP_RUNTIME_AFTER537_NATIVE_REVIEW.md)
and [startup review](SHARED_STARTUP_AFTER548_NATIVE_REVIEW.md). Keep their
actual current dependencies. The current four-file package freshly assembles
shared C0 and compares its entire physical scope without replaying that
historical runtime chain. Its stored outputs all match the Japanese targets;
whole-product source ownership remains open.
MAINL's complete held-key function is now accepted through the independent
no-trailer TC4 proof. Its alternative ASM carrier still has the historical
trailing-byte/layout question described in the
[MAINL input review](MAINL_INPUT_SCAN_AFTER549_NATIVE_REVIEW.md).
This is separate from MAIN's original-object link discrepancy below.

OP's current-source adapter supplies the original menu Git blob only while
constructing its historical staging graph, then overlays the live maintained
include before compilation. It preserves old stager pins without compiling a
historical product. The temporary read view is removed.

ZUN composes five native payloads, a semantic directory TU and launcher/transfer
TUs. Sprite16 uses pinned JWasm plus normal TLINK as a compatible OMF producer,
not an original-assembler identity claim. Its nine CODE contributions, PARA/WORD
alignment and EVEN generate the accepted layout through ordinary linking.
Reserved driver DATA remains separate. `scripts/lib/zun.py` is also a frozen
MAIN scheduling input; keep its hash.

MAIN's current proof is a **selection of independent native physical-owner
reviews**, not the historical three-TU core/round/shot experiment or one
all-source cold build. Rebuilt owners are linked against retained original
objects, with complete normal EXE/MAP and ordered relocations checked each
time. The original VSYNC storage (`VS.ASM`, eight initialized DATA/eight BSS
bytes), master global DATA/BSS carrier, MAIN root and zero-size segment-order
scaffolds now also have selected source-bound checks. Their data/segment
sizes must not be counted as executable gameplay CODE. The original 417-byte
TC4 `input_s` versus the historical 418-byte TASM link carrier is still open.

The pinned `reference.tar` is an actual OP/MAINL staging input. Keep that
source archive while those builders consume it; historical trial archives and
cleanup reports are unnecessary. See the [storage guidance](STORAGE_HANDOFF_CURRENT.md).

## Evidence and behavior

`config/units.csv` records source presence, origin, boundaries and coordinates;
`evidence.csv` and `knowledge.csv` preserve findings and qualification.
`config/oracles.toml` defines the required gates. Current decoded publications
are `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`; MAIN's detailed
proofs live in `config/main_work/`. `docs/PROGRESS.md` and `resources/progress.svg`
are generated by `scripts/progress.py`. The handoff records current blockers
and next work.

MAINL's source composer preserves the historical ownership transformations and
stages maintained Staff/root C++ verbatim. The `af1055m` refresh recompiles both
physical owners and restores decoded publication using unchanged retained cold
evidence. The standalone `af942s`/`af944r` owner reviews remain valid.
**MAIN's active source selection is now defined by `scripts/status.py` and
generated `docs/PROGRESS.md`**, not by the obsolete `af1092k` engine/BOSS
integration experiment. Reporting shows current verified physical scopes
alongside publication state. All progress bars count tracked unit extents;
MAIN's function ledger is a separate measure. Missing
publication never selects the historical 145-owner mixed-product proposal.

Native verifiers bind complete OMF records/publics, MAP allocations and ordered
relocation fields to actual producers. Comparison-buffer fixup resolution never
patches objects or executables. Ordinary same-CS far-call relaxation is accepted
only with native group/ABI proof; explicit padding/target arrays are not substitutes.

Runtime models and native ABI probes are optional supporting tools. Use them
for specific reconstruction uncertainties; full register/memory models,
allocation-failure/null-pointer matrices and exhaustive mutation/input suites
are not general acceptance requirements. An equal native body does not need a
second implementation in Python. Keep original unchecked semantics and avoid
product-hardening changes.

Existing OP nested-context and startup tools retain their historical scopes.
Hardware/DOS/library replies are interfaces, not physical execution evidence.
A stopped prefix receives no successful-return credit. New source work does not
require extending every older runtime model before native ownership review.

OP entry initialized DATA has a separate zero-procedure owner. BSS begins at
the decoded file end and remains separate. Unreferenced strings, compiler tables
and linker gaps require native ownership review rather than runtime coverage.

## Local tools

`config/toolchain.toml` pins the cold native tools, prefix and surfaces.
`config/mainl_work/exception_toolchain.toml` separately pins the optimizing
BCC4.5 producer for natural C++ allocation/exception providers; native suitability
is scoped by complete output comparison, with the existing TC4 SDK.

`config/analysis_toolchain.toml` pins Ghidra/JDK identities, full installation
trees and MZ loader behavior. Factory supplies the shared executable installations;
[shared tools](SHARED_TOOLS.md) describes their local selectors and isolated
state. Ghidra projects are under ignored `ghidra-project/`. Re-attest before
using database observations; decompiler/function boundaries are hypotheses.

Use headless tools with empty DISPLAY/WAYLAND_DISPLAY, one CPU at nice10, bounded
Java heap and one serialized Borland/Wine writer. Preserve the local prefix,
private targets/assets and actual installed tools. See the workflow for commands.
