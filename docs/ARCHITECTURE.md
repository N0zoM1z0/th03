# Architecture

TH03 has four products: OP.EXE (menu), MAIN.EXE (game), MAINL.EXE (ending)
and ZUN.COM (launcher). Product source belongs under the matching `src/`
directory; proved shared code belongs in `src/shared/`.
`.c`, `.cpp` and `.asm` are translation units; `.inl` files are bounded includes.

The Japanese targets are pinned in `config/targets.toml`. Their provenance is
`candidate-local-attested`; independent pristine-dump attestation is unknown.
OP/MAINL/ZUN use DIET storage envelopes. Decoded images are analysis inputs,
not replacements for the canonical stored targets.

`config/toolchain.toml` pins TC4J, TASM and TLINK. The game-local Wine prefix is
`.analysis/toolchain/wineprefix`; Ghidra projects are in `ghidra-project/`.
Installed tools are in `drive_c/TC4` and `drive_c/TASM50`; `drive_c/TH03WORK`
is the current MAIN build. `scripts/attest_toolchain.py` checks installed tools.
`_reference/ReC98` is candidate reference material, not authored progress.
Product dependencies use local source or explicit `compat/rec98/` forwarding.

`.analysis` keeps targets, runtime files, tools, current Ghidra state and one
working build tree. Historical experiments and validation archives are disposable.
Download archives and installation media are needed only for installation;
bootstrap checks their hashes. Routine checks verify the installed tools.
