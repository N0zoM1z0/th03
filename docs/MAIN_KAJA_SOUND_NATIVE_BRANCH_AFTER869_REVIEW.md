# TH03 MAIN after869: original PMD/MIDI interrupt leaf and 16-bit AX control

The original physical `snd_kaja` Turbo C++ 4.02 translation unit
contains one **30-CODE-byte far-Pascal** `snd_kaja_interrupt(short ax)`
service in the historical SHARED segment. It is the actual original
PMD/MIDI software-interrupt bridge, not a generic request to write an
arbitrary hardware port. The driver-active byte, strict MIDI driver
flag `==1`, original constant `INT 60h`/`INT 61h`, and the real register
result in `_AX` are preserved.

The maintained source now naturally spells the originally active-only
path as

```
if(snd_active != 0) {
    _AX = ax;
    if(snd_midi_active != TH03_KAJA_MIDI_DRIVER_ACTIVE) {
        geninterrupt(TH03_KAJA_PMD_VECTOR);
    } else {
        geninterrupt(TH03_KAJA_MIDI_VECTOR);
    }
}
return _AX;
```

This retains the *unchanged caller-visible AX* on an inactive driver,
without initializing it with zero, moving the original near/far memory
model or inventing a runtime-selectable interrupt number. Old Turbo
C++-compatible `typedef char[...]` declarations now verify the actual
16-bit short/AX and 8-bit driver flags at compile time, without adding
program DATA, CODE or runtime checks.

## Original compiler experiments

- `af869a`: reversed the PMD/MIDI branch into a natural `if(midi==1)`
  with MIDI first. The real original TC4 emitted **different CODE at
  offset 18**, even though the candidate retained 30 initialized
  bytes. This branch inversion was rejected.
- `af869b`: restored the original PMD-first branch and used explicit
  `if(snd_active ==0)` for the inactive return; complete original object
  and normal MAIN link matched exactly in both independent rounds.
- `af869c`: changed the active/inactive return arrangement into one
  natural `if(snd_active !=0) { ... } return _AX;`. **Both real original
  compiler/full normal linker rounds passed**, including the original
  inactive AX and far Pascal ABI.
- Final `af869d`: named the exact MIDI-enabled value and checked true
  original word/byte widths with TC4-compatible compile-time types.
  Both independent original TC4 and normal MAIN TLINK rounds remain exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af869d --units snd_kaja
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af869d
```

Both real original compiler/full normal TLINK rounds reproduce **all
30 original CODE bytes, 2 literal ordered native OMF FIXUPP fields and
one PUBLIC offset**, original SHARED segment/source ABI, complete normal
MAIN EXE/MAP, **124,642 Japanese loaded bytes and all 1,553 original
ordered MZ relocations**. Independent standard DOS MZ serialization
reproduces all 130,882 bytes of the pinned original Japanese MAIN.EXE;
it does not prove the original linker used identical header serialization.
The **98 other original project objects and CRT were reused**, no cold
replay, patched target/OBJ, fake NOP or direct byte-array code.

Protected real source-bound native report, original compiler writer
rounds, OBJ/EXE/MAP and logs:
`.analysis/work/exatt-layout-af869d/report.json`, SHA-256
`b5fb7f18304f2abad36d4494f4929eab7eee28a2e5bfb7ef6b1944e5bbeaaa50`.
This was previously source-covered original CODE. This native C++/ABI
improvement is **not additional distinct original CODE ownership,
raw vendor packet-identical OMF metadata, complete historical source
identity or canonical Factory packed-file acceptance**.
