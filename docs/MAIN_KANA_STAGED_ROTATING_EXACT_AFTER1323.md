# Kana BOSS: original staggered volleys, rotating phase and sprite cadence

The complete Kana BOSS now expresses the staged ring and rotating-ring
emission windows as two independent unsigned-word frame tests. The
staggered pattern selects the original slow, middle and fast volleys
only within its release interval; a middle-frame burst still fires its
ring before sixteen paired pellets. In that inner loop the byte angle
and subpixel speed now naturally use `+=` for the original `+6` and
`+3` advances *after* each `bullets_add()` call. The rotating pattern
still advances its byte angle only after the original turn-frame gate,
with the four-frame firing clock checked separately. Kana's intro blink
likewise requires both the pre-`0x20` frame window and the odd global
frame state.

Positive original TC4/TLINK source trials `af1323a` (staged window),
`af1323b` (rotating window), `af1323c` (intro blink), `af1323d` (pellet
angle advance), and `af1323e` (pellet speed advance) independently
matched the entire Kana physical owner in two rounds. After retaining
cleanly nested original-source C++, final stage `af1323f` reproduced
**1,874 CODE bytes, 274 literal ordered native fields and nine PUBLICs**.
Joint stage `af1323g` additionally recompiled the current Bullet engine:
**4,559 CODE bytes, 470 ordered fields and 29 PUBLICs** matched in both
complete normal Japanese MAIN links, including the MAP and ordered MZ
relocations. Neither stage invoked whole-source cold replay.

The original AL-mediated signed rotating delta choice and the literal
`SUB AL,10h` cloud-angle step remain intact: earlier attempts to replace
those register-visible operations had changed the original byte code.
The source work here does not assume that source-level equivalence alone
proves native machine-code equivalence.

Recheck only the current Kana source scope:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1323f
```
