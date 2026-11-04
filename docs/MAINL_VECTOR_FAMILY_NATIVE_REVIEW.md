# Japanese Borland vector apply/new/delete: four native source algorithms

Four real selected CRT members join the earlier fully recovered `vappv`
32-way vararg dispatch engine. All four contain complete symbolic 8086
algorithms, genuine 16-bit stack/near/far calls, and relocatable code tables:

| Original slot | Full module | CODE | Switch selectors / handler pointers |
| ---: | --- | ---: | ---: |
| 137 | `vapp` (`__vector_apply_`) | 674 | 32 / 32 |
| 140 | `vdelf` (`@_vector_delete_$qnvuiuluie`) | 657 | 16 / 16 |
| 145 | `vnewf` (`@_vector_new_$qnvuiuluie`) | 707 | 16 / 16 |
| 148 | `vnewvf` (`@_vector_vnew_$qnvuiuluie`) | 786 | 16 / 16 |

The source recovers original callback ABI, type-dependent near/far function
calls, 16-bit element-stride and arithmetic helpers `N_LXMUL@`, `N_LMOD@`,
`__AHSHIFT`, Borland vector allocation/deallocation, abort paths and
exception destructor count. The 80 total handler-table pointers are genuine
symbolic `dw` labels; executable CODE is ordinary `8086` instructions, **not
copied machine byte arrays**, patched OBJ streams or artificial padding.

The actual selected Japanese CRT slot and native original OMF were verified
for each module, not assumed from earlier documentation or a separate game.
Normal TASM `/m /mx /kh32768 /t` exactly reproduces all original **674 +
657 + 707 + 786 = 2,824 CODE bytes**, all public offsets, ordered imports,
zero DATA/BSS, and the original BSS/DATA GROUP. It emits **108/108** original
relocation *sites, targets, widths, addends and kinds*. `vapp` also matches
all frame methods for its 34 fields. Seven near helper frames differ:
`vdelf` CODE+167 uses original TARGET frame5 versus TASM CODE frame0;
`vnewf` and `vnewvf` have the analogous difference at CODE+152/+203/+272.
Compiler versus TASM FIXUPP record ordering is likewise different, so
full original native OBJ-record identity is deliberately **not claimed**.

`scripts/build_th03_mainl_after112_work.py vector-family` starts from the
retained original Japanese **112-source CRT** and normally recompiles all
four selected native member slots, producing **two independent TASM/TLIB/TLINK
rounds**. Both reconstruct the **entire 67,372-byte original decoded Japanese
MAINL EXE and original MAP byte-for-byte**, including **all 677 ordered MZ
relocations**. The working library has **116 source members and 54,370
original-equal CODE bytes**, leaving all **777** other vendor member programs
untouched. This is working-source evidence, **not** formally accepted-ledger
credit or whole-game source ownership. No full cold replay ran.

Evidence: `scripts/review_th03_mainl_after112_work.py vector-family`,
`tests.test_mainl_after112_work`, the retained source/driver-hash-bound
receipts and two raw OBJ/LIB/EXE/MAP vectors with writer logs under
`.analysis/work/mainl-after112-*` and `.analysis/work/after112-*`.
