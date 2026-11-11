# TH03 original Gauge saturation and Extra Attack dispatch leaves (after700)

Two original whole physical 16-bit Turbo C++ source producers
were recovered and independently current-source verified together:
`p_exatt` (41 original CODE bytes, 2 ordered FIXUPP fields
and one PUBLIC) and `p_gauge` (55 CODE bytes, 1 FIXUPP and
one PUBLIC). These are small **leaf functions**, deliberately
tested alongside the separately proved substantial character
callback/BOSS/Combo state controllers rather than mistaken
for a large-function-only recovery.

`exatt_add` selects the original player-0 character callback
with natural C++ `if(!pid)`, still compiling exactly the
original near/far callback ABI and preserving both original
one-byte PID values and 16-bit subpixel stack arguments.
Dual-native stage `af699d` proved the change.
A deliberately challenged ZUN-bloat hypothesis removed
the two local `subpixel_t` parameter copies and passed
the original `Subpixel` parameters directly to the far
function pointers. Although superficially equivalent,
**the entire native CODE changed** (`af699e`).
The original explicit conversions remain; the result
does not claim they can be removed.

`gauge_avail_add` is the complete original 55-byte
near Pascal saturating Gauge update. It retains the
real unsigned 16-bit 0xFF0 (4080) maximum and the
original post-add overflow clamp. Two separate ordinary
C++ early returns `if(p.hyper_active)` and
`if(p.gauge_avail>=GAUGE_MAX)` compile to the
original short-circuit machine instructions
(`af700a`). The historical combined condition
was source-readable but is no longer necessary
for precise C++ semantics.
A candidate combining the additive update into the
comparison `if((p.gauge_avail += charge)>GAUGE_MAX)`
changed original native CODE (`af699a`); a separate
explicit assignment `p.gauge_avail=(...+charge)`
likewise changed it (`af699f`). The actual
native-exact `p.gauge_avail+=charge;` remains.

## Original-native two-round proof

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af700c --units p_exatt,p_gauge
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af700c

The scoped source binder now supports the actual original
`p_exatt` physical project object and its *three*
complete original MAP segment rows. The unchanged-source
`af699c` compiler control established real 16-bit
CODE/ABI/layout evidence before modifications.

Both final native Turbo C++ 4.02/complete TLINK rounds
reproduce **all 96 original CODE bytes, three literal
ordered FIXUPP fields, two PUBLIC offsets**, all original
segment definitions, whole normal MAIN EXE and complete
normalized MAP, 124,642-byte Japanese loaded program,
1,553 ordered MZ relocations and independently serialized
original 130,882-byte Japanese MAIN.EXE.

Preserved proof:
`.analysis/work/exatt-layout-af700c/report.json`;
SHA-256 `c45e7b8f2770df3b31c7b8edb6be0b3018b0c262d7d48a42faa27f5219f9b114`.
Both native original compiler writer rounds and all
actual modified source/OMF dependencies are preserved.
Only the two affected complete original TUs were
compiled twice, reusing 97 other objects and CRT,
without a full cold replay. The original CODE
was previously source-owned; no newly accepted
Factory packed-game byte credit is implied.

## Player-zero callback dispatch as an exact tail exit (2026-11-11)

The 41-byte `exatt_add()` leaf can call the player-zero far-Pascal
callback and return immediately, leaving the player-one callback as
the only remaining tail. It still converts both original `Subpixel`
wrappers into distinct 16-bit local words before branching, passes the
original literal player arguments and retains each far function-pointer
call's ABI. The native code and ordered fixups are unchanged. The
historic inverse-branch trial `af858d` remains a meaningful compiler
constraint; this new early return does not invert the tested branch.

Stage `af1363h` proved the isolated 41-byte leaf. Current `af1363i`
recompiles both original Gauge and shared Extra Attack objects:
**96 CODE bytes, three ordered native fields, two PUBLICs**, with two
exact original TC4/TLINK normal MAIN links. Consumer `af1363j` also
recompiles Kotohime BOSS, Kotohime Extra Attack, Bullet, shared BOSS,
Polar and SE: **6,770 CODE bytes, 685 fields and 52 PUBLICs**, both
normal Japanese MAIN images and ordered MZ relocations exact.

Current proof: `.analysis/work/exatt-layout-af1363i/report.json`, SHA-256
`aa984ab2f33b85db1bd3fb6de142f10c4ab8d8cb79a2a65c0941bb05356cb094`.
Joint proof: `.analysis/work/exatt-layout-af1363j/report.json`, SHA-256
`26467348b4324384a4116c0983480751ab46ee5f97ac469d6bf69960bdb08d0e`.
