# OP and MAINL decoded source-coordinate review

This is a diagnostic review of the frozen direct-link queue and three bounded
MAINL functions. It adds no maintained source or exact owner. The selected stored
Ghidra databases were re-attested before this review; their packed functions were
not used as game-code observations. Canonical targets remain unchanged.

## Lineage and replay

The decoded inputs are the complete, hash-pinned outputs of
`sol-diet-restoration-20261006-b`. Their restoration receipts bind the stored
targets to the derived images. The compiler inputs are OP/MAINL products and
detailed MAPs from both rounds of `sol-main-randring-probe-20261006`. This is the
full scaffold with maintained MAIN overlays, not an unmodified reference or
authored OP/MAINL build. Source membership and source hashes come from the frozen
ReC98 revision in `config/th03_decoded_code_review.toml`.

```sh
python3 scripts/review_th03_decoded_code.py --output .analysis/decoded-code-review.json
```

The script pins the cold and restoration receipts, verifies canonical target and
decoded identities, requires every direct-link source in the detailed CODE MAP,
rejects overlapping/out-of-image contributions and straddling relocation words,
compares unmodified bytes and the original ordered relocation records, and checks
both cold rounds. The three manually reviewed functions additionally require
the candidate public entry, carrier containment, complete decoding and reviewed
return. Seven synthetic failure controls cover malformed/overlapping MAP rows,
bounds, relocation ordering, unmasked relocated words, and incomplete/wrong-return
function decoding. Repeated diagnostic output is identical.

A matching slice at a compiler coordinate does not establish target ownership.
Zero-sized CODE declarations get no byte or source credit. Neither raw nor
relocation equality here proves DATA/BSS, linkage, packing, runtime behavior or
the complete Oracle set. Generated roots and shared code remain separately scoped.

## Direct-link diagnostics

All counts below describe candidate coordinates. The detailed ignored evidence is
`.analysis/sol-decoded-code-20261006.json`, which retains every CODE contribution,
including compiler/library modules, and each original relocation sequence.

| Product | Direct files | Nonempty files with matching slices and ordered relocations | Nonempty CODE contributions | Different program bytes | Different CODE slice bytes |
|---|---:|---:|---:|---:|---:|
| OP | 27 | 13 | 100 | 4867 | 4865 |
| MAINL | 33 | 28 | 108 | 340 | 339 |

OP has a 4096-byte decoded target header and a 3584-byte candidate header. Both
program images are 59770 bytes. MAINL has 4096-byte headers and 63276-byte
program images on both sides. Comparing program images here only locates
differences: full-file equality still fails for both products.

The table lists every direct file. `same` means all nonempty candidate CODE
contributions have matching raw slices and ordered relocation records. `empty`
means no nonempty CODE contribution; neither result grants acceptance.

| Product | Direct file | Nonempty candidate CODE bytes | Differing slice bytes | Ordered relocations | Diagnostic |
|---|---|---:|---:|---|---|
| OP | `th01/vplanset.cpp` | 41 | 0 | same | same |
| OP | `th02/exit_dos.cpp` | 25 | 0 | same | same |
| OP | `th02/frmdely1.cpp` | 21 | 0 | same | same |
| OP | `th02/frmdely2.cpp` | 21 | 21 | same | differs |
| OP | `th02/snd_load.cpp` | 112 | 0 | same | same |
| OP | `th02/snd_mode.c` | 30 | 0 | same | same |
| OP | `th02/snd_pmdr.c` | 58 | 0 | same | same |
| OP | `th03/cdg_load.cpp` | 593 | 562 | differs | differs |
| OP | `th03/cdg_p_na.asm` | 114 | 112 | same | differs |
| OP | `th03/cdg_put.asm` | 382 | 0 | same | same |
| OP | `th03/exit.cpp` | 67 | 0 | same | same |
| OP | `th03/grppsafx.cpp` | 613 | 603 | differs | differs |
| OP | `th03/hfliplut.asm` | 30 | 29 | same | differs |
| OP | `th03/initop.cpp` | 105 | 94 | differs | differs |
| OP | `th03/inp_m_w.cpp` | 367 | 355 | differs | differs |
| OP | `th03/input_s.cpp` | 417 | 0 | same | same |
| OP | `th03/op_01.cpp` | 3094 | 14 | same | differs |
| OP | `th03/op_02.cpp` | 165 | 0 | same | same |
| OP | `th03/op_main.cpp` | 902 | 19 | same | differs |
| OP | `th03/op_music.cpp` | 2244 | 16 | same | differs |
| OP | `th03/op_sel.cpp` | 3013 | 28 | differs | differs |
| OP | `th03/pi_load.cpp` | 70 | 67 | differs | differs |
| OP | `th03/pi_put.cpp` | 173 | 168 | differs | differs |
| OP | `th03/polar.cpp` | 26 | 0 | same | same |
| OP | `th03/scoredat.cpp` | 229 | 0 | same | same |
| OP | `th03/snd_kaja.cpp` | 30 | 30 | same | differs |
| OP | `th03_op.asm` | 11730 | 0 | same | same |
| MAINL | `th01/vplanset.cpp` | 41 | 0 | same | same |
| MAINL | `th02/frmdely1.cpp` | 21 | 0 | same | same |
| MAINL | `th02/snd_dlyv.c` | 28 | 0 | same | same |
| MAINL | `th02/snd_load.cpp` | 112 | 0 | same | same |
| MAINL | `th02/snd_mode.c` | 30 | 0 | same | same |
| MAINL | `th02/snd_pmdr.c` | 58 | 0 | same | same |
| MAINL | `th02/snd_se_r.cpp` | 12 | 0 | same | same |
| MAINL | `th03/cdg_load.cpp` | 593 | 0 | same | same |
| MAINL | `th03/cdg_p_na.asm` | 114 | 0 | same | same |
| MAINL | `th03/cdg_put.asm` | 382 | 0 | same | same |
| MAINL | `th03/cfg_lres.cpp` | 49 | 0 | same | same |
| MAINL | `th03/cutscene.cpp` | 3195 | 3 | same | differs |
| MAINL | `th03/exit.cpp` | 67 | 0 | same | same |
| MAINL | `th03/exitmain.cpp` | 40 | 0 | same | same |
| MAINL | `th03/grppsafx.cpp` | 613 | 0 | same | same |
| MAINL | `th03/hfliplut.asm` | 30 | 0 | same | same |
| MAINL | `th03/initmain.cpp` | 62 | 0 | same | same |
| MAINL | `th03/inp_m_w.cpp` | 367 | 0 | same | same |
| MAINL | `th03/inp_wait.cpp` | 126 | 0 | same | same |
| MAINL | `th03/input_s.cpp` | 417 | 0 | same | same |
| MAINL | `th03/mainl_sc.cpp` | 338 | 0 | same | same |
| MAINL | `th03/pi_load.cpp` | 70 | 0 | same | same |
| MAINL | `th03/pi_put.cpp` | 173 | 168 | differs | differs |
| MAINL | `th03/pi_put_i.cpp` | 135 | 132 | differs | differs |
| MAINL | `th03/pi_put_q.cpp` | 177 | 0 | same | same |
| MAINL | `th03/regist.cpp` | 2720 | 6 | same | differs |
| MAINL | `th03/scoredat.cpp` | 229 | 0 | same | same |
| MAINL | `th03/snd_dlym.cpp` | 49 | 0 | same | same |
| MAINL | `th03/snd_kaja.cpp` | 30 | 0 | same | same |
| MAINL | `th03/snd_se.cpp` | 120 | 0 | same | same |
| MAINL | `th03/staff.cpp` | 76 | 0 | same | same |
| MAINL | `th03/vector.cpp` | 160 | 0 | same | same |
| MAINL | `th03_mainl.asm` | 17119 | 30 | differs | differs |

## Three complete MAINL functions

The manual decoded-body review covers the following complete functions, with
no producer padding or data bytes credited. Their CODE bytes and region-local
ordered relocation records match both frozen compiler rounds.

| Function | Decoded CS:IP | Body bytes | MZ relocation words | Return |
|---|---|---:|---:|---|
| cfg_load_resident_ptr | 095F:0003 | 49 | 3 | near RET |
| win_load | 095F:0034 | 282 | 11 | near RET |
| win_text_put | 095F:014E | 56 | 3 | near RET |

The CFG carrier is `th03/cfg_lres.cpp`, including
`th03/formats/cfg_lres.cpp`; both screen functions belong to
`th03/mainl_sc.cpp`, including `th03/mainl/screens.cpp`. Their complete 49- and
338-byte contributions partition exactly into these functions. Candidate source
hashes, target/candidate body hashes and complete disassembly are in the receipt.
Addresses are in the decoded namespace. Unit rows deliberately have no canonical
stored-file offset or maintained source path.

`cfg_load_resident_ptr` uses ENTER 8 and saves SI. It opens the DGROUP filename at
035A, reads eight bytes into SS:BP-8, closes the file, extracts the segment word
at BP-3 (configuration offset 5), writes it to resident segment 21EC, writes zero
to resident offset 21EA, returns the segment in AX, restores SI/BP and uses RET.
The frozen GAME=3 cfg_options_t has five packed bytes; cfg_t then adds the
two-byte segment pointer and one debug byte. The library calls are far Pascal;
the function does not test open/read errors or initialize a failed-read buffer.
The GAME=5 DOS branch in cfg_impl.hpp is not part of this body.

`win_load` uses ENTER 2, keeping the scalar packed character byte at BP-1 and
message byte at BP-2. It loads palette/logo resources, selects the winner using
resident byte offset 17, and tests story-stage byte offset 33 only for winner 0.
Stages 6 and 7 choose messages 9 and 10; other paths use the losing character
ID. Character ID is the zero-extended packed byte divided by two, and palette
ID is bit 0. It loads CDG slot 6, opens the selected far message filename, seeks
to message_id * 180 with a 32-bit position, reads three 60-byte lines at DGROUP
133C/1379/13B6, terminates them at 1378/13B5/13F2, closes and returns near.
The declared 183-byte win_text, two character bytes at 13F3/13F4 and bool at
13F5 explain the candidate 186-byte BSS contribution; this is layout corroboration,
not file-backed BSS equality. No filename/resource contents were imported.

`win_text_put` saves BP and calls graph_putsa_fx three times with 16-bit
coordinates x=80, y=272/288/304, attribute 002F and the three far DS:offset
line pointers. The 386 operand-size PUSH pairs real word arguments; preserve
their order and the far Pascal cleanup when maintaining the source. RET ends
the complete 56-byte function. No gameplay or device-runtime proof is claimed.

## Concrete failures and remaining scope

The target byte immediately after MAINL input_s at decoded program offset CD09
is NOP, while the candidate starts pi_put there with PUSH BP. Thus the candidate
pi_put and pi_put_i slices differ substantially at those coordinates. This is a
boundary/alignment observation; it does not prove either complete function wrong
or authorize an inserted padding byte. Establish target boundaries and the natural
producer before changing source. MAINL generated STAFF_TEXT has identical 348
bytes but a different original relocation sequence, independently preventing
acceptance of that region. OP has additional shared-code shifts and source-local
differences; the receipt preserves the first differing byte for each candidate
contribution without searching for an equality-maximizing alignment.

None of these comparisons resolves stored packing/stub ownership, the full product
graph, external data, library provenance, unlinked files, assets, headers or
conditional branches. The 504-file conservative intake and 69 accepted/boundary
review paths keep their previous scoped counts. Continue actual source/target
review rather than promoting these diagnostic matches to accepted owners.
