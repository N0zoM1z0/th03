# TH03 last applied storage audit — after439 (2026-11-05)

**Important:** newer after440, after441 and after442 source work appeared
while preparing the agent handoff. **This after439 cleanup is a frozen,
successfully completed audit, not an authorization to clean the newer
checkout.** The pinned cleanup tool now fails closed by design. Next agent:
continue any dirty source, determine the latest complete source receipt,
audit its expanded dependency graph and receipt SHA, then write a new
checkpoint-specific cleanup guard **before any further deletion**.

**Last applied protected-storage policy.** This is the verified **647-source
MAINL CRT after439** checkpoint, not the former after388/511-source or
319-source storage reports. Source-built CRT CODE = **174,691 original-
equal bytes**; two independent TASM/TLIB/TLINK rounds produce Japanese
MAINL EXE and MAP that are byte-for-byte equal to the original. This is
**working-source equality**, not Factory accepted packed-game credit.
For acceptance caveats, see [the current agent handoff](RE_HANDOFF.md).

## Immutable proof roots — do not clean

The **after439-audited** source-bound graph consists of **177 stages**, including the
55 static inherited stages and all later stages through
`after439 / streambuf-base-default-constructor-boss`.
The fully audited original receipt is:

```
.analysis/work/mainl-after439-streambuf-base-default-constructor-boss-build.json
SHA256 dd0a1a82695b00e2a3aeaa4e93a609450b50e834e4dd80b228c2eddaef5e8788
```

The guarded path inventory contains **4,464 unique protected files**
(**275.62 MiB allocated**) under `.analysis/work`: all **177 receipts,
2,055 successful writer logs, 354 native EXE, 354 MAP, 354 LIB and
1,170 assembled OBJ**. Keep the *complete* contents of both rounds,
not only the latest EXE. Source reviewers use full source/driver/parent
hashes and the original raw producer outputs. Do not rewrite these
files as hardlinks, compress them into substitutes or delete a parent
stage because the filename looks old.

Also preserve `.analysis/targets` and the original Japanese binaries,
`.analysis/toolchain` (the needed Wine/Borland prefix, ~1.3 GiB),
Ghidra/JDK attested evidence, `.analysis/runtime`, `.venv`, reference
scaffolding, the original `reference.tar` input, the accepted ledgers,
all maintained source, previous cold/provenance proofs, the unresolved
`h_ldiv` alias investigation and significant `xx`/exception diagnostics.
The **other ~140 MiB** under `.analysis/work` is *not* declared unused:
it contains separate context, old investigations and products that still
require individual source-reference/dependency analysis.

## After439 audited cleanup — actually executed

**Guard:** `scripts/cleanup_mainl_after439_handoff.py` is pinned to the
literal after439 builder/parent DAG, the above receipt SHA-256, source
files, 177-stage topology and both full raw native rounds. It fails
closed if a newer builder/receipt exists or the pinned proof changes.
Its default behavior is **dry run**, not deletion. The candidate set
comes only from *completed superseded alternative modes at a live stage*,
plus uncited regenerable top-level disassemblies, with tracked source/text
references excluded. Incomplete/failed alternative modes, source
provenance diagnostics, quoted documents, symlinked/hardlinked inputs and
all active receipt/log/output paths are protected.

A full audit selected **15 files** from the completed but superseded
`after392 / cpp-vector-delete-boss` mode, consisting of its extraction
log and two complete alternative OBJ/LIB/EXE/MAP/log production rounds.
The active `after392 / vector-destructor-boss` round files were **not
selected**. The alternate mode's small historical JSON build receipt was
retained as metadata; its retired raw outputs must be regenerated before
that *old alternative mode* can be independently rerun.

The guarded `--apply` deleted exactly **15 files / 1.54 MiB allocated**.
Its deletion inventory is preserved outside Git at
`.analysis/work/handoff-after439-retired-20261105.txt`
(SHA-256 `b5b3f14a2feb0f6e1b561098aeac1762cce750de232b4e69524d192a45970dd2`).
Separately, `clean_generated.py --caches-only --apply` removed three
regenerable Python bytecode cache trees (about **6.6 MiB reported** at
cleanup time). Such caches may be regenerated during subsequent reviews;
this is not a permanent disk saving estimate. The original `.analysis/work`
allocation dropped from **426,804 KiB** to **425,236 KiB** immediately
after the scoped pruning (before later review logs).

**Post-delete proof passed:** the complete after439 source reviewer
still reports 647/893, 174,691 original-equal CODE bytes, two byte-exact
Japanese EXE/MAP native rounds and 677 ordered MZ relocations. All five
`tests.test_mainl_after439_storage_cleanup` safeguards passed, including
SHA-256 verification of **every** active source/driver/log/raw output
path. The next guarded cleanup preview shows **zero eligible files**.

## Historical verification commands; no new pruning under newer stages

```sh
python3 scripts/cleanup_mainl_after439_handoff.py                # EXPECT FAIL CLOSED after newer source stages
python3 scripts/cleanup_mainl_after439_handoff.py --list         # likewise fails closed; do not bypass guard
# Never --apply the frozen after439 audit with after440+ source. Repin a NEW audited guard first.
.venv/bin/python scripts/clean_generated.py --caches-only --apply
# The historical tests.test_mainl_after439_storage_cleanup now deliberately
# fails closed because newer source layers exist; do NOT bypass that guard.
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after439_work.py streambuf-base-default-constructor-boss
```

The **after388** cleanup tool and its hard-coded 126-stage tests are
historical and deliberately fail closed at after439. The 511-source
policy is preserved as [after388 archive](STORAGE_HANDOFF_AFTER388.md),
and the older 319-source report as
[2026-11-05 archive](STORAGE_HANDOFF_2026-11-05.md). Do not run their
`--apply` commands on this checkout. For the next *new source layer*,
**re-audit the entire live DAG and update the pinned receipt SHA and
stage counts before cleaning**; do not weaken the guard.

**Never blanket-run** `.venv/bin/python scripts/clean_generated.py --apply`
or its `--prune-unreferenced-receipts` option: the ordinary preview does
not enumerate all dynamically read native proof dependencies. Caches-only
is deliberately restricted to regenerable cache directories and does not
remove `.analysis` proof.
