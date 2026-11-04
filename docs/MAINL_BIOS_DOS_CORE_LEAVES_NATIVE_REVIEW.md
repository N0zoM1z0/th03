# TH03 Japanese MAINL: twenty original low-level BIOS/DOS and CRT routines

Twenty distinct **selected original** Borland large-model CRT members have
complete authored symbolic 8086 source under `src/mainl/crt/`, covering
actual DOS/NEC PC-98 interrupts, video font services, BIOS clock and sound,
port memory and library conversion:

| Original slot | Member | Complete CODE | Original native function(s) |
| ---: | --- | ---: | --- |
| 84 | `longtoa` | 166 | Signed long conversion and unsigned conversion |
| 493 | `pc98clk` | 165 | PC-98 clock |
| 177 | `intr` | 164 | Far DOS interrupt register API |
| 547 | `cnecsond` | 151 | NEC PC-98 sound and silence |
| 490 | `dosvsfnt` | 119 | DOS/V set font |
| 484 | `dosvgfnt` | 119 | DOS/V get font |
| 325 | `ungetc` | 114 | Near `__Nungetc` and far `ungetc` |
| 505 | `pc98pfnt` | 65 | PC-98 user font output |
| 501 | `pc98gfnt` | 65 | PC-98 font reading |
| 473 | `bios_dsk` | 51 | IBM PC BIOS disk |
| 359 | `randblk` | 44 | Random block read/write |
| 100 | `poke` | 42 | Far memory poke and byte poke |
| 475 | `bios_key` | 41 | IBM PC BIOS keyboard |
| 98 | `parsfnm` | 41 | Parse filename |
| 483 | `dosvgenv` | 38 | DOS/V environment |
| 316 | `strupr` | 38 | Uppercase string |
| 479 | `biosequ` | 37 | BIOS equipment/memory/time |
| 99 | `peek` | 36 | Far memory peek and byte peek |
| 55 | `getcbrk` | 35 | DOS Ctrl-Break state read/write |
| 12 | `country` | 35 | DOS country information |

All source modules use genuine 8086 **instructions** with original register,
flag, stack, segment, and far/near ABI behavior; no executable machine-CODE
byte arrays, artificial padding, equivalent-but-different interrupt wrappers
or post-assembled OBJ patches. Source PUBLIC offsets and the actual original
per-member DGROUP membership are reviewed, including offset +55 for the
`pc98clk` public after its helper code, offset +130 for `__UTOA`, and the
combined two-interface `ungetc` CRT member.

Three original routines exposed an important source-code ABI trap: at CODE+108
in `intr`, `dosvsfnt`, and `dosvgfnt`, the original `FF 5E FC` is a **far
indirect call through a stack-resident pointer** (`FF /3`). Unqualified
`call [bp-4]` compiled to near `FF 56 FC` (`FF /2`), which is not the
original ABI even though the displacement and length match. The real source
now specifies `call dword ptr [bp-4]`; full original bytes agree naturally.

Each of the 20 selected native original CRT members reassembles under TASM
5.0 `/m /mx /kh32768 /t` to **all 1,566/1,566 original CODE bytes**, the
original public functions, exact empty initialized DATA/BSS/EXTDEF lists,
and its **literal original empty OMF FIXUPP inventory**. This is raw CODE and
relocation evidence, not a claim about byte identity of unrelated OMF record
classes.

`scripts/build_th03_mainl_after232_work.py bios-dos-core-leaves` inherits
the full source-bound original **232-source Japanese MAINL CRT**, and only
rebuilds these 20 selected slots in **two independent normal TASM/TLIB/TLINK
rounds**. Both reproduce the whole **67,372-byte decoded original Japanese
MAINL EXE and MAP byte-for-byte**, retaining **677 ordered original MZ
relocations** and **641 unchanged vendor CRT member programs**. Working
source CRT is now **252 genuine source members and 93,470 original-equal
CODE bytes**. The formal accepted ledger is unaffected and no full cold
replay was run.

Proof: `review_th03_mainl_after232_work.py bios-dos-core-leaves`,
`tests.test_mainl_after232_work` and the source/driver/parent-hash-bound
original OBJ/LIB/EXE/MAP vector pairs and writer logs retained under
`.analysis/work/after232-*` and `.analysis/work/mainl-after232-*`.
