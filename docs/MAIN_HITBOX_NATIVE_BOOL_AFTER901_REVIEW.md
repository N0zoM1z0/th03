# TH03 MAIN after901 — original shotpair hitbox leaf and byte/word codegen

The full original physical `hitbox` Turbo C++ 4.02 unit contains the
single **266-CODE-byte** shotpair/explosion/Chargeshot/Bomb damage
aggregator, not a stub or extracted modern equivalent. It tests shotpair
rectangle overlap with signed subpixel coordinates; invokes the original
near-segment explosion hit-testing call, the relevant player's far
Chargeshot callback, then alternate-frame Bomb damage. Original
physical caller-visible hitbox and player state remain externally owned.

The player byte ID `hitbox.pid == 0` can be written naturally as
`if(!hitbox.pid)` and the **unsigned 16-bit** Bomb frame's original
`&1 == 0` can be expressed as natural
`if(!(round_or_result_frame % HITBOX_BOMB_DAMAGE_PERIOD))` with the
original two-frame period named in C++. The ordinary **per-shot damage
of 2** can be named `HITBOX_SHOTPAIR_DAMAGE` if written as natural
`damage = damage + HITBOX_SHOTPAIR_DAMAGE`, but **not** simply as
`damage += enum_2`: the original compiler chooses different byte
register instructions for those source forms.

The full shotpair `for/continue` scan must remain the original form,
and `shotpair.alive != true` must not be silently replaced by logical
negation. Even if these are Boolean-equivalent for normal gameplay,
the native codegen is different. All early exits, near pointer steps,
original signed collision bounds, original inline near-call carrier,
and damage byte postfix timing stay exact.

## Genuine original compiler experiments, including rejected alternatives

- `af901a`: converting the entire two-continue shotpair scan to a
  natural explicit `while` changed original CODE to **267** vs
  **266** bytes, first difference CODE segment 1 offset 29. Rejected.
- `af901b`: natural `if(!hitbox.pid)` in the far Chargeshot selector
  reproduced all original CODE and complete MAIN twice.
- `af901c`: original *unsigned-word* frame `&1 ==0` became `%2==0`,
  exact in two original TC4/full normal TLINK rounds.
- `af901d/e`: alternative `!shotpair.alive` and
  `shotpair.alive == false` **both** changed original CODE at segment
  1 offset 93; exact `alive != true` expression retained.
- `af901f`: naming the shot damage via `damage += enum_2` shortened
  original initialized CODE to **262** rather than **266** bytes,
  first difference at segment 1 offset 29. Rejected.
- `af901g`: natural explicit byte assignment
  `damage = damage + HITBOX_SHOTPAIR_DAMAGE` with the *same enum* is
  **original TC4 byte-exact**, including all original FIXUPPs.
- `af901h`: changing the Bomb's mutable damage byte postfix to prefix
  emitted **271** bytes vs target **266**. Postfix retained.
- `af901i`: natural `if(!frame_remainder)` while keeping the original
  Bomb flag condition is original-exact.
- Final `af901j`: actual current C++ with all accepted natural forms
  and source-specific comments, two independent genuine original TC4
  4.02/full normal MAIN TLINK rounds, fully original-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af901j --units hitbox
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af901j
```

Both independent original compiler/normal linker rounds reproduce all
**266 original CODE bytes, 33 literal ordered native OMF FIXUPP fields,
one PUBLIC offset**, original source/segment/callback ABI, complete
normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes and all
1,553 original MZ relocations**. Independently verified standard DOS
MZ serialization matches all **130,882 original Japanese MAIN.EXE
bytes**; historical Borland header-byte identity is a separate matter.
The **98 unchanged other game objects and CRT were reused**, without
cold replay, patching source/target/OBJ or fabricated CODE arrays.

Protected real source-bound native compiler/TLINK report:
`.analysis/work/exatt-layout-af901j/report.json`, SHA-256
`79ffe472caae9103c1e80fa6158760e60a730f3c9bc2e44f8728cef780a52e48`.
These already historically source-owned CODE bytes are better
maintained C++ evidence, **not new distinct original CODE coverage,
raw vendor OMF packet identity or canonical Factory packed-file credit**.
