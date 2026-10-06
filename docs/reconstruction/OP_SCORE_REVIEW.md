# OP score candidate review

This review covers two complete direct C++ CODE carriers, one complete public
loader and one independently executed native random helper. The packed Japanese
OP target remains candidate-local-attested. Decoded coordinates do not provide
canonical stored-file offsets or exact acceptance.

| Owner | Decoded entry | Bytes | Maintained source |
|---|---|---:|---|
| Score encoder | 0990:1868 | 165 | src/op/formats/score_encode.cpp |
| Decode / recreate / checksum | 0990:190D | 229 | src/op/formats/score_data.cpp |
| Public rank loader | 0990:19F2 | 107 | src/op/formats/score_load.inl |
| Native IRAND | 0000:1D12 | 42 | Candidate context only |

The loader include remains inside the original `th03/op/m_select.cpp` carrier;
its surrounding menu code is unowned. The two maintained `.cpp` files are
translation units. Score declarations and master/common declarations are
explicit compatibility dependencies in `config/th03_op_score_candidate.toml`.
The byte encryption macros are maintained locally. No MAINL clear-flag branch
belongs in OP's encoder. Neither source presence nor compiler agreement grants
complete dependency, product or exact ownership.

## Target and original compiler observations

`review_th03_op_score.py` binds 24 frozen providers, the original cold OMF
objects and MAP public entries. Six complete bodies total 543 decoded bytes.
They match both original cold images at unchanged coordinates, including
original ordered relocation sites. Bounded initialized data is 15 bytes:
seed 1 at DGROUP 0312, a filename pointer at 0A02 and YUME.NEM at 0A04. The 206-byte
HI structure at 2394 is BSS/runtime storage, with no initialized file slice claim.

Receipt: `.analysis/sol-op-score-review-20261006.json`; SHA-256
`b8d953fec1b3a993aa4f3cf5ee90d9b80884f5da4ebb547094466bcef3e42ec1`;383 guarded inputs.

The native matrix executes 210 instruction positions and 1,168 terminal calls in
each of three images, 3,504 calls total. Per image, nested native entries include
3,488 IRAND,1,152 encoder,896 decoder,416 checksum,256 loader and144 recreate
calls. Mathematical format/LCG specifications are independent of executed
native bytes. Native near/Pascal/far frames, full CPU write spans, ordered
attempted file events, IF/DF and all memory outside the64 KiB stack are checked.
File/library replies are modeled; actual DOS persistence remains unproved.

## Format and runtime findings

The 206-byte section has a checksum word, 80 name bytes, cleared/unknown bytes,
100 sprite score digits,10 player bytes, 10 stage bytes and two key bytes.
The checksum includes 204 bytes after its own word. Encoding consumes three
native random draws in key1/key2/unknown order, then encrypts bytes 203 through0;
key bytes 204/205 remain plaintext. Decode uses the encrypted following byte,
a three-bit rotation and byte wrapping. IRAND preserves the native 32-bit
recurrence `(seed * 22695477 + 1) mod 2^32` and returns bits16..30.

Recreation writes period names, sprite zero scores, default characters/stages,
then score 10000/9000..1000 and cleared 18. Four encode/decode passes consume 12
random draws and attempt rank offsets 0,206,412,618. The final decoded buffer
contains the fourth rank's keys and checksum. OP encoding preserves an
existing cleared 99 value instead of applying MAINL resident/story conditions.

The loader returns bool16: valid checksum 0, missing/corrupt section 1 after
recreation. Only file_exist's full AX zero/nonzero result selects a path; other
file replies and carry flags are ignored. Short reads preserve the unread
buffer suffix. In particular, a zero-byte read can reuse old ciphertext and
pass the checksum. Rank multiplication wraps at 16 bits before widening to the
seek argument: rank FFFF seeks 65330; 318 seeks 65508; 319 seeks 178. No clamp or
signed host seek repair is introduced.

## Maintained source compiler probes and remaining gates

Receipt: `.analysis/th03-op-score/sol-op-score-source-20261006-d/receipt.json`; SHA-256
`638b462b6306c5e3d31670b133bc8d558806284a5ee01b4a3dfd4dce0f000125`;26 guarded inputs.

Three units totaling 501 decoded bytes are recorded as source-present. Exact
acceptance remains false.

The compiler replay uses two independent frozen source trees with maintained
source overlays and no cached objects or products. It records all 416 OMF
objects and checks determinism of20 products / 350 game objects; Research
objects containing dates/times remain diagnostic. Each fresh OP runs the
same 1,168-call score contract matrix. These scaffold products are compiler
probes, not reconstructed whole-game builds.

The initial compiler harness omitted COM products from its count and stopped
after a successful first build. Its failed log is retained separately; the
corrected replay counts the complete pinned product manifest. A second harness
check inherited MAIN's object counts and failed because its four extra owner
wrappers are absent in this OP scaffold. The final replay checks 416 total and
350 game objects; it adds no synthetic objects. A third comparison completed
all first-round native contracts but rejected live tuple arguments against
JSON receipt lists. The final comparator canonicalizes only JSON wire types,
with a regression control preserving return/argument/store/event differences. Portable controls
check malformed boundaries, branch operands, unknown callers, far/near cleanup,
full stores, segment aliasing, FFI errors, stale instruction budgets and known
scalar format/random vectors. All evidence remains analysis-bundle diagnostics.

Canonical DIET/storage ownership, full headers/dependencies/DATA/BSS, actual
DOS/device behavior, complete OP menu/root ownership and the complete Oracle
set remain open. The previously observed initializer entry/raw/ordered failure
remains unchanged; the old MAIN-overlay OP still has 4,867 differences against its compiler
scaffold. This cohort neither classifies those differences nor promotes exact.

The newer OP-only frozen compiler scaffold is recorded separately by
`review_th03_op_score_scaffold.py`. It has six changed decoded program bytes
and unequal original relocation ordering. This is a distinct comparison
against different candidate source material; it does not erase the old
4867-byte failure or establish whole OP ownership.

Receipt: `.analysis/sol-op-score-scaffold-20261006.json`; SHA-256
`c472f2df50c751599ce341c6c66ff8475e36f733d58360e1de096146ccdd3def`.

Updated independent interval coverage is 1015/55261 decoded CODE bytes,
54,246 gaps and zero overlap; 100 nonzero compiler carriers. Receipt: `.analysis/sol-op-map-unit-coverage-after-score-20261006.json`;
SHA-256 `5701de466617cb5f0d1ddab61af0462d5472528d0b05661ccdd2945c53f03c50`. Source-present rows add no extra byte credit.
