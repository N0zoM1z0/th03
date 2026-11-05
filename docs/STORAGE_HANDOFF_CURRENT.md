# TH03 active storage / agent handoff — after388, 2026-11-05

**This is the current storage policy, not the archived 319-member snapshot.**
It is tied to the pinned Japanese MAINL `after388 / string-default-constructor-boss`
working-source checkpoint: **511 complete CRT source members** out of 893,
**159,111 original-equal CODE bytes**, two full decoded Japanese EXE/MAP
byte-identical native rounds. These are **working-source results**, not
Factory-accepted packed-game credit. The active receipt is
`.analysis/work/mainl-after388-string-default-constructor-boss-build.json`
(SHA-256 `d0baf1d6ab2d1019c97d59021b2038f40bbfe434fd0ae77b6136fdf3068d23b9`).

## What MUST remain available

The protected source-bound dependency chain contains **126 active stages**:
55 inherited stage receipts in the `after317` static list, followed by 71
later stages through `after388`. They explicitly use **3,308 files** under
`.analysis/work` (original build receipts, all successful writer phase logs,
and **both complete raw OBJ/LIB/EXE/MAP production rounds**). These account
for approximately **188 MiB of file content** and must not be deleted,
archived into stand-ins, replaced with hardlinks, or inferred disposable
from their age. The source reviewers read and hash their contents.

Also preserve the `.analysis/targets` original Japanese binaries, all
original vendor OBJ/CL.LIB, the existing cold/runtime provenance,
`.analysis/toolchain` (about **1.3 GiB** of necessary Wine/Borland tools),
Ghidra/JDK attested trees, `.venv`, `_reference`, accepted ledgers, source
code, the original `reference.tar` input and the `h_ldiv` alias-order
investigation. Old posttzset/xx/native-library vectors and the apparently
large `mainl-exception-previous-acceptance.json` may support other recipes;
they have **not** been declared garbage simply because they are not among
the 126 current incremental receipts.

## Safe, narrowly scoped cleanup

`python3 scripts/cleanup_mainl_after388_handoff.py` is an **audited dry-run**
by default. It:

1. Pins the latest source builder, source-DAG topology (126 stages), and
   the exact current receipt hash; if any newer `after389+` builder/receipt
   exists or the pinned hash changes, it refuses deletion.
2. Enumerates and protects every live stage's receipt, successful phase
   logs and both raw output rounds, then selects **only** artifacts
   explicitly listed in *completed superseded alternative-mode* receipts.
   Small old receipts stay as historical metadata; failed/incomplete
   `h_ldiv` alternatives and their diagnostics are protected.
3. Adds only unreferenced, regenerable top-level `.analysis/work/*.ndis`
   and `*.dis` disassemblies. Files named in tracked documentation or
   source, symlinks, multi-linked files and non-worktree paths are rejected.
   The `xx-*-xxdisp.lst` **assembler listing evidence is protected** even
   though it may not be referenced by a literal filename in source: its
   historical per-round evidence is explicitly documented.
4. Validates candidates again before unlinking and writes the actual
   removed-path inventory to ignored
   `.analysis/work/handoff-after388-retired-20261105.txt`.

```sh
python3 scripts/cleanup_mainl_after388_handoff.py          # preview
python3 scripts/cleanup_mainl_after388_handoff.py --list   # path-by-path preview
# After reviewing source proof, targeted tests and displayed candidate set:
python3 scripts/cleanup_mainl_after388_handoff.py --apply
.venv/bin/python scripts/clean_generated.py --caches-only --apply
```

## Executed 2026-11-05 cleanup and actual savings

The above pinned plan was inspected and **applied** on the 511-source
`after388` checkout. The guarded script removed **256 ignored files**:
**92 raw OBJ/LIB/EXE/MAP/log artifacts** belonging to completed but
superseded *alternative* mode receipts, plus **164 uncited, regenerable**
`.ndis`/`.dis` disassembly files. **7.04 MiB allocated** was recovered.
The precise deleted-path inventory is preserved in ignored local
`.analysis/work/handoff-after388-retired-20261105.txt` (256 entries;
SHA-256 `ebf84558acb89a28a4ab21e10d5eb65c88c97d7ebbbe6dfac5e1e0d18f2565fe`).
The still-existing alternative JSON receipts are historical **metadata
only**: the retired raw alternate vectors would have to be regenerated
before independently verifying those old branches again.

Separately, `clean_generated.py --caches-only --apply` reclaimed another
**approximately 5.4 MiB** of Python bytecode caches. Combined allocated
savings were **about 12.4 MiB**, with `.analysis/work` falling from roughly
**340 MiB to 333 MiB**. All **3,308 active receipt/log/native files** remain
untouched. The local Borland/Wine prefix (about **1.3 GiB**) and the original
Japanese targets were deliberately **not** deleted. Original `xx` assembler
listing evidence (`*.lst`), `h_ldiv` investigation, original cold/runtime
inputs and the previous accepted-source diagnostic file were also retained.

The **same post-delete original MAINL reviewer still passes**: 511 members,
159,111 original-equal CODE bytes, 677 original ordered MZ relocations, all
latest literal original FIXUPPs, and two identical Japanese EXE/MAP rounds.
The targeted native and cleanup tests (5/5), preflight, tracking validation,
and generated progress check also passed. A repeated cleanup preview shows
**0 eligible files**. Re-running `--apply` with no candidates is a no-op;
the deletion manifest is intentionally not overwritten.

**Never use blanket** `scripts/clean_generated.py --apply` (including its
receipt-prune option) on this working source DAG: its general preview can
list dynamically read proof inputs. `--caches-only` is limited to
regenerable caches and does not touch `.analysis` proof state.

The older [319-source storage report](STORAGE_HANDOFF_2026-11-05.md) and
its frozen `cleanup_mainl_handoff_artifacts.py` are **historical** and
intentionally refuse to clean this newer checkout. For a new source
checkpoint, audit and update this guarded script's DAG/receipt SHA before
using it again; do **not** relax the guards.

## Post-cleanup verification (not a full cold replay)

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after388_work.py string-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after388_work tests.test_mainl_after388_storage_cleanup -v
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
git status -sb
```

Only an **inspected** cleanup + the same still-passing source-bound proof
justifies a storage-savings claim. This is not a new cold replay or formal
Factory source acceptance.
