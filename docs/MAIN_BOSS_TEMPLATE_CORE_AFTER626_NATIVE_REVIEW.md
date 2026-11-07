# Physical 32-byte BOSS state: four large controllers and shared helpers (after626)

The original DGROUP `boss_character_template` contains 32 bytes per
player. Chiyuri, Ellen, Rikako, Reimu and the shared BOSS controller
had five independently re-declared structs with the **same physical
stride**, but inconsistent trailing interpretations. The maintained
`boss_template_state_t` in `src/main/boss/template_state.hpp` now
replaces these declarations. The existing callback and update code
continues to use its original field names and compiler ABI:

- Chiyuri uses a signed runtime effect radius; its template initializes
  zero at physical +18. The shared template's unsigned radius occupies
  the exact same two bytes without changing that write.
- Ellen and Reimu use fewer tail fields than other characters; their
  previously reserved physical bytes remain present, but uninitialized
  by this template source.
- Rikako writes its signed spin delta at +1A. The shared declaration
  makes the exact offset and signedness explicit.
- `ba_sring` and `ba_srest` compile the shared 348-byte explosion
  ring and 601-byte, seven-function BOSS controller from one source.
  The latter still copies the genuine 32-byte structure using the
  original inline SI/DI/ES/CX + REP MOVSW sequence: a plain struct
  assignment is known to compile to an original-unequal helper call.

Two independent actual Turbo C++ 4.02 compile/TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af626a --units ba_chiyu,ba_ellen,ba_rikak,ba_reimu,ba_sring,ba_srest
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af626a

Every rebuilt object identifies the **actually consumed** source and
new template header in its Borland OMF COMENT dependency records. The
entire **8,975 CODE bytes**, 1,185 ordered native FIXUPP fields, 45
PUBLIC offsets and segment metadata are original-equal in both rounds.
Both normal full MAIN links and normalized complete MAPs reproduce the
retained source-native original; all 1,553 ordered Japanese MZ
relocations and the independently serialized 130,882-byte Japanese
MAIN.EXE are equal.

Retained genuine native receipt:
`.analysis/work/exatt-layout-af626a/report.json`;
SHA-256 `a1983380ccd7a5a9d925df40e368c452c92103843409ba6c2c96287d7593d5dd`.
No cold replay, object patching, target-copying or historic receipt
repinning occurred.

The new work is a safer maintainable reconstruction of the physical
source layout shared across large BOSS functions; these original CODE
bytes were already accounted for. Raw historic vendor OMF packet
identity, canonical packed-file Factory credit and physical PC-98
runtime behavior remain distinct unanswered questions.
