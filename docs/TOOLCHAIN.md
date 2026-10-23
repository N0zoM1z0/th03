# Tools

`config/toolchain.toml` pins Turbo C++4.02J, TASM32 5.0 and TLINK6.10.
The local prefix is `.analysis/toolchain/wineprefix`; tools are installed in
`drive_c/TC4` and `drive_c/TASM50`. `drive_c/TH03WORK` is the current MAIN tree.
Keep one Borland/Wine writer at a time and use console tools with DISPLAY and
WAYLAND_DISPLAY empty. Do not terminate unrelated Wine processes.

Use `.venv/bin/python` with `requirements-ci.txt` for Capstone/Unicorn checks.
`python3 scripts/attest_toolchain.py` checks the local tool installation.
Old replay outputs are intentionally absent; regenerate current verification.
