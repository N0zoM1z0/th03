# TH03 MAIN after846: exact original explosion collision, chain and score source

The original physical `e_expl` is the complete **630-CODE-byte
far-`__cdecl` explosions_hittest()** module. It traverses all EFE
slots, performs enemy/pellet/fireball intersections, increments the
original byte-saturating chain counts, awards original signed 16-bit
bonuses/score and updates fireball/Extra Attack charge in their original
order. It is a small *physical owner*, but not a trivial no-op leaf.

The current C++ now names all real bonus and geometric parameters:
subpixel explosion radius multiplier, blue/red fireball base bonuses
100/444 and per-hit 16, pellet per-hit 2, score awards 1/40/80, gauge
charges 4 and `against2*3`, and the three ascending hit-count regions
(4/10/20) with their 2/5/2/2 progressive charge gains. The original
8-bit hit count stops at 255; the signed `bonus += round_speed` and
`bonus >>= 1`/`bonus += bonus` remain distinct so arithmetic and
rounding are not silently changed. Enemy-pid filtering, per-four-frame
hit rate and original collision traversal order are preserved.

## Original TC4 experiments, including two genuine negative controls

- `af846a` challenged `expl_p->frame &3` with natural byte `%4` and
  **failed** whole CODE comparison (639 initialized candidate bytes
  versus original 630). The original bit test remains.
- `af846b` challenged the apparently equivalent byte hit saturation
  check `hits <255` with `hits !=0xFF`. This also **failed** real
  original codegen despite the candidate retaining 630 initialized
  bytes. The original strict `<` comparison remains.
- `af846c` named radius/score/bonus constants and the original 255
  threshold; two independent original TC4/TLINK rounds fully matched.
- `af846d` additionally named **all four** real chain charge increments
  in the original 4/10/20 hit regions, with unchanged 8-bit mutations.
  Both native rounds still matched every original byte.
- Final `af846e` has precise comments on byte clock saturation and
  signed bonus arithmetic; the whole maintained source was compiled
  again in two genuine original compiler and full normal linker rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af846e --units e_expl
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af846e
```

Both final original Turbo C++ 4.02 and normal TLINK rounds reproduced
**all 630 original CODE bytes, 49 literal ordered native OMF FIXUPP
fields, one PUBLIC**, original source/segment/ABI, full original normal
MAIN EXE/MAP, all **124,642 Japanese loaded program bytes and 1,553
original MZ relocations**. The separately reviewed standard MZ
serializer recreates all 130,882 original Japanese MAIN.EXE bytes.
The other **98 original project objects and CRT were reused**,
no all-project cold replay or byte patching. Protected full current-source
proof `.analysis/work/exatt-layout-af846e/report.json`, SHA-256
`1c07a4c097d94e06dd05cc67e41924262973a1d1045f8964da1db66b68a2c68f`.

This is revalidated source fidelity for an *already historically
source-covered original physical owner*. These 630 bytes cannot be added
again as new distinct covered CODE, nor promoted to vendor packet-
identical OMF or canonical packed-file Factory acceptance.
