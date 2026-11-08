# TH03 MAIN Fireball: separate explosion sprite and collision geometry

The full fireball explosion renderer now distinguishes its 64x64 visual
sprite from the 64x48 collision placement rectangle. The sprite dimensions,
hitbox dimensions and half-width/half-height offsets are named independently.
The original vertical placement bug is preserved: the visual sprite is
centered using a 48-pixel collision height, so it appears 16 pixels lower
than a correctly centered 64x64 sprite.

The complete fireball owner retains the original animation keyframes,
division-by-four sprite selection, 24-slot update/collision/render loops,
generation/chain state and the byte predicates from af964d.

## Direct-call experiment

The separate af964f trial replaced the original inline far-return carrier
with the apparently natural condition:

    if(!hitbox_hittest()) { ... }

The original hitbox function returns with RETF, while the original caller's
NOP / PUSH CS / CALL NEAR sequence is a group-relative far-return idiom.
TC4's direct C++ call selected a different call relocation and the complete
e_fireb CODE comparison failed. The source restores the original carrier;
the successful af964e proof below includes it unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af964e --units e_fireb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af964e

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire 1,555-byte original E_FIREB_TEXT object and linked each through the
complete normal MAIN response. Both reproduce all 115 literal ordered OMF
FIXUPP fields, ten PUBLIC offsets, the original one-byte DATA and one-byte
BSS carriers, the complete 124,642-byte Japanese MAIN loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects and the
original Borland CRT were reused; no full cold replay.

Protected source-current report:
.analysis/work/exatt-layout-af964e/report.json, SHA-256
3f03d78b2808918c5377e79bb14a164d86c38d585642db79e95358fd2f287cba.
The af964d receipt is the immediately preceding source snapshot with the
same object CODE and the natural byte predicates; af964e is the current
source proof including the named explosion geometry.
