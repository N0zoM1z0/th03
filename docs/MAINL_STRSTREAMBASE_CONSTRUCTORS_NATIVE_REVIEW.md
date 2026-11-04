# Original Japanese `strstreambase` constructors with native far adjustors

Two distinct actual selected CRT programs, **850 `srctr1`** and **851
`srctr2`**, have complete original Borland C++ 16-bit source. CODE is
**444 + 429 = 873 bytes**, with **20 initialized DATA bytes each**, empty
BSS, and original far `@strstreambase@$bctr$qncit1` / `$bctr$qv` PUBLICs.
Both implement the native `ios`/`strstreambuf` base-object construction,
far allocation, exception/ref-destructor registration and unchecked 16-bit
Borland ABI. Real `_TEXTA` source instructions are followed by one **12-byte
executable far destructor-adjustor thunk per module** and genuine
non-executable C++ RTTI descriptors for `strstreambase`, `strstreambuf`,
`ios`, and `streambuf`. Original 20-byte DATA unwind tables contain typed
relocatable far pointers. No original machine-CODE arrays, byte patches or
size padding are used.

Independent TASM 5.0 `/m /mx /kh32768 /t` reproduces **873/873 original CODE
bytes**, **40/40 DATA bytes**, original segment sizes/classes, ordered
nine imports and original PUBLIC offsets. **All 36 original OMF relocated
fields** match at native site, width, target, addend and frame method.
Original BCC and TASM FIXUPP **record ordering** is different; full original
OBJ byte identity is therefore not asserted.

`build_th03_mainl_after256_work.py strstreambase-constructors` extends the
source-bound 256-source Japanese CRT with both real selected original member
slots. **Two independent normal TASM/TLIB/TLINK rounds** reconstruct the
entire original **67,372-byte decoded Japanese MAINL EXE and MAP byte-for-
byte**, preserving all **677 ordered MZ relocations**, leaving **635
original vendor program records unchanged**. Working-source CRT reaches
**258 members and 96,065 original-equal CODE bytes**. This is working
source, not formally accepted-ledger promotion, and no full cold replay ran.

Proof: `review_th03_mainl_after256_work.py strstreambase-constructors`,
`tests.test_mainl_after256_work`, real native tool logs, and two source-bound
OBJ/LIB/EXE/MAP pairs retained under `.analysis/work/after256-*`.
