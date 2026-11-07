# TH03 both background periodic controllers: exact native phase source (after672)

The physical Chain 1 and Chain 2 background objects share the
`src/main/background/phase.inl` state machine, inlined into
their respective **large periodic render/update functions**.
These are not small leaves: both producers also own complete
particle-update, drawing and frame-dependent movement/rendering
logic, including original DS:DI, ES and PC-98 service contracts.

The old shared periodic logic originally used byte masks for
its three independently verified timed operations. Actual
original Turbo C++ 4.02 now compiles the more natural C++
expressions to the exact original native instructions:

- `frame = static_cast<unsigned int>(round_or_result_frame) % 4096`
  instead of `round_or_result_frame & 4095` (fresh dual-native
  `af672a`).
- `static_cast<unsigned int>(frame) % 8 == 0` for the original
  1024..1279-frame phase increment clock (`af672b`).
- `static_cast<unsigned int>(frame) % 4 == 0` for the original
  2048..2303-frame decrement clock (`af672c`).

Each experiment **recompiled both full source producers** in
two independent original compiler and whole MAIN TLINK
rounds. Current source/OMF COMENT dependency binding
confirms that both complete, actually maintained C++ sources
and the shared modified `phase.inl` were consumed.
The independent reviewer checks the header's actual stage
bytes against the current maintained include, not an old
snapshot in TH03WORK.

An equally-looking modulo-128 rewrite of
`(frame & 127) < 64` in the later periodic window
**changed original CODE** (`af672d`), so that real mask
remains. The original C++ source also has a deliberately
uninitialized byte `changed` read on some phases.
This is not portable defined C++; neither the state
nor its machine-code behavior was silently repaired.
The phase labels and original gotos remain where
native alignment or branching requires them.

Final two-round full source-native integration proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af672f --units chain1,chain2
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af672f

Both genuine original Turbo C++ 4.02/TLINK rounds reproduce
**all 1,245 original CODE bytes, 86 literal ordered FIXUPP
fields, nine PUBLIC offsets**, all OMF segment definitions,
complete normal MAIN executable, path-normalized MAP,
Japanese loaded program, all 1,553 original ordered MZ
relocations, and independently serialized exact original
130,882-byte Japanese MAIN.EXE.

Retained complete compiler/source/OMF/native writer evidence:
`.analysis/work/exatt-layout-af672f/report.json`,
SHA-256 `48e188dbd7e22146763dd85f2f26155a4e680044a7e3d7e131bede921dba9152`.
Only the two actual physical Chain C++ owners were compiled
in each round; the other 97 original project objects and
startup/CRT libraries were reused, with no full cold replay.

These already tracked original bytes are source/ABI
recovery, not new canonical Factory packed-game credit,
historic vendor raw OMF packet identity, or PC-98
hardware/runtime proof.
