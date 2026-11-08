# TH03 MAIN Rikako BOSS: natural signed orbit-angle selection

The orbit spread's signed angular choice no longer needs an explicit cast on
the negative arm. The original source expression selected between a positive
`0x30` and `(signed char)-0x30`; the maintained source now uses the named
signed values directly in the ordinary C++ conditional expression. Both
branches still convert to the original `signed char angle_delta`, and the
RNG draw remains exactly once before the radial bullet loop.

This is a fresh compiler result rather than a general rule about signed
compound updates: Rikako's mutable `boss_spin_delta` and render-frame byte
updates retain their original compound expressions because different natural
rewrites have already changed TC4 output.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af963a --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af963a
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 1,677-byte original Rikako BOSS** and linked each object through the
complete normal MAIN response. Both reproduce all **215 literal ordered OMF
FIXUPP fields and eight PUBLIC offsets**, the full original Japanese MAIN
loaded image (**124,642 bytes**) and all **1,553 ordered MZ relocations**.
The other **98 original game objects and original Borland CRT** were reused;
no full cold replay, target patch, original OBJ patch, synthetic byte buffer
or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af963a/report.json`, SHA-256
`78fa528372b3450e59d4b9ae5467e04018390feb3601f56fc76b8f6d677302ff`.
The preceding `af961c` report is now a historical source snapshot because
this follow-up changes the same physical owner. During `af961a`, two new enum
identifiers collided after Turbo C++'s 31-character significant-name limit;
shortening the identifiers fixed the compile without changing the source ABI.
