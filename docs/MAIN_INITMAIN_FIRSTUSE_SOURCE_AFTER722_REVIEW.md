# TH03 MAIN initmain: first direct native owner-source verification — after722

The MAIN `initmain` physical object contains the full original 16-bit
`game_init_main()` hardware and DOS memory initialization leaf. It is a
**different** original physical TU from the main `entry` frame/stage
scheduler. Its pinned Japanese original OMF has exactly **62 initialized
SHARED CODE bytes, 7 literal ordered FIXUPPs and 1 PUBLIC**, and zero
private initialized DATA or BSS bytes. The original MAIN TLINK includes
this object directly as `obj/th03/initmain.obj`.

The scoped original-TC4 source compiler was extended to build the **actual
maintained** `src/main/core/initmain.cpp` in place of that original linker
slot, preserve its three-segment original OMF layout, original MAP module
rows, and require the live source's emitted Borland OMF dependency. The
unchanged source control `af722a` rebuilt the complete leaf independently
in two native rounds and matched original bytes and full MAIN linking.

After that source/compiler provenance was established, its DOS memory
allocation macro was recovered into natural C++ compile-time enum form:

    enum { MAIN_DOS_MEMORY_PARAGRAPHS = (288000L >> 4) };

The original 16-byte DOS paragraph unit and original 288,000-byte amount
remain explicit; the 18,000-paragraph constant is emitted at compile time
with no additional DATA/BSS storage. The rest of original hardware startup
order is preserved: DOS memory, VRAM plane setup, VSYNC, EGC, 400-line
mode, joystick, then original archive init.

Both **modified-source** genuine TC4 4.02 compiler/full normal TLINK
rounds `af722b` exactly match all **62 original CODE bytes, 7 ordered
native relocation fields, 1 original PUBLIC and original segment definitions**.
The complete normal MAIN executable and normalized MAP, original Japanese
124,642-byte loaded program, all 1,553 original ordered MZ relocations
and independently serialized entire Japanese 130,882-byte MAIN.EXE match.
Only **one** original object was recompiled; the 98 other original game
objects and CRT were reused. No cold replay or byte patching.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af722b --units initmain
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af722b

Source-bound native receipt:
`.analysis/work/exatt-layout-af722b/report.json`, SHA-256
`8f4f2f4520b78e3e266a0d71a46cb6aff5753acc3f1ad11672a5fb8faecc7ea7`.
The unmodified `af722a` control and changed-source `af722b` proof each
retain both native compiled OBJ/EXE/MAP rounds and writer logs. This
establishes a freshly, directly tested original physical source owner in
the scoped workflow. It is **not** new Factory canonical packed-file credit,
original vendor raw OMF packet identity or entire MAIN source ownership.
