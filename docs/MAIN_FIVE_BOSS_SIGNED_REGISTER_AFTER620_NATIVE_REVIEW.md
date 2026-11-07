# Five major BOSS renderers: exact signed C++ shift (after620)

These are the complete original Chiyuri, Kana, Kotohime, Ellen and Rikako
BOSS C++ translation units. Together they contain pattern schedulers,
large attack/update functions, intro and ring renderers, not merely isolated
leaf tests. This revision recovers the screen-Y signed right shift in
natural Turbo C++ **without** embedding the SAR opcode:

    _AX = top;
    static_cast<int16_t>(_AX) >>= 4;
    top = _AX;
    sprite16_put(left, _AX, sprite_offset);

In Rikako's original loop, the existing `_AX += -8` between shift and
assignment remains unchanged. The 16-bit **signed** lvalue conversion
is necessary. An ordinary `_AX >>= 4` emits SHR AX,4 (C1 E8 04) while
original requires SAR AX,4 (C1 F8 04). Replacing the whole AX/local/
argument sequence by `top >>= 4; sprite16_put(...top...)` also changes
compiler-owned local writes. The typed expression preserves the entire
original register and stack protocol and supplies the original opcode
from real natural C++ lowering.

The earlier after603–605 overlay `v1` runs had incorrectly compiled a
stale source path and cannot establish equality of those old rewrites.
The corrected v2 source-bound controls show `af620a` (old Chiyuri
rewrite) fails, `af620b` (unaltered original) passes, `af620c`
(unsigned AX expression) differs by the SHR/SAR ModR/M byte, and
`af620d` (signed AX expression) matches the full 2,654-byte Chiyuri
BOSS again. The four other BOSSes similarly compile exactly in
`af620e` using the typed signed expression.

Kana's cloud-ring angle is a separate low-level byte operation. Simple
`_AL -= 0x10` and signed cast `static_cast<int8_t>(_AL) -= 0x10`
generate ADD AL,F0 (04 F0), while original requires SUB AL,10h (2C 10).
The correct inline-ASM instruction is therefore preserved with an
explanatory comment. `af620f` and `af620g` retain those negative
compiler controls.

Final two independent native source- and OMF-dependency-verified compiler
and normal MAIN linker rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af620h --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af620h

| Original full BOSS TU | CODE bytes | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| Chiyuri | 2,654 | 381 | 11 |
| Kana | 1,874 | 274 | 9 |
| Kotohime | 1,840 | 262 | 11 |
| Ellen | 1,675 | 213 | 9 |
| Rikako | 1,677 | 215 | 8 |
| **Total** | **9,720** | **1,345** | **48** |

All native OBJ CODE payloads, literal ordered fixup fields, PUBLIC offsets,
segment definitions, path-normalized complete MAPs and two full normal
MAIN links are original-equal. The loaded Japanese 124,642-byte MAIN image,
all 1,553 ordered MZ relocations and the separate complete standard MZ
serializer (130,882-byte Japanese MAIN.EXE) remain equal. No full cold
replay or object-byte patching was used.

Receipt: `.analysis/work/exatt-layout-af620h/report.json`,
SHA-256 `359c55052577f48270fdff9635fc780fd585bd5330d1e4e4b4ef79ce5642d08b`.
Both actual compiler/linker rounds, writer logs, source overlays and
all raw OBJ/EXE/MAP files are retained. No new canonical packed-file
Factory credit, historic vendor OMF packet identity or physical hardware
behavior claim is made.
