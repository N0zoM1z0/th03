# Complete OP entry carrier review

Frozen reference: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
The Japanese YUMEZIKU target remains `candidate-local-attested`; independent
pristine-dump attestation is unknown. Canonical OP is packed DIET. The guarded
restoration is a separate decoded namespace, never a replacement stored target.

The entire original `th03/op_01.cpp` CODE carrier at `0990:0008..0C1E` is3094
bytes in15 complete functions. It contains previous configuration271 bytes,
maintained menu1338 bytes and new1485 bytes: story390, VS drawing66, VS365,
demo202, wait105, score94 and far startup263. The new bytes are two disjoint
unit extents (`0117..05DD`1222 and `0B17..0C1E`263); the menu interval is never
credited twice. Native IRAND42 and compiler SCOPY28 are reviewed context,
without new maintained source credit.

Receipt: `.analysis/sol-op-entry-review-20261006.json`; SHA-256
`7c39a8f7ca07aa3ac1093aa8207e80410e650aa3d14ab5757a8cb2e59640613c`; 180 guarded inputs.

Original and two previous cold images each pass2236 cases with all1037 native
instruction positions exercised across the carrier and two helpers. Complete
raw bytes and original ordered relocation observations agree unchanged for
all17 bodies. The original carrier MAP, normalized TC86 Borland C++4.02 OMF,
frozen providers, original scalar data and previous declared menu overlay are
bound. Ghidra attests the canonical packed database; automatic functions and
decoded compiler equality remain diagnostic evidence.

## Maintained source and compiler

Receipt: `.analysis/th03-op-entry/sol-op-entry-source-20261006/receipt.json`; SHA-256
`8bb73e41c37e0f8d20d0f5b03fa83076827ef36d1d522cf7625ca21659c810e7`; 197 guarded inputs.

`src/op/entry.cpp` replaces the original private entry TU using explicit
`compat/rec98/` forwarding for19 reference imports. Its original CODE group,
near/far/Pascal types, global/static data order, packing and inline handoff
remain natural source. `menu_state.inl` retains its previous independent unit;
its enums and `choice_tram_y()` context are now in the maintained entry TU.
The source removes the upstream all2^32-seed termination/unreachable retry
claims; no behavioral repair is made. Reference headers and linked libraries
remain candidate dependencies, without inherited ownership or exactness.

Two new frozen archives independently compile the full entry TU and previous
2647 score/title/menu source bytes. Each OP reruns2236 entry cases,4160 previous
menu cases and96 title cases. Previous543 score/helper bytes are checked raw
and in original relocation order; the old1168-call score proof is not a new
rerun. Twenty products and350 game object hashes agree across both rounds;
all416 normalized OMF outputs are recorded. The whole OP retains its six raw
byte inequalities and original relocation-order failure. Canonical packaging,
startup CRT, linked heap/devices/resources and whole-product Oracles are open.

The earlier three configuration units become source-present in this TU;271
bytes were already reviewed and add no new coverage. New1485 source bytes plus
those271 bytes bring OP source-present decoded bytes from2647 to4403 in three
C++ TUs and three bounded includes. Sixteen OP units include10 source-present
extents and six other candidates337 bytes; reviewed coverage is4740. OP exact
remains0. MAIN, MAINL and ZUN acceptance is unchanged.

## Native contracts and limits

An independent scalar state model compares native entry counts, ordered stores,
API arguments/text/file events, explicit external fixture writes and the whole
1MiB map outside the64KiB stack. Native menu drawing and selection, configuration,
LCG and compiler copy bodies execute. Near/far return frames, C caller cleanup,
Pascal callee cleanup, saved BP/SI/DI/DS, SS aliases and instruction boundaries
are checked. The complete existing switch tables remain data and every target
is a real instruction boundary. `_main` returns far; its CRT caller is unreviewed.

File/text/sound/selection/animation/init/keyboard/exec APIs are finite reply
fixtures. The resident is ordinary mapped memory, including unaligned offsets
and invalid diagnostic fields, with no claim to valid DOS allocation or physical
VRAM behavior. The initial CFG read uses real native caller frames; native SCOPY
clears DF for the eight-byte exit save. Ordinary four-byte save defines only
its first three bytes. Byte3 is uninitialized stack storage: the full actual
file bytes are retained and compared between images, without a scalar value
assertion. Other physical memory changes remain fully checked.

Ten negative/control tests exercise reentry, timeout/returning exec, VS cancel,
startup held input, native store changes, call operands, far SS aliases, demo
byte wrap, ordinary undefined CFG byte and original palette/skill behavior.
Initial incomplete coverage diagnostics were retained; missing option cases
were added before the complete passing review.

## Observations

- Story initializes CPU flags, story stage/lives and mode before character
  selection. A nonzero low-byte selection reply returns1 without launch. The
  LCG seed is copied from the resident and six distinct opponents from0..6 are
  chosen excluding the stage7 table choice. Palette equality swaps, fixed last
  opponents,16 score-byte clears, credits3 and byte skill70+rank*25 are preserved.
  Eighteen palette values/four seed values/three ranks under four IF/DF combinations
  are checked; this is not an exhaustive all2^32-seed proof.
- `opponent_seen` is a seven-byte static array and is not reset. After one
  successful selection and a returning exec reply, a second story call fails
  to terminate within10000 instructions because all available choices are
  marked or excluded. The same original/cold failure is retained. It establishes
  behavior of this fixture, without a physical process-lifetime or liveness Oracle.
- VS immediately processes the first held input because previous input starts0.
  Cancel is ignored in this menu; only shot/OK accepts, after up then down.
  Modes128..255 bypass the menu using mode-128. Selection failure sets mode0
  and returns1; success clears scores and performs the common handoff.
- Demo increments the byte counter before its upper-limit check. Counter255
  wraps to0, so native data reads reach bytes before the intended pairing/seed
  arrays. Valid counters use the original pairings and600/1000/3200/500 seeds.
  This is a diagnostic invalid-state observation, not valid C++ array indexing.
- Waiting clears input, polls, increments the resident DWORD and signed frame
  counter, then checks frame>520 before delaying. If exec returns, polling
  continues; a key arriving at frame522 still triggers a second demo call.
  Fourteen column/sprite callbacks at176..280 follow the first left sprite.
  Column bodies retain their earlier raw failure and attempt-only hardware model.
- Score sets stageFF/show-score1/mode0, clears16 score bytes and frees the sprite
  library during handoff. Handoff order is cfg-save, gaiji restore, song stop,
  optional sprite free, game exit, C `execl` with two filename pointers/null.
  A returned exec result is ignored; story/VS/score return low-byte0.
- Startup creates the resident-palette object before checking the GDC zoom word.
  The zoom-error path prints three messages/gets a key/returns; init failure
  prints one error/gets a key/returns. Neither path reaches normal cleanup.
  Successful startup loads gaiji/CFG, can resume VS, chooses intro/fade, waits,
  sets input0 and calls the main menu before loading character part2. Thus the
  initial held input can be processed immediately on the first poll. The loop
  dispatches main/option, advances the DWORD seed and delays; exit uses cfg-exit,
  gaiji restore, text clear, DOS exit helper then palette free. Actual DOS child
  execution, resource lifetime, IRQ timing and device behavior remain unproved.

Next: full character-selection and Music Room carriers, then root/header/DATA/
BSS/library/resource ownership and canonical packaging/complete Oracles. The
505-file intake goal remains open.

Full verification: `.analysis/sol-op-entry-complete-ci-20261006.log`, SHA-256
`2c416556f580e50dcc6ac7690f819df6a971d167d4ab2bc82013f38e6be84626`, passes472 tests and all available private headless gates. Current
worktree/staged whitespace checks and all197 compiler/9 coverage input guards
pass. The final verification journal adds one evidence row after that CI run.
