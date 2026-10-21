# MAINL graphics: natural TC4 producer

Three complete maintained candidate functions cover 355 decoded CODE bytes:
CDG upward-motion restoration123, clear-blue21, and CDG dissolve211.
They are compiled source candidates, not installed in the default carrier.
Source/exact totals stay unchanged pending source-level product integration.

The retained v03 TC4 compilation succeeded with native exit0 and certain owned
cleanup. Its unmodified853-byte OMF has a byte-aligned MAINL_03_TEXT contribution
of355 bytes, public starts0/123/144, empty DATA/BSS, and explicit near Pascal
RET6/RET8 contracts. All333 non-fixup bytes equal the corresponding decoded target
bodies. Clear-blue's entire21 bytes already equal the target. The remaining22
bytes are nine genuine symbolic external fixup fields: four CDG metadata
references, two alpha flags, one pattern pointer and two far calls. No target
address is injected into a source, object or linked image. Full linked raw body
and ordered MZ relocation equality remain unproved.

The20 previously differing CODE bytes are a natural compiler-inline-assembler
versus standalone-TASM encoding distinction. The same symbolic MOV/SUB/ADD/XOR
instructions produce the target direction-bit form under TC4 inline assembly.
Symbolic AND SI,3 also naturally emits a16-bit immediate, eliminating the
frozen dissolve include's raw-opcode DB workaround. The first probe established
this mechanism; the second full-function probe exposed two AX temporary
expansions. Explicit assignment to DX/BX followed by register shifts produces
the correct final sizes without padding, opcode arrays or OMF rewriting.

Behavior intentionally preserves signed center division, truncated whole-word
width, incoming direction flag, three unput rows, modulo-eight dissolve
strength and the zero-width LOOP underflow. No clipping or new guard is added.
The near/Pascal unput ABI is explicit rather than copying the underspecified
reference header. A16-byte CDG record is asserted; assets and storage remain
external. Existing transitions/snow reviews explain the original runtime
quirks; this checkpoint does not newly claim physical PC-98 behavior.

Evidence is `.analysis/mainl-graphics-encoding-probe-20261021-v03/` and
`.analysis/mainl-graphics-encoding-output-20261021-v03/`. The unmodified object
is `.analysis/toolchain/wineprefix/drive_c/MGE03/probe.obj`, SHA256
`dbfe67ef668954fab6fadad72b776c8d8a6ed9861817d5d7ec2e42c155abd47b`.
The earlier v01/v02 probes remain preserved. Replay:

    python3 scripts/replay_th03_mainl_graphics_producer.py
    python3 -m unittest discover -s tests -p test_mainl_graphics_producer.py

`config/th03_mainl_graphics_producer.json` records consumed source/flags and
symbolic storage aliases. The recipe and native manifest, source, runner, launch arguments, completion,
finish, compiler log and registry transition are hash-bound. The source-to-native
check permits only LF-to-CRLF
materialization. The replay validates OMF checksums, all three public extents,
ordered explicit external fixup fields/addends and source consumption. It
reports non-fixup equality separately; it does not silently normalize fixups.

Next integration must preserve existing MAINL_03_TEXT order: unput+clear,
snow, dissolve, transitions/staff. Public byte-aligned segment concatenation
from source-level TUs is legitimate; object record surgery is not. A complete
3339-byte maintained staff/snow producer is still open. No packed mapping,
cold-aggregate, default-link or whole-product credit is granted.

Separately, target DATA0E3F:0849 is90 where the current carrier has00. The frozen
vsync data include ends with genuine EVEN; its companion source names TASM3.0
and OPTASM1.6. An older assembler alignment policy is only a hypothesis.
This checkpoint leaves that byte untouched, with no guessed DB90 fill.
