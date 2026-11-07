# MAIN ten physical Extra Attack producers: unified native C++ entity, after602

The large Kotohime, Ellen, Chiyuri, Yumemi, Rikako, Mima, Marisa and
Kana character-specific Extra Attack routines, plus the shared flight
and Reimu update producers, now use a **single 32-byte C++ entity ABI
view**. The two remaining duplicate structures (Marisa and Kana) were
removed; both had an unreferenced +0x11 byte. This does not assume that
this byte means the same thing across characters: the shared
`character_mode` union distinguishes Ellen's signed spin step from
Kotohime's unsigned attack mode. Rikako's +0x17 homing flag remains a
character-specific tail overlay. This is a code/layout ownership improvement,
not redundant accepted CODE credit.

The after601 Chiyuri control-flow and beam taper improvements are included:
both large beam/update functions now lower from C/C++ without authored inline
assembly for the state-0 bypass and phase subtraction, while the shared
beam-radius interface still intentionally uses Turbo C++'s `_AX` pseudo-register.

The scoped proof compiles these **ten complete original TUs**, not merely
small helpers, with the real 16-bit Turbo C++ compiler and original TLINK:

| Original owner | Complete CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| ex_yume | 1,696 | 87 | 5 |
| ex_mima | 727 | 44 | 4 |
| ex_rika | 702 | 46 | 5 |
| ex_rfly | 825 | 51 | 8 |
| ex_reup | 331 | 22 | 2 |
| ex_ellen | 1,129 | 79 | 6 |
| ex_koto | 1,054 | 100 | 8 |
| ex_chyu | 978 | 55 | 4 |
| ex_maris | 676 | 35 | 5 |
| ex_kana | 663 | 44 | 5 |
| **Total** | **8,781** | **563** | **52** |

Command used (once, without running a cold replay):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af602a \
      --units ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana

Both new compiler/linker rounds match the original full CODE payloads,
**literal ordered native FIXUPP fields**, symbol offsets, and all OMF
segment definitions. Both complete normal TLINK EXEs and path-normalized
MAPs equal the pinned after596 MAIN source link; the original 124,642-byte
loaded program and 1,553 ordered MZ relocations match the Japanese
reference, and the separate standard MZ serialization matches the entire
130,882-byte Japanese MAIN.EXE.

Native receipt: `.analysis/work/exatt-layout-af602a/report.json`,
SHA-256 `14ff7cf31612fdb4b5c10ac3dcc6a0cda155f7d62add2b241dadd1073de6dd6b`.
Both compiler rounds' OBJ, complete linked EXE/MAP, compact MZ, compiler
commands/logs and overlay sources remain in ignored local evidence.
The old after596 source-bound receipt and original game artifacts were not
rewritten, deleted or repinned.

**Boundaries:** raw original vendor OMF packet byte identity, independent
canonical packed-file provenance, full physical runtime behavior, and
Factory whole-product acceptance remain unproved. This result strengthens
maintainable natural C++ code and ABI consistency across a large source
family; all 8,781 CODE bytes were already source-owned before this refresh.
