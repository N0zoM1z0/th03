# TH03 MAIN after913 — complete Kotohime Extra Attack native 10-entity state

This recompiles the original complete eight-function `ex_koto` physical
Turbo C++ 4.02 owner. The original eight ordinary and two special
32-byte Extra Attack slots, two distinct four/ten-bullet volley
controllers, beam-event lifecycle (4/8/12/16), hitbox/collmap update
and full ten-slot render all stay in their historical physical object.

The eight-slot first-free allocator and the substantial full ten-slot
beam/flying/arrival collision-and-barrage controller now use natural
C++ `while`. Its inactive `continue` explicitly advances the original
signed index and near entity pointer; the active path advances both
after the original calls and mutable byte frame update. Original
state==FREE tests naturally spell enum equality instead of truth tests.
The original four- and ten-shot attack rings and ten-slot renderer
already used native-exact natural loops and remain in the same source.
The original 32×32 and 64×64 beam sprites, special duration/radius
and 0x280/0x282/0xA00 sprite offsets have named physical constants.

Actually compiled original TC4 trials:

- `af913a`: complete ten-entity state update with its original
  inactive `continue` changed to natural `while`, complete physical
  owner and normal original MAIN exact in both compiler/linker rounds.
- `af913b`: ordinary eight-slot first-free allocator `for` to `while`,
  preserving the physical RNG and near-pointer movement; original
  CODE remained exact twice (unlike several other owners).
- `af913c`: explicit FREE enum comparisons in allocator and update,
  full native CODE/normal MAIN exact twice.
- `af913d`: replacing byte event `p->angle++` with prefix generated
  **1,059** CODE bytes instead of original **1,054**, first mismatch
  CODE segment 4 offset 702. Original postfix restored.
- `af913e`: independently replacing byte `p->frame++` with prefix
  also generated **1,059** original candidate CODE bytes instead of
  1,054. Original frame postfix restored.
- `af913f`: named original sprite/duration/radius geometry, full
  source/native object and normal linker matched twice.
- Final `af913g`: explanatory original-ABI comments and all current
  maintained full source passed two genuine independent TC4 4.02/full
  normal MAIN TLINK rounds, byte exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af913g --units ex_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af913g
```

Both independent original native rounds matched **1,054 CODE bytes,
100 literal ordered original OMF FIXUPP fields and 8 PUBLIC offsets**,
original source/segment/near-far ABI, complete original normal MAIN
EXE and normalized MAP, **124,642 Japanese loaded program bytes and
all 1,553 ordered original MZ relocations**. Independently checked
standard DOS MZ serialization matched the 130,882-byte original
Japanese MAIN.EXE; this does not prove vendor header-byte identity.
**98 other original game objects and CRT reused**, without all-project
cold replay, original target/OBJ patches, code buffers or fake NOPs.

Protected genuine source-bound native receipt:
`.analysis/work/exatt-layout-af913g/report.json` SHA-256
`eb379f57ddc317199f64b5a354a9b43ba3c8a290b2765f74badf1e959482e143`.
The original object was historically source covered. This is improved
maintained exact C++, **not new distinct CODE ownership, raw vendor
packet-identical OMF or canonical Factory packed-game acceptance**.
