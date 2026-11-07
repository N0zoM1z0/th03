# Kana full BOSS rotating barrage and sixteen-sprite renderer after704

The entire original Kana major BOSS is a complete nine-function,
1,874-CODE-byte physical Turbo C++ 4.02 translation unit.
The large cloud-ring and rotational shot patterns, damage
selection, original BOSS scheduler and the sixteen-sprite
arrival renderer are verified together, not in extracted snippets.

Actual source edits verified with original TC4 and TLINK:

- The sixteen-shot producer and all sixteen ring-sprite
  rendering iterations use natural C++ prefix increment
  `++i` rather than postincrement.
- The cloud warning/spawn gate uses natural
  `if(randring_far_next16_and(1))`, retaining the
  single original random draw and its exact order.
- The BOSS hit flash, player-specific sprite resource
  selection and arrival odd/even skipping use normal
  C++ nonzero state tests without explicit `!=0`.
- Every edited expression was first tested with
  current-source native stage `af704b` and extended
  by `af704c`. The full original CODE, literal ordered
  FIXUPPs and the whole linked MAIN remained exact.

Critically, the opposite hypothesis was tested rather
than trusted: turning the four random signed rotation
alternatives into direct byte-field assignments instead
of the original AL register intermediate changed the
native CODE (`af704a`). The original signed choice
and AL-mediated store remain. The exact old
`SUB AL,10h` cloud angle operation is also preserved
rather than replacing it with a mathematically equivalent
ADD AL,F0 instruction.

Fresh accepted two-round modified-source/packed-BOSS-header
OMF dependency proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af704d --units ba_kana
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af704d

Both original TC4.02 compiler/complete MAIN TLINK rounds
reproduce all **1,874 original CODE bytes, 274 ordered
literal native FIXUPPs, nine PUBLIC offsets**, all
original OMF segments and ABI, complete normal MAIN
EXE and path-normalized MAP, Japanese loaded program,
1,553 original ordered MZ relocations and independently
serialized original 130,882-byte Japanese MAIN.EXE.

Full original source/OBJ/EXE/MAP and writer evidence:
`.analysis/work/exatt-layout-af704d/report.json`.
Only this one affected complete original source TU was
compiled; the other 98 original project objects and CRT
libraries were reused. No complete cold replay, new
canonical Factory packed-game acceptance or historical
raw vendor OMF packet equality is claimed.
