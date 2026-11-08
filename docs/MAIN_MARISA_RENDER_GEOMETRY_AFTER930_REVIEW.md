# TH03 MAIN Marisa BOSS: renderer sprite identity and TC4 code generation

The complete maintained `ba_maris` physical source now distinguishes the
hit-flash and flicker-overlay sprite offsets (`+0x16` and `+0x1C`), the two
separate strip art offsets (`+0xF00` and `+0x1180`), the final 112-by-16 strip
and the ring high-level threshold. These named values preserve the original
order and arithmetic in the full Marisa major BOSS.

The byte-accurate original TC4/TLINK experiment `af930e` recompiled the
**entire 1,431-byte** BOSS object twice, verifying **199 literal ordered
OMF fixup fields, nine PUBLICs**, the unchanged complete normal Japanese
MAIN EXE/MAP, all 124,642 loaded bytes and 1,553 ordered MZ relocations.
The original unchanged 98 game objects and CRT were reused; no cold replay.
Native report: `.analysis/work/exatt-layout-af930e/report.json`, SHA-256
`1a3ddb766270922058f02bdb1528e38a3805fd44bcd6c3e9fdcf617ad0d563b7`.

A separate `af930d` trial also replaced the renderer's *register-local*
left/top arithmetic literals with named enum values. Although mathematically
equivalent, TC4 emitted 1,447 instead of 1,431 original CODE bytes, with
a different instruction sequence starting in the renderer and shifted
fixups. That rejected source was not retained. This distinction matters:
identical integer constants do not guarantee the same 16-bit native codegen
when they participate in register-local arithmetic.

This confirms the edited original physical source and its normal-link output,
not new distinct CODE coverage, raw vendor OMF packet identity or canonical
Factory packed-file acceptance.
