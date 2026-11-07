# TH03 MAIN after836: Kana full BOSS native modulo and attack geometry

The entire original physical `ba_kana` owner is compiled here, including the
BOSS template, accelerated/staged/cloud/rotating bullet controllers, update,
collision, animated main/intro renderer and final dispatch. Natural unsigned
`boss_frame % 4` now replaces the rotating ring's original mask; likewise
the original unsigned 16-bit intro animation's `((boss_frame >> 2) & 3)`
can be written as `((boss_frame >> 2) % 4)` without changing CODE. The four
accelerated-ring Extra Attack angles, five-bullet rotating ring and intro
radius have named semantic C++ constants. Byte phase increment expression,
original two separate intro scale stages and RNG order are preserved.

Actual original TC4 4.02 + complete normal MAIN TLINK tests:

- `af836a`: whole BOSS ring `%4` passed twice.
- `af836b`: added intro `%4`, whole BOSS passed twice.
- `af836c`: direct signed-byte C++ cloud angle subtraction in place of
  original `SUB AL,10h` **failed** complete CODE equality. The source
  retains the original AL instruction, not an equivalent-looking patch.
- `af836d`: after restoration, all current named attack geometry and
  timing passed **both independent original compiler and TLINK rounds**.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af836d --units ba_kana
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af836d
```

Both final rounds reproduce **all 1,874 original CODE bytes, 274 literal
ordered OMF FIXUPP fields and 9 PUBLICs**, original segment ABI, full
normal MAIN EXE/MAP, the 124,642-byte Japanese loaded program and all
1,553 ordered MZ relocations. The independent standard MZ serializer
reproduces the pinned 130,882-byte Japanese MAIN.EXE. Only one original
object was recompiled; 98 other project objects and CRT were reused,
**no whole cold replay**. Protected genuine source-bound receipt:
`.analysis/work/exatt-layout-af836d/report.json`, SHA-256
`4ee38d11d3991e0ea3979a59de0244d17f70a95b2a297ffc5957dbca8ac4e902`.

This was already a historically covered original owner; revalidation does
not confer new unique CODE bytes, raw vendor OMF metadata identity or
canonical Factory packed-file acceptance.
