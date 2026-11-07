# Yumemi original BOSS: signed ring direction and four natural cadence tests (after665)

The current full nine-function Yumemi major BOSS translation unit owns
**2,358 original CODE bytes**. It includes the large update dispatcher
and all five attack families (expanding ring, aimed/random volley,
four-cross rings, player chase, and bullet rain), in addition to
template/rendering code. This review is based on two fresh native
Turbo C++ 4.02 compiler/TLINK rounds of **the real changed source**,
not on a historical unchanged-source receipt.

The expanding ring now chooses its signed direction without staging
AL register assignments:
    yumemi_angle_delta = (
        (randring_far_next16_and(1) == 0) ? 3 : -3
    );

The exact same original RNG draw, signed 8-bit storage, branching and
native x86 code are generated, as established in `af665b`. This
removes the old `_AL = ...; yumemi_angle_delta = _AL;` register
shuttle, not merely a cosmetic integer rename.

Four original attack cadence masks are now natural unsigned
C++ remainders: `boss_frame % 4 == 0` gates expanding ring
volleys, `% 4 == 1` gates pre-aim warning bombs,
`% 2 == 0` gates every-second-frame random aimed bullets,
and `% 16 == 15` controls the chase warning/Extra Attack.
The full original-unit native source-bound control `af665a`
proved every rewritten mask original CODE-equal. Frame
boundaries, RNG sequence and bullet-template state are preserved.

The original chained introductory register shifts
`((boss_frame << 3) << 4)` remain untouched: collapsing
them to a single shift was found original-native-unequal in an
earlier scoped experiment. No new runtime state, DATA/BSS,
injected instructions or target bytes were added.

Native source/OMF-dependency and complete MAIN verification:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af665b --units ba_yumem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af665b

Both independent original TC4 compiler/TLINK rounds reproduce
**all 2,358 CODE bytes, original ordered literal FIXUPP fields,
PUBLIC offsets and entire segment metadata**. Both normal
complete MAIN EXEs and path-normalized MAPs agree with the
source-native original. Original Japanese program image,
all 1,553 ordered MZ relocations and the separately
serialized 130,882-byte Japanese MAIN.EXE remain exact.

Retained report:
`.analysis/work/exatt-layout-af665b/report.json`
SHA-256 `44be85c7d4f598e4e4a37f08aec7e6efbe207eff5fee0ba4b6eae59cea9ab7f9`.
The compiler-consumed modified source path is attested via
emitted OMF COMENT dependencies. Only this original BOSS
TU was rebuilt; the remaining 98 original project objects
and startup/CRT libraries were reused without full cold replay.

This is natural-source progress over existing original
BOSS CODE, **not** new canonical Factory packed-game
credit, historic vendor OMF packet-byte identity, or
physical PC-98 runtime certification.
