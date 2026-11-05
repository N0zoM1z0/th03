# Original MAINL DOS INT 24h critical-error handler (after390)

The previously contextual Japanese `CL.LIB` member **harderr** (original
index 356) is now recovered in natural 8086 assembly at
`src/mainl/crt/harderr.asm`, complete with its **300 CODE** and **12 BSS**
bytes. The real interrupt entry saves/restores the interrupted registers and
original DOS error-action stack; four exported far CRT APIs occupy original
CODE offsets 84 (`___harderr`), 132 (`__harderr`), 180 (`__hardresume`) and
207 (`__hardretn`). The two callback types store their function pointers in
separate BSS words, with a shared saved interrupt SP and mode flag.

The original has **20 logical OMF relocations**: the interrupt entry's true
DGROUP segment, the four segment/offset operands used to install INT 24h, ten
BSS accesses and three far external calls (`_setvect`, `_bdos`). TASM50
reproduces the **complete original CODE payload, all 20 relocation fields,
public/import ABI, 12-byte BSS and exact original `08ff03ff02` GROUP record**.
The BSS-first `DGROUP` member order required declaring the group before
opening the BSS SEGDEF; moving it later silently reversed the group members
in native TASM output despite identical CODE. No original target byte arrays
or patched OMF are used.

The scoped native builder
`scripts/build_th03_mainl_after390_work.py dos-critical-error-boss` inherits
the validated 512-member after389 receipt without a new full cold replay. It
replaces the original member in both independent actual TASM/TLIB/TLINK
rounds, producing a **513/893 source-linked CRT**, with 380 untouched vendor
members and **159,721 bytes** of original-equal source CODE. Both fresh full
Japanese decoded `MAINL.EXE` and `.MAP` equal the originals byte-for-byte;
the EXE retains 67,372 bytes and 677 ordered DOS MZ relocations.

The raw original Borland vs TASM member **FIXUPP record chronology differs**;
we attest all 20 fields with their original frame values but do not claim
original member-program serialization. This working-source CRT milestone is
not a new packed-file unit or Factory source-acceptance decision.

Reproduce the verified local result:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after390_work.py dos-critical-error-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after390_work -v
```
