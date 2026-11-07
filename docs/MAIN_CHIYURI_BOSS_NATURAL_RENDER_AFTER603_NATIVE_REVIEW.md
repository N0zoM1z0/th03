# Chiyuri BOSS: naturally emitted ring renderer and mono interrupt (after603)

The maintained `src/main/boss/chiyuri.cpp` is a **complete 11-function,
2,654-CODE-byte BOSS** source TU, not an isolated leaf or extracted opcode
sequence. The new local native overlay compiles the entire module in two
independent Turbo C++ 4.02 rounds, then relinks only its original BOSS
object slot into the existing 99-object normal MAIN linker response.

Two real C++ substitutions were proved separately:

- In `chiyuri_render_ring`, the prior explicit `_AX = top`,
  `asm { sar ax, 4 }`, `top = _AX`, and `_AX` sprite argument are now the
  natural signed expression `top >>= 4; sprite16_put(left, top, sprite_offset);`.
  This is original-equal *compiler output*, including the screen position and
  per-particle loop. Its register code need not be authored instruction by
  instruction.
- In `chiyuri_render_mono`, the interrupt's explicit `asm { xor dx, dx }`
  is now `_DX = 0;`. Turbo C++ emits the original instruction sequence with
  the prescribed DOS/PC-98 interrupt register contract. The peripheral
  interrupt API itself remains machine-specific and was not pretended to be
  ordinary portable C++.

The control run `af603c` rebuilt the unchanged maintained BOSS source and
established the correct physical `af567c` slot and full MAP normalization.
The `af603d` run changed the full ring renderer; `af603e` also changed the
mono helper. Both new source variants passed in **two fresh** compiler/link
rounds; no patching of OBJ bytes, target-copying or full cold replay occurred.

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af603e --units ba_chiyu

The entire original **2,654 CODE bytes**, **381 ordered native fields**,
**11 PUBLIC offsets**, and every OMF segment definition agree with the
original object. Both full source-native MAIN EXE/MAP outputs equal the
retained after596 outputs. Their 124,642-byte program image and 1,553 ordered
relocations match the Japanese target, and independent standard DOS MZ
serialization yields the exact 130,882-byte Japanese MAIN.EXE.

The complete proof, writer logs, both original compiler round objects and
full EXE/MAP outputs are retained under
`.analysis/work/exatt-layout-af603e/report.json`, SHA-256
`5251535828799c01cad953620465af0e95a72d328c1b4dc24e9f595b4743063a`.
This scope's historical complete native BOSS source and third-party
runtime/target inputs were not overwritten.

This is a source-naturalness and original-native-code result for an already
owned BOSS, **not** an additional 2,654 accepted bytes or evidence of
historical raw OMF vendor packet identity, canonical DIET acceptance or
physical hardware runtime verification.
