# Headless Borland toolchain

The lock file `config/toolchain.toml` is copied unchanged from TH04. Compiler
probe inputs are also byte-preserved. It selects Turbo C++ 4.0J (4.02),
TASM32 5.0, TLINK 6.10 and ReC98 MS-DOS Player P0281 through Wine.

The local installation copies TH04's media and canonical unpacked tools, then
creates a fresh `.analysis/toolchain/wineprefix` and installs `C:\TC4` and
`C:\TASM50`. It does not copy TH04 build outputs, registry state or receipts.
Always regenerate the local receipt:

```sh
python3 scripts/attest_toolchain.py
python3 scripts/inspect_omf.py path/to/candidate.obj
```

Both compiler/assembler/linker probe rounds and linked probe execution must
pass. Optional host Wine hashes are observations; required portable surfaces
remain strict. DISPLAY and WAYLAND_DISPLAY are cleared during executable probes.

For an empty machine, clone pinned ReC98 first, then run the inherited
`bash scripts/bootstrap_toolchain.sh`. The acquisition hashes are fixed and
the script refuses to overlay an existing prefix or installation.

```sh
git clone https://github.com/nmlgc/ReC98.git _reference/ReC98
git -C _reference/ReC98 checkout --detach b6ba5b0a529edbb31efdf8c0e939263804f8ee47
DISPLAY= WAYLAND_DISPLAY= bash scripts/bootstrap_toolchain.sh
python3 scripts/cold_build_rec98.py --run-id UNIQUE
```

Cold reference builds are calibration candidates, not maintained products.
Use `survey_rec98_outputs.py SOURCE --gate exact --compact` for strict raw
comparison; `--gate calibration` also requires the imported object identities.
Never update calibration hashes merely because a local check fails.
