# TH03 current handoff

## Phase

Formal MAIN exact reconstruction using the TH04 cold-source overlay method.
Ten maintained exact owners now contain twenty exact functions / 1340 exact
owned bytes: `th03-main-vector-far` (160, including one alignment byte),
`th03-main-exit` (67), `th03-main-polar` (26), `th03-main-frame-delay` (21),
`th03-main-input-sense` (417), `th03-main-snd-se` (120),
`th03-main-snd-kaja` (30), `th03-main-initmain` (62), `th03-main-pi-load` (70),
and `th03-main-input-modes` (367). Target-first boundaries,
far/cdecl/Pascal ABI, full unnormalized bytes, MAP contributions and ordered
MZ relocation sites/values are reviewed. The whole-product graph
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
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-vector-far
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-exit
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-polar
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-frame-delay
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-input-sense
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-se
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-snd-kaja
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-initmain
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-pi-load
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
All 20 configured outputs and 351 game objects are deterministic, all 417 OMF
objects are valid, all ten accepted owners and all twenty full bodies match,
and the existing DOS ABI/behavior probe stays passing. The maintained sources
have no upstream includes or copied target-byte payloads. The vector owner uses
symbolic TASM and `EVEN` rather than the historical raw opcode bytes / C++
`codestring`; its 159 function bytes plus one alignment byte match as one
160-byte owner. The 417-byte
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
14 function / 951-byte exact checks. The subsequent non-leaf
`th03-main-initmain` owner is one complete 62-byte body with one caller, seven
callees, Pascal far-pointer cleanup, and six ordered owner relocation sites.
Development probes `gpt-web-initmain-probe1` and
`gpt-web-initmain-probe2-0936` passed with the aggregate expanded to 15
functions / 1013 bytes. Post-promotion aggregate
`gpt-web-main-six-owner-final-20261005-b` then began with all six owners
already accepted and passed the same two-round product/object vector plus all
function, MAP and ordered-relocation checks. Native TH03 Truth Kernel
publication remains unavailable.

The next data-flow owner `th03-main-pi-load` is one complete 70-byte far
Pascal body. Target instructions independently confirm the 0x48-byte
`PiHeader` stride, parallel four-byte far-pointer buffer slots, two master.lib
callees, `RETF 6`, and owner relocation sites 31 and 60. Development replay
`gpt-web-pi-load-probe1-0948` passed two fresh full builds with the aggregate
expanded to 16 functions / 1083 bytes. Post-promotion aggregate
`gpt-web-main-seven-owner-final-20261005-a` then began with all seven owners
already accepted and independently passed the same two-round product/object,
full-function, MAP and ordered-relocation checks. The next complete owner,
`th03-main-snd-kaja`, is the 30-byte far Pascal KAJA interrupt bridge at
`SHARED:03C2`; TH03 confirms the snd_active early return, AX argument load,
INT 60h/61h dispatch selected by snd_midi_active, two direct callers, `RETF 2`,
and zero owner relocation sites. Development replay `gpt-web-snd-kaja-probe1-1005`
and post-promotion aggregate `gpt-web-main-eight-owner-final-20261005-a` both
passed, bringing that frontier to 17 functions / 1113 bytes. The next
`th03-main-vector-far` owner replaces MAIN's historical raw-inline-opcode
translation unit with symbolic TASM: `VECTOR2` is 69 bytes, `EVEN` contributes
one reviewed NOP, and `VECTOR2_BETWEEN_PLUS` is 90 bytes. Target review confirms
15/4 direct callers, the sole `IATAN2` callee in the between-plus body, far
Pascal cleanup, and the single owner relocation at relative site 94.
Development replay `gpt-web-vector-far-probe1-20261005-1828` passed two fresh
full builds, expanding the maintained aggregate to 19 functions / 1272 function
bytes and 1273 owned bytes. MAIN now links `vectorfar.obj`; the deterministic
all-game vector is 351 game objects / 417 generated OMF objects because the
historical `th03/vector.obj` remains required by other products.

Post-promotion aggregate `gpt-web-main-nine-owner-final-20261005-a` began with
all nine owners already accepted and independently passed the same full two-round
20-product / 351-game-object vector, all 417 OMF validations, all 19 function
bodies / 1272 function bytes, the one declared alignment byte, the 1273-byte
owned aggregate, MAP placement, and ordered relocations.

The adjacent `th03-main-exit` owner is now independently reconstructed as
natural C++: one complete 67-byte far-cdecl body, one caller, seven unique
callees / eight far calls, and the exact PC-98 A6/A4 port sequence. Development
replay `gpt-web-exit-probe3-20261005` passed two fresh full builds and
expanded the frontier to 20 functions / 1339 function bytes / 1340 owned bytes.

Post-promotion aggregate `gpt-web-main-ten-owner-final-20261005-a` began with
all ten owners already accepted and passed the same two-round 20-product /
351-game-object vector, all 417 OMF validations, all 20 function bodies /
1339 function bytes, the one declared alignment byte, the 1340-byte owned
aggregate, MAP placement, and ordered relocations.

## Next bounded work

Continue MAIN first and do not restrict the frontier to tiny leaves. Vector math
and the adjacent exit owner are now closed. Rank the next gameplay owners by
their complete linker extents rather than adjacency: `e_expl.cpp` contributes a
single 0x276-byte (630-byte) C++ block; `e_fireb.cpp` contributes 0x613
(1555) bytes; `bullet.cpp` contributes 0x53 + 0xA2A (2685) bytes across
two segments; and `e_enemy.cpp` contributes multiple blocks totaling more than
3 KiB. Prefer a complete several-hundred-byte owner next, then escalate to the
multi-segment bullet/enemy owners once their shared segment/data dependencies
and function boundaries are explicitly mapped.

After the input/math frontier, proceed into timing/state update and then
two-player dispatch/game-object logic. Determine packed/decoded ownership for
OP/MAINL/ZUN before treating their storage inventories as game functions.
MAIN has 1553 MZ relocations; the other three containers have zero. This is
observed structure, not proof of packer identity. Keep replaying the entire
accepted MAIN aggregate after every new owner, and investigate OMF identity
drift separately without changing the imported calibration hashes.
