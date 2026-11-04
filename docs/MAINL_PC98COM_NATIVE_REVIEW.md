# Original Japanese TH03 `pc98com`: ten-function PC-98 serial driver

The **actual selected** Borland CRT member **494**, `pc98com`, contains
**1,467 CODE / 55 initialized DATA / 54 uninitialized BSS bytes**, three
ordered external dependencies (`_getvect`, `_setvect`, `___nec_delay`), and
ten far public interfaces, original CODE offsets:

| CODE offset | Original public | Function |
| ---: | --- | --- |
| 468 | `_pc98cominit` | Interrupt/vector and serial port initialization |
| 923 | `_pc98comterm` | Restoration and termination |
| 998 | `_pc98comsend` | Send buffer and port state |
| 1067 | `_pc98comrecv` | Receive buffer and port state |
| 1208 | `_pc98comgetstat` | Read serial status |
| 1244 | `_pc98comsetstat` | Update serial status |
| 1267 | `_pc98comchkbuf` | Ring buffer inspection |
| 1322 | `_pc98comsendbreak` | Original break handling |
| 1367 | `_pc98comreset` | Reset serial parameters |
| 1422 | `_pc98comcheckbaud` | Check PC-98 baud divisor |

`src/mainl/crt/pc98com.asm` is natural 8086 source for the original
interrupt receive/transmit routines and all ten public PC-98 console serial
APIs, including original port I/O, 16-bit ring-buffer arithmetic, port flags
and stack handling. Initialized DATA is expressed as symbolic mode/control/
baud tables; BSS is explicitly uninitialized state at original offsets,
**not** artificially initialized zero bytes. There are no embedded original
machine-code CODE arrays or object patches.

An original ABI trap was caught, tested and corrected before linking: at
CODE+10 the interrupt handler loads the **DGROUP segment** into BP and then
DS, not the code `_TEXT` segment. Both encode a zero relocation placeholder
in the raw CODE, but using `seg _TEXT` emits the wrong OMF target-method
(`SEGDEF` vs the original `GRPDEF`) and would be semantically wrong after
linking. `mov bp,seg DGROUP` emits the **genuine original OMF GROUP target**.
The other local CODE segment and initialized DATA/BSS offsets were separately
verified. Operand ordering `xchg al,ch` was also required to emit the
original 8086 ModRM despite the semantically equivalent reversed spelling.

Native TASM 5.0 `/m /mx /kh32768 /t` reconstructs **all 1,467/1,467 CODE**
and **55/55 DATA** bytes, the **54-byte unmaterialized BSS**, ten original
publics, three ordered EXTDEFs and original `08ff03ff02` group. All
**130/130 OMF fixups agree with the original at every site, width, location
kind, target method, addend and frame method**, including CODE+10's GROUP
reference. The original compiler's FIXUPP **record sequence** differs from
TASM's, so original complete literal OMF program identity is **not** claimed.

`scripts/build_th03_mainl_after117_work.py pc98com` inherits both actual
source-bound 117-member Japanese CRT native rounds. Two independent TASM/
TLIB/TLINK rounds rebuild the entire **67,372-byte decoded Japanese MAINL
EXE and original MAP byte-for-byte**, preserving **all 677 ordered MZ
relocations** and **775 unchanged original vendor CRT member programs**.
Working-source CRT reaches **118 members / 57,276 original-equal CODE bytes**.
No full cold replay ran and no new accepted-ledger credit is asserted.

Proof: `review_th03_mainl_after117_work.py pc98com`,
`tests.test_mainl_after117_work`, and retained raw OBJ/LIB/EXE/MAP vector
pairs and tool writer logs under `.analysis/work/after117-pc98com-*` with
source-hash-bound native receipts.
