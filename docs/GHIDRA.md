# Headless Ghidra

`config/analysis_toolchain.toml` pins the same Ghidra 12.1.3 and Temurin
21.0.12.1+1 installations used by TH04. `.tools/ghidra` and `.tools/jdk` are
relative stable selectors. Acquisition archives are in `.tools/downloads`.

```sh
bash scripts/bootstrap_analysis_toolchain.sh
python3 scripts/attest_analysis_toolchain.py
python3 scripts/ghidra.py th03-main import --max-cpu 2
python3 scripts/ghidra.py th03-main check
```

Import once for each of `th03-op`, `th03-main`, `th03-mainl`, `th03-zun`.
Imports refuse existing projects. Databases live in `ghidra-project/TH03-*.gpr`
and `.rep`, exports and independent receipts below `.analysis/ghidra`.
Ghidra rejects dot-prefixed components in a project path.

The pinned MZ loader uses load segment 0x1000, applies relocation words, and
maps the original header separately. Full file bytes, header/load mapping,
relocations, entry and deterministic samples are independently checked.
Automatic function/block boundaries remain provisional.

The native Factory wrapper accepts `check`, `decompile OUTPUT ADDRESS...` and
`query OUTPUT OPERATION ARG...`, with optional `--artifact ARTIFACT`.
It is strictly read-only and clears DISPLAY/WAYLAND_DISPLAY while enabling
Java headless mode. No GUI, per-game HTTP listener or visible desktop is used.
