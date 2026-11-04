# Original Japanese TH03 MAINL `ostint`: signed and unsigned long ostream

Selected original Borland large-model CRT member **813**, `ostint`, exports
the two far C++ `ostream` long-integer insertion methods at original CODE
+242 (`@ostream@$blsh$ql`) and +618 (`@ostream@$blsh$qul`). The **entire
884-byte `_TEXTA` CODE** and **54-byte initialized `_DATA`** are recovered in
`src/mainl/crt/ostint.asm` as genuine symbolic 8086 code, near/far ABI and
human-readable format data. The module owns zero BSS and four ordered
original imports: `ostream::outstr`, `F_LUMOD@`, `F_LUDIV@`, `F_LXURSH@`.

The original format DATA contains both lower/upper hex-digit lookup strings,
`+`/`-` signs and the original `0`, `0X`, `0x` prefix combinations. There
are no original executable CODE byte arrays, binary patches or artificial
padding. The native TASM lexer is case-insensitive: the initial symbolic
labels `prefix_0X` and `prefix_0x` collided, but distinct descriptive
`prefix_hex_upper`/`prefix_hex_lower` symbols reproduce the original offsets
naturally, with the actual capitalized and lowercase text preserved.

Native TASM `/m /mx /kh32768 /t` reproduces **884/884 original CODE bytes**
and **54/54 DATA bytes**, both original C++ public entry offsets, the native
`_TEXTA,_DATA,_BSS` segment structure and `08ff02ff03` DGROUP membership,
and all **17/17 original OMF fixup sites, location kinds, target methods,
addends, widths and frame methods**. Original BCC FIXUPP *record order*
differs from native TASM; complete original literal OMF record identity is
explicitly **not** claimed.

**Provenance and actual linked product:** `build_th03_mainl_after118_work.py
ostint` extends the complete selected 118-source Japanese CRT (including the
previous large `istelng` and ten-function PC-98 serial driver) by replacing
only original slot 813. Two independent normal TASM/TLIB/TLINK rounds
reproduce the **entire 67,372-byte original decoded Japanese MAINL EXE and
MAP byte-for-byte**, preserving all **677 ordered MZ relocations** and the
other **774 untouched original vendor program records**. Working-source CRT
is now **119 members and 58,160 original-equal CODE bytes**. No formal
accepted-ledger credit is claimed; no full cold replay was run.

## Verification bottleneck corrected without weakening the evidence

The first 119-source link rounds completed successfully, but reviewing
repeatedly called every parent `retained()`/`review_parent()` recursively,
which multiplied prior checked work and eventually timed out. This is not a
source or native-link failure. The driver now checks the complete original
**62→118-source receipt DAG in one topological pass**, validating each
unchanged ancestor's raw OBJ/LIB/EXE/MAP vectors, exact selected program
positions, original target EXE/MAP, source/driver/parent hashes, literal
original profiles and actual Borland tool phase logs. The full local DAG
validation completes in seconds instead of recursively recomputing earlier
proofs. After changing the driver, both **119-source native rounds were
rerun**, so their receipts bind the current source and driver, not a stale
hash. This is a scoped rebuild, **not** a cold replay.

Verification entry points: `review_th03_mainl_after118_work.py ostint` and
`tests.test_mainl_after118_work`. Raw native OBJ/LIB/EXE/MAP pairs, actual
writer logs and source-bound receipts are retained under
`.analysis/work/after118-ostint-*` and `.analysis/work/mainl-after118-*`.
