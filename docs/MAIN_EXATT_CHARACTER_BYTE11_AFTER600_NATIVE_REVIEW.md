# MAIN original Extra Attack entity +0x11: Ellen/Kotohime/Chiyuri, after600

A single 32-byte entity pool is shared by all characters, but **not every
field has the same meaning**. In particular:

- Ellen writes signed `-1` or `+1` to byte **+0x11** while preparing a
  rotating trail. Its update uses the *signed* byte as `angle += spin_delta`.
  The other Ellen initializer copies a script-supplied signed step there.
- Kotohime writes **0** for the ordinary projectile and **1** for the
  explicit Extra Attack. The same +0x11 byte chooses sprite dimensions,
  attack behavior and lifetime conditions. It is not Ellen's spin direction.
- Chiyuri declares the same 32-byte entity and runs paired beam/update
  functions, but its current code does not read +0x11. We do not ascribe
  either other character's meaning to Chiyuri without evidence.

`src/main/player/exatt_entity.hpp` now provides a **one-byte union**
(`character_mode.ellen_spin_delta` signed, and
`character_mode.kotohime_extra_mode` unsigned). The original relative
field offsets and 32-byte stride are checked by the 16-bit compiler;
the preceding Rikako-specific +0x17 flag remains an independent tail
overlay. Large Ellen, Kotohime and Chiyuri translation units now all
consume the common structure, rather than maintaining untracked copies.

The full eight-owner scoped proof covers both large functions and leaves:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af600b \
      --units ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu

| Owner | Original CODE bytes | Ordered fields | PUBLICs |
| --- | ---: | ---: | ---: |
| ex_yume | 1696 | 87 | 5 |
| ex_mima | 727 | 44 | 4 |
| ex_rika | 702 | 46 | 5 |
| ex_rfly | 825 | 51 | 8 |
| ex_reup | 331 | 22 | 2 |
| ex_ellen | 1129 | 79 | 6 |
| ex_koto | 1054 | 100 | 8 |
| ex_chyu | 978 | 55 | 4 |
| **Total** | **7,442** | **484** | **42** |

For two independent 16-bit TC4.02 compile/link rounds, complete CODE payloads,
all ordered native fixup sites, PUBLIC offsets and OMF segment definitions are
equal to original project objects. Both links produce the exact original normal
MAIN EXE and normalized full MAP relative to the existing after596 source
link. The original Japanese program image and 1,553 ordered MZ relocations
match, and the separate standard DOS MZ serializer produces the exact Japanese
130,882-byte file.

Evidence is kept in the ignored native tree at
`.analysis/work/exatt-layout-af600b/report.json`
(SHA-256 `f6aaf05a95672c93b1d580f485bc760821f4b2194816e9553d9b04b828d049c0`),
alongside all original compiler command logs, both sets of new objects and
complete EXE/MAP output. No original object/library/target is modified.
Historical after596 inputs and both old proof rounds are preserved.

The preceding after599 review initially transcribed the two Reimu unit
FIXUPP counts incorrectly: **51** and **22** rather than 57/28;
the actual machine report's sum is **250**, not 262. Those presentation
values are corrected in its review and handoff here, with no change to
the independently stored after599 receipt or compiled output.

Original raw vendor OMF packet identity, which is not established by these
CODE/FIXUPP/PUBLIC comparisons, remains unclaimed. No previously accepted
game CODE bytes are re-credited, and no canonical packed-file Factory
acceptance or untested physical runtime behavior is inferred.
