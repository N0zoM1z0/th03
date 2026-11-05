# Original PC-98 cursor hardware-control boss — after395

Recovered the complete Japanese Borland `CL.LIB` member **cneccrsr** (index
538) as maintained natural 16-bit ASM at `src/mainl/crt/cneccrsr.asm`. It
provides public far `___nec_setcursortype` at CODE+168 and the real
hardware-facing private helpers: ESC sequence output through NEC video
service, direct 60h/62h/5fh port handshaking with saved interrupt flags,
and the INT 18h cursor path. Source branches on actual screen height and
current video state rather than substituting a DOS PC simulator.

The original member contains **346 complete CODE bytes** and **12 initialized
DATA bytes** (`ESC[>5l\0` followed by `ESC[>5h\0`). Both bytestrings
are maintained as normal named data. An initial source reconstruction had the
two mode references backwards: original CODE relocation sites **193 →
DATA+6** and **200 → DATA+0** disprove that guess. A second original-vs-TASM
comparison exposed a swapped `DGROUP` record; declaring the BSS-first group
before the BSS SEGDEF reproduced original group record `08ff03ff02`.

Final TASM source matches the original full CODE and DATA payloads, all three
segment sizes (346/12/0), public/import interface and **all 7 literal
ordered FIXUPP fields**, including genuine frame/target/addend distinctions
for near video calls, original DGROUP data offsets and `__video+14`. No
embedded target byte arrays, post-assembly patches or relaxed fixup checks.
Full original Borland OMF member-record serialization is *not* claimed.

`scripts/build_th03_mainl_after395_work.py pc98-cursor-control-boss` reuses
the unchanged after394 native parent proof and assembles/relinks in two
fresh actual TASM/TLIB/TLINK rounds. Both complete decoded original Japanese
MAINL EXE and MAP reproduce byte-for-byte (EXE 67,372 bytes and 677 ordered
MZ relocations). The working-source CRT contains **536/893** members,
**161,608 original-equal CODE bytes**, and **357** unchanged vendor members.
Full source/driver/receipt-bound native OBJ/LIB/EXE/MAP rounds and writer logs
are retained; no full cold replay is performed. These source-linked CRT facts
do not grant new packed-file units or Factory acceptance.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after395_work.py pc98-cursor-control-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after395_work -v
```
