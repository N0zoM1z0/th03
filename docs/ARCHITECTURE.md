# Architecture

The product boundary follows TH04 with TH03's actual four artifacts:
OP.EXE (menu), MAIN.EXE (gameplay), MAINL.EXE (ending), and ZUN.COM (launcher).
All four supplied stored targets are MZ containers, including ZUN.COM.
OP, MAINL and ZUN use DIET storage envelopes. The guarded private restoration
recipe in `scripts/review_th03_diet.py` yields MZ images for OP/MAINL and a flat
COM launcher for ZUN. These are separate decoded analysis namespaces, not
replacement canonical files or source/whole-product acceptance. The canonical
Ghidra projects continue to attest the stored images.

`config/targets.toml` pins the Japanese HDI, FAT partition and artifact bytes.
The required products are TH03 only. Optional TH01/02/04/05 targets remain
private calibration controls and contribute no TH03 progress.

`config/toolchain.toml` binds TC4J, TASM32, TLINK, runner, includes, libraries
and configuration. `.analysis/toolchain/wineprefix` is game-bound mutable
state. `.tools/ghidra` and `.tools/jdk` select physical local copies of the
same pinned TH04 tools. No mutable TH04 prefix or project is shared.

Ignored local state is intentionally split from disposable output. Preserve
`.analysis/toolchain`, `.analysis/targets`, `.analysis/runtime`,
`.analysis/ghidra`, and evidence files referenced by `config/evidence.csv`.
Cold-build trees, replay work directories, development probes, logs and Python
caches are disposable and can be pruned with
`python3 scripts/clean_generated.py --apply`.

`scripts/lib/pc98.py`, `omf.py` and `ghidra.py` preserve the TH04 container,
relocation and database-checking methods. `scripts/factory_ghidra.py` combines
a read-only query and nonce-bound full MZ export in one headless process.
The Factory independently parses the private MZ and checks the returned
attestation before exposing query output.

The reference build uses `git archive` of pinned ReC98 into a fresh private
directory. It is separate from maintained TH03 product source. The whole-build
skeleton is explicitly open until translation units, startup, linker order,
data/resource ownership and packaging are reconstructed.
