# TH03 MAIN after858: exact original Extra Attack 16-bit callback leaf

The real original physical `p_exatt` is one **41-CODE-byte near Pascal
`exatt_add` translation unit**, not an independent fake helper. It
routes 16-bit `Subpixel` argument wrapper values to the **per-character
far Pascal callbacks**, with two actual signed 16-bit local copies and
the original *byte*-valued player-ID branch. It now naturally expresses
those two 16-bit coordinate copies as **immutable `const subpixel_t`
locals**, and the zero-player test as `if(pid == 0)`. The source also
has **authentic TC4-compatible file-scope typedef size constraints**
for the 16-bit subpixel word and 8-bit player ID without allocating
additional DATA/BSS or assuming a newer C++ parser.

## Independently compiled native alternatives

- `af858a`: natural `if(pid == 0)` in the original zero branch,
  both real TC4/full normal MAIN TLINK rounds byte exact.
- `af858b`: both 16-bit Subpixel wrapper locals become C++ `const`,
  still all original CODE/FIXUPP/PUBLIC and full MAIN exact twice.
- `af858c`: replacing **both** callback arguments with direct wrapper
  field accesses, rather than preserving the two locals, emitted
  **50 CODE bytes** versus **41** original. This is a genuine rejected
  original compiler result, independently reproducing the ABI concern.
- `af858d`: inverting the two player-ID branch directions and callback
  order changed original machine CODE **without changing its 41-byte
  length**. Preserve zero-player path and original branch sequence.
- Final `af858e`: restored exact callback/local register semantics,
  original size guards, current source and two independent actual
  original Turbo C++ 4.02/full normal MAIN TLINK rounds all match.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af858e --units p_exatt
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af858e
```

Both original native compiler/link rounds reproduce **all 41 original
CODE bytes, 2 literal ordered native OMF FIXUPP fields and one PUBLIC
offset**, original source/segment/16-bit far Pascal ABI, the complete
original normal MAIN EXE/MAP, **124,642 loaded Japanese program bytes
and 1,553 ordered MZ relocations**. The independent reviewed standard
MZ serializer reproduces all 130,882 original Japanese MAIN.EXE bytes.
The **98 other unchanged original project objects and CRT** were reused,
no cold replay, padding, target substitution or OMF object patching.

Protected source-bound genuine compiler/linker report:
`.analysis/work/exatt-layout-af858e/report.json`, SHA-256
`41e6347a18ffe69effe9d8c6e74178fad8dd63029a80bd0475f3fc6a310d5ea9`.
This improves natural C++ and ABI confidence for an **already source-owned
original physical leaf**, not new distinct CODE, original vendor packet-
identical OMF or canonical Factory packed-file acceptance.
