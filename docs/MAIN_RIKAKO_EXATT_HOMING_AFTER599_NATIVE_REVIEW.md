# Rikako homing flag and five native Extra Attack producers — after599

Rikako's Extra Attack update contains a real branch that applies an eighth of
the signed angle difference toward the opposite player only if byte +0x17 of
the shared 32-byte entity is zero and its frame is in [0x40, 0x50].
Its initializer chooses that byte randomly; the immediate extra-attack
initializer forces it to one, suppressing the homing adjustment. The old
`tail[1]` access was byte-correct but hid this gameplay state.

This change gives +0x17 the per-character name
`character.rikako.homing_disabled` in a union over ten raw trailing bytes,
rather than incorrectly assigning Rikako's interpretation to every character.
`offsetof` and `sizeof` 16-bit compiler assertions bind the +0x16 tail,
+0x17 flag and complete 32-byte stride. Rikako's large update and render
source now includes the same header as shared flight/Reimu, Mima and Yumemi.

## Native proof

Use the original 16-bit Turbo C++ 4.02 and normal TLINK, not a host compiler:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af599t --units ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup

The complete native proof contains two fresh compiler/linker rounds and keeps
both original-code/ordered-fixup/public and whole-link evidence. Original
object sizes and native ordered fields:

| Original slot | CODE bytes | Ordered fields | PUBLICs |
| --- | ---: | ---: | ---: |
| ex_yume (large renderer) | 1696 | 87 | 5 |
| ex_mima | 727 | 44 | 4 |
| ex_rika (homing update) | 702 | 46 | 5 |
| ex_rfly (shared flight + Reimu prefix) | 825 | 51 | 8 |
| ex_reup (Reimu update/render) | 331 | 22 | 2 |
| **Total** | **4281** | **250** | **24** |

The emitted CODE, ordered 16-bit relocation fields, PUBLIC offsets and
segment definitions in **both rounds** match each original OBJ. Both linked
normal MAIN EXEs and normalized complete MAPs match the retained after596
source link. The target program and all 1,553 ordered MZ relocations match
the Japanese MAIN, and the separate serializer gives the exact 130,882-byte
original file.

Evidence: `.analysis/work/exatt-layout-af599t/report.json`;
SHA-256 `7bd72139d434db696ae8bb3ca868c5d3931449b3c9e2ae067d9a02c1ec63c5c1`.
Both round objects, links, MAPs, commands, logs and overlay sources are
retained in ignored native work.

A failed early `af599s` experiment passed the flight producer but hit
a native DOS TCC command-line problem while passing the long Reimu compile
definition as an option. The successful stage puts the compile-time partition
definition in the *source wrapper*, not on the DOS command line. This does
not change the product source and naturally produces the original 331-byte
Reimu update record. The `af599r` three-owner control also previously passed.

This work strengthens a specific C++ entity/ABI/source interpretation. All
4,281 CODE bytes were already owned; **no new accepted code-byte credit**,
original vendor OMF byte identity, packed-file provenance or Factory whole-game
acceptance is implied.
