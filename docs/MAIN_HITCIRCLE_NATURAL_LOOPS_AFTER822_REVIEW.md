# TH03 MAIN after822: original HitCircle animation and renderer natural loops

The complete original `hitcirc` physical TC4 owner includes all four
original functions: enemy and player hit-circle spawn, per-frame update,
and the mixed-color/clipped sprite renderer. Its original 13 physical
records consist of twelve enemy-animation slots plus the deliberately
**single shared player hit marker**. That quirk and the original 4-frame
cel, 16-frame lifespan, pointer-stride, source record and hardware modes
are preserved; no defensive behavior was added.

## Genuine natural C++ recovery

Both major animation traversal loops now use ordinary typed C++ `for`
statements with their original signed index and near pointer advancement:
`for(; i < HITCIRCLE_COUNT; (i++, p++))` for frame advancement/freeing,
and the corresponding `HITCIRCLE_ENEMY_COUNT` renderer loop. Actual original
Turbo C++ 4.02 retains the exact original register allocation, memory
accesses, jump layout and rendered sprite order in the complete owner.

The explicit low-level PC-98 sprite service is intentionally kept where
natural code does **not** compile into the target's exact instruction:

- `af822a` tried replacing `asm { and dx,1 }` with natural `_DX &= 1`.
  The target has `81 E2 01 00` (`AND DX,imm16`, **four bytes**), whereas
  original TC4 chooses `83 E2 01` (`AND DX,imm8`, **three bytes**) for
  the C++ compound assignment. This 1-byte difference shifts the full
  owner, so the candidate was rejected and original hardware assembler
  preserved. This is a real native opcode-encoding difference, not a
  semantic claim.
- `af822f` challenged the original BX-based four-frame sprite-cel
  offset with a natural local index and `* HITCIRCLE_VRAM_W`. It changed
  original TC4 CODE and was rejected; this calculation still uses the
  original BX register arithmetic. Early `af822b/c` exploratory drafts
  had a missing function closing brace, failed original compiler parsing,
  and are **not** evidence that the `for` form cannot compile.
- `af822d` passed after recovering the update loop. Final **`af822e`**
  passed with **both complete update and renderer loops** rewritten to
  ordinary `for` without altering original raw CODE or OMF fixups.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af822e --units hitcirc
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af822e
```

Both independent original TC4 4.02 compiler and full normal MAIN TLINK
rounds reproduced **445 original CODE bytes, 30 literal ordered OMF FIXUPP
fields, 4 PUBLIC offsets**, the original segment and source owners, the
complete normal MAIN EXE/MAP, all **124,642 Japanese loaded bytes**, and
**1,553 original relocation words**. Standard independent serialization
reproduces the original 130,882-byte MAIN.EXE. **98 other original game
objects and the original CRT were reused**; no all-project cold replay,
patching, byte padding or canonical packed-file Factory acceptance.
This is a native-verified C++ readability/structure improvement for a
historically covered physical source, not newly distinct byte credit.

Protected original-source-bound report:
`.analysis/work/exatt-layout-af822e/report.json`, SHA-256
`3b31dcbcff20ae1df0ce280fb936f54554ef86552c5b40d46162aafb1f586b91`.
