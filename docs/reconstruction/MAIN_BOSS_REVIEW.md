# MAIN boss-attack owner review

This review expands the TH03 MAIN authored frontier into the complete
MAIN_03_TEXT boss-attack segment. The boundary partition is target-derived;
source and exact acceptance are recorded separately below. The immutable
Japanese MAIN.EXE is the byte oracle; frozen ReC98 labels and MAP publics are
corroborating names only.

## Complete segment partition

MAIN_03_TEXT occupies 0F1F:000A..47E9, exactly 18400 bytes. The target
review partitions the entire segment into one shared boss-helper owner and nine
character-local owners:

| Owner | Range | Bytes | Functions | Function bytes | TC4 table bytes | Relocations |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| shared | 000A..03BE | 949 | 8 | 949 | 0 | 16 |
| Marisa | 03BF..0955 | 1431 | 9 | 1350 | 81 | 23 |
| Mima | 0956..10D7 | 1922 | 9 | 1841 | 81 | 32 |
| Yumemi | 10D8..1A0D | 2358 | 10 | 2278 | 80 | 61 |
| Reimu | 1A0E..21F1 | 2020 | 9 | 1948 | 72 | 30 |
| Ellen | 21F2..287C | 1675 | 9 | 1594 | 81 | 26 |
| Kotohime | 287D..2FAC | 1840 | 11 | 1760 | 80 | 24 |
| Chiyuri | 2FAD..3A0A | 2654 | 11 | 2573 | 81 | 49 |
| Kana | 3A0B..415C | 1874 | 9 | 1794 | 80 | 35 |
| Rikako | 415D..47E9 | 1677 | 8 | 1596 | 81 | 30 |
| **Total** | **000A..47E9** | **18400** | **93** | **17683** | **717** | **326** |

The retained target review is:

    .analysis/th03-main-boss/target-review-v1.json

It is reproduced with:

    python3 scripts/review_th03_main_boss.py       --output .analysis/th03-main-boss/target-review-v1.json

Every reviewed function linearly decodes from its accepted start through a real
RET/RETF boundary. The owner intervals are disjoint and collectively cover the
full segment. No MZ relocation crosses an owner edge.

## Compiler switch data is not function code

A naive PROC-start-to-next-PROC-start partition is wrong for all nine
gba_boss_update_* routines. Each update returns before an immediately following
Turbo C++ switch table. Treating that data as instructions produces
plausible-looking garbage disassembly and, for several characters, spurious RET
opcodes inside table bytes.

The target-derived update bodies and following table spans are:

| Character | Update body | Function bytes | Table span | Table bytes |
| --- | --- | ---: | --- | ---: |
| Marisa | 0658..0764 | 269 | 0765..07B5 | 81 |
| Mima | 0CE8..0E11 | 298 | 0E12..0E62 | 81 |
| Yumemi | 151A..1689 | 368 | 168A..16D9 | 80 |
| Reimu | 1E43..1F6A | 296 | 1F6B..1FB2 | 72 |
| Ellen | 24C6..25D2 | 269 | 25D3..2623 | 81 |
| Kotohime | 2C58..2DA3 | 332 | 2DA4..2DF3 | 80 |
| Chiyuri | 34B8..371C | 613 | 371D..376D | 81 |
| Kana | 3DF8..3F33 | 316 | 3F34..3F83 | 80 |
| Rikako | 4471..458D | 285 | 458E..45DE | 81 |

The 81-byte forms contain one zero alignment byte followed by 20 word keys and
20 word destinations. The 80-byte forms contain the two 20-word arrays without
padding. Reimu uses 18 keys and 18 destinations for 72 bytes. All destination
words point back to real instruction starts inside the corresponding update
body. The normal key set is 0..0x11, 0x80, 0xFF; Reimu uses
2..0x11, 0x80, 0xFF.

This classification accounts for all 717 non-function bytes. None are credited
as functions, and no target byte blob has been copied into maintained source.

## Analyzer cross-check

The attested TH03 Ghidra database independently recognizes Marisa's entry,
update and render at the target-loaded addresses. The 269-byte Marisa update
has five direct callees, including shared boss helpers, collision-map and hitbox
logic; the 94-byte render has three direct callees. Ghidra's update body
membership covers fewer bytes than the raw reviewed function span, so analyzer
membership is intentionally not used as the ownership oracle.

## Reconstruction frontier

The shared prefix and Marisa are now exact. The next implementation target is
the complete 1922-byte Mima owner, not an isolated leaf. It contains nine
functions, including the 298-byte gba_boss_update_mima, 101-byte render,
multiple 200–300-byte private helpers, and an 81-byte compiler switch table.

Yumemi, Reimu, Ellen, Kotohime, Chiyuri, Kana and Rikako stay
boundary-reviewed only. Physical producer grouping, DATA/BSS ownership and
historical filenames remain open until compiler/link evidence establishes
them.

## Marisa natural TC4 producer

src/main/boss/marisa.cpp now reconstructs the complete 1431-byte Marisa
logical owner as natural Turbo C++. The owner contains all nine reviewed
functions plus the compiler-generated 81-byte switch-table range following
gba_boss_update_marisa; the object emits no private DATA/BSS.

The source reconstruction was driven by compiler evidence rather than copied
target bytes. Several details were material:

- gba_boss_update_marisa must switch directly on the shared mode byte.
  Caching it in an explicit local makes TC4 allocate a duplicate switch
  temporary and grows the update by three bytes.
- The spread pattern source control flow is the less-than-0x50 body followed by
  the reset path, which restores the target conditional-branch direction.
- Case blocks are written in the target producer order: spread, wide, ring,
  narrow, fall. The key array stays sorted, while this source ordering fixes
  the generated destination table.
- The historical producer requires TC4J -a2. With -a1, the same natural source
  emits 1430 bytes and an 80-byte switch range; -a2 naturally emits the
  target one-byte alignment and exact 1431-byte owner layout. A separate parity
  probe with a temporary preceding natural function did not create that byte
  under -a1, rejecting the simpler translation-unit parity explanation.
- One five-byte object-level far call in the 269-byte update is relaxed by
  TLINK to the target NOP; PUSH CS; CALL near sequence without changing span
  or semantics. The probe records this linker transformation explicitly rather
  than masking bytes.

The retained object-shape replay is:

    python3 scripts/probe_th03_main_boss_marisa_cpp.py \
      --run-id gpt-web-marisa-boss-proof-v08-20261007

Receipt:

    .analysis/th03-main-boss-marisa-cpp/gpt-web-marisa-boss-proof-v08-20261007/receipt.json

It passes all nine function starts and sizes, linker-normalized instruction
shape, the 81-byte switch alignment/key/destination structure, and zero private
DATA/BSS. Full-link acceptance is now proved by the default aggregate described
below. Historical physical filenames and DATA/BSS producer ownership remain
separate questions.

## Shared boss-helper natural TC4 producer

src/main/boss/shared.cpp now reconstructs the complete 949-byte shared prefix
of MAIN_03_TEXT as natural Turbo C++. A fresh pinned TC4J compile emits one
949-byte CODE contribution, zero private DATA/BSS and all eight reviewed
function boundaries with linker-normalized instruction shape matching the
immutable target.

This owner includes two substantial routines rather than only leaf helpers:
boss_explosion_ring is 348 bytes and boss_update_start is 178 bytes. Two
source-level compiler details were material:

- The explosion ring must branch directly on pid_current when selecting the
  opposite playfield clipping bounds. Expressing this as the generic
  sprite16_clip_set_for_pid(1 - pid_current) macro makes TC4 calculate the
  opposite PID through a temporary and grows the function by five bytes.
- The startup routine copies the fixed 32-byte character boss template into
  the active boss state with SI/DI, ES=DS and REP MOVSW. A normal C++ struct
  assignment selects a different runtime-copy shape, so the maintained source
  expresses the target's fixed-size copy through Borland register pseudos and
  symbolic REP MOVSW rather than copying target opcodes.

Reproducible object probe:

    python3 scripts/probe_th03_main_boss_shared_cpp.py \
      --run-id gpt-web-boss-shared-v03-20261007

Receipt:

    .analysis/th03-main-boss-shared-cpp/gpt-web-boss-shared-v03-20261007/receipt.json

The single-object shared producer was a useful negative control: it produced
all 949 target bytes and the same relocation sites, but emitted the relocation
table in the opposite two-group order. Full-link acceptance therefore uses two
consecutive TC4J physical producers from the same maintained semantic source:
348 bytes for boss_explosion_ring, then 601 bytes for the remaining seven
helpers. Historical physical filenames are unknown.



## Mima natural TC4 producer

src/main/boss/mima.cpp now reconstructs the complete 1922-byte Mima logical
owner as natural Turbo C++. The producer covers all nine reviewed functions,
including the 298-byte update and 305-byte render helper, plus the
compiler-generated 81-byte switch table after the update. It emits zero
private DATA/BSS.

The retained object-shape replay is:

    python3 scripts/probe_th03_main_boss_mima_cpp.py       --run-id gpt-web-mima-boss-v06-20261007

Receipt:

    .analysis/th03-main-boss-mima-cpp/gpt-web-mima-boss-v06-20261007/receipt.json

Material source-level details recovered from TC4 codegen include the common AL
store for Mima's plus/minus 7 orbit delta, deliberate recomputation of
1 - pid_current after the shared target helper, the Pascal distance/angle
split-render argument order, and the mode-2-first render control flow that lets
TC4 merge the historical draw tails naturally. All nine starts/sizes and the
switch key/destination structure match. Full-link MAP, raw bytes and ordered
relocations remain the next gate.

## Shared + Marisa full-link exact promotion

The default maintained replay now includes both owners without a candidate
manifest:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-boss-prefix-promote-final-p02-20261007

Receipt:

    .analysis/th03-main-exact/gpt-web-boss-prefix-promote-final-p02-20261007/receipt.json

Both fresh rounds pass 192 functions / 25961 function bytes / 26248 owned
bytes, 20 product outputs, 369 deterministic game objects, 435 validated OMF
objects and the maintained DOS behavior probe. Nine Research benchmark objects
retain normalized diagnostic drift outside the declared game-object vector.

The shared owner contributes exactly 949 bytes and all 16 ordered relocations.
Its physical producer model is ba_sring (348 bytes) followed by ba_srest
(601 bytes). A zero-byte bo_shim TASM object preserves historical TLINK
first-seen segment order because the C++ object metadata otherwise introduces
an empty E_EXPL_TEXT segment too early; the shim owns no game bytes. Carrier
calls to the far boss_hittest_end helper use a normal external call rather than
the historical same-segment nopcall spelling, allowing TLINK's far-to-near
relaxation to reproduce the original single NOP + PUSH CS + CALL near sequence.

Marisa contributes exactly 1431 bytes, including the 81-byte compiler switch
table, and all 23 ordered relocations. No private C++ DATA/BSS is emitted by
either semantic owner; carrier aliases retain the already-observed historical
storage locations.

This raises the maintained default exact aggregate from 175 to 192 functions
and from 23868 to 26248 owned bytes. The remaining MAIN_03_TEXT frontier starts
with Mima.
