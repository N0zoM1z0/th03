# TH03 player core and full Hyper dispatcher: source-native after707

The complete original `core` physical Turbo C++ project object is
3,135 CODE bytes, 260 ordered native FIXUPP fields and 21 PUBLIC
offsets. The owner includes the original player movement/state/shot
setup and **ten Hyper handlers**. Its actual historical normal
MAIN linker input is `probe/af593p/rN/core.obj`, not an inferred
`obj/th03/core.obj` response slot.

The v2 source-bound compiler/reviewer now explicitly stage the
current maintained `src/main/player/hyper.inl` implementation,
rewrite the include to its per-round actual source path, verify its
byte-for-byte snapshot, and **require the emitted native OMF COMENT
dependency** to name that exact current file. The other original
core include implementations were not modified in this session and
continue to be reused. An initial unchanged-source two-round proof
`af706a` verified the real complete original CORE image and link.

A meaningful Hyper function-body recovery in Ellen's four-frame
charged attack changes the explicit near-pointer reinterpretation:
    (*(unsigned char near *)&round_frame & 3) == 0
to the natural equivalent low-byte C++ cast:
    (static_cast<unsigned char>(round_frame) & 3) == 0

The complete original native object matches byte-for-byte in
`af707b`; the cast preserves the original **byte** access and
does not accidentally turn the 32-bit global into a word/long
division. Separately changing the bitmask to `%4` was
native-unequal (`af707a`) and rejected.

The original Hyper acceleration/deceleration implementation is now
explicit about its distinct signed steps: cardinal +0x20,
diagonal +0x18, cardinal -0x10, Marisa diagonal -12 and
Rikako diagonal -8. These are compiler-time C++ enum names in
the same inline functions used across the nine character handlers;
the `hyper_rikako` Gauge activation threshold retains its
original **strictly greater than 0xFA0** comparison. All named
original values preserve exact actual compiler output (`af707d`).
The seemingly identical `>=0xFA1` rewrite was original-native
unequal (`af707c`) and therefore rejected.

Final actual-source/OMF-COMENT-attested original Turbo C++ 4.02
and complete normal MAIN TLINK two-round native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af707e --units core
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af707e

Both rounds reproduce all **3,135 CODE bytes, 260 literal
ordered native FIXUPP fields and 21 PUBLIC offsets**,
complete original OMF segment metadata, the normal full
MAIN EXE and path-normalized MAP, the Japanese loaded program
and 1,553 ordered MZ relocations. Independently serialized
standard MZ reproduces the original 130,882-byte Japanese
MAIN.EXE in both rounds.

Preserved actual compiler inputs/OMF/objects/EXE/MAP writer proof:
`.analysis/work/exatt-layout-af707e/report.json`.
Only this affected full physical original TU was freshly compiled
twice. The other 98 original project objects and CRT libraries
were reused. No cold replay, target patch, new canonical
Factory packed-game acceptance or historical raw vendor OMF
packet-byte identity is claimed.
