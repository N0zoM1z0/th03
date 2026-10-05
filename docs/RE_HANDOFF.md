# TH03 current handoff

## Phase

Formal MAIN exact reconstruction using the TH04 cold-source overlay method.
Two complete maintained owners contain ten exact functions / 393 exact authored
bytes: `th03-main-polar` (26 bytes) and `th03-main-input-modes` (367 bytes).
Target-first boundaries, far/cdecl/Pascal ABI, full unnormalized bytes, MAP
contributions and ordered MZ relocation sites/values are reviewed. The
whole-product graph remains open in `config/build.toml`.

## Verified local inputs

- The same supplied archive is copied to `../game_exe/`. Import selects the
  hash-pinned Japanese `zun.hdi`, never the translated image.
- Four required YUMEZIKU artifacts are pinned in `config/targets.toml`:
  OP.EXE 36041 bytes, MAIN.EXE 130882, MAINL.EXE 37975, ZUN.COM 16242.
  All are structurally valid MZ containers. Provenance remains
  `candidate-local-attested`; explicit release version is unknown.
- Ghidra 12.1.3/JDK 21.0.12.1+1 are physical local copies of TH04 tools.
  All four `ghidra-project/TH03-th03-*.gpr` projects pass independent full
  target/header/load/relocation/entry/sample checks.
- TC4J/TASM/TLINK media, unpacked installations and required hashes are
  preserved. A new TH03 Wine prefix passes both headless probe rounds,
  valid OMF production, link and execution. The optional host wine64 hash
  differs from the old observation; required surfaces and execution pass.
- Pinned ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` is cloned
  independently. Cold run `bootstrap-th03-20261005` produces all 20 known
  EXE/COM hashes and 416 valid OMF objects. Private receipts are under
  `.analysis/builds/rec98-b6ba5b0a52/bootstrap-th03-20261005/`.
- The imported all-game calibration gate FAILS on dependency-normalized OMF
  set identities for all five games. Archive identity, candidate hashes,
  candidate comparison vectors, object counts and object validity pass.
  The cause is unresolved. Keep the imported calibration hashes unchanged;
  no exactness or whole-object reproducibility follows from this run.

## Commands

```sh
python3 scripts/preflight.py
python3 scripts/ci.py
python3 scripts/build.py --status
python3 scripts/build.py --reference --run-id NEW_UNIQUE_ID
python3 scripts/ghidra.py th03-main check
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-polar
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-modes
```

Use the shared Factory repository `th03`; four native provider IDs are
`th03-ghidra`, `th03-op-ghidra`, `th03-mainl-ghidra`, `th03-zun-ghidra`.
Factory replay of exact TH03 units is not configured yet. Native analysis and
repository shell work grant no exactness credit. Deployment details remain
private in the Factory, with its existing endpoint and processes preserved.
TH03 repository discovery exposes read-only reference `/references/th04`.
The actual TH04 maintained math source was read through the public MCP, with
write denial and unchanged reference bytes. Existing MCP/worker PIDs survived
the hot deployment; the Factory fix is committed separately.

## Exact replay observations

`input-math-owned-candidate` performs two independent full `git archive`
materializations, overlays frozen local source and recompiles every object.
All 20 configured outputs and 350 game objects are deterministic, all 416
OMF objects are valid, both full owners and all ten full bodies match, and
both DOS ABI/behavior probes pass. The maintained sources have no upstream
includes or target-byte payloads. Seven portable positive/negative Oracle
tests cover full-byte and relocation failures. See
`docs/MAIN_INPUT_MATH_EXACT.md` and the scoped CSV evidence rows.

Nine auxiliary Research benchmark objects differ because their LEDATA embeds
`__DATE__/__TIME__`; preserve those differences as diagnostics. They are outside
the declared game object vector. This is separate from the unresolved imported
TH04 all-game calibration mismatch; its old hashes have not been changed.
Local exact-owner evidence does not publish Factory Truth Kernel acceptance.

Post-promotion run `factory-main-input-math-exact` executed the same checked-in
Oracle through the public Factory repository shell. It covered both accepted
owners, passed the full two-cold vector and DOS probes, and preserved HEAD and
visible source state. Its two scoped aggregate evidence rows bind the current
source/configuration/Oracle hashes. The public native Ghidra query also returned
the expected 26- and 76-byte target bodies. The broader Factory validation
passed 166 tests; flexible addresses and read-only TH04 references are hot-live.

## Next bounded work

Determine packed/decoded ownership for OP/MAINL/ZUN before treating their
storage inventories as game functions. MAIN has 1553 MZ relocations; the
other three containers have zero. This is observed structure, not a proof
of packer identity. Extend the maintained MAIN graph one reviewed owner at a
time, always replaying the accepted aggregate. Investigate OMF identity drift
using isolated repeated builds before establishing a new local calibration.
