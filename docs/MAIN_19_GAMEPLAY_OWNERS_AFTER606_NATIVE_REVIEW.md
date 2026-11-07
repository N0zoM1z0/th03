# MAIN full BOSS + Extra Attack source graph: nineteen TUs, after606

After restoring natural C/C++ control flow and a single, character-specific
entity ABI in the maintained game source, a source overlay **simultaneously
recompiled every major BOSS and every character Extra Attack producer** in
the original TH03 16-bit Turbo C++ 4.02 toolchain. This is more than isolated
leaf-byte equality: the full source-native 99-object MAIN normal link
resolves and reproduces all game entrypoints and data/relocation dependencies
with these **nineteen** project slots replaced together.

- Nine full BOSS TUs: 17,451 original CODE bytes, 2,434 ordered native fixup
  fields, 85 complete functions/PUBLICs (after605, natural renderer/byte math).
- Ten full Extra Attack TUs: 8,781 original CODE bytes, 563 ordered fields,
  52 PUBLICs (after602, 32-byte entity ABI and natural Chiyuri beam math).
- Combined simultaneous source proof: **26,232 CODE bytes, 2,997 native
  fields, 137 PUBLICs**. Both independent rounds give identical complete
  normal TLINK EXEs and path-normalized complete MAPs, preserving the
  original loaded MAIN program and **1,553 literal ordered MZ relocations**.
  The separate standard-MZ serialization reproduces all **130,882 original
  Japanese MAIN.EXE bytes**. No original target or OBJ/library was modified.

Native compiler/normal linker construction was limited to these 19 source
units, two independent rounds, with the other 80 project objects and original
vendor startup/libraries reused unchanged. It is **not** a full project cold
replay or multi-game runtime test.

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af606a \
      --units ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris

Actual complete native proof:
`.analysis/work/exatt-layout-af606a/report.json`, SHA-256
`07cba64c0547cb890b905e5dea71f31982dd78d36b339cec3e9a24849924d9aa`.
It retains both output vectors (native OBJ/EXE/MAP/compact MZ), source overlay
copies, original response files and real writer logs. The stored receipt
is source-bound and should not be silently repinned if a later source change
makes it stale.

A new **read-only** validator verifies this exact source/receipt binding,
checks every overlay input against current maintained C++ and entity headers,
all OMF CODE, ordered fields, PUBLICs and segments against the unchanged
original objects, original response slots, writer logs, complete MAPs,
program images, ordered relocations and cross-round equality. It does not
invoke a compiler or relinker:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af602a af605c af606a

All three retained stages passed this source-bound read-only verification.
The earlier after596 reviewer is historical and intentionally rejects changed
source hashes; it is not the current reviewer for these refreshed source TUs.

This does **not** re-credit previously source-owned CODE bytes, claim original
vendor raw OMF packet byte identity or linker/header provenance, establish
independent pristine packed-file authenticity, or certify game behavior on
real PC-98 hardware. Canonical Factory whole-game acceptance remains open.
