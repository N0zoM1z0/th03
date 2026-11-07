# All nine major BOSSes + shared controllers: one native 32-byte template

This native source recovery consolidates **eleven physical Turbo C++
translation units** behind a single checked representation of the
original 32-byte per-player BOSS state in DGROUP. Each character's
large C++ update, attack scheduler, initializer and sprite renderer
continues to compile as its *own original* code producer.

Kana, Kotohime and Yumemi were first established in after625.
Chiyuri, Ellen, Rikako, Reimu and the shared explosion-ring/seven-helper
source followed in after626. Mima and Marisa now complete the entire
family. Both former Mima/Marisa templates used anonymous physical
bytes +10–+15; their initializer now names the fields accurately as
`hit`, `mode`, `angle`, `pattern_i` and `render_mode`.
These map to exactly the same byte offsets as the old declarations.
The remaining +18..+1F region stays character-specific: e.g. Rikako's
signed spin delta at +1A, Ellen's reserved tail, Chiyuri's radius zero.

The common header `src/main/boss/template_state.hpp` checks the
complete 32-byte stride and key physical offsets at **compile time with
the original 16-bit compiler**, not with a host compiler. The v2 native
source overlay forces the header and each physical C++ source to the
actual per-round input paths and checks Borland OMF dependency records;
it does not accidentally compile a stale copy of the source from the
historical TH03WORK tree.

The final **simultaneous** source-native compiler/linker proof is:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af627b \
      --units ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af627b

Two genuinely independent Turbo C++ 4.02 compile/TLINK rounds verify
the entire **18,400 original CODE bytes**, **2,540 ordered native
FIXUPP fields**, **93 PUBLIC offsets**, all native object segment
definitions, both complete original normal MAIN EXEs and path-normalized
MAPs. The pinned Japanese 124,642-byte program image, **1,553 ordered
relocations** and independently serialized 130,882-byte Japanese
MAIN.EXE also match in both rounds. The original remaining project
objects and C0/CRT libraries were reused unchanged; no cold replay or
target/object patching occurred.

Receipt: `.analysis/work/exatt-layout-af627b/report.json`, SHA-256
`21bbafe2afeaeb0f22677e9059044857497c5f6e7569fed165aaf8af011671b2`.
Earlier source-attested controls are `af625b`, `af626a`, `af627a`;
all sources, compiled native OBJ pairs, complete EXE/MAP outputs and
compiler/linker writer logs are retained.

This is an ABI and maintainable C++ reconstruction improvement, **not**
18,400 additional unique accepted bytes or proof of historical raw vendor
OMF packets, pristine packed-file provenance, canonical Factory
acceptance or real PC-98 runtime behavior.
