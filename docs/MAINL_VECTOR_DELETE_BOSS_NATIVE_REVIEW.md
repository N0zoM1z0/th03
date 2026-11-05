# Original Borland C++ array-destructor boss `__vector_delete_` (after392)

Recovered the entire previously contextual Japanese `CL.LIB` member `vdel`
(index 139) into maintained 16-bit assembly in `src/mainl/crt/vdel.asm`.
The full **343-byte original CODE** is reconstructed as instructions,
including the far public `__vector_delete_` entry (CODE+0), element count
and size arithmetic, backward iteration, near/far destructor callback
selection, seven table-directed callback cases plus an eighth default, special array-count header
adjustment, and the original far `operator delete` call.

The 7-entry jump table at CODE+329 uses `dw offset` labels and represents the
original logical mode dispatch targets at CODE+148, +162, +176, +188, +200,
+218 and +236; it is not a copied machine-code payload. All **9 original OMF
relocation fields**, including the jump-table CODE-relative offsets and far
`@$bdele$qnv` import, match their original sites, width, frames, targets
and addends. The original `_TEXT`/`_DATA`/`_BSS` layout is 343/0/0, with
exact public/import ABI and original DGROUP membership. Source was checked
against the real original member: one initial branch selected the wrong
unconditional mode-7 fallback and was corrected according to CODE+140
before producing this receipt. That demonstrates why the original bytes,
not a guessed prose explanation, are the authority.

`scripts/build_th03_mainl_after392_work.py vector-destructor-boss` links the new
member into the unchanged native after391 source carrier. Both independent
TASM/TLIB/TLINK rounds produce the identical original Japanese decoded
EXE and MAP (67,372-byte EXE and 677 ordered MZ relocations). Source-linked
CRT membership increases to **532/893** with **361** unchanged vendor
members and **160,332 original-equal CODE bytes**. Full raw OBJ/LIB/EXE/MAP
and writer logs remain retained in the source-bound receipt DAG.

As for some other Borland-vs-TASM members, the **literal ordered original
FIXUPP record sequence differs** even though the entire original logical
relocation population is exact. Full original Borland OMF record-program
serialization, packed-file source credit and Factory acceptance are not
claimed. No full cold replay was run.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after392_work.py vector-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after392_work -v
```
