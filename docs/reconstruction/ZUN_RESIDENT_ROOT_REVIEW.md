# ZUN -5 maintained resident root

This checkpoint adds maintained source presence for the two existing decoded
resident function units, not new units or canonical-file exact acceptance.
`cfg_init` at inner COM `0367` is 97 bytes; `main` at `03C8` is 225 bytes.
The complete root contributes 322 CODE bytes, 307 initialized DATA bytes and
zero BSS. DATA is separately verified and is not counted as more CODE.
ZUN source presence is now 15/18 tracked units and 1,855 scoped CODE bytes;
exact remains zero. Canonical packed-file offsets remain blank.

## Source and compiler contract

The maintained owners are `src/zun/res_yume.cpp`, `res_init.inl` and
`cfg_init.inl`. They preserve the CP932/LF implementation bytes from ReC98
revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`; only include routing
changes. Seven forwarding compatibility headers retain declaration boundaries.
`config/zun_resident/source.json` and the source-only staging script validate
the full ten-file overlay and reverse include changes back to the three pinned
reference hashes. They never compile or link.

Both native materializations use the declared tiny-model recipe:

    tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -mt -nobj/th03/ th03/res_yume.cpp
    tlink @obj\th03\res_yume.@l

The original `#pragma option -2` remains. The link response is
`-c -s -t c0t.obj obj\th03\res_yume.obj, bin\th03\res_yume.com, obj\th03\res_yume.map, bin\masters.lib emu.lib maths.lib ct.lib`.
C0T, masters, EMU, MATHS, CT and all direct library bodies are unowned context.
No project OBJ is a staging input. No padding, binary patch or linker-output
mutation is used.

## Fresh evidence and preserved correction

The first build, RESY01, ran at 23:36:47–23:37:01 UTC on 2026-10-21 under
manifest `86460dfdc3555f4ee84dffaff5864f086e2256ba701134854aa96e36699d20b4`.
The separately declared RESY02 build ran at 23:47:20–23:47:31 under manifest
`d207d2120cc087efddee15f7e7dee893289621d96e1d188cfde1a858fc764461`.
Both used clean HEAD `cd4756656748afb888bfa7174c1b66d4070f5c00`.
All 31 staged inputs have identical bytes, modes and declared nanosecond
mtimes. The two compile/link pairs are four actual native phases, each
headless, one CPU, nice 10 or greater, with 90-second execution and 15-second
exact-owned cleanup bounds, shared writer claim and bounded registry policy.
Captured precompile inventories, phase commands/environments, clean terminal
inventories and raw registry transitions are independently replayed.

All three raw pairs are equal, without timestamp normalization:

- OBJ: 2,392 bytes, SHA-256 `60fa42bc7e386d41cc251c0dd42dfe0ddc1d5edc7448d486c157acce58ef5422`.
- MAP: 15,282 bytes, SHA-256 `942b5dc331b3ce2121717c665f7977e4d3d92995bffe06baab9fdf190a6be702`.
- COM: 5,618 bytes, SHA-256 `cfe11aff09ae2bb92e6775c3d0aead8ae610e6bc2ad7e0551ec9f42e838734b8`.

The first verifier failed only because it expected eleven EXTDEFs. The actual
object has twelve, in a fixed ordered vector with type index zero. The added
`__setargv__` is an absolute linker selector exported by CT.LIB's `setargv.asm`
member, not an extra authored call. Its raw 781-byte member at offset 151040
has SHA-256 `66c6a19256ed0c609b0942c16b4c8936857cf606dff32d28e5066fc4979f2af4`.
The member, its CODE/DATA/INITDATA MAP contributions, the compiler marker,
`main(int argc, const unsigned char **argv)` and vendor C0 initialization and
argc/argv setup corroborate compiler/runtime selection. The causal association
with this signature is an inference, not a controlled compiler probe or a C0
source reconstruction. The corrected verifier retains exact membership,
ordering and type checks; it does not drop the import gate.

Original manifest, verifier, failed report and completion are unchanged. The
new correction and runtime report bind them explicitly. The old missing
historical cold receipt was not recreated or used as fresh evidence.

## Structural and bounded runtime scope

Twenty structural gates verify the complete three-public root, exact mangled
`@cfg_init$qur10resident_t`, public/MAP addresses, complete initialized DATA,
CODE coverage and FIXUPP presence, exact import vector, startup-selector
context, whole root bodies, procedure decoding and ABI. Root CODE occupies
`0367..04A9`, DATA occupies `131E..1451`, with zero BSS. The first 26 DATA bytes
bind debug/default options, `yume.cfg` and `YUMEConfig`; all 307 bytes match.

The retained runtime report has 21 passing gates and exactly 40 modeled calls:
20 scenarios on the target and 20 on RESY01. RESY02 was not separately modeled;
its byte identity links it to the first candidate evidence. Models cover
argument/debug/removal paths, resident lookup, allocation and fallback,
configuration I/O and error behavior, preserving SI/DI/BP/DS/stack. DOS,
MCBs, files, allocation and GRCG ports are modeled, and CRT startup is bypassed.
Unchecked fallback behavior, signed handle comparisons and ignored errors
remain source behavior, not silently corrected behavior. This is not physical
DOS/PC-98 timing, rendering, device or whole-game validation.

The full COM matches the decoded `-5` target at decoded launcher offset `4322`,
using the pinned DIET restoration lineage. That whole-COM equality remains a
contextual diagnostic: vendor startup/runtime/master bodies are not adopted
as maintained ownership, no packed launcher is rebuilt, and independent
pristine provenance remains unresolved.

## Maintained replay and retention

    .venv/bin/python3 -B scripts/replay_th03_zun_resident.py

This is offline structural/receipt replay, not another compiler or model run.
It checks current maintained sources against the consumed native overlay,
replays both guarded native captures, and compares the retained actual model
rows. The six local helper modules are checked against the original native
manifest before loading. Target configs and stored target bytes are explicitly
bound. Unrelated tracked ledgers/docs are not required to remain frozen.
The native v01 and corrected v02 verifiers themselves remain immutable.

The compact tracked `config/zun_resident/proof.json` binds the detailed ignored
inventory in `.analysis/zun-resident-maintained-proposal-v01/`. That directory's
`retention.json` has an `inputs` dictionary for cleanup retention. Pre-runtime
completion records retain their original `runtime_pending` fields; later
runtime evidence is separate. Neither proof nor replay grants Factory,
whole-payload, launcher or exact acceptance.
