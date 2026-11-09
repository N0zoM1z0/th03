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
The unchanged after596 cold parent is retained, not repeated for
every source refactor.

MAIN's cold builder additionally re-extracts its one explicitly pinned VS vendor module
with native TLIB in each round;installed CRT/runtime remain vendor context.
Current reports live in `.analysis/work/`. MAINL uses native TLIB extraction and
rebuild without changing the893-member order. The historical cold normal-library
pair had28 source providers; that is not the current source-bound library count.
The separate historical full-xx candidate added provider29 and linked the actual
product, but was raw-different and unaccepted. See [xx product review](MAINL_XX_PRODUCT_REVIEW.md);do not replace the
accepted publication with that candidate.

The full-xx candidate uses actual BCC4.5 `-c -y` objects. Separate `-S` output
supplies mangled names only;native source-file/LINNUM records bind all50 bodies
to transported definitions. Earlier S/TASM bank/full-TU miniatures stay separate.
Named instruction intrinsics cover unsupported386 operations;all addresses keep
compiler symbols and offsetof-derived member offsets. Normal TLIB/TLINK own the
library and product layout;no object/ASM patch supplies product bytes.

The historical shared-runtime chain reaches after548. The retained after554
MAINL selected link contains root552, picture table553 and both text banks554.
Its 893-slot source-bound library and source-generated
C0 link both MAINL and OP with complete original decoded-file equality;
OP's original packed-file proof is retained from the earlier packing stage. Actual selected CRT material is
75/76 members, respectively. The shared `src/shared/crt/dos_exec.asm` corrects
the real original LIDATA initialization and four literal frames; historical
`src/mainl/crt/exec.asm` stays as an unchanged ancestor input. See the
[shared runtime proof](SHARED_EXEC_OP_RUNTIME_AFTER537_NATIVE_REVIEW.md).
After538–548 retain that source DAG and refine selected frames, GROUP, PUBLIC
and literal field order. The live shared startup `src/shared/crt/startup_large.asm`
now reproduces all 58 ordered C0 fields, original raw entry/segment/import
records, 623 initialized CODE/144 DATA bytes, two true CODE cache holes and
128 reserved STACK bytes. Native TASM is retained; the tested compatible JWasm
entry/frame changes are rejected. C0 PUBLIC packets agree as sets but remain
unordered. See the [latest native review](SHARED_STARTUP_AFTER548_NATIVE_REVIEW.md).
That chain uses after548's actual startup pair and the after554 report's actual
root/picture/text-bank objects, retaining after535 as its frozen startup baseline.
Its 893 library members stay unchanged from after547;
C++ exception owners retain 2,117 CODE/296 DATA bytes and 89 ordered fields.
Their reviewed PUBLIC packing differences and four BSS bytes remain explicit.
`stdio_buffer.asm` still has two MOV operand pairs in the wrong fixup order,
the sole order-only member among the 76 selected OP runtime streams. These
refinements add no authored-function or whole-product acceptance credit.

A separate MAINL input candidate in `src/mainl/hardware/input_scan.asm` reproduces
all 417 instruction bytes and 42 ordered fields of the held-key scan. The
following target 90 byte has no adopted source owner; its omission changes
later addresses, so the input candidate remains unaccepted. The historical after554
link retains the previous contextual input object. A read-only audit locates project allocations outside published
decoded scopes without interpreting tables, alignment or BSS as missing code.
See the [input candidate review](MAINL_INPUT_SCAN_AFTER549_NATIVE_REVIEW.md).

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

MAIN's current player core, round-result and active-shot producers group only
complete functions (3135/1060/449 bytes). Their ordinary native records and
link positions reproduce all1553 literal MZ entries while preserving the prior
load image. Historical standalone wrappers remain separate from this current
three-TU graph. A subsequent native TLIB extraction restores the original
master.lib VS DATA8/BSS8 between real root head/tail source contributions; its
physical90 closes1DB05 without source padding. This explicit prebuilt vendor
context adds no authored/source-exact credit. EC2D and the header remain open.

The old-named `reference.tar` remains a pinned OP/MAINL cold-graph source input.
Output age or proximity to this archive does not establish that a native proof
tree is disposable; follow the [current storage policy](STORAGE_HANDOFF_CURRENT.md).

## Evidence and behavior

`config/units.csv` records source presence, origin, boundaries and coordinates;
`evidence.csv` and `knowledge.csv` preserve findings and qualification.
`config/oracles.toml` defines the required gates. Current decoded publications
are `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`; MAIN's detailed
proofs live in `config/main_work/`. `docs/PROGRESS.md` and `resources/progress.svg`
are generated by `scripts/progress.py`. The handoff gives a dated snapshot.

MAINL's cold backend pins predate the maintained Staff and root-controller
sources, so its broad decoded publication is pending. Current source-native
reviews at `af942s` and `af944r` validate these physical owners independently;
MAIN's `af1053k` review validates its selected twelve-owner integration. Reporting
shows their verified scopes alongside publication state. All progress bars use
tracked unit extents; MAIN's function ledger is a separate measure. Missing
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

`config/toolchain.toml` pins the cold native tools,prefix and surfaces.
`config/mainl_work/exception_toolchain.toml` separately pins the optimizing
BCC4.5 producer for natural C++ allocation/exception providers; native suitability
is scoped by complete output comparison,with the existing TC4 SDK.

`config/analysis_toolchain.toml` pins Ghidra/JDK, full installation trees and MZ
loader behavior. Ghidra projects are under ignored `ghidra-project/`. Re-attest
before using database observations; decompiler/function boundaries are hypotheses.

Use headless tools with empty DISPLAY/WAYLAND_DISPLAY, one CPU at nice10, bounded
Java heap and one serialized Borland/Wine writer. Preserve the local prefix,
private targets/assets and actual installed tools. See the workflow for commands.
