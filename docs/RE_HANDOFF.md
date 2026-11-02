# TH03 handoff

## Current state

Natural source recovery and exact native output are the goal. Use the pinned
Japanese targets in `config/targets.toml` (`candidate-local-attested`); never
substitute translated, patched or reference-game binaries. MAINL is the ending.
Read [workflow](RE_WORKFLOW.md),[architecture](ARCHITECTURE.md) and
[detailed notes](RE_NOTES.md) before changing
native recipes. Inspect Git; all dirty work belongs to this reconstruction.

Latest native source recovery restores a typed 48-byte near-stack resume
frame in RaiseException, passed to the original empty context hook. Its
complete1151-byte object body and five literal ordered relocations now match
the fixed Japanese target,as do the linked body and the390-byte frame.
Both actual linked386 Raise probes agree,including alternate entry SP=FF10.
The precise historical C++ type name remains unproved;this is a meaningful
used local,not a padding array. exceptionHandled also matches its complete
216-byte native and linked bodies. The whole xx member remains unaccepted.
Native field ordering follows actual emitted CODE LEDATA records:the source
now includes one1023-byte record at0x1C00,not a uniform1024-byte partition.
The complete1495-byte call bank and88 ordered fields remain unchanged;the
matching prefix is2822 bytes/92 fields. Full product still differs by four
CODE bytes and other linked relocation/layout content. Earlier experiments
are not authority over the current source and actual outputs.
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
| Full decoded EXE | 67,372 | 67,372 |
| xx CODE | 12,622 | 12,618 |
| Literal native fields | 187 | 187 |
| Ordered xx MZ words | 20 | 20 |
| xx DATA/BSS | 18/10 | 18/10 |
| RTTI tail | 1,735 | 1,735 |
| Raise frame allocation | 390 | 390 |

Both EXEs have4096-byte headers/677 relocations;raw EXE/MAP still differ.
Both objects now link at DGROUP0E3F with no remaining paragraph shift.
All CODE bytes resolve through18 real library interfaces;all22 public bindings
pass. Net CODE length4 is not a differing-byte count. Matching field counts
also do not establish complete literal ordered field equality.

Current useful proofs and open questions:

- The first2822 object/linked bytes and92 literal ordered fields agree. This
  includes the complete1495-byte call bank/all88 fields,the157-byte comparator
  and339/372-byte type helpers. The four virtual-base SI transfers use register
  variables;nonvirtual ASM transfers retain the final branch shape.
- Six original forward FAR CALLs are retained. Complete linked destruction
  bodies129/715 agree. All50 bodies are compared;34 agree raw. These bounded
  observations add no accepted bytes while xx remains unaccepted.
- dtorCleanup1035/frame32 now differs in one local CALL displacement
  byte;ExceptionHandler880/frame56 has five operand-byte differences.
  Their natural code and helper interfaces remain intact. Native handler
  fields have the same relative order,though the source block begins
  at0x1FFF rather than the original0x2000.
- initCatchArg remains674 versus678/frame24,with two original branch forms
  not yet recovered. exceptionHandled now matches all216 native and linked
  bytes/frame8 via symbolic descriptor LES and typed ES:BX access.
- The89/170-byte public throw/rethrow wrappers now both match complete
  native and linked bodies. Original local ordering is caller-PC DWORD
  first,then optional exception pointer,and the frame WORD last;the
  previous opposite order emitted the wrong BP stack slots.
- RaiseException now matches all1151 native and linked bytes,five ordered
  native fields,and its390-byte frame. A real48-byte stack-local resume
  image supplies the empty hook's SS pointer. Both SP=FF00 and SP=FF10
  linked probes agree,including EFLAGS84h and80h respectively. Historical
  source type identity is still unproved;no fake stack filler or byte patch
  was added.
- Native386 intrinsics keep symbolic BP addresses. The checked minus-member-
  offset spelling avoids BCC's local-member assembler bug. No target-function
  arrays or object patches supply code;see [product review](MAINL_XX_PRODUCT_REVIEW.md).
- Native metadata136/tail1735 now has one optional zero in dense LEDATA,no LIDATA. The S/TASM miniature
  instead has CODE12616/181 fields and metadata136/tail1735 with one LIDATA zero.
  Inspect actual records;address parity does not prove an initializer.
- before matches120 unlinked bytes and its strcmp EXTDEF8 field;the linked
  displacement still differs. All18 imports retain original order.

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
`gpt-web: ...`. Full CI is for broad infrastructure changes.

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

The2026-10-31 cleanup corrected stale RE_NOTES/CRT README claims and retired
superseded private scripts,source/object copies,download catalogs and Python
caches. It retained written records and all286 protected native output files;
the audited inventory is `.analysis/work/cleanup-20261031-audit.json`.
Git packing preserved all10797 existing objects and refs without pruning.

For cleanup,follow [working-file rules](RE_WORKFLOW.md#working-files). Remove
superseded experiments and duplicate staging trees after checking dependencies;
retain documents,ledgers and experiment/verification records while deleting
unused code copies and rebuildable binaries. Generic cleanup preview is not a
complete dependency oracle.
