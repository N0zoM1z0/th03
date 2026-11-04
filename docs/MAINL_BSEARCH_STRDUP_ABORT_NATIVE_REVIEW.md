# Japanese MAINL original CRT search/allocate/abort recovery

Three previously untouched *selected* Borland large-model CRT members were
recovered from their actual original OMF records, not inferred from another
game or treated as recovered merely because standalone vendor OBJs existed:

| Member | Original library index | CODE | External dependencies | Relocations |
| --- | ---: | ---: | --- | ---: |
| `bsearch` | 198 | 125 | none (far comparator pointer supplied by caller) | 0 |
| `strdup` | 296 | 75 | `_memcpy`, `_strlen`, `_malloc` | 3 |
| `abort` | 2 | 20 | `_raise`, `__abort` | 2 |

`src/mainl/crt/bsearch.asm` reconstructs the complete original far-pointer
binary-search loop: unsigned remaining-count loop, 16-bit midpoint and signed
stride multiplication, indirect far comparison callback, signed comparator
result, and original return ABI. `strdup.asm` uses original far `_strlen`,
word-sized allocation and conditional far `_memcpy` and preserves unchecked
size behavior. `abort.asm` raises signal 22 then reaches the original runtime
abort fallback. All three are real symbolic 8086 assembly sources, without
embedded target code, padding, object patches or substituted code semantics.

Native TASM `/m /mx /kh32768 /t` builds reproduce **125/125, 75/75 and
20/20 original CODE bytes** respectively, including all public positions,
import order, zero DATA/BSS, segment layouts and five combined FIXUPP
locations/targets. `bsearch` has no relocations; the native literal OMF
program records for the other two are **not claimed identical** (compiler
metadata/field order differ from TASM).

`build_th03_mainl_after66_work.py strerror-bsearch-strdup-abort` extends the
retained complete 66-source Japanese original carrier. Two independent
TASM/TLIB/TLINK rounds replace these three members plus `strerror`, each at
its original index, and verify every other member program stays unmodified.
The complete original **67,372-byte decoded Japanese MAINL EXE** and original
**MAP** match byte-for-byte, including **677 ordered MZ relocations**. Working
source CRT is now **70 modules / 30,611 original-equal CODE bytes**; the
remaining **823** contextual vendor members are unchanged.

The two raw OBJ/LIB/EXE/MAP vectors, source-hash-bound receipts and phase logs
are retained in `.analysis/work/after66-strerror-bsearch-strdup-abort-*`.
Verification: `review_th03_mainl_after66_work.py` with the combined mode and
`tests.test_mainl_after66_work`. These are *working native source* results,
not newly accepted ledger credit; no full cold replay was run.
