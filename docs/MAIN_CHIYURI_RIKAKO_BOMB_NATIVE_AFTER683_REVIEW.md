# Chiyuri and Rikako complete Bomb controllers: native source / exact C++ geometry (after683)

The four character-specific Bomb objects were previously not part
of the 43-source gameplay integration scope. A fresh original
Turbo C++ 4.02 native experiment `af681b` compiled **all four**
complete sources (`b_chiyu`, `b_kana`, `b_koto`, `b_rika`)
in two separate rounds, matching 2,090 original CODE bytes,
207 literal ordered FIXUPP sites and four PUBLIC offsets.
Three private bomb objects use the original external BSS carrier;
compiling duplicate private BSS would change original addresses.
The v2 compiler now selects each character's actual source in
the preserved physical original CODE-only object slot, rather
than reusing the older Ellen-only external-storage wrapper.

In Chiyuri's complete 490-CODE-byte Bomb controller, the original
16-bit timed color and four-axis warning/explosion geometry are
naturally expressed as:
- `255 - frame * 4` instead of authored `frame << 2`;
- `((frame - 64) * 2) * 16` instead of a later left shift;
- `255 - frame * 8` for the terminal palette fade.

Independent actual-source TC4 `af682a`, `af682b`, `af682c`
experiments proved all three changed sources compile to **the
same original native bytes**. The 64/144 frame transitions and
four-point outward explosion call order remain unchanged.
A candidate signedness-correct unsigned `frame%4 < 2` shake
comparison changed actual CODE (`af682d`); the original
`frame & 3` is deliberately retained.

Rikako's complete 546-CODE-byte bomb controller now renders
the initial gradient via natural `frame * 4`, the late
palette fade via `frame * 8`, and its RNG-seeded horizontal
burst via named original subpixel coordinates:
`for(; x <= TO_SP(288); x += TO_SP(96))`.
The two-round original TC4 controls `af683a` and
`af683b` confirm full CODE, fixup and linked-program
equality. The exact original RNG consumption, paired
GRCG vertical lines, unmodified physical line-offset
storage carrier and service call order are preserved.

Final two-round original compiler and full normal MAIN
TLINK source/OMF-dependency evidence:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af683c --units b_chiyu,b_rika
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af683c

Both genuine native rounds produce **all 1,036 original
CODE bytes, 104 literal ordered FIXUPP fields and two
PUBLIC offsets**, entire original OMF segment metadata,
complete normal MAIN EXE/path-normalized MAP, exact Japanese
loaded program, 1,553 ordered MZ relocations and separately
serialized original 130,882-byte Japanese MAIN.EXE.

Retained source/native/OMF writer evidence:
`.analysis/work/exatt-layout-af683c/report.json`,
SHA-256 `2f350acfb56a7810163672d3f0e5f87925b1c29eb07c2564598bec13d726e00a`.
Only the two affected original physical CODE producers were
recompiled in the final pair. The other 97 original project
objects and startup/CRT libraries were reused, **not**
a complete cold replay. Earlier failed variants and
complete writer logs remain in ignored native evidence.

These are previously tracked original game CODE bytes,
not new canonical Factory packed-game acceptance,
original historical vendor raw OMF packet-byte identity
or real PC-98 runtime proof.
