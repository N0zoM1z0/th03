# Complete ZUN -2 initialization candidate review

All 494 lines of frozen `th02_zuninit.asm` were reviewed: nine complete
procedures, startup, resident interrupt handlers, text drawing, vector/state
data, Japanese messages, installation, uninstallation and all terminal paths.
Both pinned cached scaffold outputs equal the complete 1390-byte TH03 decoded
-2 payload. This closes a bounded candidate review, not source/exact acceptance.
No maintained source, exact function or accepted intake CODE path is added.

```sh
python3 scripts/review_th03_zun_init.py --output .analysis/NEW_INIT_REVIEW.json
python3 -m unittest discover -s tests -p test_zun_init_review.py -v
```

The reviewed receipt is `.analysis/sol-zun-init-review-20261006.json`.
It binds the canonical stored ZUN identity, DIET restoration, full decoded
image, frozen source and both complete cached payloads. All direct edges and
complete procedure decodes are checked. Source labels remain provisional
diagnostics, and the packed Ghidra database contributes no observations.

## Identity and compiler association

Frozen revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
The header's input MD5 `04f7fc8f2c807428042289437780947f` equals the whole
TH03 payload, despite its original TH02 file-name annotation. Full payload
SHA-256 is `27fe52738878c1fa267c5dc82b0d70957d72dca5a6da375620a74d163b61e2d8`.
This is a local upstream-input association, not independent pristine evidence
or inherited cross-game exactness.

The decoded payload starts at outer file `05C4`, outer runtime `06C4`, and
ends at file `0B32`. After the wrapper copies it, it executes at `CS:0100`;
all addresses below use that inner namespace. Canonical stored-file offsets
are deliberately absent from the unit ledger.

The frozen Tupfile explicitly links `th02_zuninit.asm` as a standalone tiny
assembler product and selects it as TH03 option `-2`. The TU uses `.286`,
`.model tiny`, `_TEXT segment use16`, `org 100h`, no source includes and no
external symbols. The source has symbolic instructions, labels and real
string/vector data, with no unexplained interprocedure zero padding or opaque
instruction arrays. The observed `jmp short $+2` at `052E` remains a real
instruction in the candidate; it is not removed to beautify control flow.

The frozen source is Shift-JIS with LF lines. Each pinned cached compiler
source equals **only** its LF-to-CRLF conversion; the script requires that
exact byte transformation and records both hashes. No other whitespace,
source encoding, instruction or target-byte normalization is accepted.
The old whole-scaffold receipt is hash-checked and records equal products.
This gives a cached input/output association; it does not prove a fresh
maintained build. Future UTF-8 maintained source would need an explicit,
reviewed compiler encoding stage to preserve Japanese string bytes.

## Complete boundaries, storage and ABI

| Inner address | Size | Candidate procedure | Reviewed terminal/role |
| --- | ---: | --- | --- |
| `0100` | 3 | `start` | Near JMP to `043A`; startup thunk |
| `0103` | 51 | `sub_103` | IRET; error-message interrupt |
| `0136` | 18 | `sub_136` | IRET; latch state 1, invokes common handler |
| `0148` | 18 | `sub_148` | IRET; latch state 2, invokes common handler |
| `015A` | 150 | `sub_15A` | Near RET; message/key polling and latch reset |
| `01F0` | 18 | `sub_1F0` | Near RET; character-word conversion arithmetic |
| `0202` | 59 | `sub_202` | Near RET; character and attribute writes |
| `0413` | 39 | `sub_413` | Near RET; banner and resident signature check |
| `043A` | 251 | `start_0` | DOS exit/TSR requests; option/install/remove paths |

Bodies account for 607 bytes. Resident data `023D–0412` accounts for 470
bytes; transient strings `0535–066D` account for 313. Together they cover all
1390 bytes. The marker at `023D` is two assembler word literals (`'ZU','NP'`),
whose **actual byte order is `55 5A 50 4E`**, not the source label's spelling.
Three saved far vectors occupy `0241/0245/0249`; byte `024D` is the shared
latch. The error table at `0312` has six near message pointers; AX is doubled
without a recovered bounds check. All messages and their `$` terminators were
reviewed, including retained key/error messages and transient DOS strings.

Startup inherits PSP DS/ES and the wrapper's stack. It scans the tail from
`0081` with LODSB and relies on the wrapper's CLD. An empty tail or first
ordinary non-option word takes the install path. `/R` and `-R` accept either
case and ignore trailing text after the option letter; an absent option letter
or another letter selects the invalid-option message. These are observed
branches, not a repaired parser. Normal non-TSR exits use `AX=4C00h`, including
invalid options and reported free errors.

Detection obtains vector `59h` with DOS function `35h` and compares the marker
at ES:`023D`, independent of the returned BX. Installation saves the previous
`59h`, `06h`, `05h` far vectors and installs `DS:0103`, `DS:0136`, `DS:0148`
through DOS function `25h`. It then computes `(0413h >> 4) + 1 = 42h`
paragraphs and requests TSR termination with `AX=3100h`. With a PSP-relative
origin, this nominal retained boundary is offset `0420`, including all
resident handlers/data and thirteen bytes of the otherwise transient detector.
It does not allocate a separate resident stack; interrupt handlers use the
interrupt caller's stack. Actual DOS ownership/lifetime remains unproved.

Removal restores all three vectors using the detected resident segment's
saved values, saves/restores DS, requests freeing the environment segment at
resident PSP:`002C`, then requests freeing the resident segment itself. Unlike
the reviewed -4 driver, this path preserves the actual saved offsets.

The three far procedures terminate with IRET, not RETF. The common handler
and error handler save flags, AX/BX/CX/DX/DS/DI/ES; untouched SI/BP are retained.
State 1/2 dispatchers suppress processing when latch `024D` is already nonzero.
The common handler draws at byte offsets `0650/06F0/0790`, polls modeled masks
1/2 until release and re-press, clears those message rows, and resets the latch.
The source's inherited IDA `INT 18h` IBM-PC ROM BASIC comments are not PC-98
evidence. This review records the genuine AH/AL requests and register effects;
it does not adopt those comments as BIOS behavior or claim keyboard hardware.

Text output reads two-byte words through CS:BX, stops on a `$` first byte,
applies `01F0` arithmetic, and writes two character words at ES=`A000h` per
source word. It then writes attribute word `0041h` at ES=`A200h`, using the
same character count. CS-relative reads and near-call/IRET stack conventions
must be preserved; DS cannot be assumed to equal the resident CS on interrupt
entry. Direct code has no CLD in these handlers, so inherited DF is part of
the caller contract, still requiring review against actual callers.

## Bounded CPU and modeled interface results

The target and both cached candidates each run eighteen cases (54 observations):
ten DOS-interface cases, seven synthetic interrupt/keyboard cases and one
constructed empty-string text case. Capstone/Unicorn versions, exact inputs,
events, string hashes, vector values, register/frame state and memory hashes
are in the receipt. The script stops at DOS exit/TSR requests or a synthetic
return sentinel. DOS vector/free calls and BIOS return registers are explicit
models; no actual kernel, memory manager, hardware or game execution occurs.

* Installation, already-resident, removal, absent resident, invalid/empty
  option, ordinary text and ignored option suffixes reproduce all observed
  branch results. Removal restores all original offsets and segments before
  requesting environment/resident frees. The wrapper's retained stack word
  remains at SP=`FFFC` at each terminal request.
* Error/state-1/state-2 interrupt frames return with all tested registers,
  SP and saved flags restored. Nonzero latch cases perform no modeled BIOS
  calls and leave the latch unchanged. The constructed keyboard sequences
  exercise both polling loops. This does not establish reentrancy timing.
* With DF set on error/state-1 interrupt entry, direct STOSW writes run
  backward. Text and attribute memory hashes differ from DF-clear cases while
  IRET restores DF. No CLD or invented DF guarantee is added.
* If the modeled environment free fails but resident free succeeds, the
  success message at `05B7` is selected. If resident free fails, the error
  message at `0647` is selected. Both exit with code 0. The first CF result
  is not checked before the second call overwrites it; preserve that behavior.
* A constructed `$`-only string has CX=0 at the attribute loop. DEC wraps it
  to `FFFFh` and the loop performs **65536 word writes** of `0041h`, changing
  the whole 64-KiB modeled attribute segment. No reviewed valid caller is
  currently proved to supply that string. This is an unchecked contract,
  not an observed game failure or a reason to insert a new guard.

Six synthetic tests reject wrong size/terminals, branches into data, calls
into interiors and unexpected indirect edges. A wrong model interrupt is
captured inside the ctypes callback and raised after emulation, with clean
callback stderr. Tests contain no target assets.

## Remaining acceptance work

This payload is boundary-reviewed with no maintained source. Full cached raw
equality is useful but insufficient: fresh frozen compilation, reviewed
compiler input encoding, natural whole-module ownership/layout, caller and
resident ABI, original stored packaging and the complete Oracle set remain
required. MAIN exact counts and the 69 scoped intake CODE paths are unchanged.
Current Wine and Ghidra probes fail under the restricted sandbox; `.git`
remains read-only. The full 505-file review/migration goal is still open.
