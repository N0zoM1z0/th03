# Six complete native istream bulk/read, ignore, character-get and putback APIs

Six original Japanese Borland C++ iostream members have been reconstructed
as complete native 8086 source from their **actual pinned CL.LIB programs**,
not partial wrappers or serialized machine-code arrays. The full code
implements prefixed stream checks, virtual underflow/get, counted reads,
character extraction into three C++ character reference types, ignored
character scanning, and putback with the original ios state/error paths.

| Original member | Original CODE | Far public C++ method |
| --- | ---: | --- |
| `istread` (784) | 287 | `@istream@read$qnci` |
| `istign` (781) | 272 | `@istream@ignore$qii` |
| `istgpchr` (777) | 274 | `@istream@get$qmc` |
| `istgschr` (778) | 274 | `@istream@get$qmzc` |
| `istguchr` (780) | 274 | `@istream@get$qmuc` |
| `istpback` (783) | 205 | `@istream@putback$qc` |

All six original `_TEXTA` CODE payloads match **1,586 bytes in total**,
including the actual original far calling convention, near branches,
public offsets, zero DATA/BSS and DGROUP order `08ff02ff03`. Their **15
original imported far FIXUPP fields** are reproduced literally, including
site, frame, target, addend and the original *descending record order*.
That exact chronology is achieved with genuine `ORG` at actual imported
call instruction boundaries; no executable byte arrays, dummy filler or
post-link binary rewrite was used. Complete Borland OBJ program records
still differ in nonsemantic OMF metadata, and full original OBJ identity is
not claimed.

`scripts/build_th03_mainl_after366_work.py istream-read-ignore-get-putback`
inherits the **432-member** source/receipt-verified Japanese MAINL CRT,
rebuilds these six entire original objects, and reconstructs all **893
original library positions** with native TASM/TLIB/TLINK in **two independent
rounds**. Both reproduce the pinned **67,372-byte Japanese MAINL EXE and
full MAP byte-for-byte**, including all **677 ordered DOS MZ relocations**.
Working source now covers **438 complete original-equal CRT members**,
**455 unchanged contextual programs** and **139,421 source-compiled original-
equal CODE bytes**, an increase of **1,586 bytes**. Original and native raw
OBJ/LIB/EXE/MAP, writer logs, driver/parent/source SHA receipts and all
scoped validations are retained under `.analysis/work/after366-*`,
`scripts/review_th03_mainl_after366_work.py` and
`tests/test_mainl_after366_work.py`.

No full cold replay, formal Factory acceptance, canonical packed-file unit
credit or whole-game source exactness is claimed.
