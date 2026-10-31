# TH03 handoff

## Current state

Natural source recovery and exact native output are the goal. Use the pinned
Japanese targets in `config/targets.toml` (`candidate-local-attested`); never
substitute translated, patched or reference-game binaries. MAINL is the ending.
Read [workflow](RE_WORKFLOW.md),[architecture](ARCHITECTURE.md) and
[detailed notes](RE_NOTES.md) before changing
native recipes. Inspect Git; all dirty work belongs to this reconstruction.

Latest source work recovers the complete1495-byte DOS call-adapter bank and
all88 literal ordered native fields. Four virtual-base SI assignments use
Borland register variables;the complete native prefix now matches2822 bytes
and92 ordered fields. The whole xx member remains unaccepted.
Preflight/scoped compiler checks passed in that source session;run preflight
when starting a new session or changing environment/targets. Re-attest Ghidra
before using a database;the fixed decoded MAINL DB is distinct from the old
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

The maintained `src/mainl/crt/xx.cpp` composes all exception/RTTI banks in original
order. The normal product now uses actual BCC4.5 `-c -y` output,then TLIB/TLINK.
Separate `-S` output supplies mangled names only;it is never assembled into the
product. Native source-file/LINNUM records bind all50 procedure boundaries to
actual transported source definitions. Earlier S/TASM miniatures remain useful
separate diagnostics,with their own codegen and field order.

Two rounds repeat complete raw ASM/OBJ/LIB/EXE/MAP vectors. All893 library
positions,892 surrounding member program records,28 prior source providers,
36 project objects and real startup/EMU/MATHL inputs are retained. Candidate xx
is provider29;the accepted28-provider library and published211 owners stay unchanged.

| Extent | Original | Native candidate |
| --- | ---: | ---: |
| Full decoded EXE | 67,372 | 67,308 |
| xx CODE | 12,622 | 12,554 |
| Literal native fields | 187 | 187 |
| Ordered xx MZ words | 20 | 20 |
| xx DATA/BSS | 18/10 | 18/10 |
| RTTI tail | 1,735 | 1,734 |
| Raise frame allocation | 390 | 342 |

Both EXEs have4096-byte headers/677 relocations;raw EXE/MAP still differ.
Candidate DGROUP0E3B versus original0E3F produces ordinary64-byte file movement.
All CODE bytes resolve through18 real library interfaces;all22 public bindings
pass. Net CODE length68 is not a differing-byte count. Matching field counts
also do not establish complete literal ordered field equality.

Current useful proofs and open questions:

- The complete first2822 object and linked bytes agree,with all92 literal
  ordered prefix fields. This includes sameTypeID157,findBaseType339,
  compatibleType372 and the complete1495-byte call bank with88 fields.
  callCopyCtor750,callDestructor392 and callMemberFunc185 now agree raw.
  Only the four virtual-base SI writes use `_SI = FP_OFF(destination)`;
  changing every SI write leaves one wrong branch byte. All18 imports retain
  original order;see [call review](MAINL_XX_CALLS_REVIEW.md).
- Native compilation preserves all six original five-byte forward FAR CALLs
  without TASM shortening. destroyBases129 and destroyVariable715 now match
  complete linked bodies;their literal fields retain original shapes and
  callee identities. Whole xx remains raw-different,so no accepted credit follows.
- dtorCleanup1035/frame32 differs only at object offsets976/977 in the
  callMemberFunc operand. Its literal field order now matches40/996/932;
  all1025 bytes outside five proven near-CALL operands agree.
- ExceptionHandler880/frame56 retains all854 bytes outside proven operands.
  Seven raw operand bytes still differ. Switch field order now matches10..0,
  but body-field order remains original372/294/724/703/700 versus native
  724/703/700/372/294. No normalization or exact credit.
- initCatchArg is674 versus678,frame24. Native compilation recovers the class
  guard;two reference-branch forms remain. exceptionHandled223 versus216
  retains the10/17-byte LES versus DX:AX load difference. Native field orders
  remain distinct;see [catch review](MAINL_XX_CATCH_REVIEW.md).
- Raise stays1081 versus1151,frame342 versus390. Its count/index/copy block
  matches all71 raw bytes. Native386 intrinsics express individual unsupported
  instructions;symbolic BP addresses use offsetof-derived member offsets.
  An actual linked probe caught BCC's reversed local-member displacement:
  `context.field` and `context + offset` were wrong;`context - offset` recovers
  the intended address. No hardcoded BP slot or target-function byte array.
- The corrected real-linked Raise path agrees at entry SP=FF00,including flags
  84h/84h. At FF10 only the known80h/84h difference remains;both use actual
  library memcpy twice. Original BP[-134,-86) ownership stays unproved.
  Do not invent storage or adjust flags to close the48-byte gap.
- Native RTTI metadata135 has no optional zero or LIDATA;tail1734 still differs
  raw. The retained S/TASM miniature instead has CODE12553/181 fields and
  metadata136/tail1735,with one actual LIDATA zero. Inspect actual record
  presence;do not infer an initializer from address parity.
- `typeinfo::before` matches120 unlinked object bytes,including literal strcmp
  EXTDEF8 at+96;the linked operand still differs. Catch branches,Raise storage
  and the remaining source/codegen/layout gaps stay open.

See [normal product review](MAINL_XX_PRODUCT_REVIEW.md),
[RTTI review](MAINL_XX_RTTI_REVIEW.md) and [throw review](MAINL_XX_THROW_REVIEW.md).
Earlier bank miniatures have their own provider counts,CODE sizes and traps.
Keep original unchecked DOS behavior;do not import later reference-RTL behavior.

## Verification and retained local state

Rebuild/review affected scope;validate/reuse unchanged pairs. No full cold/DIET
or unchanged ancestor runtime chain is required each turn. Source changes that
actually affect an earlier producer do require refreshing its native binding.
Recent affected checks:dispatch/destruction/calls/catch/types/throw/full-TU/normal-link
native pairs,9 targeted tests,
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
