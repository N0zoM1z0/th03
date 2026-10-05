# TH03 current handoff

## Phase

Infrastructure bootstrap from TH04. Maintained game source, reviewed authored
ownership and accepted exact units are empty. The whole-product graph remains
open in `config/build.toml`. Do not advertise a playable reconstructed build.

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
```

Use the shared Factory repository `th03`; four native provider IDs are
`th03-ghidra`, `th03-op-ghidra`, `th03-mainl-ghidra`, `th03-zun-ghidra`.
Factory replay of exact TH03 units is not configured yet. Native analysis and
repository shell work grant no exactness credit. Deployment details remain
private in the Factory, with its existing endpoint and processes preserved.

## Next bounded work

Determine packed/decoded ownership for OP/MAINL/ZUN before treating their
storage inventories as game functions. MAIN has 1553 MZ relocations; the
other three containers have zero. This is observed structure, not a proof
of packer identity. Recover the first bounded startup/library unit and its
ABI, then build a checked-in TH03 source graph. Investigate OMF identity drift
using isolated repeated builds before establishing a new local calibration.
