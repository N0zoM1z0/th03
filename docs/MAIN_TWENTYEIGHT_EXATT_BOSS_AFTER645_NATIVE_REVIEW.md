# TH03 MAIN after645: genuine native source integration after Extra Attack/BOSS recovery

This is a **fresh** original-source-compiled Turbo C++ 4.02/TLINK
integration proof after a substantial set of new C++ changes in
large Extra Attack update/render functions and major Chiyuri BOSS
cardinal/fan generators. It is not reuse of the earlier after639
receipt and does not treat a successful unchanged historical compile
as proof that the edited source was actually compiled.

The code newly recovered in the active maintained game source includes:

- **Kotohime Extra Attack** (8 complete native functions): true
  meaning of the `angle` byte as an **event tick after arrival**,
  4/8/12/16 pulse timing, eight normal/two special projectile
  slots and two four-/ten-shot bullet generators. The attempted
  signed ternary for the four-shot direction changed original
  code and was rejected.
- **Mima Extra Attack**: the long bouncing/acceleration/collision
  function now expresses one-bit duration parity as
  `static_cast<unsigned int>(duration) % 2`; plain signed
  `duration % 2` was original-unequal. It preserves the original
  signed duration arithmetic, bounce priority and fixed six-slot
  pool.
- **Ellen Extra Attack**: the seven-sample history shift, return-flight
  history fill and 6/4/2/0 trail renderer have natural C++ for-loop
  initializers; real 16-bit compiler static checks bind the full
  30-byte history-slot stride and the +02/+10 coordinate offsets.
- **Rikako Extra Attack**: the 14-slot projectile update's inclusive
  0x40..0x50 tracking window, the original +0x17 per-character
  homing bit, and an unsigned typed `frame % 2` sprite flicker.
  A same-valued enum in signed `angle_delta /= 8` changed
  TC4 codegen and was rejected; the literal 8 is retained.
- **Chiyuri major BOSS**: both substantial cardinal and fan attacks
  now compile many ordinary field assignments rather than explicit
  staged AL loads/stores: cardinal angles `+=8/-=8`, three
  quarter-turns `+=0x40`, four fan speed changes `+=2/-=2`
  and both mirrored angle expressions `(0 - bullet_template.angle)`.
  Unary negation was original-unequal and rejected.

All five individual current-source, OMF-COMENT-dependency-attested
compiler/linker checkpoints are retained separately at `af640c`,
`af641c`, `af642c`, `af643e` and `af644h`.

## Full current native link of 28 physical original objects

| Original source family | Physical TUs | Original CODE bytes | Literal ordered FIXUPP fields | PUBLICs |
| --- | ---: | ---: | ---: | ---: |
| Nine complete character BOSS controllers | 9 | 17,451 | 2,434 | 85 |
| Shared BOSS ring and seven-function controller | 2 | 949 | 106 | 8 |
| Ten Extra Attack and shared-flight producers | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion and four Enemy objects | 7 | 8,195 | 582 | 50 |
| **Total** | **28** | **35,376** | **3,685** | **195** |

The original Turbo C++ compiler was run for **only these 28 actual
changed/relevant complete source translation units**, each in two
independent rounds, with original TLINK linking them in the
source-backed 99-object full MAIN response. The other 71
original project objects and startup/CRT libraries were reused
unchanged. This is **not** a whole-game cold replay.

The scoped v2 driver forces the actual modified source (and both
maintained 32-byte BOSS/Extra Attack header files where consumed)
into the compiler's per-round include paths and validates the
emitted OMF COMENT dependency paths. The independent read-only
reviewer compares the complete source-bound compiler inputs,
new raw OMF CODE/DATA payloads, ordered fixup literals, PUBLIC
offsets, original segment definitions, both full normal TLINK
EXEs and path-normalized complete MAPs against the original
source-native parent.

Both new linked MAIN program images match **all 124,642 Japanese
program bytes and the 1,553 literal ordered relocations**. The
independent standard MZ serializer produces the original
130,882-byte Japanese MAIN.EXE in both rounds. The normal modern
TLINK MZ header is kept separate from historical source provenance.

Run/read only this bounded scope:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af645a \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest,ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af645a

Native source and binary evidence:
`.analysis/work/exatt-layout-af645a/report.json`,
SHA-256 `1abe750a84347dcc591350ed6861e722f3d2a540ad57ce4e49e5e5471ee156dd`.
The ignored proof retains 56 real new objects, both complete linked
EXEs/MAPs, independent MZ files, original response files,
compiler/writer logs and compiler-consumed source/headers.

**Exactness boundary:** This proves the revised maintained C++ emits
the original native code in 28 already source-owned objects and links
them into the original MAIN program image. It does **not** establish
original Borland vendor raw OMF packet identity, unique pristine
packed-file provenance, newly accepted canonical Factory credits,
full game ownership, or real PC-98 physical execution.
