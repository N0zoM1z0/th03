# Complete shared input and timing carriers

Four complete natural CPP translation units contain 535 CODE bytes. Shared
input modes and frame delay account for 388 bytes; OP's second frame helper
adds 21 and MAINL's confirmation/measure waits add 126. OP independently owns
409 bytes and MAINL 514. This is bounded source presence, with source and exact
acceptance still false. The 505-file intake remains open.

| Original carrier | Maintained source | OP decoded 0BEB | MAINL decoded 0C7E | CODE |
| --- | --- | --- | --- | ---: |
| `th03/inp_m_w.cpp` | `src/shared/hardware/input_modes.cpp` | 0AD6 | 0DC2 | 367 |
| `th02/frmdely1.cpp` | `src/shared/hardware/frame_delay.cpp` | 02EE | 0372 | 21 |
| `th02/frmdely2.cpp` | `src/op/hardware/frame_delay_2.cpp` | 0CD6 | absent | 21 |
| `th03/inp_wait.cpp` | `src/mainl/hardware/input_wait.cpp` | absent | 0C4D | 126 |

Each CPP imports dependencies through declared `compat/rec98/` forwarders.
The new measure header is a pure forwarding include, not authored header or
sound-driver progress. Existing input/frame declarations remain forwarding
boundaries. Shared ownership follows independent OP and MAINL observations;
TH02 names and existing MAIN source do not establish TH03 exactness.

The frozen keyboard implementation ends with `#pragma codestring "\x90"`.
It is not migrated. Its native function is 417 bytes / 115 instructions at
OP0304 and MAINL0388, in a 418-byte CODE carrier. The trailing NOP, the scanner,
and BIOS declarations remain unowned by this migration. Original zero-distance
jump and the native two-sample scanner execute as context. No injected byte
array, padding or fake ABI is used to manufacture equality.

## Evidence and producer ownership

Selected original packed Japanese Ghidra databases were reattested before
review. Provenance remains candidate-local-attested; independent pristine dump
attestation is unknown. Diagnostic decoded images have their existing guarded
DIET restoration lineage and do not supply canonical packed-file offsets.

Diagnostic receipt:
`.analysis/sol-shared-input-review-20261006-b.json`, SHA256
`b745faf78395381ef239d3a0992a2c7d2167b9d372894d2e3930abc1d0e0c97e`,
723 guarded inputs. Eighteen frozen wrapper/implementation/header/root/link
providers bind both prior PI cold trees. Those current trees use the original
input implementations; older MAIN-remapped cached observations in
`MAINL_INPUT_REVIEW.md` remain historical. The only current link substitution
is the already recorded MAINL vector ASM carrier.

Manifest: `config/th03_shared_input_candidate.toml`. Physical producer
associations remain GAME2/large/O for `obj/th02/frmdely1.obj` and
`frmdely2.obj`, GAME3/large/O for `obj/th03/inp_m_w.obj`, GAME3/large/L
for `obj/th03/inp_wait.obj`, at original link ordinals. CODE SEGDEF records
are respectively `281500020301`, `281500020301`, `286f01020301`, and
`287e00020301`; each has empty DATA `480000040501` and BSS `480000060701`.
These complete producer facts do not settle referenced DGROUP ownership.

Both source rounds passed. Receipt:
`.analysis/th03-shared-input/sol-shared-input-source-20261006-b/receipt.json`,
SHA256 `37d956f61667d1ba35589989286aaa54d55b9cc8ee121743c0d70dd63d32cbeb`,
733 guarded inputs. Nine Research nongame differences are recorded per round.

Source replay compares complete original nondependency TC86 records in their
original order, with dependency-file/time records separately reported. It
checks complete CODE raw equality, original unsorted MZ carrier relocations,
MAP contribution ownership, every input/frame function public and every bound
input/joystick/sound/counter DATA public. The current link graph remains
unchanged. All 20 product hashes and 351 game object hashes must match across
two fresh rounds; all 417 OMF objects are recorded. The 347 other game objects
must equal the parent PI proof, as must all 20 products. Nongame Research
object changes are separately reported and do not receive determinism credit.

The first full compiler run completed, but a post-build validator used
`-nth03/`/`-nth02/` instead of `-nobj/th03/`/`-nobj/th02/` and rejected its
compiler association. Original replay snapshot and both transcripts remain at
`.analysis/sol-shared-input-first-validator-failure-20261006/`. Successful
replacement cold rounds alone receive source credit. Failed-output cleanup
preserves those records and all retained input states. Cleanup removes2555files
/31,309,403bytes (29.9MiB), with all2052retained private input states unchanged.
Receipt `.analysis/sol-shared-input-temporary-cleanup-20261006.json`, SHA256
`00b3678c714438b6d5486d19602c3a8fc707eb387a3db07fdde2ece595858b96`.

## Native contracts and boundaries

Each target and each prior/source cold image executes the same matrix:
OP268 calls / 264 returns / 4 prefixes, all278 instruction positions; MAINL275
calls / 262 returns / 13 prefixes, all321 positions. Owned positions are
163/206; the scanner's115 positions are contextual. OP has2117 ordered native
DGROUP stores and72 joystick/driver events, MAINL2569 stores and147 events.

Terminal cases compare complete 64KiB DGROUP to an independent scalar result,
not only named outputs. Full physical1MiB outside64KiB caller stack is guarded
with declared BIOS sample-bank writes. Native writes outside owned input,
joystick and counter words or caller stack fail. Ordered native writes and
modeled device events compare target/source exactly; reset order is separately
controlled. Caller stack locals and complete prefix register equivalence are
not claimed. Native far frames, return CS, Pascal cleanup0/2/4, preserved
BP/SI/DI/DS and incoming IF/DF are checked for returns.

The host supplies explicit fixtures for BIOS key bytes, `js_sense`, INT60/61
music replies, and polling-time counter updates. No native joystick, music
ISR, VSYNC ISR/PIC or physical614.4-microsecond timing is accepted. IRQ counter
updates are host scheduling, not an interrupt-delivery Oracle. Both frame
helpers are actual native loops, including the stalled-counter prefixes.

Observed behaviors:

- The scanner clears P1, P2, interface and joystick words in that order. It
  combines two BIOS samples separated by1024 OUT5F byte writes, so a key in
  either sample is retained. All used and unused bits in sampled groups,
  first/second-only inputs and combined presses are exercised.
- Joystick-versus-key and key-versus-joystick overwrite selected player
  state. CPU and attract modes merge and clear player/interface states as
  observed; nonzero `js_bexist` controls sensing.
- Change wait first waits for release, even when its signed timeout is
  negative. Zero becomes9999 and both values reset the waited counter, so a
  press-free schedule does not terminate. Prefix observations are bounded
  execution only.
- Frame delay compares its signed `int` argument with an unsigned counter
  using JB. High-bit and negative arguments behave as large unsigned counts.
  Both helpers reset the same `vsync_Count1`, including the helper named `_2`.
- Confirmation wait executes its first sense even for zero frames. Sound-off
  measure wait delegates to it. Sound-on selects INT60/61, using DX00C0 for
  MMD, but native scanning clobbers AX with keyboard P1 before the unsigned
  measure comparison. The returned song measure is not the compared value.

Twelve controls cover independent DATA/call bindings, branch-into-operand and
far-cleanup mutations, second-only held keys/reset order, shortened sampling
loop rejection, mode overwrite/merge, release-before-negative timeout,
zero/9999 prefixes, stalled clocks, unsigned high-bit waits, measure AX
clobber, extra physical byte rejection and complete native coverage.

## Remaining acceptance

Twelve existing MAINL rows, including `decoded-linked-tail-delay`, are upgraded
without adding interval credit. Eleven OP functions add409 reviewed bytes.
MAIN owners/manifests and accepted aggregate remain unchanged. Full OP6-byte
and MAINL21-byte inequalities and whole original relocation-order failures
remain. No whole-product, canonical packing, scanner NOP, header/DGROUP,
native device/IRQ/timing, dependency or complete Oracle acceptance follows.

```sh
python3 scripts/review_th03_shared_input.py --output .analysis/NEW_SHARED_INPUT.json
python3 -m unittest discover -s tests -p test_shared_input_review.py -v
python3 scripts/replay_th03_shared_input.py --run-id NEW_SHARED_INPUT
```

Full CI: `.analysis/sol-shared-input-complete-ci-20261006.log`, SHA256
`50c7f30a507f3d3570176ce8b9d8a61fc750ba4bd8bca3259dc8003861c438af`;593tests/54.348seconds and all available private headless gates
pass. Current coverage uses both source cold MAPs, with zero overlaps:
OP12386reviewed/55262bytes (42876gaps), MAINL28381/58340 (29959gaps). MAINL
interval union is preserved. Receipt
`.analysis/sol-current-decoded-coverage-after-shared-input-20261006.json`,
SHA256 `efdd19c333d0d41ccb8a46d3297de7816cade5cd632a2ff64d26e6deb6209f8b`,
748 guarded inputs.
