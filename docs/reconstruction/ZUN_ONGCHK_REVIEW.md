# Complete ZUN -1 ONGCHK binary intake review

Frozen ReC98 supplies `libs/kaja/ongchk.com` as a binary input, without an
ONGCHK translation unit. All 926 bytes equal the TH03 decoded -1 payload.
This review covers the complete stored code/data partition, direct control
flow, PSP parsing, detector contracts, RAM transfers and polling paths.
It grants no maintained source, compiler observation or exact credit. The
binary remains private; neither it nor instruction arrays are imported.

```sh
python3 scripts/review_th03_ongchk.py --output .analysis/NEW_ONGCHK_REVIEW.json
python3 -m unittest discover -s tests -p test_ongchk_review.py -v
```

The reviewed receipt is `.analysis/sol-ongchk-review-20261006.json`. It guards
the Japanese canonical stored target, DIET restoration receipt, decoded image,
frozen binary and analysis scripts before and after execution. Ghidra's check
could not run in the current sandbox; no database observation is used.

## Identity, partition and shared tails

Frozen revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Full binary SHA-256:
`4f9a9451f19bdd8d3ea8949a5ea75df6c2f92a9a84dcf39e1d7cf13421acc8a0`.
Equality is a local binary intake association, not independent pristine
attestation or upstream authored-source acceptance.

The outer decoded file interval is `0226–05C3`, outer runtime start `0326`.
After copying, execution starts at `CS:0100`. All following addresses are
inner COM addresses. Canonical packed-file coordinates remain unproved and
are absent from the unit ledger.

| Inner start | Bytes | Analysis region | Terminal |
| --- | ---: | --- | --- |
| `0100` | 39 | Startup and DOS exit | INT 21h |
| `0127` | 121 | Detection/RAM controller | Near RET |
| `01A0` | 167 | Result-class 3 detector | JMP to shared success |
| `0247` | 123 | Result-class 2 detector | JMP to its retry loop |
| `02C2` | 27 | Shared success and port-word stores | Near RET |
| `02DD` | 7 | Shared failure and result reset | Near RET |
| `02E4` | 23 | RAM controller | Near RET |
| `02FB` | 173 | Test-data writer | Near RET, early timeout RET |
| `03A8` | 128 | Test-data reader | Near RET |
| `0428` | 33 | Dummy reader | Near RET |
| `0449` | 12 | 32-byte comparison | Near RET |
| `0455` | 39 | Register/value writer | Near RET |

These twelve contiguous regions cover 892 bytes and 390 instructions. Direct
edges must reach decoded instruction boundaries; CALLs must reach the nine
reviewed call entries. The success/failure tails are shared by both detectors
and the controller's fallback path. They are **not twelve independently owned
functions**. In particular, fallback JMPs reach their RET without executing
the controller's `CLC` at `019E`: no-device result 0 retains CF=1, while
successful fallback result 1 has CF=0. Startup requests DOS exit with the result
byte and does not branch on CF.

Initialized data `047C–049D` accounts for the remaining 34 bytes: a 32-byte
ASCII ADPCM RAM check string, port override `049C=FF`, and result `049D=00`.
Mutable locations `049E–04C7` are outside the stored binary: four port words,
ROM flag, priority byte and 32-byte read buffer. Their roles are derived from
the instructions. Calling them compiler BSS or assigning a source producer
would be inference without an OMF/MAP/source record. The analysis never
disassembles the initialized string or treats this workspace as stored bytes.

## PSP parser and detector contracts

Startup executes CLD, sets DS/ES to CS, initializes priority to zero and loads
SI with `0080`, the PSP **tail length** address. LODSB skips `20h` bytes and
sets priority only when the next byte is `38h`. This does not implement a
normal text scan from `0081`. Constructed standard PSP tails establish:

- Empty tail and one-character `8` keep priority 0.
- Any 56-character tail sets priority 1, even if its text contains no `8`.
- A 32-character tail first skips its length byte, then actual leading spaces;
  priority depends on whether its first nonspace text byte is `8`.

No adjustment of SI or parser repair is accepted. The wrapper separately
rewrites the PSP tail length after removing the selected option; it supplies
no special ONGCHK length-byte format. The current probe starts at the payload
entry with a constructed PSP, rather than running the wrapper and payload
together.

Priority 0 tries class 3, then class 2. Priority 1 tries class 2, then class 3.
Only if both fail does the fallback echo probe run. Detectors set result 3 or
2 before probing; shared failure resets it to 0. Fallback sets result 1 and
tests register `0Bh` with an `AAh` data echo. Default pairs are `0088`, `0188`,
`0288`, `0388`; class 3 starts at `0188` and tries two pairs. An override other
than FF replaces DH and reduces each search to one pair. Success stores base,
base+2, base+4 and base+6 in the four workspace words.
The original initialized override is always FF. Four override cases explicitly
initialize `049C` to 5 in private emulator memory to exercise otherwise unused
branches; this changes constructed program data, not the stored target or
frozen upstream binary. No actual caller that changes this byte is proved.

Both detectors compare the ROM word at `FD80:0002` with `2A27h` and consult
its version word at `0004`. A matching version below 6 rejects class 3;
class 2 instead skips its `A460h` setup and continues. Class 3 requires a
non-FF `A460h` read and probe-data AND equal FF; class 2 accepts probe-data
AND unequal FF. The common base+2 probe expects 01 after writing register FF.
Class 3 success updates `A460h/A66Eh`, uses port `5Fh` delays and writes
`6Eh=1` only when the ROM signature was present. Physical board identities
and device timing are unproved; result-class names describe decoded behavior.

## RAM, ABI and bounded CPU observations

Results 2/3 invoke the RAM controller. Successful full comparison adds two,
yielding 4/5; write timeout or unequal data retains 2/3. Result 1 skips RAM.
The register writer interprets DX as register DH/value DL, preserves AX/BX/DX
and CX, and restores saved FLAGS with PUSHF/POPF around CLI and port writes.
Other transfer/detector paths use unconditional STI. RAM setup resets DS/ES
to CS. All reviewed calls/returns are near, with no Pascal argument cleanup;
complete terminal probes retain the wrapper's SP=`FFFC` selected-option word.

The writer sends all 32 signature bytes through extended register 08. Its
post-write ready-bit loop counts `2710h` (10000) polls before an early STC/RET.
Other busy-bit loops have no counter. Reading performs two dummy data reads,
then 32 STOSB writes to `04A8`, polling ready bit 08 and busy bit 80 without
timeouts. REPE CMPSB compares all 32 bytes and supplies ZF to the controller.

Thirty terminal CPU/model cases cover all result codes 0–5, four default
fallback pairs, class 2/3 pair limits, one-pair override, failed override,
six PSP parser cases, priority fallback, ROM versions 5/6, exact transfers,
last-byte mismatch and bounded write timeout. Four additional executions
stop at an explicit 100000-instruction budget in the reader's pre-transfer
busy, ready and post-ready busy loops, and the register helper's busy loop.
These stops remain nonterminal observations; they are never counted as
successful DOS returns. Static control-flow review independently establishes
that those loops have no software exit counter.

The port model supplies selected detector responses and records actual OUTs.
RAM reads return the bytes that the executed writer supplied, preceded by two
dummy values, with an optional deliberate mismatch. ROM words, PSP, DOS exit
and all port behavior are constructed. Trace hashes, result flags, pair/order
lists, byte counts and buffer hashes are recorded. This provides repeatable
CPU contracts, not actual DOS, sound hardware, bus timing or game runtime.
Seven synthetic tests reject incomplete regions, data/operand edges, unreviewed
CALL entries, indirect edges, callback failures and implicit terminal credit.

## Acceptance limits

Binary intake review closes this bounded ONGCHK input analysis. Source
recovery, ownership, natural compiler/layout producers, fresh cold builds,
actual caller/device/runtime behavior, stored packaging and the complete
Oracle set remain open. The 505-file intake, remaining ZUN CRT/graphics/shared
libraries and OP/MAIN/MAINL dependency/artifact work are still unfinished.
