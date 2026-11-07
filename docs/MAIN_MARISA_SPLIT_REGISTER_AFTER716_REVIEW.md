# TH03 MAIN Marisa BOSS split renderer: natural register C++ after716

The complete Marisa major-BOSS source includes `marisa_render_split(int
 offset)`, a near-Pascal split-sprite renderer which alternates 0xAAAA/0x5555
image masks and resets the mask to 0xFFFF. Its old maintained code manually
wrote `_SI = offset` and calculated `(left - _SI)` and `(left + _SI)`.

Two **actual original TC4 4.02** codegen experiments challenged that:

1. `af716a`: Natural `register int signed_offset = offset`, declared **after**
   `register screen_x_t left`, compiled, but **six original CODE bytes
   differed**, at CODE offsets 1225, 1263, 1284, 1286, 1308 and 1310;
   this is a **negative control**, not an accepted original match.
2. `af716b`: Declaring **`signed_offset` before `left`** let the original TC4
   register allocator produce the exact SI/DI assignment itself, without
   manual `_SI` writes. Both compiler/link rounds matched complete original
   CODE, ordered OMF FIXUPPs and PUBLICs, segments, normal TLINK MAIN/MAP,
   Japanese loaded program and ordered MZ relocations.

A source comment was subsequently added explaining the sensitive declaration
order. The `af716b` receipt correctly failed **live-source** reviewer hash
checks after that edit, even though the comment cannot affect machine code.
Rather than repin the older receipt, the **final current-source** was
recompiled independently in fresh `af716c` with the explanatory comment.
Both rounds passed again: **1,431 CODE bytes, 199 literal ordered native
FIXUPP fields, 9 PUBLICs**, complete original TLINK MAIN/MAP, all **1,553
original Japanese MZ relocations** and standard MZ full Japanese file bytes.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af716c --units ba_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af716c

Proof: `.analysis/work/exatt-layout-af716c/report.json`, SHA-256
`8524f92f8410753dcb6b3eab56d819dac83b0e7411012378277f2ed90f9c51d0`.
Retained evidence includes both native compiler rounds, OBJ, complete
EXE/MAP, current-source dependencies, Japanese full-MZ serialization,
linker responses and writer logs. Only `ba_maris` was rebuilt; 98 other
original objects and CRT reused. No cold replay.

This is **natural C++ recovery of original register allocation**, not new
canonical packed-file Factory acceptance or historical vendor OMF packet
identity. The first failed native experiment remains retained as evidence.
