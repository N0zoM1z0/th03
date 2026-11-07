# TH03 MAIN after867: full Chiyuri Extra Attack paired entity and beam loops

The complete original physical `ex_chyu` Turbo C++ 4.02 source owns
**four functions**: two-entity spawn, the ~518-byte GRCG beam renderer,
full ~298-byte paired-entity update/arrival/collision controller and
16-slot rendering. This is an authentic whole-translation-unit rewrite,
not isolated simulated sprite leaves. It reuses the original 16 × 32-byte
per-player shared entity carrier and all original near/far callbacks.

## Natural source recovery and an independently found 128-unit Y distinction

All **three actual paired-entity loops** now use natural typed C++
`while`: allocate the first unused even pair, update the two entities
with original `goto chiyuri_first_done` and `continue` semantics, then
render eight independent pairs. The update loop makes the subtle
**two different pointer/index continuation paths explicit**: the
inactive/active branch jumps to its preexisting label, advances the
physical entity pointer twice and the signed pair index once; the
flying/arriving path increments the second physical entity pointer
once inside the body then once at the end, retaining the original
register allocator and original first/second entity frame updates.

The original random X range/bias, original launch speed, collision tile
width and distinct beam coordinates now have meaningful constants. A
fresh failed experiment exposed an important original gameplay fact:
**Chiyuri's second entity is initially aimed at `Y=0x1780`, but after
flight it snaps to `Y=0x1700`**, also used by the beam warning effect.
Those are **different source values** and must never be unified. The
original signed two-half beam coordinate and AX/DX hardware caller ABI
are retained rather than using mathematically similar substitutes.

## Actual original Turbo C++ experiments

- `af867a`: the complete 16-slot **paired render loop** changed to
  natural `while`, exact in two genuine original TC4/TLINK rounds.
- `af867b`: the paired spawn loop likewise became a natural `while`
  with conditional creation and post-skip two-entity stepping;
  original CODE, fixups and full Japanese MAIN still exact twice.
- `af867c`: a deliberate physical-geometry trial erroneously reused
  the **launch target `0x1780`** for the original second entity's
  arrival snap `0x1700`. The native comparator **correctly failed**
  at original CODE segment 4, offset 877, where the original
  `MOV [SI+4], 1700h` became `...1780h`. This is a concrete **semantic
  correction**, not merely a compiler spelling difference.
- `af867d`: distinct `0x1780` launch target and `0x1700` beam warning/
  arrival snap restored; both native compiler/link rounds passed.
- `af867e`: converted the large original **paired update loop** from
  a `for` with two pointer/index mutations and an inner `goto/continue`
  to a readable native-exact `while` with explicit increments on both
  control paths. Both real compiler/whole MAIN link rounds passed.
- `af867f`: challenged signed `radius = (int)_AX / 4` with arithmetic
  `>> 2` in the 518-byte beam renderer; genuine TC4 produced **975
  CODE bytes** rather than original **978**, and negative rounding
  also differs. Original signed division was restored.
- Final `af867g`: reindented and documented the three actual native-
  exact loops, separate 16-bit Y coordinates and signed division;
  both independent original compiler/full normal linker rounds exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af867g --units ex_chyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af867g
```

Both actual original TC4 4.02 and complete normal MAIN TLINK rounds
match **all 978 original CODE bytes, 55 literal ordered native OMF
FIXUPP fields, 4 PUBLIC offsets**, physical segment/source/ABI,
complete original normal MAIN EXE/MAP, **124,642 Japanese loaded program
bytes and all 1,553 original ordered MZ relocations**. Independent
standard DOS MZ serialization recreates all **130,882 bytes** of the
pinned Japanese MAIN.EXE, without claiming historical vendor header
serialization. The other **98 unchanged original game project objects
and CRT** were reused, without cold replay, patched target, NOP
padding or synthetic code buffers.

Protected source-bound proof, both native writer rounds, actual source,
OBJ/EXE/MAP and logs:
`.analysis/work/exatt-layout-af867g/report.json`, SHA-256
`32e2c8d61d0a889ecc45c18571885420a549c0d14a5a16ff02acda847d2fae3f`.
This already historically source-covered object gains real current
natural C++ and a corrected gameplay coordinate hypothesis; **no new
unique original CODE byte credit, raw vendor packet-identical OMF,
complete source-text provenance or canonical packed-game Factory
acceptance** is claimed.
