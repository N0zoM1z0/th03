# TH03 MAIN Mima BOSS split renderer: original TC4 register allocation after717

After experimentally recovering Marisa's C++ register allocation, the
analogous Mima BOSS `mima_render_split(int distance, unsigned char angle)`
was investigated independently against Mima's **own original physical
object**, not assumed to match because the characters look similar.

The old renderer manually assigned `_SI = distance` and used `_SI` as the
polar radius in **four separate `polar()` evaluations**, interleaved with
sprite16 mask interrupts and sprite rendering. We replaced that manual
register state with natural `register int split_distance = distance`,
**declared before** the existing register `left`, and used that local as
the radius in all four original C++ calls. The two masks, far calls, angle
rotation, native ABI and original ordering remain unchanged. The original
`0xAAAA`, `0x5555` and `0xFFFF` overlap mask interrupt sequence remains
hardware-specific because it has an actual side effect.

The very first independent native trial (`af717a`) **passed**: original Turbo
C++ 4.02 naturally allocated the two locals exactly as in the original
binary without hand-writing `_SI` at all.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af717a --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af717a

Both genuinely compiled native rounds matched the **complete 1,922-byte
original Mima CODE, 9 PUBLIC offsets, all ordered literal OMF fields**,
original segment definitions, complete normal TLINK MAIN/MAP, all 1,553
Japanese MZ relocations and independent full original Japanese
130,882-byte MZ output. Only `ba_mima` was compiled; 98 other original
project objects and CRT reused. No full cold replay.

Receipt: `.analysis/work/exatt-layout-af717a/report.json`, SHA-256
`e4608ad8a2073098d851350af7d7e781eb44f8d6754006e4a1fb578328e99ea4`.
Evidence retains actual native source and OBJ dependencies, both full
linker rounds, original byte comparisons and native logs. This is a
natural C++ improvement to original BOSS source, **not** extra canonical
Factory packed-unit acceptance or proof of historical vendor raw OMF
packet identity.
