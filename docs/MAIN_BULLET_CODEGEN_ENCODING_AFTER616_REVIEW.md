# Bullet and GRCG 386 render native opcode encoding (after616)

Three earlier attempts to replace manual register instructions in
`src/main/bullet/bullet.cpp` with Turbo C++ pseudo-register assignments
were semantically similar but **not source-exact**. A v1 proof incorrectly
compiled the unchanged historical `TH03WORK/src` instead of the changed
candidate. The corrected v2 compiler source binding exposes these precise
differences:

| Scope | Original opcode | Natural TC4 expression emits |
| --- | --- | --- |
| `grcg_pellet_put` address stride | `D1 E0` (SHL AX,1) | `03 C0` (ADD AX,AX) |
| `bullets_update` trail pointer | `31 DB` (XOR BX,BX) | `33 DB` (XOR BX,BX) |
| `bullets_render` pellet color | `31 D2` (XOR DX,DX) | `33 D2` (XOR DX,DX) |

The register-result semantics are comparable, but byte-exact reconstruction
must preserve the original instruction forms. The three native assembly
statements are restored, now with comments explaining why they are **not**
replaced by the intuitive C++. The real differences were obtained from
isolated negative controls `af611j`, `af611k` and `af611l`; original
Bullet source passes the v2 positive control `af611i`.

The accepted corrected source was compiled in two original Turbo C++ 4.02
rounds from **forced, OMF-dependency-verified current source paths**, with
normal full MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af612d

The complete original **2,685 CODE bytes**, **196 literal ordered native
fields**, **20 PUBLIC symbols**, original 9,500-byte BSS and segment layout,
the full normal linker output and MAP are identical to the original source
baseline. All 1,553 Japanese MZ relocation entries and the separate exact
130,882-byte Japanese MAIN.EXE serialization are verified.

Retained native proof:
`.analysis/work/exatt-layout-af612d/report.json`,
SHA-256 `59b7bf3bb9f8156ca81f08124a373472a93d023d367bd3c99fa4339ca7ea7c21`.
This correction does not add previously owned CODE credit or imply that
all other raw vendor OMF packets match the historical compiler output.
