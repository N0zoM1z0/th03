# MAIN Mima charge/gauge and bomb checkpoint

Status: **source-present only, zero accepted exact credit**. Two complete
natural C++ producers cover 13 routines and 2,171 original CODE bytes. Native
compilation and a retained-input diagnostic link succeeded; the full independent
two-round cold replay, behavior gates and whole-product acceptance remain open.

## Ownership and target

Japanese MAIN.EXE SHA-256:
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
Provenance remains candidate-local-attested, not independent pristine-dump proof.
The MZ header is 6,240 bytes (`0x1860`).

| Ledger extent | Load interval | Target file start | Bytes/functions/MZ entries | Physical source |
|---|---|---|---|---|
| th03-main-mima-charge | `153BB..158F5` | `16C1B` | 1338 / 10 / 9 | `src/main/player/chargeshot_mima.cpp` |
| th03-main-mima-bomb | `17043..17384` | `188A3` | 833 / 3 / 13 | `src/main/player/bomb_mima.cpp` |

Both `units.csv` rows intentionally name the logical owner's primary source
`src/main/player/chargeshot_mima.cpp`, as the original replay validates each
extent's source against its logical unit. This does not assign bomb's physical
compiler production to charge: `cs_mima` produces HITBOX_TEXT charge/gauge and
`bm_mima` produces BULLET_TEXT bomb, both in MAIN_04 frame `139D`.
`src/main/player/mima_gameplay.hpp` describes existing storage without allocations.

## Observed results and limitations

- Target boundary audit decodes all 13 complete bodies and their return cleanup.
  Gauge's internal RET 2 is part of one 483-byte routine. The original ordered
  MZ lists are kept literally; neither target bytes nor record order is patched.
- Actual two-object TC4 compile succeeds: 1,338 + 833 CODE bytes, all 13 routine
  spans/returns, zero private DATA/BSS. Retained receipt:
  `.analysis/gpt-dots-mima-gameplay-source-v01/probe-v03/compile-first-v03/receipt.json`
  (`68cdbe1b0c793c99c3add08bc7978b13c6f05b665b6842d3f2a91af21cfb634d`).
- Retained-input TASM/TLINK diagnostic matches **all 2,171 raw bytes, all 13
  routines, both MAP contributions and all 22 literal ordered relocations**.
  All 76 prior declared extents (74 plus Marisa and Reimu/shared) remain exact
  in this bounded comparison. Receipt:
  `.analysis/gpt-dots-mima-gameplay-source-v01/relink-proposal-v01/run-first-v01/receipt.json`
  (`d010a880b9577bc14303b8e84fd2a06d72ead18176c222876c8eab75155f841d`).
- Outside combined Reimu+Mima scope, complete raw payload and literal relocation
  order match the **original Marisa cold baseline**. Separately, raw payload
  matches the historical retained-Reimu output, but its literal order differs.
  These distinct comparisons are not combined, and the historical failed-order
  observation remains preserved. No whole-image equality is claimed.
- Storage remains alias-based in the carrier, not reallocated by the C++ TUs.
  Factory read-only command `938b340ee2814cb4af902a5983ca5e5a` separately
  checked ten Mima aliases plus shared timing, all 512 existing DGROUP publics,
  33 allocation rows, initialized data/header identity, six angle bytes and
  three same-frame calls. No separate storage-audit artifact was created;
  the retained receipt's storage field still says pending separate review.
  These observations can be recomputed from the pinned MAP/EXE and do not
  establish historical physical compiler ownership.
- The independent round-initializer source's one-byte blocker is outside this
  checkpoint and is neither included nor credited.

## Source and ABI review

Charge uses 15 ten-byte records/player: active byte, unknown byte, signed x/y
and velocity words. Bomb uses eight four-byte columns/player: x and sprite
words. Existing six angle bytes remain in place. The gauge argument is a word
stack slot with a genuine word comparison; only its template assignment narrows
to byte. Hittest returns a hit count in AL. The sprite API halves height, so
source height 16 implements target hardware height 8. Bomb columns stop at the
first uninitialized sprite, retain division-based phase, and preserve both
EGC-on calls in the early phase.

Two ordinary guard/continue rewrites and a positive hit conjunction reproduce
native control-flow behavior without register allocation forcing. The one MRS
caller compatibility expression `(_AX = pid_current)` follows the maintained
Marisa/Reimu precedent: its genuine bool formal remains unchanged, the callee
reads byte `[BP+6]`, and the caller zero-extends the word stack carrier. It is
not an AX-parameter ABI. BX use at the VRAM fill helper is a real hardware ABI.
No target-byte arrays, fake ABI, padding, OMF calibration or order forcing is
used for these Mima producers.

## Required next verification

The installed candidate manifest composes Marisa, Reimu/shared and Mima:
`config/th03_main_mima_gameplay_candidate.toml`.
After the reviewed ledger append is installed, the original replay command is:

    python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_mima_gameplay_candidate.toml --run-id mima-gameplay-cold-review-v01

This command is a reproduction plan, **not a recorded successful run**. It must
complete the original cold/behavior/ownership gates and supplemental outside-
combined preservation checks before any exact promotion. Historical failed
compile-driver HEAD assertion and retained-Reimu order mismatch remain evidence.
