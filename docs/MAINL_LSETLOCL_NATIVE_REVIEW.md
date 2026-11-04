# Original Japanese TH03 MAINL locale-library manager: 4,652-byte Boss

`src/mainl/crt/lsetlocl.asm` reconstructs original selected Borland
large-model CRT member **248**. It is a complete **4,652 CODE / 59 initialized
DATA / zero BSS** source unit exporting **eleven** original functions:
`__lsetlocale` (+0), `___open_localelib` (+1805),
`___open_locale` (+2027), `___find_localecat` (+2247),
`___set_localestring_locale` (+2516), `___locale_error` (+2698),
`___read_localecat` (+2814), `___read_localeenv` (+3441),
`___find_localelib` (+3573), `___delete_locale` (+3825) and
`___dup_locale` (+3960). All 29 original ordered imports and the complete
original `_TEXT/_DATA/_BSS` segment sizes and `_BSS,_DATA` group are retained.

This is a **large multifunction CRT** unit for dynamic locale-file opening,
loading, lookup and deletion, locale category/error construction, environment
search, and 16-bit far memory/string ownership. Its executable CODE is
recovered as 1,660 genuine symbolic 8086 instructions with named branch
labels, **not** embedded original CODE bytes or object patches. Two original
CODE dispatch tables have been reconstructed as relocatable label references:
**15 entries at CODE+1775 and 7 entries at +3427**. The original first
branch indexes the first table at base **+14**, a detail established from the
original relocation addend rather than guessed from adjacent code. DATA
contains actual text strings for C locale category specifications, a `%s;...`
format and `LANG`, at their original offsets 0/14/16/30/32/54.

The source also preserves original near helper and far-function call forms;
scoped zero-byte `ASSUME CS:NOTHING` avoids TASM rewriting the original
internal *far* calls into shorter `PUSH CS` plus near `CALL` forms. The BCC
source's 16-bit calling convention, unchecked pointer arithmetic and original
ordinal CODE public offsets are preserved rather than modernized.

**Native original selected-member evidence:**

- **4,652/4,652 CODE bytes**, **59/59 DATA bytes**, original 11 PUBLIC offsets,
  original ordered 29 EXTDEF symbols, segment and group identities.
- **227/227** original OMF relocation sites, widths, targets, addends and
  modes; all **22 table pointers** use symbolic original CODE labels.
- **224/227** also match frame metadata; the only three frame discrepancies
  occur at CODE+4231/+4329/+4427: original BCC uses TARGET frame5 for near
  `N_LDIV@` helper calls while native TASM uses CODE frame0. Compiler versus
  TASM literal FIXUPP ordering also differs. No literal native-OBJ record
  identity is claimed or manufactured with byte edits.

`scripts/build_th03_mainl_after97_work.py lsetlocl` reuses the complete
hash-bound **97-source original Japanese MAINL carrier**, performing actual
source assembly, complete 893-member library reconstruction and full normal
link in **two independent TASM/TLIB/TLINK rounds**. Every prior selected
source member and the **795 remaining vendor program records** are checked
unchanged. Both rounds exactly reproduce the complete original **67,372-byte
decoded Japanese MAINL EXE** and its **MAP**, including all **677 ordered
MZ relocations**. Working source CRT reaches **98 members** and **43,215
original-equal CODE bytes**. This remains **working-source evidence**, not
additional formal accepted-ledger credit or proof of whole-game source
completion.

Raw native OBJ/LIB/EXE/MAP vectors, source-bound receipts and original tool
phase logs remain under `.analysis/work/after97-lsetlocl-*` and
`.analysis/work/mainl-after97-lsetlocl-*`; reviewer:
`review_th03_mainl_after97_work.py lsetlocl`, regressions:
`tests.test_mainl_after97_work`. **No complete cold replay** was performed.
