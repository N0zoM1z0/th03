# TH03 MAIN after834: original PMD sound-effect interrupt and priority ownership

The original small physical `snd_se` TC4 source owns two far functions,
`void far pascal snd_se_play(int)` and `void far snd_se_update(void)`, in
**120 original SHARED CODE bytes**. It is not the entire PMD or MIDI driver:
those original owner boundaries and hardware services remain separate.

The maintained source now expresses the **actual PMD sound-effect play
service directly in the updating function**, rather than routing
`AH=PMD_SE_PLAY`, `AL=snd_se_playing` and `INT 0x60` through a redundant
inline helper taking an unsigned-byte reference. The vector is an original
constant (`TH03_SE_PMD_VECTOR=0x60`), not runtime dispatch. The returned
register/interrupt semantics remain the same: a frame-zero effect is
played only when FM sound is active and a valid effect has been selected.
The original priority arbiter still indexes `snd_se_priorities` first by
current effect then incoming effect, resets `snd_se_frame` only on
preemption, and retains postfix mutation of the original **8-bit global
frame** before checking the original timeout table. No new checks,
bounds handling or behavioral defensive fix was introduced.

## Actual original-compiler codegen tests

- `af834a`: removing the inline reference helper and directly issuing the
  PC-98 software interrupt from `snd_se_update()` **passed two genuine
  original TC4/normal TLINK rounds**, with the whole 120-byte object exact.
- `af834b`: reordering the semantically equivalent priority comparison
  into `priority[new] >= priority[current]` changed evaluation/codegen
  and **failed** the original OMF CODE comparison (**121** candidate
  initialized bytes vs **120** original). The original order was restored.
- `af834c` and final **`af834d`**: the original constant PMD vector is
  named and the source documented. Both stages separately compile the
  complete maintained original owner in two original TC4/TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af834d --units snd_se
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af834d
```

Both final rounds match **all 120 original CODE bytes, 18 ordered literal
native OMF FIXUPP fields, two PUBLIC offsets**, original segment/storage
layout, the full normal MAIN EXE and MAP, all **124,642 Japanese loaded
program bytes and 1,553 original ordered MZ relocations**. The independent
standard MZ serializer reproduces the entire **130,882-byte Japanese
MAIN.EXE**. The **98 other original project objects and CRT** were reused
without a cold replay. Complete current-source proof and protected actual
native compiler/writer evidence:
`.analysis/work/exatt-layout-af834d/report.json`, SHA-256
`c70db428da0d361cc9bc9670f6aef8f39d88a1cb1af54ef3bf481899fd4a8ea8`.

`snd_se` was already a previously source-backed original physical owner;
this is **new natural C++ source and native proof quality**, not additional
distinct original CODE byte credit, historical raw OMF packet equality,
complete PMD source ownership or canonical packed-game Factory acceptance.
