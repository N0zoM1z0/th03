# Kotohime charged-shot native C++ state and physical ABI (after655)

The complete original cs_koto physical TU contains nine source functions
and exactly 690 CODE bytes in the original MAIN_10_TEXT linker group.
It owns player charged-shot reset, creation, motion/culling, private
sprite rendering, hitbox test, batch render and Gauge-to-Extra Attack
control. The real source was forced through the v2 Borland TC4.02
compiler, not an inherited stale TH03WORK copy.

Two natural C++ state tests compile to original bytes:
- The collision check reads a nonzero active byte through ordinary
  C++ truthiness, rather than explicitly comparing to zero (af655c).
- The update/render early-return checks use ordinary logical
  negation on that same byte (af655d).

The original physical charged-shot record is eight bytes:
one-byte active and animation fields, four-byte center at +02,
and two-byte vertical velocity at +06. Compile-time original
16-bit size and offsetof assertions protect the layout.
The per-character Gauge timing view is also exactly four bytes.
Charged-shot downward velocity starts at -16 and accelerates by
-2 until the projectile crosses the original negative Y boundary.
The Gauge state emits an Extra Attack at its first frame and
ends on frame 0x80. Named compiler-time values carry these
physical and temporal semantics without adding DATA.

Important negative control: replacing the collision routine's
original BX-cast macro with a natural register-near pointer
made TC4 select SI and save it on the stack, increasing CODE from
690 to 692 bytes (af655b). The original BX register/near pointer
contract remains explicit, as does the unmodified collision and
one-hit side effect. This is not a safe refactor merely because
the resulting high-level semantics look equivalent.

Final original-source/OMF-COMENT-attested TC4/TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af655e --units cs_koto
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af655e

Both independently compiled native object rounds match all 690
original CODE bytes, all 79 literal ordered native FIXUPP fields,
nine PUBLIC offsets, complete original OMF segments, the normal
whole MAIN EXE and path-normalized complete MAP. The Japanese
loaded program, 1,553 ordered MZ relocations and independently
serialized 130,882-byte Japanese MAIN.EXE match byte-for-byte.

Retained native evidence:
.analysis/work/exatt-layout-af655e/report.json
SHA-256 11a15643519ac516e9acb95796f08b113a71961dd0698670855a7fa41bffbf94.
Only this one physical TU was recompiled; the other 98 original
objects and CRT libraries were reused without a cold replay.
Historical raw vendor OMF packet byte identity, new canonical
Factory packed-game credit and PC-98 hardware runtime behavior
remain separate unproven questions.
