# Original Japanese TH03 CRT `vappv`: 32-way vector call dispatcher

Selected original Borland large-model CRT member **138**, `vappv`, exports
`__vector_applyv_` at CODE+0. It consists of **848 CODE bytes**, zero DATA,
zero BSS and two distinct **32-word CODE tables**: a descriptor-type selector
table at CODE+720, and a relocatable handler-offset table at CODE+784.
The real 8086 function handles variant near/far descriptors, arguments,
indirect near and far function calls, type-code dispatch and failure via the
original far `_abort` import. This is a substantial algorithm/ABI module,
not a wrapper that simply forwards to another function.

The reconstructed `src/mainl/crt/vappv.asm` contains 306 real 8086
instructions with symbolic branch labels, 32 typed `dw` selector values and
32 genuine relocatable `dw handler` symbols, **not machine CODE byte arrays**.
TASM 5.0 `/m /mx /kh32768 /t` reproduces the original **848/848 complete
CODE bytes**, original public/export, `_abort` EXTDEF, `_BSS,_DATA` DGROUP
and all **34/34 original relocation sites, kinds, target names, addends and
frame methods**. The native FIXUPP record enumeration order differs from
Borland BCC's original; literal OMF program-record identity is **not** claimed.

A second, independent proof integrates this module in the **actual selected
original 893-member Japanese CRT library**, not simply a standalone vendor
object. `build_th03_mainl_after97_work.py lsetlocl-wild-vappv` produces two
complete original source-native TASM/TLIB/TLINK rounds on the retained
97-source Japanese carrier, with the already source-built 4,652-byte
`lsetlocl` and 795-byte `wild` modules in their original positions. Both
rounds reproduce the complete **67,372-byte decoded Japanese MAINL EXE and
original MAP byte-for-byte**, including all **677 ordered DOS MZ relocations**.

**Current working-source CRT: 100 members / 44,858 original-equal CODE
bytes**; the other **793 vendor CRT member records remain unchanged**.
These source-only native results do **not** grant formal accepted-ledger
credit or imply complete original OMF record equality, and no full cold
replay was performed.

Provenance: `scripts/review_th03_mainl_after97_work.py lsetlocl-wild-vappv`,
`tests.test_mainl_after97_work`, hash-bound native receipts and two raw
OBJ/LIB/EXE/MAP vectors under `.analysis/work/mainl-after97-*` and
`.analysis/work/after97-*`.
