# TH03 MAIN after782: six genuinely modified original physical sources compiled together

This is the latest **current-maintained-source simultaneous two-round
original Turbo C++ 4.02 / complete normal MAIN TLINK** verification.
The real original game uses 99 project objects; only the **six**
complete original physical translation units changed in this session
were recompiled. The remaining **93 original project objects plus
Borland CRT** were reused from the frozen source-native after596 normal
MAIN parent. This is not an all-99-object cold replay, a hand-patched
object or an inferred union of disjoint prior stages.

| Original physical owner | Complete source functions actually compiled | CODE bytes | Ordered native OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `cs_yume` | **Yumemi Chargeshot**: complete ten-function enemy/BOSS target search, charged projectile update and hitbox, 16-sprite blooming rings, long original switch-table Gauge controller | 1,645 | 133 | 10 |
| `ex_rika` | **Rikako Extra Attack**: 14-entity spawn/render, signed homing turn and movement, 16-bit hitbox/collmap, active-entity update | 702 | 46 | 5 |
| `cs_mima` | **Mima Chargeshot**: 30-shot reset, 15-entity creation/update, six-angle emission, collision and dual 8/16-frame Gauge ring state | 1,338 | 150 | 10 |
| `ex_chyu` | **Chiyuri Extra Attack**: 16 physical paired entities, 518-byte GRCG beam renderer and large original paired update; manual BX state/Jcc is now native C++ | 978 | 55 | 4 |
| `ba_yumem` | **Major Yumemi BOSS**: attack families, whole collision/update, GRCG main render and four-phase 112-pixel entrance rasterizer with two-stage natural signed C++ shifts | 2,358 | 343 | 10 |
| `ex_kana` | **Kana Extra Attack**: full eight-slot creation, accelerating bullets, sprite animation, collision/flight update and renderer | 663 | 44 | 5 |
| **Six complete original physical source owners together** | | **7,684** | **771** | **44** |

## Native original-code and whole-game link evidence actually executed

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af782a --units cs_yume,ex_rika,cs_mima,ex_chyu,ba_yumem,ex_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af782a

Both genuine original Turbo C++ 4.02 compiler/full TLINK rounds reproduce
**every 7,684 initialized original CODE byte, all 771 literal ordered
original OMF FIXUPP fields, all 44 PUBLIC offsets**, original OMF
segment and uninitialized DATA/BSS declarations, and the real
compiler-emitted current-source dependency COMENT records. The complete
99-project-object normal MAIN EXE and path-normalized MAP match. The
original Japanese **124,642-byte loaded program** and **all 1,553
ordered MZ relocation words** match. A separately validated standard
DOS MZ serializer reproduces every byte of the original **130,882-byte
Japanese MAIN.EXE**. That serializer's MZ header is not claimed to be
the exact header bytes emitted by the historical vendor's linker.

Current-source independent evidence:
`.analysis/work/exatt-layout-af782a/report.json`, SHA-256
`d42120816ae6a1a1279872a9237cbe41a83e822f5fb9ef963b66781814f58ef7`.
The original/native OBJ, source/headers, OMF COMENTs, both compiler
writer logs and TLINK response files, full EXE/MAP and original
serialized Japanese MZ are preserved as protected ignored evidence.
No original input or previous receipt was repinned, replaced or padded;
recompilation needs a new unused DOS-safe stage ID.

## New C++ recovery and separately preserved failed experiments

The most substantial handwritten-assembly removal is in Chiyuri's
paired-entity update: TC4 generates the original `MOV BX` / memory
byte compare / conditional branch directly from ordinary
`if (!exatt_entity_p->state) goto chiyuri_first_done;`. It still
preserves the original jump label, paired pointer increment and exact
GRCG/hitbox timing. The *different* late beam-radius branch cannot be
reduced to `_AX = CHIYURI_BEAM_FINISH - phase`; original AX/DX and
stack ordering remains explicit (`af779c` negative control).

Yumemi's major BOSS 112-pixel entrance rasterizer now generates its
original four positional stages from natural **two distinct C++ left
shifts** (`(frame << 3) << 4`), with 0x18/0x30/0x48/0x60 named
phase gates. Collapsing both shifts to `frame << 7` changes original
CODE (`af780b`); natural `_DX ^= _DX` does not generate the original
`XOR DX,DX` encoding (`af780c`). Both rejected forms were restored.

The full Yumemi Chargeshot and target-search controller uses natural
signed loop indices, state/target Boolean checks and a 16-sprite
`frame << 1` ring angle. Original *byte* `frame % 2` special-sound
and `% 8` Gauge launch clocks could **not** be replaced by masks
(`af776a`/`af776d`). Rikako's 14-entity homing controller naturally
uses frame parity and state tests but preserves original signed
`angle_delta /= 8` (not arithmetic shift) and original byte
`p->speed++` (`af777b`/`af777c` rejected).

Mima's original 30-projectile Chargeshot now uses signed local prefix
loops and natural active-state tests, but **all three** original
4/8/16-frame byte-modulo clocks independently fail direct bit-mask
replacement (`af778c`/`af778d`/`af778e`). Kana's full eight-slot Extra
Attack similarly preserves its `%16` bullet period and the *separate*
`frame / 4` and `%4` sprite-cel computations; each individual shift or
mask alternative changed CODE (`af781b`/`af781d`/`af781e`). These are
real compiler experiments, not conjectures about C++ equivalence.
All failed native compiler trees remain separately protected and are
**never** claimed as accepted current source.

## Acceptance boundaries and previous receipts

Current-source independent review passes this `af782a` receipt, its six
individual after776..781 final source stages, and unchanged previous
`af775a` (eight-source) and `af766a` (eight-source) receipts. Different
stages may cover overlapping original CODE; never sum them as new
physical ownership credit. Older `af758a`/`af741b` original native
compiler snapshots remain historically retained but correctly fail
current-live-source input hash checks after later product source changes.

The 417-byte original BIOS `input_s` is **not** included: the old frozen
parent uses an experimental 418-byte input object with an extra 0x90
NOP, so its exact source-native original OBJ still has a one-byte full
MAIN link gap. Do not fake an inserted NOP or claim a full linked pass.
Current MAINL source-publication acceptance remains separate and pending.
This scoped natural C++ proof is **not** new canonical Factory packed-file
unit acceptance, proof of original vendor raw OMF packet identity, or
full source-owned 99-object project closure.
