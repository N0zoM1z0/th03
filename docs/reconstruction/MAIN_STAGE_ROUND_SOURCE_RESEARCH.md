# MAIN stage setup and round initialization: bounded research checkpoint

## Result and scope

Research only: no new accepted source, exact bytes, original TU ownership or
whole-game completion claim. Target MAIN SHA-256:
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
Worktree HEAD was `e8a1ed73d0971af2ed00c869ea8ac877cf0220c7` throughout these
experiments. All five receipts preserve HEAD, status, input bytes and modes,
staged inputs, and report no timeout or owned cleanup survivors. Original 19
modified tracked files plus one untracked file remain unchanged.

Complete stage target [9B14,9EBF) is 939 bytes: 900-byte body, one observed zero,
and three compiler-style tables (9 character, 4 rank, 6 stage entries). The
following initializer [9EBF,A21F) is 864 bytes: 855-byte body, one observed zero,
and a four-entry rank table. The genuine no-op hook [9B0F,9B14) is five bytes.
Combined target [9B0F,A21F) totals 1808 bytes, including 1760 function-body bytes,
46 table bytes and two observed zeros. Numerical proximity is not exactness.

## Experiments, including preserved failures

1. Stage source v01: native compiler exit 1. Actual header types exposed source
   mistakes: score_lebcd_t requires `.digits`, PlaycharPalettedOptional requires
   `.v`, and SPRITE16_RES_Y requires its existing sprite16 header. No object.
2. Stage v02 fixed only these real field/header accesses and added layout
   assertions. Compiler exit 0, CODE 936. Driver failed because it wrongly
   expected C public `_stage_setup`; source correctly emitted C++
   `@stage_setup$qv`. The failed receipt is retained. Corrected driver checks the
   exact source-specific name and rejects aliases/wrong signatures/duplicates.
   Independent analysis found a two-byte branch contraction: native JNE lunatic
   replaced target JE rank followed by JMP lunatic. Body 898 versus target900,
   plus absent target zero after RET. All 19 table cases retained their order.
3. Stage v03 replaced the reconstructed goto into the rank switch with ordinary
   if/else: both-CPU assigns 65535L; otherwise the rank switch includes its own
   65535L case. Compiler/driver passed; body900 and CODE938. No other source
   changes, options or forced branches. Independent comparison found no body
   differences outside actual fixup operands and five equal-width linker
   far-call relaxation sites. All19 cases match; target zero9E98 still absent.
4. Combined v01 uses real no-op hook, unchanged stage-v03 body and unchanged
   initializer-v04 body, in target order. Historical common-TU ownership is
   UNPROVEN. Hook is selected at9CA3 into DS:118A for ordinary/non-demo play and
   called indirectly at99D4; active demo handler9AD6 stays external. Thus it is
   genuine program behavior, not padding. Compiler exit0, CODE1806, physical
   publics hook0/stage5/initializer943. Old driver failed by confusing PUBDEF
   record order with physical order. Its receipt remains unchanged. Corrected
   checker requires exact unique name set, separately sorted physical order,
   same segment, distinct offsets and first function at0. Same-profile prefix
   context did not produce either target zero: 5+938+863, not1808.
5. Combined v02 changes one directive only: post-header `-a.` becomes explicit
   vendor-supported `-a2`. All bodies/declarations/assertions and compiler flags
   are unchanged. Compiler/driver pass, CODE1807: hook5+stage938+initializer864.
   This is partial producer research, not an accepted linked result.

## Exact scope of the final independent comparison

Combined-v02 vs combined-v01 inserts one00 at native object offset+706h (1798),
after initializer RET at+705h. Its dispatch operand at+502h changes0706h→0707h.
The four initializer table FIXUPP locations move
1804/1802/1800/1798→1805/1803/1801/1799; table payload values remain unchanged.
The first1023-byte LEDATA payload is identical. Both objects' physical CODE is
one MAIN_01_TEXT contribution in MAIN_01, with no added DATA/BSS storage.

All23 switch-case destinations remain consistent with the target. Initializer
body855 is unchanged except for its fixup-covered table operand; its extent is
now864. Hook5 and stage938 remain unchanged. Function-relative body855 followed
by tableoffset856 is consistent with local compiler alignment accounting, but
is not proof of compiler internals. The earlier global-parity explanation is
not supported by this experiment. No 1024-byte internal-buffer claim follows
from LEDATA framing or ordered original relocation runs.

Target stage zero at9E98 remains missing. Initializer consequently begins at
combined offset943 versus target944. Full1808-byte equality is NOT established.
All external fixup resolutions, original ordered MZ relocations, original
physical/source ownership and full cold links remain open. A comparison that
excludes actual OMF fixup fields is useful diagnostics, never raw-byte proof.

## Alignment evidence and constraints

The actual successful compiler dependencies comprise110 entries/67 unique
files, all available and pinned. Raw directive audit found only the source's
-a- and -a. alignment directives; vendor STDDEF contains warning pragmas only.
No hidden later header reset was found. Numeric compiler default remains
unproved: TURBOC.CFG only sets include/library paths. Explicit-a2 was one
bounded documented-profile hypothesis, not an option sweep. Record assertions
were retained and passed. No target arrays, filler, artificial side effects,
forced jump bytes, object patching or comparator weakening were used.

## Reproducible evidence and retained sources

`MAIN_STAGE_ROUND_SOURCE_EVIDENCE.json` records all five immutable receipt hashes, actual compiler
commands, source/driver hashes, object hashes, physical publics, record framing
and source-preservation checks. The evidence file is a compact snapshot of retained private receipts; it is
not a claim that native execution or acceptance ran during documentation.
See [reproduction instructions](MAIN_STAGE_ROUND_REPRODUCTION.md) for the
maintained source paths, pinned driver recipe and evidence boundaries.

Keep the original ignored experiment directories/receipts intact. The latest natural core source is preserved as
`src/main/round/stage_round.cpp` and `src/main/round/initialize.hpp`. Historical
standalone source variants remain in the private experiment directories.
The retained combined driver/tests are under
`.analysis/gpt-dots-stage-round-owner-source-v02/probe-v01/`;
38 mock-only tests passed. The checked driver uses one fresh object, oneCPU,
nice+10, bounded timeout, pinned tool identity and owned-process cleanup.

Historical compile command form (not a request to run another experiment):

    python3 -B .analysis/gpt-dots-stage-round-owner-source-v02/probe-v01/probe_compile_stage_round.py --run-id first-v02 --timeout 90

That run ID now exists and must not be reused. Additional native work needs a
new reviewed question, fresh run ID and parent-owned exclusive writer interval.
This checkpoint preserves bounded authored source and compact findings; it
excludes target binaries, toolchains, frozen reference archives and generated
object payloads. The source is experimental and is not integrated into the
accepted build or exactness manifests. No acceptance ledger or claimed exact
scope is changed by preserving this source.
