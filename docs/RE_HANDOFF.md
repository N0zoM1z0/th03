# TH03 current handoff

## Phase

Formal MAIN exact reconstruction using the TH04 cold-source overlay method.
Five maintained exact owners now contain fourteen exact functions / 951 exact
authored bytes: `th03-main-polar` (26), `th03-main-frame-delay` (21),
`th03-main-input-sense` (417), `th03-main-snd-se` (120), and
`th03-main-input-modes` (367). Target-first boundaries, far/cdecl/Pascal
ABI, full unnormalized bytes, MAP contributions and ordered MZ relocation
sites/values are reviewed. The whole-product graph
remains open in `config/build.toml`.

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
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-frame-delay
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-sense
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-se
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

The maintained exact replay performs two independent full `git archive`
materializations, overlays frozen local source and recompiles every object.
All 20 configured outputs and 350 game objects are deterministic, all 416 OMF
objects are valid, all five accepted owners and all fourteen full bodies match,
and the existing DOS ABI/behavior probe stays passing. The maintained sources
have no upstream includes or copied target-byte payloads. The 417-byte
`input_reset_sense_key_held` body deliberately excludes the target's following
one-byte NOP at `SHARED:033D`; no `codestring` is used to manufacture ownership.
Portable positive/negative Oracle tests cover full-byte and relocation failures.
See `docs/MAIN_INPUT_MATH_EXACT.md` and the scoped CSV evidence rows.

Nine auxiliary Research benchmark objects differ because their LEDATA embeds
`__DATE__/__TIME__`; preserve those differences as diagnostics. They are outside
the declared game object vector. This is separate from the unresolved imported
TH04 all-game calibration mismatch; its old hashes have not been changed.
Local exact-owner evidence does not publish Factory Truth Kernel acceptance.

The earlier post-promotion run `factory-main-input-math-exact` remains the
baseline receipt for the original polar/input-mode pair. The next expansion
independently re-screened `frame_delay` as one complete 21-byte body with three
direct callers and `input_reset_sense_key_held` as one complete 417-byte body
with ten direct callers and no callees. The new `th03-main-snd-se` owner adds
the complete adjacent 60-byte `SND_SE_PLAY` and 60-byte `_snd_se_update`
bodies. Their target owner is exactly the 120-byte MAP contribution, with 55
and three direct callers respectively and no owner relocation sites. Development
probe `gpt-web-snd-se-probe3` passed two fresh full builds, identical
20-product and 350-game-object vectors, all 416 valid OMF objects, and complete
raw/MAP/relocation checks. The existing DOS probe also stayed passing, but it
does not directly exercise the new sound owner. Post-promotion aggregate
`gpt-web-main-five-owner-final-20261005-a` then began with all five owners
already accepted and independently passed the same two-round vector plus all
14 function / 951-byte exact checks. Native TH03 Truth Kernel publication
remains unavailable.

## Next bounded work

Continue MAIN first. Do not restrict the frontier to tiny leaves. The next
low-dependency candidates immediately around the recovered foundation are
`th03/snd_kaja.cpp` (30 bytes), `th03/initmain.cpp` (62 bytes, seven callees),
and `th03/pi_load.cpp` (70 bytes, two callees); `initmain` is the preferred
non-leaf control-flow owner. The bounded math candidate remains the 160-byte
`th03/vector.cpp` SHARED contribution at `0E8F:008A`: target-local comparison
shows the pinned reference contribution is byte/relocation exact, but the
historical source relies on raw inline opcode bytes and a `codestring` NOP.
Ghidra splits it into a 69-byte `VECTOR2` body, one intervening padding byte,
and a 90-byte `VECTOR2_BETWEEN_PLUS` body. Treat that as routing evidence only;
recover acceptable natural source or justified original-style ASM and keep the
padding ownership separate rather than promoting the historical trick.

After the input/math frontier, proceed into timing/state update and then
two-player dispatch/game-object logic. Determine packed/decoded ownership for
OP/MAINL/ZUN before treating their storage inventories as game functions.
MAIN has 1553 MZ relocations; the other three containers have zero. This is
observed structure, not proof of packer identity. Keep replaying the entire
accepted MAIN aggregate after every new owner, and investigate OMF identity
drift separately without changing the imported calibration hashes.
