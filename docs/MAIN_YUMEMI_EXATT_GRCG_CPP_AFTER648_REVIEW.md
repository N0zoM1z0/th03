# Yumemi Extra Attack: natural signed GRCG beam extent and original slot ABI (after648)

The Yumemi Extra Attack original physical compiler module is a full
five-function, **1,696-CODE-byte** owner. It contains ordinary flying
projectile creation, explicit on-field warning creation, a very
large GRCG cross-beam plus sprite-outline renderer, a dual hitbox
and striped collision-map state machine, and batch rendering.
This proof is for the **entire** actual compiler object, not a
render-subroutine fragment.

The long `yumemi_exatt_render_one` previously represented the
beam-shrinking extent as a byte-cast, signed-byte `0xF8`
addition and subtraction:

    extent = ((signed char)(p->duration + (signed char)0xF8 - p->frame));

The clearer, typed natural C++ is now:

    extent = static_cast<signed char>(p->duration - 8 - p->frame);

Both expressions maintain the original signed 8-bit truncation and
the surrounding 16-bit Turbo C++ code generation, including the
range check, hardware GRCG line operations and the full mixed
sprite outline. The independent actual-source-rooted native
compiler/linker checkpoint `af648a` proved the complete original
CODE and OMF fixups unchanged; no fake jump-table padding or
target-byte embedding was used.

The maintained original entity pool is now explicitly described
as **16 physical 32-byte slots per player**, eight ordinary
flying projectiles plus eight special warning beams. The creation
and batch loops use those named bounds, and preserve the original
special pool base address. The renderer's 0x10-frame opening
window, late sprite-corner radius 0x18, the update's 8-frame
radius growth and 0x28 arrival-state gate are named separately;
the original +8 duration fade end and its two intersecting
collision regions are unchanged. These are compile-time enums,
not newly allocated DATA/BSS.

Both actual original Turbo C++ 4.02/TLINK rounds of the complete
source, including the shared source-bound 32-byte entity header,
have exact OMF COMENT source dependency paths and match:

- Every one of the **1,696 original CODE bytes**;
- All **87 literal ordered native FIXUPP fields**;
- All **five PUBLIC offsets**, original segment metadata, and
  native 16-bit near/far register ABI;
- Both complete normal MAIN EXEs and path-normalized full MAPs;
- The original loaded Japanese MAIN image and **1,553 ordered MZ
  relocations**, with the separate standard MZ serialization
  reproducing the exact 130,882-byte Japanese MAIN.EXE.

Build/review only this affected source owner:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af648b --units ex_yume
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af648b

Retained native report:
`.analysis/work/exatt-layout-af648b/report.json`
SHA-256 `436f6aeb5bae02b9c480fa552fe580be2f0cec9d3f9155aae4fcda036f1bbd8c`.
Both actual modified-source compiler outputs, OBJ, EXE, MAP, linker
responses and writer logs are retained under ignored native evidence.
No whole-project cold replay was performed.

This improves source-level physical meaning and signed arithmetic
within *previously counted* original CODE. Historical vendor raw
OMF packet identity, canonical packed-file Factory acceptance,
untested PC-98 hardware behavior and independent pristine
source provenance remain separate claims.
