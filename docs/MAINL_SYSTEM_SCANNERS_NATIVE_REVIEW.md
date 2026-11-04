# TH03 Japanese MAINL original Borland `system`, `scanf` and `sscanf`

Three original selected large-model Borland CRT members have been recovered as
real 8086 assembly, preserving the native DOS environment and C-format scan
calling convention rather than substituting modern libc implementations:

| Original member | Slot | Original CODE | DATA | Public ABI |
| --- | ---: | ---: | ---: | --- |
| `system` | 377 | 385 | 19 | far `_system` at CODE+0 |
| `sscanf` | 288 | 136 | 0 | `_sscanf` +57, `_vsscanf` +96 |
| `scanf` | 280 | 39 | 0 | far `_scanf` at CODE+0 |

`src/mainl/crt/system.asm` reconstructs the entire COMSPEC lookup, DOS
command buffer construction, original C shell `c ` prefix, environment
handoff, allocation/error handling, and `__spawn`/`__DOSENV` near helpers.
The original DATA is three symbolic strings `COMSPEC`, `COMSPEC`, `c `
with terminators, not a copied executable byte array. `sscanf.asm` restores
both near string-scanning callbacks at original CODE+0 and +42 and its two
public far wrappers. `scanf.asm` preserves original `__streams`, `__Nfgetc`,
`__Nungetc` and near `__scanner` callback ABI. All source uses original 16-bit
near/far pointers, unchecked Borland behavior and original stack cleanup.

The original selected CRT member record identity was checked for **each**
slot. Normal TASM 5.0 `/m /mx /kh32768 /t` recompiles all **385/385 + 136/136
+ 39/39 CODE bytes** and all **19/19 initialized DATA bytes**. All publics,
ordered EXTDEFs, section classes, group order and **33/33 original relocation
sites, kinds, targets and addends** match. Original near helper TARGET frame5
versus TASM CODE frame0 remains bounded to five fields: `system` CODE+274
`__DOSENV` and +333 `__spawn`, `sscanf` CODE+87/+127 `__scanner`, and `scanf`
CODE+30 `__scanner`. Original versus TASM FIXUPP record order also differs;
we do **not** claim complete original OMF record identity or patch OBJ bytes.

`build_th03_mainl_after100_work.py system` and `system-scanners` start from
the retained original 100-source Japanese CRT, verifying the complete
source-bound 62→100 receipt DAG in topological order, and run **two independent
TASM/TLIB/TLINK native rounds each**. Both modes rebuild the original full
**67,372-byte decoded Japanese MAINL EXE and MAP byte-for-byte**, including
all **677 ordered MZ relocations**. Source-built CRT now totals **103 members
and 45,418 original-equal CODE bytes**, with the other **790 original vendor
member program records unchanged**.

Review: `review_th03_mainl_after100_work.py system-scanners` and
`tests.test_mainl_after100_work`. Full raw OBJ/LIB/EXE/MAP pairs, phase logs
and source/driver-hash-bound receipts are retained in
`.analysis/work/after100-system-scanners-*`. This is working-source evidence,
not additional formally accepted ledger credit. **No full cold replay ran.**
