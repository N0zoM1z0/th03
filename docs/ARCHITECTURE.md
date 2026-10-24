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

The ZUN sprite16 driver also has a bounded compatible OMF producer pinned in
`config/th03_zun_driver_jwasm.toml`. Its public source and private native tool
are attested separately; the normal TLINK still links the resulting object.
This does not identify the original assembler or change the base Borland tools.
The syntax adapter preserves all maintained instruction and data includes.
The driver uses one translation unit with nine CODE contributions in DGROUP.
Root WORD/EVEN alignment and eight PARA contributions generate its 71 intergroup
zero bytes through normal TLINK layout; no sized filler arrays supply them.
This compatible organization preserves every linked byte and public address;
the original source/object organization is unknown. Three plus nine reserved
DATA bytes remain separate, unreviewed context.

`src/shared/hardware/input_modes.cpp` is one complete nine-function / 367-byte
CODE producer in both OP and MAINL, retaining its GAME3/O first-use wrapper.
Its two link layouts and six ordered far-pointer relocations are reviewed
independently. `review_th03_shared_input_work.py` binds the full current cold
pairs to complete input-policy and wait witnesses; per-product publication
retains separate source acceptance. Keyboard, joystick and frame services are
bounded interfaces, with zero private DATA/BSS ownership in this producer.
MAINL also owns two ending waits / 126 CODE bytes in a separate GAME3/L
producer. They execute the owned input interface: its AX result replaces the
sound query result before the unsigned measure comparison. Frame waits use
an unsigned IRQ counter and preserve their distinct far Pascal cleanup sizes.

`.analysis` keeps targets, runtime files, tools, current Ghidra state and one
working build tree. Historical experiments and validation archives are disposable.
Download archives and installation media are needed only for installation;
bootstrap checks their hashes. Routine checks verify the installed tools.
