# Nine complete MAIN BOSS TUs — native compiler-owned C++ after605

This checkpoint covers **all nine major BOSS source translation units** of
TH03 MAIN, rather than only small local leaf functions or hand-encoded bytes.
It combines the earlier five complete BOSS render improvements with the
Yumemi BOSS arrival renderer's original-equal C++ register expression:
`_DX = 0` now replaces the handwritten `asm { xor dx, dx }` before the
PC-98 sprite overlap interrupt. The Mima, Reimu and Marisa full TUs were
independently recompiled as controls without altering their source.

The earlier Chiyuri ring and mono changes, Kana cloud-angle normalization,
and Kana/Kotohime/Ellen/Rikako natural signed screen-coordinate shifts are
included, and all nine are linked **simultaneously** into the complete
99-object MAIN. No library or other original project source slot was cold
rebuilt or patched for this evidence.

Native scoped procedure:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af605c \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris

The two fresh 16-bit Turbo C++ 4.02 compiler and original TLINK rounds
both prove **17,451 original CODE bytes** over **85 complete BOSS functions**,
**2,434 ordered native fixup fields** and **85 PUBLIC offsets**, plus the
full original compiler-emitted OMF segment definitions for every boss.
The full normal MAIN EXEs and path-normalized MAPs are identical to the
retained after596 source-native link; the Japanese target's 124,642 loaded
program bytes and **all 1,553 original ordered MZ relocations** match.
Standard DOS MZ serialization independently matches the entire original
130,882-byte Japanese MAIN.EXE.

Native artifact proof:
`.analysis/work/exatt-layout-af605c/report.json` — SHA-256
`74c8ee310379eb430471cbb2038cddb67941aee362abeac595614b211cf89501`.
Both genuine compiler round OBJ records, TLINK EXE/MAP files, compact MZ,
actual compiler logs, source overlays and linker response files are retained.
The prior `af605a` four-BOSS original baseline and `af605b` Yumemi C++
variant control remain alongside the earlier after603/604 proofs.

These BOSS functions were already maintained and previously linked.
The improvement is **natural source recovery and complete exact native
regression** across the large BOSS family, not 17,451 newly accepted bytes,
original historic vendor OMF packet identity, canonical packed-file credit,
or untested physical behavior. The former after561 review is a historical
checkpoint, not automatically applicable to changed source SHA pins.
