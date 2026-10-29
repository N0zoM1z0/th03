# TH03 handoff

## Current state

Natural source recovery and exact native output are the goal. Use the pinned
Japanese targets in `config/targets.toml` (`candidate-local-attested`); never
substitute translated, patched or reference-game binaries. MAINL is the ending.
Read [workflow](RE_WORKFLOW.md),[architecture](ARCHITECTURE.md) and
[detailed notes](RE_NOTES.md) before changing
native recipes. Inspect Git; all dirty work belongs to this reconstruction.

Latest source checkpoint: `8773096` (before codegen and Raise stack flow), after
`baa9ba0` (throw locals and complete dispatcher body). The following cleanup
changes documentation/local disposable state, not product source or acceptance.
Preflight/scoped compiler checks passed in that source session; run preflight
when starting a new session or changing environment/targets. Re-attest Ghidra
before using a database; the fixed decoded MAINL DB is distinct from the old
packed MAINL DB. Decompiler sizes and signatures remain hypotheses.

| Product | Accepted source scope | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions /78,737 CODE bytes /106 extents | Open |
| OP | 60 extents /92 procedures /13,221 CODE +1,764 DATA bytes | Open |
| MAINL | 211 owners /288 procedures or entries /34,333 CODE +2,613 file DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts36,946 bytes:16,695 authored +20,251 library. Its DATA total includes
2,607 initialized bytes and6 genuine uninitialized file-storage bytes. ZUN accepts
8,635 bytes:2,179 authored +1,390 original ASM +5,066 library. Source presence is
250 extents/60,028 gross bytes. These are different measures; whole-game source
and function denominators/completion percentage remain unknown. Old overlapping
cutscene3195/regist2720/root2488 rows must not be counted again.

## Current xx candidate

The maintained `src/mainl/crt/xx.cpp` composes all recovered exception/RTTI banks
in original order. It builds under real module name xx in the normal893-member
library and actual MAINL link. Two native BCC4.5/TASM/TLIB/TLINK rounds repeat
complete raw ASM/OBJ/LIB/EXE/MAP vectors. All892 surrounding member program
records,28 earlier source providers,36 project objects and startup/EMU/MATHL
inputs are retained. Candidate xx is provider29;the accepted28-provider library
and published211 owners remain separate and unchanged.

| Extent | Original | Candidate |
| --- | ---: | ---: |
| Full decoded EXE | 67,372 | 67,340 |
| xx CODE | 12,622 | 12,585 |
| Literal native fields | 187 | 181 |
| Ordered xx MZ words | 20 | 20 |
| xx DATA/BSS | 18/10 | 18/10 |
| RTTI tail | 1,735 | 1,735 |
| Raise frame allocation | 390 | 342 |

Both whole EXEs have4096-byte headers/677 relocation entries;raw EXE/MAP still
differ. Candidate DGROUP0E3D versus original0E3F gives ordinary32-byte file-size
movement. Every candidate CODE byte resolves through the real18 library
interfaces;all22 original public MAP bindings pass. Net length37 is not a count
of differing bytes. No exact credit or DOS boot/ending-playthrough claim follows.

Current useful proofs and remaining differences:

- Complete dispatcher140 linked bytes match in both miniature and normal link.
- Raise count/index/copy block6AC0..6B06 matches all71 raw bytes. Local -O-v
  removes two extra WORD induction pointers;FS/GS writes,the16-bit zero chain,
  direct SS and CX/ES/BX resume-address operations follow native order.
- `typeinfo::before` matches all120 unlinked object bytes. Its one strcmp field
  at+96 retains literal original/current EXTDEF indices8/18. The linked call
  displacement still differs. Scoped -O1 works when -O2-pg/-Os/-O-i/**-Z-** are
  restored afterward;earlier reset trials omitted -Z-.
- BCC explicitly emits the current one-byte RTTI initializer as `db 1 dup (0)`;
  actual nested TASM LIDATA owns it. Do not infer that byte from final-label
  parity after assembler relaxation. Tail length equality is not raw equality.
- The tested Raise context agrees at entry SP=FF00,including flags84h/84h.
  One alternate SP=FF10 exposes original80h/source84h through the real linked
  memcpy twice. The original48-byte region at BP[-134,-86) still has unproved
  type/purpose. Do not invent storage or adjust flags to close it.
- Typed toss cache restores its72-byte frame;body812 versus815 remains.
  Wrapper89/170 lengths agree,not their full raw bodies. Raise is1081 versus1151.
  `dtorCleanup` is1056 versus1035;earlier -O-v experiments matched its length
  only and have not proved the complete body/fields. This is a useful next
  large-function codegen question,alongside the remaining full-TU gaps.

See [normal product review](MAINL_XX_PRODUCT_REVIEW.md),
[RTTI review](MAINL_XX_RTTI_REVIEW.md) and [throw review](MAINL_XX_THROW_REVIEW.md).
Earlier dispatch/destruction/calls/catch/types reviews describe retained smaller
miniatures;their provider counts,CODE sizes and traps are not the current full TU.
Their ABI findings remain useful. NOSMART/single-pass TASM trials did not obtain
exactness and are not adopted. Keep original unchecked DOS behavior;do not import
later Win32/Delphi/CV/friend/specification behavior from reference RTL.

## Verification and retained local state

Rebuild/review affected scope;validate/reuse unchanged pairs. No full cold/DIET
or unchanged ancestor runtime chain is required each turn. Source changes that
actually affect an earlier producer do require refreshing its native binding.
Recent affected checks:throw/full-TU/normal-link native pairs,25 targeted tests,
tracking validation and `git diff --check`. Commit substantial progress as
`gpt-6.1-sol: ...`. Full CI is for broad infrastructure changes.

Use direct headless tools,DISPLAY/WAYLAND_DISPLAY empty,one CPU at nice10 and
one serialized Borland/Wine writer. CPU16 is available here. Native probes use
`.venv/bin/python`,not the system Unicorn installation. Poll the same live
process/session after observation timeouts;never restart a writer solely because
an observation expired.

Preserve `.analysis/toolchain/wineprefix/`,TC4/TASM/JWasm/scoped BC45,`.tools/ghidra`,
`.tools/jdk`,`.venv`,`_reference/ReC98`,fixed targets/assets and `ghidra-project/`.
Keep the current working builds TH03WORK/TH03OP/TH03ML/TH03ZUN. The archive
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar` remains
an actual OP/MAINL source input. Do not delete it because of its historical name.

Under `.analysis/work/`,keep current `*-build.json`/`*-review.json`,their complete
raw pairs,actual transported sources/wrappers,responses/context fixtures and
native phase logs. In particular preserve all current `xx-product-*`,
`xx-rtti-*`,`xx-throw-*` proof inputs plus the earlier reviewed xx baselines and
accepted exception/stdio/path/constructor/loadprog/exec/farheap inputs. A report's
hashes do not list every dynamically named file read by its reviewer.

The accepted MAINL publication SHA is
`de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551`.
All39 current retained binary link inputs and938 cold outputs remain unchanged.
Do not rewrite frozen historical runtime hashes or `scripts/lib/zun.py`'s MAIN
binding. MAIN still has EC2D90 versus00 and MZ header/layout differences despite
1553 agreeing relocation entries. TH04 is an authorized source reference,not a
replacement target or build dependency.

For cleanup,follow [working-file rules](RE_WORKFLOW.md#working-files). Remove
superseded experiments and duplicate staging trees after checking dependencies;
retain documents,ledgers and experiment/verification records while deleting
unused code copies and rebuildable binaries. Generic cleanup preview is not a
complete dependency oracle.
