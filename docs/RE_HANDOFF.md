# TH03 current handoff

## Phase

Formal MAIN exact reconstruction using the TH04 cold-source overlay method.
Thirteen maintained exact source owners now span fourteen exact CODE extents and
contain forty exact functions / 6210 exact owned bytes. The prior twelve owner
sizes remain vector-far 160 (including one alignment byte), exit 67, polar 26,
frame-delay 21, input-sense 417, snd-se 120, snd-kaja 30, initmain 62, pi-load
70, input-modes 367, explosion-collision 630, and fireballs 1555. The new
complete bullet source owner adds 2685 CODE bytes split across PELLET_PUT (83)
and BULLET_TEXT (2602), plus a 0x251C-byte BSS MAP contribution. Target-first
boundaries, near/far/cdecl/Pascal/register ABIs, full unnormalized bytes, MAP
contributions, compiler switch tables/alignment, and ordered MZ relocation
sites/values are reviewed. The whole-product graph remains open in
`config/build.toml`.

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
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-explosion-collision
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-fireballs
python3 scripts/replay_th03_main_exact_units.py --unit th03-main-bullets
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
objects are valid, all fourteen accepted CODE extents and all forty full bodies
match, and the existing DOS ABI/behavior probe stays passing. The bullet owner
uses explicit frozen `compat/rec98/` forwarders rather than direct upstream
includes. There are no bulk copied target-byte payloads; `bullets_render`
retains one two-byte `__emit__` solely to select TC4J's target XOR AH,AH ModR/M
direction without changing argument order or register allocation. The vector
owner uses symbolic TASM and `EVEN` rather than the historical raw opcode bytes
/ C++ `codestring`; its 159 function bytes plus one alignment byte match as
one 160-byte owner. The 417-byte
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

The first gameplay owner is now closed as well. th03-main-explosion-collision
is the complete 630-byte E_EXPL_TEXT:2D3D contribution from th03/e_expl.cpp,
containing the single large explosions_hittest body. TH03 target review
confirms two callers, five unique callees, the 64-entry / 0x30-byte record
walk, the chain/bonus state updates, and one far-call relocation at
owner-relative site 342. Development replay gpt-web-expl-probe-20261005-2
passed both cold rounds. The replay Oracle was generalized at the same time to
bind segment/group per owner, so gameplay owners outside SHARED can be verified
without weakening the existing checks. Post-promotion aggregate
gpt-web-main-eleven-owner-final-20261005-1 began with all eleven owners
accepted and passed all 21 function bodies / 1969 function bytes plus the one
declared alignment byte for 1970 exact owned bytes.

The next complete gameplay owner is now closed as well. th03-main-fireballs
covers the full E_FIREB_TEXT:43DE..49F0 contribution: eight contiguous
functions totaling 1555 code bytes. Independent target review corrected the
initial seven-public reading by identifying a separate 86-byte near-Pascal
chain_fire_charged_exatt at 139D:479D. The owner has eleven ordered MZ
relocations. Its initialized variant byte at 1D56:0BEC is raw-exact, while the
Oracle also fixes that one-byte DATA contribution and the one-byte
generation_prev BSS contribution at 1D56:8DF8 through MAP checks. Development
replay gpt-web-fireball-probe-20261005-1 passed both cold rounds.
Post-promotion aggregate gpt-web-main-twelve-owner-final-20261005-1 began with
all twelve owners accepted and passed all 29 function bodies / 3524 function
bytes plus the one declared alignment byte for 3525 exact owned bytes.

The complete bullet gameplay source owner is now closed as the first
multi-segment maintained owner. Target review separates the 83-byte PELLET_PUT
extent from the 2602-byte BULLET_TEXT extent and identifies eleven function
bodies totaling 2579 bytes. BULLET_TEXT additionally owns two switch tables
(90 + 14 bytes) and two alignment bytes; these are producer-owned but are not
counted as functions. Its 16 ordered MZ relocation sites match, PELLET_PUT has
none, and MAP fixes the zero-length DATA plus 0x251C-byte BSS contributions.
Ghidra's polluted switch-recovery body maxima for group_velocity_set and
bullets_add were explicitly rejected in favor of RET boundaries, dispatch-table
operands, MAP adjacency, and original target bytes. Fresh two-round replay
`gptweb-bullet-fresh-20261005-2044-a` passed all 40 functions / 6103 function
bytes and all 6210 owned bytes before final aggregate promotion. Post-promotion
aggregate `gpt-web-main-thirteen-owner-final-20261005-b` then began with both
bullet extents already accepted, froze the tracking/evidence/function ledgers
as replay inputs, and independently passed the same two-round 20-product /
351-game-object / 40-function / 6210-byte checks.

## Next bounded work

Continue MAIN first and do not restrict the frontier to tiny leaves. Vector
math, exit, explosion-collision, fireballs, and the complete multi-segment
bullet.cpp gameplay owner are now closed. Continue directly into the next large
gameplay source owner: e_enemy.cpp contributes multiple code blocks totaling
more than 3 KiB. Rebuild its segment/data dependency map from the TH03 target
first, use TH04/ReC98 only to propose semantics, and take complete owner extents
rather than retreating to another small leaf.

After the input/math frontier, proceed into timing/state update and then
two-player dispatch/game-object logic. Determine packed/decoded ownership for
OP/MAINL/ZUN before treating their storage inventories as game functions.
MAIN has 1553 MZ relocations; the other three containers have zero. This is
observed structure, not proof of packer identity. Keep replaying the entire
accepted MAIN aggregate after every new owner, and investigate OMF identity
drift separately without changing the imported calibration hashes.
