# TH03 MAIN Fireball: natural byte predicates across the full 24-slot engine

The complete fireball owner now uses natural C++ zero predicates in the
movement, collision and render controllers:

- The free-slot exits in both 24-projectile forward passes use !p->flag.
- The large reverse collision scan uses !p->hp for the original zero-HP
  destruction condition.
- The hitbox result uses !_AL for the original zero-damage skip.

These are byte values, not C++ bool storage. The original enum/state values,
the post-collision frame reset, signed index and near-pointer updates,
uninitialized historical chain_slot behavior, RNG/generation side effects,
and both 24-slot traversal orders are unchanged.

## Cross-segment call investigation

The remaining manual hitbox call is not a routine direct-call cleanup.
The original hitbox function ends in RETF and the original caller uses the
five-byte NOP / PUSH CS / CALL NEAR sequence. A fresh earlier experiment
(af945a) added samecodeseg and attempted a direct C++ call while retaining
the inline stack setup; TC4 emitted PUSH CS / LCALL instead and grew the
complete fireball CODE from 1,555 to 1,557 bytes. The source keeps the
original far-return carrier until a natural spelling can reproduce the
same group-relative call and stack layout. This is based on the actual
object and compiler output, not just a stale comment.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af964d --units e_fireb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af964d

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire 1,555-byte original E_FIREB_TEXT object and linked each through the
complete normal MAIN response. Both reproduce all 115 literal ordered OMF
FIXUPP fields, ten PUBLIC offsets, the original one-byte DATA and one-byte
BSS carriers, the complete 124,642-byte Japanese MAIN loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects and the
original Borland CRT were reused; no full cold replay.

Protected source-current report:
.analysis/work/exatt-layout-af964d/report.json, SHA-256
270c036089c7c395a44dc3bd52b6ebf1646eddbe56fb0247140d15c5b87df29b.
The earlier af964b and af964c reports are retained as intermediate source
snapshots; af964d is the combined current-source proof for all three
predicates.
