# TH03 after710 — narrowly audited cleanup for next-agent handoff (2026-11-07)

This records the **actual applied changes**, not a proposed blanket source
proof deletion. The active after709 native proof and source-bound ancestors
remain intact. The [current storage policy](STORAGE_HANDOFF_CURRENT.md)
and [short current handoff](RE_HANDOFF.md) are the live entrypoints.
The earlier [after597 audit](STORAGE_HANDOFF_CURRENT.md#actually-removed-in-the-after597-disposable-only-audit)
is separate: do not add its old reclaimed allocation again.

## Applied: six isolated source-probe configuration failures

The new strict source-controlled tool
`scripts/cleanup_after710_disposable_native_stages.py` permitted
only **six explicit IDs**, each consisting of two private trees:
one `TH03WORK/probe/<stage>` and one
`.analysis/work/exatt-layout-<stage>`. These attempts failed due
to **native verification tool assumptions about linker input slots
or MAP row ownership**, not because target code was reconstructed
incorrectly. All had **no completed `report.json` and no second
native compiler round**, were absent from tracked source/docs and
from all other ignored work JSON reports, and were not an active
source-bound native proof DAG root.

| Retired stage | Original, later corrected verifier mistake |
| --- | --- |
| `af694a` | `ch_setup` historic TLINK input was not the generic OBJ slot |
| `af694b` | `p_gauge` really has three MAP rows, not four |
| `af696a` | Both physical Combo producers really have six MAP rows |
| `af699b` | `p_exatt` really has three MAP rows, not four |
| `af705a` | `core` historic TLINK input was not the generic OBJ slot |
| `af705b` | `lose` MAP module name was incorrectly normalized |

**Physically deleted:** exactly **12 isolated directories, 93 files and
1,847,296 allocated bytes (1.76 MiB)**. No complete original/native
proof receipt, Japanese target, successful TC4 pair, compiler/toolchain,
tracked source, current native linker response, selected object or
accepted output was deleted.

The audit was **written before removal**, with full per-file
relative path, size, allocated-block count and SHA-256 under
the ignored protected directory:

    .analysis/handoff/after710-linkslot-disposable-trials/report.json
    .analysis/handoff/after710-linkslot-disposable-trials/deleted-tree-manifest.json

The manifest SHA-256 recorded in the immutable local report is:

    693697df1b7cb93351615bf4a2a2710bfd6466aa8a74e0be30fba3ed193559c7

The script defaults to preview, `--apply` refuses an existing audit
and will **not** delete any other stage, and `--verify` checks the
retirement receipt/hash and confirms the accepted after686, after703
and after709 source-native roots still exist:

    .venv/bin/python scripts/cleanup_after710_disposable_native_stages.py --verify

## Applied: official regenerable cache cleanup

The separately approved command was executed:

    .venv/bin/python scripts/clean_generated.py --caches-only --apply

Its own preview and completion both reported **approximately 9.5 MiB**
of disposable `scripts/__pycache__` and `scripts/lib/__pycache__`
bytecode. Python imports and read-only review commands may subsequently
regenerate those directories; this is gross cache allocation, **not**
durably retired native evidence. Combining it with the exact one-time
stage retirement suggests **roughly 11.3 MiB gross temporary cleanup**,
not an exact permanent reduction in the size of `.analysis`.

## Verification after actual deletion

Read-only native source/OBJ/EXE/MAP reviews succeeded afterward:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af709a
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af703a

They still verify both original Turbo C++ rounds, complete selected
object CODE, ordered literal FIXUPPs, PUBLICs, full normal MAIN/MAP,
the Japanese loaded image and its 1,553 original ordered MZ
relocations. The earlier
`scripts/cleanup_after597_handoff_storage.py --verify` also
passed prior to the new deletion.

## Explicit *not* deleted

The `.analysis` tree was approximately **3.7 GiB before this
cleanup**. Most of it is *not proven disposable*: original Wine/Borland
and Ghidra inputs, after596 MAIN, after587 MAINL, after559/561 BOSS
dual rounds, the many source-native proof intermediates, two-round
OBJ/EXE/MAP, compiler source snapshots, linker responses and logs.
**Do not delete or recompress these based only on age or disk usage.**
The after520/after597 audits are bounded, historical precedents,
not general authorizations. A new large-scale purge requires
a fresh complete active receipt-DAG audit and new independent
original-native reviewers after the physical deletion.

### Handoff rule

For ordinary next-agent work, **do not rerun `--apply`**, and never
run `clean_generated.py --prune-unreferenced-receipts` or an old
after439/388/319/511 cleanup command. Use only bounded preview,
existing protected manifests, targeted verification and the
current [AGENTS.md](../AGENTS.md) policy. If further cleanup is
considered, create a new one-time allowlist and audit first.
