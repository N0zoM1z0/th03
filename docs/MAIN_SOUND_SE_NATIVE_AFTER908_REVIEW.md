# TH03 MAIN after908 — exact PMD sound effect leaf and byte-state update

The original physical `snd_se` Turbo C++ 4.02 owner contains **both
complete far sound-effect functions**: `snd_se_play(int)` and
`snd_se_update()`. Their real source ABI is a PC-98 fixed software
interrupt **INT 60h**, with AH operation 0x0C and AL the selected byte
sound-effect ID, and separate byte priority/frame arrays. No new
runtime DATA or guessed hardware interface was introduced.

Both sound-active checks can naturally use explicit `snd_se_active()==0`,
and the zero-frame interrupt trigger can use `snd_se_frame==0`,
without affecting the original short-circuit ordering or register code.
The expiry comparison can also read naturally as
`snd_se_frame > snd_se_priority_frames[snd_se_playing]` in place of its
reversed operand form, while preserving the true byte frame
postincrement and 0xFF none sentinel. The priority choice inside
`snd_se_play()` **cannot** similarly have its operands reversed without
a native-code difference.

Independent actual original TC4 trials:

- `af908a`: explicit `==0` in sound-active and interrupt-frame tests,
  complete original CODE and normal MAIN exact twice.
- `af908b`: same explicit inactive guard in the second function,
  preserving original `||` evaluation, exact in both native rounds.
- `af908c`: changed byte `snd_se_frame++` to prefix. Original TC4
  generated **124** vs **120** CODE bytes (first difference segment
  1 offset 66); original postfix restored.
- `af908d`: reversed the expiry-frame comparison to a natural
  `frame > duration`, still original-code exact twice.
- `af908e`: separately reversed the **priority-table** operand order
  in `snd_se_play`. Real TC4 emitted **121** vs **120** CODE bytes,
  first difference at CODE segment 1 offset 4. Reverted, confirming
  the earlier codegen warning independently.
- Final `af908f`: full current source and explicit PC-98 register/ABI
  comments compiled in two independent actual original TC4 4.02 and
  complete normal MAIN TLINK rounds with exact native CODE and fixups.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af908f --units snd_se
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af908f
```

Both rounds reproduce **120 original CODE bytes, 18 literal ordered
native OMF FIXUPPs and two PUBLIC offsets**, original source/segment/
far-register ABI, complete normal MAIN EXE and normalized MAP, all
**124,642 Japanese loaded bytes and 1,553 ordered MZ relocations**.
Independent standard DOS MZ serialization reproduces 130,882 pinned
Japanese MAIN.EXE bytes, not vendor header-byte serialization identity.
**98 other original project objects and CRT reused**, no full cold
replay, modified original CODE/OBJ or synthetic NOP padding.

Protected genuine source-bound TC4/TLINK report:
`.analysis/work/exatt-layout-af908f/report.json`, SHA-256
`c5a864c7c20e02e4c038f08ea567e986cfbe29aa87c422872c16fc5c93784203`.
This was historically source-covered original CODE; no new distinct
CODE ownership, raw vendor packet identity or canonical Factory
packed-game acceptance is claimed.
