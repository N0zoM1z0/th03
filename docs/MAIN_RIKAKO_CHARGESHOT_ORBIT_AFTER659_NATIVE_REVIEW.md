# Rikako charged-shot: natural signed orbit turning and four-projectile ABI (after659)

The physical `cs_rika` original Turbo C++ producer is an entire
eleven-function 1,280-CODE-byte unit, including four orbiting shot
initialization, private player-centered shot, large orbit update,
sprite rendering, collision hit tests and the paired four-shot Gauge
attack. It was source-bound for the first time in the independent
two-object `af658a` control.

The original large `chargeshot_update_rikako` changed each
projectile's unsigned 8-bit polar angle according to the slot
index's parity using `p->angle = p->angle + ((i & 1) ? 8 : 0xF8)`.
Both of the following actual natural C++ recovery steps emitted
**identical original Turbo C++ CODE**:

- `static_cast<unsigned int>(i) % 2` replaces the masked
  parity test, retaining its true 16-bit unsigned bit meaning
  (`af659a`).
- `p->angle += ((static_cast<unsigned int>(i) % 2) ? 8 : -8)`
  directly writes the signed +8/-8 orbit rotation into the
  original one-byte angle field, replacing manual addition and
  opaque positive 0xF8 (`af659b`).

Real codegen is material: a tempting rewrite of the Gauge attack's
`bullet_template.angle = -bullet_template.angle` as binary
`0 - bullet_template.angle` changed the original CODE
(`af659c`), so that original unary expression remains.

The maintained C++ also names the four real charged projectiles
per player, the original six-byte record (+00 4-byte center,
+04 unsigned angle, +05 reserved), two player attachment modes,
the expansion/retreat frame thresholds 0x20/0x80/0x90, the
0x20/0x60 radius changes, and Gauge expiration at 0x80.
Compile-time original TC4 `sizeof`/`offsetof` assertions
check the record and four-byte Gauge timing view. The special
`_CX`/CL register-bound four-shot initialization remains
intact; no unrelated runtime state or BSS is introduced.

Final changed-source/OMF-dependency-attested original native
Turbo C++ 4.02 and full MAIN TLINK two-round proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af659e --units cs_rika
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af659e

Both native objects reproduce all **1,280 original CODE bytes,
137 literal ordered FIXUPP fields, eleven PUBLIC offsets**,
original complete segment metadata and normalized whole MAIN MAP.
Both normal MAIN executables match the frozen source-native parent,
including all 1,553 ordered Japanese MZ relocations, the loaded
program image and the separately serialized exact 130,882-byte
Japanese MAIN.EXE.

Complete preserved original source, emitted OMF and writer evidence:
`.analysis/work/exatt-layout-af659e/report.json`, SHA-256
`d2370071d9d402ed497f913d0059f9f13d74ee607d85d205b09c30c228a9e94e`.
Only the affected original source TU was compiled twice, reusing
all 98 other project objects and startup/CRT libraries. No full
cold replay or target/object byte patching.

This is original-byte-exact natural C++ improvement to already
tracked source-owned game CODE. Historic vendor raw OMF packet
identity, canonical packed-game Factory credit and PC-98
hardware runtime remain separately unproven.
