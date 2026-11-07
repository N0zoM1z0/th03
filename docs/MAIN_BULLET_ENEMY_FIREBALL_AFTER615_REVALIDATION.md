# Real-source recertification of full Bullet, Fireball and Enemy units — after615

The after607–609 source-refresh experiments were made with an overlay
whose wrapper accidentally included stale `TH03WORK/src` files, rather
than the copied changed C++ files. Their original-MAIN equality is **not
proof that the changed code was compiled**. These records are preserved
as past diagnostic evidence, not deleted or silently accepted.

The corrected v2 source-rooted compiler checked each previously claimed
replacement against the true original object. Several semantically
reasonable C++ edits **change exact machine code**, requiring restoration
of original source forms:

- Complete Bullet, **2,685 CODE bytes**: replacing manual `xor dx,dx`
  by `_DX = 0` emitted `33 D2` versus original `31 D2`; similarly
  `_BX = 0` emitted `33 DB` versus `31 DB`. `_AX <<= 1` emitted
  `ADD AX,AX` (`03 C0`) rather than `SHL AX,1` (`D1 E0`). The original
  register-specific inline assembly is retained, with these exact
  compiler-choice reasons annotated. The three separate negative probes
  are `af611j`, `af611k`, `af611l`; original Bullet compiled exactly as
  `af611i`, and the final source with comments passed `af612d`.
- Complete Fireball, **1,555 CODE + 1 initialized DATA byte**:
  replacing `goto free_and_continue` and the shared
  `switch_to_fall` transfer path with direct `continue`/combined
  conditions changed branch layout. Negative controls `af612f`,
  `af612g` independently demonstrate each difference, and complete
  changed source `af612a` produced 1,561 versus 1,555 CODE bytes.
  The original controlled jumps are retained; original source proved
  exact as `af612e`.
- Complete Enemy four-object script/update/formation group,
  **3,325 CODE bytes**: flattening the `enemy_move_and_clip` early
  returns changed native branch targets (`af612c`); inverting
  `enemy_run()` movement conditions changed an original near conditional
  jump into a short conditional jump plus an unconditional near jump
  (`af612h`/`af612i`), and inlining segmented script pointer addition
  changed the original stack-store/add instruction sequence. Original
  label/nesting, the two-step pointer arithmetic, script duration and
  loop cases were restored. Original ENEDAT loop quirks remain intact.

The actually source-bound **large Explosion collision function** remains
modified and recertified (`af611g`), replacing alias macros, an enum
union and the radius/double-size local without altering the original
630 CODE bytes, 49 native fixups or the 1-function PUBLIC. The current
Bullet, Fireball, Explosion and four Enemy original physical TUs were
then rebuilt **together**, not just checked separately:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af615a --units e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af615a

**Two independent genuine TC4/TLINK rounds**, with OMF dependency
records binding the actual staged changed source, reproduce all
**8,195 original CODE bytes**, one initialized Fireball DATA byte,
all 582 literal ordered native fixup fields, all 50 PUBLICs, exact
source segment/BSS layouts, the complete original normal MAIN EXE/MAP,
124,642 loaded Japanese program bytes and 1,553 ordered MZ relocations.
Separate standard MZ serialization gives the exact 130,882-byte original
Japanese MAIN.EXE.

Full raw original compiler/linker artifacts, writer logs, input overlays,
response files and OMF-attested source receipts are retained under
`.analysis/work/exatt-layout-af615a/report.json`, SHA-256
`c0062b9709b975ed8a310b31931402ed8fc11ad150fb9cab0d8b92110f351483`.
All rejected edited sources and output controls are retained in ignored
native work; old commits are not rebased, amended, or erased.

This recertifies real native source exactness, **not new packed Factory
credit, raw historic vendor OMF packet identity or PC-98 runtime behavior**.
It explicitly corrects incorrect previous natural-source exactness claims
rather than perpetuating them.
