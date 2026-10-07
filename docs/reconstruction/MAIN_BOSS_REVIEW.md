# MAIN boss-attack owner review

This review expands the TH03 MAIN authored frontier into the complete
MAIN_03_TEXT boss-attack segment. It is a target-boundary review, not a
source or exactness claim. The immutable Japanese MAIN.EXE is the byte
oracle; frozen ReC98 labels and MAP publics are corroborating names only.

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

The next implementation target is the complete 1431-byte Marisa owner, not an
isolated leaf. It contains nine functions, including the 269-byte boss update,
the 94-byte render, several substantial private helpers, and the 81-byte
compiler switch table. Source reconstruction must recover natural Turbo C++
that reproduces both the function instruction shape and producer-owned table
layout before any full-link exact promotion.

The shared helper owner and the remaining eight character owners stay
boundary-reviewed only. Physical producer grouping, DATA/BSS ownership and
historical filenames remain open until compiler/link evidence establishes them.

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
DATA/BSS. This is source/producer evidence only. Full-link MAP placement,
ordered MZ relocations, final linked bytes, historical physical producer
grouping and state ownership are still separate gates.
