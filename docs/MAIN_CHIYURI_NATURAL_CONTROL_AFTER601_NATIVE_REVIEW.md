# Chiyuri Extra Attack: naturally lowered branch and beam phase (after601)

The Chiyuri Extra Attack object covers four functions and **978 original
CODE bytes**, including its large paired-beam update and renderer. This
source refresh removes *both handwritten inline-ASM blocks* from
`src/main/player/exatt_chiyuri.cpp`, not merely a leaf helper:

1. The pair-update loop previously manually loaded `exatt_entity_p` into BX,
   compared its state and jumped into a C++ `if` body (`chiyuri_first_done`).
   A normal C++ free-slot guard followed by `exatt_entity_p++; continue;`
   preserves the exact original native control-flow lowering. The active
   beam branch continues to skip its partner; the alternative flight path
   still advances and updates both endpoints independently.
2. The beam renderer previously authored `mov al, phase; mov ah,0; push ax;
   mov ax,88h; pop dx` then `_AX -= _DX` to compute the final taper frame.
   The same Turbo C++ emits the exact native instructions from the expression
   `_AX = (0x88 - phase)`. This retains the **observed AX register ABI**
   at the shared `beam_radius` label but no longer spells the instruction
   sequence in an inline assembler block. The preceding expansion phase
   remains `_AX = phase - 0x10`; division by four and both trapezoid widths
   are unchanged.

The original compiler, *not a hand-edited object*, produced byte-identical
complete CODE, ordered native relocation fields, PUBLIC symbol offsets and
segment definitions for **two fresh rounds**, with normal TLINK and the
source-backed after596 full MAIN as the unchanged parent:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af601e --units ex_chyu

Both linked normal MAIN EXEs and normalized complete MAPs are original-equal,
including the complete **1,553-entry relocation vector** and full Japanese
130,882-byte MAIN.EXE after the independent standard-MZ serialization.

The iterative controls are retained separately: `af601a` first confirmed
native equality of the C++ conditional `goto`; `af601b` proved that a natural
`continue` guard also compiles identically; `af601c` then proved the native
replacement of the beam-register assembly. `af601e` is the final formatted
source variant. Its proof is
`.analysis/work/exatt-layout-af601e/report.json`, SHA-256
`201b7cf39feac20e67d6cb792f28bd76c52dda03c9a8ee46e71329fe176f0fd4`.
The original historical after596 source snapshots and both retained full
link proofs are not changed. No new canonical packed-file Factory acceptance,
original historical OMF packet identity or physical runtime coverage is
claimed; these 978 CODE bytes were already accounted for.
