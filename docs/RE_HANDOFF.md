# TH03 handoff

## Current state

Natural source recovery and exact native output are the goal. Use the pinned
Japanese targets in `config/targets.toml` (`candidate-local-attested`); never
substitute translated, patched or reference-game binaries. MAINL is the ending.
Read [workflow](RE_WORKFLOW.md),[architecture](ARCHITECTURE.md) and
[detailed notes](RE_NOTES.md) before changing
native recipes. Inspect Git; all dirty work belongs to this reconstruction.

Latest source work restores the complete18-entry DOS EXTDEF declaration order,
after `ab566fb` (all157 comparator bytes through local -O-m).
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
| Full decoded EXE | 67,372 | 67,324 |
| xx CODE | 12,622 | 12,569 |
| Literal native fields | 187 | 181 |
| Ordered xx MZ words | 20 | 20 |
| xx DATA/BSS | 18/10 | 18/10 |
| RTTI tail | 1,735 | 1,734 |
| Raise frame allocation | 390 | 342 |

Both whole EXEs have4096-byte headers/677 relocation entries;raw EXE/MAP still
differ. Candidate DGROUP0E3C versus original0E3F gives ordinary48-byte file-size
movement. Every candidate CODE byte resolves through the real18 library
interfaces;all22 original public MAP bindings pass. Net length53 is not a count
of differing bytes. No exact credit or DOS boot/ending-playthrough claim follows.

Current useful proofs and remaining differences:

- All18 EXTDEF names/indices now agree literally,in order,through explicit DOS
  import declarations in xx_abi.h. Normal EXE/MAP are unchanged by this fix.
  Header changes refreshed all affected xx miniature/native pairs,without cold replay.
- Complete dispatcher140 linked bytes match in both miniature and normal link.
- sameTypeID now matches all157 raw object/linked bytes at original0000:583E.
  Local -O-m removes an extra cached-mask WORD and restores frame10;restore -Om
  afterward. Both native field vectors and the function's MZ vector are empty.
  This is a complete function proof within the still-unaccepted xx member.
- Raise count/index/copy block6AC0..6B06 matches all71 raw bytes. Local -O-v
  removes two extra WORD induction pointers;FS/GS writes,the16-bit zero chain,
  direct SS and CX/ES/BX resume-address operations follow native order.
- `typeinfo::before` matches all120 unlinked object bytes. Its one strcmp field
  at+96 now retains literal EXTDEF8 in both objects. The linked call
  displacement still differs. Scoped -O1 works when -O2-pg/-Os/-O-i/**-Z-** are
  restored afterward;earlier reset trials omitted -Z-.
- Current BCC output emits no optional RTTI zero and no LIDATA record:
  metadata135/tail1734 versus original136/1735. The comparator's extra byte
  leaves total CODE12569 unchanged. Check actual directive/record presence;
  do not infer it from final-label parity or insert a compensating byte.
- The tested Raise context agrees at entry SP=FF00,including flags84h/84h.
  One alternate SP=FF10 exposes original80h/source84h through the real linked
  memcpy twice. The original48-byte region at BP[-134,-86) still has unproved
  type/purpose. Do not invent storage or adjust flags to close it.
- Typed toss cache restores its72-byte frame;body812 versus815 remains.
  Wrapper89/170 lengths agree,not their full raw bodies. Raise is1081 versus1151.
  `dtorCleanup` now has the original1035 bytes/32-byte frame after local -O-v.
  Its complete object differs at only3 bytes,in two local CALL operands;
  all1025 bytes outside the five local CALL operands agree,and all five calls
  resolve to the original helper identities. Literal field offset order stays
  original40/996/932 versus current40/932/996,so no exact credit follows.
- destroyVariable's member/array search matches72 raw bytes after recovering
  its declaration/initialization order. Remaining destroyBases129/128 and
  destroyVariable715/714 differences include TASM's forward far-call shortening.
  See the current section of [destruction review](MAINL_XX_DESTRUCTION_REVIEW.md).
- compatibleType now has the original372 bytes/four-byte frame. Local -O-m
  removes the common-mask temporary;masked CV,bitwise DWORD count OR and the
  positive base-return path recover every byte except two local CALL operands.
  Both calls resolve to sameTypeID/findBaseType;both literal field vectors are
  empty. See [type review](MAINL_XX_TYPES_REVIEW.md#current-compatibility-loop-recovery).
- ExceptionHandler880/frame56 now keeps both unwind argument-cleanup pairs by
  declaring the existing filter after the first call. No optimizer switch is
  needed. All854 bytes outside proven operands agree;seven calls and the12-byte
  switch table are checked. Six raw differing bytes and literal field-order
  differences remain;see [handler review](MAINL_XX_DISPATCH_REVIEW.md#current-full-tu-handler-recovery).
- initCatchArg now has the original24-byte frame and all local BP offsets:
  the existing near-pointer expansion temporary precedes keep_original.
  Its678/676-byte bodies differ structurally at three branch forms;all other
  instructions agree outside verified branch/CALL operands. exceptionHandled's
  first type declaration now outlives the buffer branch,so its second descriptor
  reuses the count slot at BP-8. Its216/223-byte bodies retain one10/17-byte load
  difference. Ordered fields still differ in both helpers;see
  [catch review](MAINL_XX_CATCH_REVIEW.md#current-catch-local-storage-recovery).
- Direct BCC -c accepts16-bit PUSHA but rejects PUSHAD/PUSHFD,EAX and FS even
  with -3. Copy-adapter trials retain767 bytes,or762 under -O1,versus750;
  Turbo's754-byte result changes other adapters too. These routes are not adopted.
- Fresh TASM controls confirm NOSMART retains all six forward FAR CALL fields
  (187 total) but widens17 Boolean immediate encodings and yields CODE12592.
  Local ASSUME controls disturb destruction codegen;version T200/T300 retain
  the default shortening. A private JWasm route retains187 fields/CODE12575
  after two operand-spelling adaptations,but changes accumulator encodings.
  None of these assembler/source experiments is adopted. Keep the default
  current pipeline;the cause of the forward-call gap is now explicit.
- A private direct-BCC route now compiles the complete TU using semantic386
  instruction intrinsics and symbolic BP displacements. CODE12576 has187 fields;
  its first1327 bytes and all four ordered prefix fields match the original.
  Plain/-y payloads and fields agree;LINNUM binds the boundary to callCopyCtor.
  This remains an experiment,not the current product recipe or accepted source.
  The ordinary48-byte struct-return probe passes a far four-byte result pointer,
  unlike the original hook's two-byte argument;the Raise gap stays unproved.

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
