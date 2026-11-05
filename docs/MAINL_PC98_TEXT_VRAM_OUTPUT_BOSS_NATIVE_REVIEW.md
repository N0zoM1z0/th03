# PC-98 text VRAM output and double-byte character boss — after396

Original Japanese Borland `CL.LIB` member **cnecputn** (index 544) is now
maintained in natural 8086 source at `src/mainl/crt/cnecputn.asm` with
complete **247 CODE** and **4 BSS** bytes. The four original near public
entries are `__NEC_RESET_VRAM_ACCESS` at CODE+0,
`__NEC_START_VRAM_ACCESS` at +11, `__NEC_END_VRAM_ACCESS` at +94, and
`__NEC_OUTPUT_CHAR` at +160. The source retains real PC-98 text VRAM
plane accesses, cursor character-width handling, two-byte Japanese character
conversion, original shared cursor pointer state and the actual `___row`,
`___col`, `__video`, `__wgarbage` import semantics.

Two initially tempting assumptions were **disproved** by the original
member's OMF: `__NEC_END_VRAM_ACCESS` tests the imported column byte
(`___col`) at CODE+111, not the row; and original external variables use
TARGET-style OMF frame method 5 while group-owned BSS state accesses use
explicit DGROUP-style frame method 1. Removing unjustified `DGROUP:`
overrides on external operands restored all **21 original literal ordered
FIXUPP fields**, including actual frame, site, target, width and addend.
The original BSS-first group record `08ff03ff02`, CODE payload, exported
API offsets, imported symbol order and true BSS boundary also match.
No original CODE byte arrays or patched OMF are involved; full Borland
library-member record serialization remains a separate unproved property.

Native source-linked producer
`scripts/build_th03_mainl_after396_work.py pc98-text-vram-output-boss`
inherits the unchanged after395 proof without a full cold replay and
performs two actual fresh TASM/TLIB/TLINK rounds. Both complete Japanese
decoded EXE/MAP are byte-for-byte original-equal, including the 67,372-byte
EXE with 677 ordered DOS MZ relocations. The working CRT reaches **537/893**
original-equal source members and **161,855 CODE bytes**, retaining **356**
original contextual vendor programs. Source/member ownership in the packed
file and Factory acceptance remain open.

Focused reproducibility:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after396_work.py pc98-text-vram-output-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after396_work -v
```
