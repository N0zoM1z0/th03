# MAINL root trigonometric tables — after555 native review

Recovered the **256-byte arctangent lookup table** and the **320 signed-word
sine/cosine lookup table (640 bytes)** from the mathematical definitions in
A. Koizuka's public-domain `master.lib` comments. The sine and cosine tables
share one storage allocation, with cosine starting 64 angles later. The
maintained pure generator is `src/shared/math/trig_tables.py`. It does not
read target files, original objects, extracted table bytes or native outputs.

Read-only comparison of independently generated values against the original
`obj/th03/mainl.obj` at DATA+030A and DATA+04A8 showed **0 differing bytes
across 896 bytes**. An actual native TASM5 assembly replaced exactly the two
historic table includes in a retained contextual root module. The remainder
of its 10,944 CODE bytes, 2,036 DATA bytes and 5,108 BSS bytes is not claimed
as newly reconstructed source by this stage.

`build_th03_mainl_root_trig_work.py` performed **two independent native
assembly and link rounds**, reusing after554's registered text banks, after553
picture C table, after552 natural root C++ object and after548 source C0/CRT
library. In each round, all initialized original object bytes, all **392
literal ordered OMF fields**, all **363 PUBLIC definitions/offsets**, and all
other non-variable OMF metadata matched. Different assembler PUBLIC packet
ordering is not claimed to have been closed.

Both entire decoded **67,372-byte original MAINL EXEs** matched, including
all **677 ordered MZ relocations**. MAP layout, segment sizes and contribution
addresses matched, after accounting solely for the candidate's source
filename path. The two complete raw OBJ/EXE/MAP vectors were identical.
Native output rounds, writer logs, emitted includes, the stage source and
configuration copies are retained, not deleted.

Recheck retained evidence without rebuilding the cold chain:

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
  .venv/bin/python scripts/review_th03_mainl_root_trig_work.py
```

This proves bounded *library-origin DATA* source and selected-link
reproducibility. It does **not** establish complete original OBJ byte identity,
new authored-game code credit, canonical packed-unit Factory acceptance or
whole-product source ownership. The unowned root contextual data still needs
separate, independently checked source work.
