# Kana charged-shot: four 13-sample trails and native Gauge C++ after658

The complete original nine-function Kana charged-shot source owner
`cs_kana` has 1,291 original CODE bytes. It includes full four-trail
state initialization, a substantial trailing-history physics update,
individual trail rendering, hit testing, sprite-overlap mode switching
and the two-sided Gauge barrage. The real source-bound original native
TC4 control `af658a` established the original object before edits.

The actual four-trail history update now shifts the **13 two-byte X/Y
samples** using a natural descending C++ loop:

    for(point = 12; point > 0; --point) {
        p->x[point] = p->x[point - 1];
        p->y[point] = p->y[point - 1];
    }

This preserves the crucial descending order and the historical
`vector2` call location. Genuine original Turbo C++ 4.02
`af658b` compiler/TLINK rounds produce *identical original
native CODE* from the edited source.

Kana's physical projectile record has **54 bytes**: 13 signed
two-byte X coordinates at +00, 13 Y coordinates at +1A,
one-byte angle at +34 and one-byte length at +35. The current
C++ uses compile-time size and offset assertions that the
historical compiler checks. Four such trails per player,
their initialization angles, the 0x30 initial length and 0x80
release length, the 0x28 release timer and the four-sample
sprite stride retain their original meanings.

The full Gauge barrage has also been improved: the reflected
X coordinate no longer needs a manual `_DX` register
intermediate, and now uses ordinary C++:

    bullet_template.center.x.v = (
        TO_SP(PLAYFIELD_W) - kana_gauge_x[pid_current]
    );

Original native TC4 test `af658d` proved it exact. The
64-frame left/right sweep, 32-frame half-period and original
0x80 end frame are separate compiler-time C++ phase names;
the existing dynamic bullet interval and all RNG state
are preserved (`af658e`). The renderer's original
`asm xor dx,dx` remains because replacing XOR with a
register assignment could change historic opcode form.

The final genuine source-/OMF-dependency-attested two-round
native compiler/full MAIN TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af658e --units cs_kana
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af658e

Both rounds exactly reproduce all **1,291 original CODE bytes, 117
literal ordered FIXUPP fields, nine PUBLIC offsets**, the entire
original OMF segment/ABI metadata, normal full MAIN EXE and
normalized complete MAP. The original Japanese loaded program
and all 1,553 MZ relocations match; independently serialized
130,882-byte original Japanese MAIN.EXE remains identical.

Retained real compiler/linker source evidence:
`.analysis/work/exatt-layout-af658e/report.json`, SHA-256
`b511bd0565618e9ab60e024d814d49ee01f063748df79a33ed32905056672984`.
Only this affected physical original project object was compiled
in two fresh rounds; remaining 98 original objects and libraries
were reused without full cold replay.

This is maintainable C++ recovery for existing source-owned bytes;
it does not assert original vendor raw OMF packet-byte identity,
new canonical Factory packed-file credit or PC-98 hardware behavior.
