# PI resource loader: a real 16-bit return local

The complete far-Pascal `pi_load` owner frees the requested image slot
before loading the new packed PI resource. The 16-bit `load_result` local is
not redundant source scaffolding: a direct `return graph_pi_load_pack(...)`
changed the original TC4 CODE (`af1173a`). Declaring the same local
separately (`af1173b`) or naming its purpose (`af1173c`) retains the native
instruction stream and exact order of the two far calls.

`af1173c` matches the entire original 70-byte CODE owner, six ordered
native fields, the PUBLIC and full Japanese MAIN image/relocations in two
independent original TC4/TLINK rounds.

## 2026-11-11: near-first-use return local without a stack change

The maintained `pi_load()` now frees the previous PI slot before
introducing `const int load_result` initialized by the actual far-Pascal
`graph_pi_load_pack` call. This moves the declaration to the first use
and makes its read-only lifetime explicit, while retaining the original
16-bit return local (required for exact TC4 codegen) rather than returning
the far call directly. The original slot-pointer arithmetic and far
function call order are unchanged.

`af1358m` proved first-use initialization; current `af1358n` additionally
proved `const` with two original TC4/TLINK rounds. The entire **70 CODE
bytes, six ordered native fields and one PUBLIC** match, as does the
normal MAIN image. Joint stage `af1358o` recompiled this leaf with the
current Yumemi BOSS and its relevant combat/render dependencies.

Current proof: `.analysis/work/exatt-layout-af1358n/report.json`, SHA-256
`175f3ced0be41d1cf84d122d5ee2183887d147fe983fbd79ad344dcac1e9598c`.
