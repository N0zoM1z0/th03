# TH03 handoff

## Current state

Natural source recovery and exact native output are the goal. Use the pinned
Japanese targets in `config/targets.toml` (`candidate-local-attested`); never
substitute translated, patched or reference-game binaries. MAINL is the ending.
Read [workflow](RE_WORKFLOW.md),[architecture](ARCHITECTURE.md) and
[detailed notes](RE_NOTES.md) before changing
native recipes. Inspect Git; all dirty work belongs to this reconstruction.

The complete native Borland C++ xx translation unit now matches all
12,622 Japanese CODE bytes and187 literal ordered OMF fields. The actual
29-provider working library replaces only the original xx member among893,
retaining892 other member programs. Both normal links reproduce the entire
67,372-byte decoded Japanese MAINL EXE and original MAP byte-for-byte,
including all677 MZ relocations. All50 linked xx functions are raw-equal,
including initCatchArg678, _ExceptionHandler880, RaiseException1151,
searchBaseClass582 and __DynamicCast357. These are natural source and
ordinary BCC -c outputs,not postprocessed binaries. The accepted28-provider
library and211-owner publication remain frozen until separately promoted;
no new ledger credit is claimed. No full cold replay or ancestor chain ran.
See [complete native xx product review](MAINL_XX_PRODUCT_REVIEW.md).
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

## Independent native memcpy source

`src/mainl/crt/memcpy.asm` now reproduces the complete original36-byte
DOS far-cdecl memcpy module,zero ordered fields and original CODE/DATA/BSS
extents. Two TASM/TLIB/TLINK rounds replace only member261 of893;the other
892 program records remain untouched and actual decoded Japanese MAINL
EXE/MAP are each raw-equal in both rounds. The accepted211-owner publication
and28-source library are deliberately unchanged;no new ledger exact credit.
See [native memcpy review](MAINL_MEMCPY_WORK_REVIEW.md) for the scoped commands
and retained private raw pairs. No full cold replay is needed.

## Independent native memcmp source and combined CRT link

The new src/mainl/crt/memcmp.asm exactly reproduces40 original DOS
memcmp CODE bytes,its no-fixup OMF public interface,and the original
BSS-before-DATA group record. A two-round scoped producer reuses the
retained exact source memcpy library,then replaces original members260
and261 with these two maintained CRT sources. All891 other real members
are unchanged. Full decoded Japanese MAINL EXE (67,372 bytes) and MAP
match raw in both rounds;677 original MZ relocation entries are retained.
See [combined source review](MAINL_MEMCMP_WORK_REVIEW.md).
The accepted211 owners/28-provider library remain unchanged,so no
published additional exact credit is claimed and no full cold is run.

## Cumulative three-source CRT link

Original DOS strcmp is now a 48-byte byte-for-byte source/OBJ match with
zero fixups and verified BSS-before-DATA GRPDEF. The retained two-source
memcpy/memcmp library is reused and the original strcmp member at index292
is replaced. Two TASM/TLIB/TLINK rounds preserve the remaining890 vendor
member programs and reproduce the entire67,372-byte decoded Japanese
MAINL EXE and its native MAP,including677 MZ relocations. All three
natural source CRTs total124 CODE bytes. Neither the accepted28-provider
library nor the211-owner publication is changed. See
[three-member CRT review](MAINL_STRCMP_WORK_REVIEW.md). No full cold replay.

## Four cumulative source CRT members

The new memchr.asm restores37 original far-cdecl CODE bytes,its empty
BSS-before-DATA OMF GRPDEF and its original zero-field public interface.
Two complete source-only TASM/TLIB/TLINK rounds retain the earlier
memcpy36/memcmp40/strcmp48 members and replace the original member259
with memchr. All889 remaining original member program records agree.
The four reconstructed routines total161 CODE bytes and their
entire67,372-byte decoded Japanese MAINL EXE and MAP are raw-equal
with677 ordered relocations. The unchanged28-source accepted library
and211-owner publication are separate;no new accepted credit is booked.
See [four-member CRT review](MAINL_MEMCHR_WORK_REVIEW.md). The
independent cumulative CRT builder can re-check further original
members without a full cold replay.

## Five cumulative source CRT members

The newly recovered memset.asm contains the exact72 original DOS CODE
bytes,including native _setmem and _memset far entries. With the
existing memchr/memcmp/memcpy/strcmp sources,the five-member scoped library
now has233 byte-exact source CODE bytes at indices259/260/261/263/292.
The other888 original CRT members remain unchanged. Two actual isolated
TASM/TLIB/TLINK runs rebuild the full original67,372-byte Japanese MAINL
EXE and MAP raw equal,with677 original relocations. The accepted28-source
library and211-owner ledger are still unchanged. See
[five-member CRT review](MAINL_MEMSET_WORK_REVIEW.md).

## Six-source DOS memory CRT native link

The recovered `strlen.asm` adds its complete original33-byte DOS far
cdecl body,including the original full null-pointer guard and forward
REPNE SCASB. All six CRT source modules (memchr,memcmp,memcpy,memset,
strcmp,strlen) now give266 raw-exact native CODE bytes in original
members259/260/261/263/292/300. The other887 member programs are
unchanged. Two actual TASM/TLIB/TLINK runs match the entire67,372-byte
original Japanese decoded MAINL EXE and MAP,including677 relocations.
The accepted28-source CRT/211-owner publication remains separately frozen;
this is source-only working evidence,not new ledger credit.
See [native strlen review](MAINL_STRLEN_WORK_REVIEW.md). No full cold replay.

## Seven-source DOS memory/string CRT native link

The alignment-aware63-byte far `strchr.asm` now also matches the entire
original object code,one public symbol and all empty segment/group
ownership. Seven source members (memchr,memcmp,memcpy,memset,strchr,strcmp,
strlen) provide329 native-exact CODE bytes in original library slots
259/260/261/263/291/292/300;the other886 native members stay untouched.
Two isolated TASM/TLIB/TLINK rounds reproduce the full original67,372-byte
Japanese decoded MAINL EXE and complete MAP byte-for-byte,including all677
MZ relocations. The accepted211-owner publication and28-provider library
remain frozen,no new formal accepted byte credit and no full cold replay.
See [strchr source recovery](MAINL_STRCHR_WORK_REVIEW.md).

## Seven cumulative source CRT members

strchr.asm adds63 exact DOS bytes with the original far-pointer
word/byte search ABI. The seven-member native source CRT now totals
329 CODE bytes (including the dual-entry memset),at original
members259/260/261/263/291/292/300. The other886 members are
untouched. Both independent TASM/TLIB/TLINK rounds produce entire
original decoded Japanese MAINL EXE/MAP,677 relocations and matching
native member ownership. See [seven-source CRT review](MAINL_STRCHR_WORK_REVIEW.md).
The accepted ledger remains deliberately unchanged.

## Combined eight-source MAINL native carrier

The exact native BCC xx.cpp object (12622 CODE bytes,187 ordered fields,
50 complete linked function bodies) and all seven exact-source DOS memory/
string CRT members (329 CODE bytes) now **coexist in one normal original
893-member CRT link**. All885 other real library member programs are
unchanged. Two actual TLIB/TLINK rounds rebuild the complete original
67,372-byte Japanese decoded MAINL EXE and MAP byte-for-byte,including
677 ordered relocations. The simultaneous native source CODE scope totals
12951 bytes. Only the isolated source-library carrier changed:accepted
211-owner publication and28-provider library remain frozen,and this does
not claim formally accepted bytes. See [eight-member normal-link review]
(MAINL_XX_CRT8_COMBINED_REVIEW.md). No full cold replay was performed.

## Fifteen-source exact strncat using real movmem/strlen edges

The original DOS strncat translation unit is now completely
reconstructed as a natural BCC4.5 source,with all105 CODE bytes,
two original far strlen calls,the movmem call,and all3
literal ordered OMF fields. Moving strlen(source) assignment into
the limit comparison preserves AX and eliminates a non-original
three-byte local reload. It links with the whole xx TU,seven original
CRT memory/string helpers,strstr,strtok,strtoul,strtol,strncpy
and dual-entry movmem. All15 source members supply14056 exact CODE
bytes,with878 unchanged programs. Both native links reproduce the
whole Japanese decoded MAINL EXE/MAP including677 relocations.
Accepted ledger stays frozen;no cold replay.
See [strncat source review](MAINL_STRNCAT_NATIVE_REVIEW.md).

## Full native overlap-safe movmem and memmove

The real 119-byte original DOS movmem CRT member is recovered as
source TASM,including two complete public far entry points (_movmem
and _memmove),the original N_PCMP@ import/fixup and both copy directions.
Its overlap-safe BSS-free far pointer handling and the wrapper's
near CALL/codegen match every original byte. Alongside native
strncpy and the previous12 real CRT sources,the14-source library
has13951 CODE bytes exact,with879 other native member programs
unchanged. Both full source-only normal links generate the entire
original Japanese decoded MAINL EXE and MAP raw equal,including677
relocations. Accepted ledger credit is still frozen;no cold replay.
See [overlap-safe movmem recovery](MAINL_MOVMEM_NATIVE_REVIEW.md).

## Native exact counted strncpy

A real 8086 DOS far-cdecl strncpy.asm source restores49 complete
original CODE bytes,zero OMF fixups and the uninitialized segment
group. Its count-limited scan/copy/zero-fill control flow is natural
TASM source,not an embedded byte array. Combined with the previously
proved full xx and eleven additional native CRT sources,it produces
13832 exact original CODE bytes across13 source members,with880 other
library members unchanged. Two TASM/TLIB/TLINK rounds reproduce the
original decoded Japanese MAINL EXE/MAP byte-for-byte;formal accepted
ledger remains frozen. See [counted copy](MAINL_STRNCPY_NATIVE_REVIEW.md).

## New exact overlap-safe movmem and bounded strncpy

The original DOS far-cdecl strncpy produces49 exact native CODE bytes,
including its segment swaps and counted NUL/zero-fill control.
The independent native movmem module contains a complete82-byte
overlap-safe _movmem and a37-byte far _memmove wrapper. It matches
all119 original CODE bytes,its single near N_PCMP@ relocation,
both public offsets and its original BSS/DATA GRPDEF. Fourteen
simultaneous source CRT modules including full xx now recover
13951 exact CODE bytes;two actual TASM/TLIB/TLINK rounds produce
the complete original Japanese decoded MAINL EXE/MAP and677
ordered MZ relocations. All879 other native library members
remain unchanged. The accepted28-provider library and211-owner
publication are frozen;no formal added credit and no cold replay.
See [movmem original source review](MAINL_MOVMEM_NATIVE_REVIEW.md)
and [strncpy review](MAINL_STRNCPY_NATIVE_REVIEW.md).

## Signed strtol large original control-flow recovery

The original 290-byte DOS BCC4.5 signed strtol translation unit is
now recovered naturally. It contains two private near scanner
callbacks,its original far public at offset56,sign handling,overflow
clamps and seven literal ordered OMF fields. The correct native
10-byte stack frame required keeping the ES segment from the
whitespace loop;the typed volatile far access through MK_FP(_ES,...)
eliminates one non-original LES. All290 CODE bytes and seven fields
are exact. A twelve-source original library containing the whole
xx TU and previously proved CRT string/memory/scanner modules
now has13783 native-exact CODE-segment bytes. The other881 of893
library programs remain unmodified,and two real BCC/TLIB/TLINK
rounds reproduce the entire Japanese MAINL EXE/MAP raw-equal.
No full cold replay or new formally accepted ledger credit.
See [signed native scanner review](MAINL_STRTOL_NATIVE_REVIEW.md).

## Larger unsigned long parsing TU now native exact

The genuine DOS Borland strtoul.cpp reconstructs231 full CODE bytes,
two private near character callbacks and the original far public at
offset56. Native BCC4.5 now reproduces all six ordered OMF fixups and
the exact errno/ctype/scantol import order. Far stack output pointers,
the extra unget character argument and the typed _AX test were essential:
the preceding natural C++ trial differed by one OR-register byte.
A joined original CRT library with complete xx,seven established CRT
string/memory units,strstr,strtok and strtoul now has eleven source
members,totaling13493 original CODE-segment bytes. Two BCC/TLIB/TLINK
rounds produce the exact full Japanese decoded MAINL EXE/MAP and677 MZ
relocations;all882 remaining library programs are unchanged. Formal
accepted211-owner publication is still frozen,with no new ledger credit.
See [unsigned parser source review](MAINL_STRTOUL_NATIVE_REVIEW.md).

## Full native stateful strtok with original ordered OMF fields

The original 203-byte DOS BCC4.5 tokenizer now has a natural C++ source
at src/mainl/crt/strtok.cpp. Both nested delimiter loops,far-payload
mutations and a real4-byte static BSS cursor are recovered. BCC's
typed ES:BX pseudo-register access avoids a redundant far reload.
The native object now agrees in all203 CODE bytes,all12 emitted OMF
fields in literal order,one far public and original DATA/BSS group.
Ten source CRT members including the whole xx TU and previously
recovered strstr yield13262 original CODE bytes inside one original
893-member library. All883 other members are preserved. Two actual
BCC/TLIB/TLINK rounds reproduce the full Japanese decoded MAINL
EXE/MAP and677 MZ relocations byte-for-byte. No new formal ledger
credit and no full cold replay. See
[stateful strtok review](MAINL_STRTOK_NATIVE_REVIEW.md).

## New exact nine-source strstr carrier

The original far strstr is now a108-byte raw-equal TASM source unit,
including original DS/ES search/control flow and four exact XCHG operand
encodings. It is assembled at original CRT member312 together with
the complete xx BCC source and seven already-verified DOS memory/
string CRT source members. Two actual TLIB/TLINK rounds reproduce the
entire original67,372-byte decoded Japanese MAINL EXE and MAP,with677
MZ relocations and884 other original native member programs unchanged.
All nine source members total13059 exact CODE bytes. Published acceptance
is frozen,so no new ledger credit is claimed. See
[nine-source strstr review](MAINL_STRSTR_NATIVE_REVIEW.md);no cold replay.

## Eight-source combined exception/CRT native working library

A further actual TLIB/TLINK integration now combines the complete natural
xx source object (12,622 CODE bytes and187 exact literal fields) with all
seven recovered native CRT string/memory modules (329 CODE bytes),at
eight original member positions in the same893-member library. The
remaining885 member programs are unchanged. Two complete source-library
links reproduce the whole Japanese decoded MAINL EXE (67,372 bytes) and
its original MAP raw-equal,including677 original MZ relocations. This
proves **12,951 total source-built native CODE segment bytes** working
together,not just in separate experiments. The accepted28-provider CRT
library and211-owner publication remain untouched;no ledger credit has
been automatically promoted. See
[eight-source integration review](MAINL_XX_CRT_INTEGRATION_REVIEW.md).
Only the affected normal library/link was rebuilt; no full cold replay.

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
| xx CODE | 12,622 | 12,622 |
| Literal native fields | 187 | 187 |
| Ordered xx MZ words | 20 | 20 |
| xx DATA/BSS | 18/10 | 18/10 |
| RTTI tail | 1,735 | 1,735 |
| Raise frame allocation | 390 | 390 |

Both EXEs have4096-byte headers/677 relocations and agree raw,including their complete MAP.
Both objects now link at DGROUP0E3F with no remaining paragraph shift.
All CODE bytes resolve through18 real library interfaces;all22 public bindings
pass. The complete CODE byte vector and the full literal187 ordered-field
vectors,not merely their lengths or counts,now match.

Current useful proofs and open questions:

- The first2822 object/linked bytes and92 literal ordered fields agree. This
  includes the complete1495-byte call bank/all88 fields,the157-byte comparator
  and339/372-byte type helpers. The four virtual-base SI transfers use register
  variables;nonvirtual ASM transfers retain the final branch shape.
- Six original forward FAR CALLs are retained. Complete linked destruction
  bodies129/715 agree. All50 bodies are compared;all50 agree raw. These bounded
  observations add no accepted bytes while xx remains unaccepted.
- All50 complete linked functions agree raw,including
  dtorCleanup1035, _ExceptionHandler880 and initCatchArg678.
  The latter retains its original24-byte frame,three ordered fields
  and semantic JE/JMP edges using _CX as its live mask.
- searchBaseClass582 and __DynamicCast357 also match after
  reordering the far address comparison and testing the incoming
  destination descriptor for null. No filler or object patches.
- Throw/rethrow89/170,exceptionHandled216 and RaiseException1151
  remain exact,with both linked Raise stack-entry flags checks passing.
- Native386 intrinsics keep symbolic BP addresses. The checked minus-member-
  offset spelling avoids BCC's local-member assembler bug. No target-function
  arrays or object patches supply code;see [product review](MAINL_XX_PRODUCT_REVIEW.md).
- Native metadata136/tail1735 now has one optional zero in dense LEDATA,no LIDATA. The S/TASM miniature
  instead has CODE12619/181 fields and metadata135/tail1734 with no LIDATA zero.
  Inspect actual records;address parity does not prove an initializer.
- before matches120 unlinked and linked bytes with its original strcmp EXTDEF8 field. All18 imports retain original order.

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
