# All nine MAIN large BOSS units: genuine source-rooted native link (after621)

After identifying the v1 source-overlay include bug, the complete nine-BOSS
family has been retested using the real 16-bit Turbo C++ 4.02 compiler with
explicit per-round modified-source includes and validated OMF COMENT
dependency paths. This is **not** a retrospective acceptance of the
earlier v1 `af605c` result.

The five Chiyuri/Kana/Kotohime/Ellen/Rikako BOSS modules now compile signed
AX sprite-coordinate shifts from natural C++:
`static_cast<int16_t>(_AX) >>= 4` preserves the original SAR AX,4 opcode
and local/register/stack interface. Independent v2 experiments confirmed
unsigned AX instead emits SHR and more drastically rewritten `top >>=4`
changes surrounding original code. Their full five-source proof is
`af620h`. Kana's SUB AL,10h remains inline assembly because byte C++
subtraction emits original-unequal ADD AL,F0.

Yumemi's large arrival renderer was independently rechecked: the previous
`_DX=0` emits XOR DX,DX with a different ModR/M byte. `af621a` recorded
that negative result. The original `asm { xor dx,dx }` form and its
explicit encoding rationale were restored, after which the full
Yumemi/Mima/Reimu/Marisa control passed in `af621b`.

The **nine complete physical BOSS TUs** were then simultaneously rebuilt
and linked twice (the other project objects plus C0/CRT unchanged):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af621c \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af621c

Both source-bound original TC4/TLINK rounds reproduce all **17,451 CODE
bytes**, **2,434 literal ordered native FIXUPP fields**, **85 PUBLICs**,
and all original segment definitions. Normal TLINK output and normalized
full MAP match the retained after596 original MAIN source-native link.
Both original Japanese 124,642-byte loaded programs and all **1,553
ordered MZ relocations** match; the separately reviewed standard MZ
serialization reproduces the full 130,882-byte Japanese MAIN.EXE.

Receipt:
`.analysis/work/exatt-layout-af621c/report.json`
SHA-256 `74e806307a39bdf8692040b911b647af613f8d4a3434429483fa60c5aa78c00d`.
The two actual writer rounds, dependency-checked source overlays, native
OBJ, EXE/MAP and MZ outputs are retained in ignored evidence. No
historical receipt was repinned, and no full cold replay was used.

The improvement is verified natural C++ in the large sprite loops and
faithful native expression of the other original BOSS functions; these
were previously owned original bytes. Original vendor raw OMF packet
identity, independent packed-game provenance, PC-98 hardware behavior
and canonical Factory acceptance are not asserted.
