# Five full BOSS modules: compiler-owned render and attack math, after604

This work is a real **five-BOSS source change**, not a source-only stub or
isolated leaf test. The maintained Chiyuri, Kana, Kotohime, Ellen and Rikako
MAIN_03_TEXT translation units each contain multiple full pattern/update,
render, init and dispatch functions. The native test replaces all five
original BOSS object slots in the already source-linked, complete MAIN.

Source changes, all compiled as natural Turbo C++ 4.02 expressions:

- Chiyuri's ring `top >>= 4` and mono `_DX = 0` from after603 are retained.
- Kana, Kotohime and Ellen ring renderers replace explicit AX assignments,
  `asm { sar ax, 4 }`, and AX-based sprite arguments with the signed
  C++ expression `top >>= 4; sprite16_put(left, top, sprite_offset);`.
- Rikako's corresponding intro renderer preserves the extra **-8 pixel**
  adjustment as `top = ((top >> 4) - 8)` and the natural sprite argument.
- Kana's `kana_pattern_cloud_ring` no longer authors `asm { sub al, 10h }`.
  Its random 5-bit offset and signed angle normalization now use
  `_AL -= 0x10` before assigning the signed-char local. Its separate
  pattern function still preserves the original byte wrap and sign.

Native proof: `scripts/probe_th03_main_exatt_layout.py` (the same general
scoped source overlay also exercises large BOSSes); one run consists of two
fresh actual 16-bit C++ compile/link rounds, not a whole-project cold replay:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af604f \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak

| Full original BOSS owner | CODE bytes | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| ba_chiyu | 2,654 | 381 | 11 |
| ba_kana | 1,874 | 274 | 9 |
| ba_koto | 1,840 | 262 | 11 |
| ba_ellen | 1,675 | 213 | 9 |
| ba_rikak | 1,677 | 215 | 8 |
| **Total** | **9,720** | **1,345** | **48** |

Both rounds reproduce **all** original producer CODE payloads, ordered
literal native FIXUPP sites, PUBLIC offsets and segment definitions, not
just the instructions adjacent to the edits. Original normal TLINK EXE
and complete normalized MAP equal the after596 retained source-native link
in both rounds. The Japanese-target program bytes, **1,553 original
ordered relocations**, and separate standard MZ serialization to the full
**130,882-byte original MAIN.EXE** remain equal. There is no patched
OBJ, target-byte embedding, padding or extra base linker stage.

Native proof: `.analysis/work/exatt-layout-af604f/report.json`, SHA-256
`619bde1758dc1fb6b3a1f5cb27948cbe17c5851a0f3cd46e23bef8850b1adae6`.
Both raw object/link rounds, MAPs, compact MZ files, overlay sources and
actual native compiler/writer logs are retained. The `af604a` unchanged
four-owner baseline, `af604c` four natural renderers, `af604d` five-owner
combined proof, and `af604e` Kana cloud leaf control are retained separately.
The incomplete `af604b` edit attempt changed only Kana/Kotohime before a
source-edit assertion stopped; its successful native proof applies only to
those two changed sources. No evidence is silently promoted from it.

These BOSS modules were already present and source-backed. This is a
significant natural C/C++ **semantic/source and native-output** improvement,
not 9,720 new accepted bytes, whole-game provenance/OMF vendor packet
identity, canonical packed-file acceptance or physical emulator coverage.
