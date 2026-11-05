# Twelve original DOS drive, video, MBCS and C++ ios ABI leaves — after416

Twelve previously contextual original Japanese Borland `CL.LIB` members now
link from maintained source in `src/mainl/crt/`: `dosgdriv`, `getdisk`,
`timecvt`, `ccomscrl`, `ccomscrn`, `MBSBTYPE`, `FMBSBTYP`, `stdec`, `sthex`,
`stoct`, `fgetpos` and `cputs`. Their complete **640 original CODE bytes**
cover original 16-bit DOS one-based drive selection, far file-time
conversion APIs, NEC/IBM scroll and move-line dispatch with Pascal near
stack cleanup, Japanese multibyte classification by actual byte offset,
C++ `ios` decimal/hex/octal base-mask manipulation, original far file
position retrieval and the conio string printer. This is not merely a
collection of empty stubs: the full code paths, near/far calls, imports and
public offset identities are maintained.

The old `src/mainl/crt/dosgdriv.asm` was **already a correct tracked
maintained source**, but the member was still contextual in the after415
CRT. We reassembled and independently compared its original CODE, GROUP,
ABI and zero FIXUPPs, then integrated it without overwriting a pinned
historical source. The remaining eleven members were newly authored.
Each is compared with the *active* Japanese original library member and
complete TASM output, not with a guessed CRT-name list.

All 12 native members reproduce complete original CODE, segment sizes,
GROUP records, public/import ABIs, and full logical OMF relocation
site/width/frame/target/addend values. **Four of twelve** reproduce literal
Borland FIXUPP record order: `dosgdriv` (zero sites), `MBSBTYPE`,
`FMBSBTYP` and `fgetpos`. The two drive wrappers, three ios manipulators
and video/move-line/console routines have original-versus-TASM record
chronology differences. A total of *five* near external calls additionally
use original Borland TARGET-frame method 5 versus TASM CODE-frame method 0:
`ccomscrl` CODE+35/+57, `ccomscrn` +32/+51 and `cputs` +30.
The scoped builder **normalizes only these five attested frame gaps** and
checks all remaining original fields exactly. An initial draft of
`ccomscrn` also took an equivalent but wrong one-byte `jmp` displacement;
we restored Borland's actual intermediate branch at CODE+53 rather than
normalizing a byte difference. Raw original library-member serialization
is not claimed equal for the batch.

`scripts/build_th03_mainl_after416_work.py` validates and reuses the
unchanged 591-member after415 source-bound CRT and runs two fresh actual
TASM/TLIB/TLINK producer rounds with all raw OBJ/LIB/EXE/MAP and writer
logs retained. Both whole decoded Japanese MAINL EXE and MAP remain
byte-for-byte original-equal (67,372-byte EXE, 677 ordered DOS MZ
relocations). Working CRT: **603/893 source-linked members**, **167,323
original-equal CODE bytes** and **290** untouched contextual vendor members.
No full cold replay, canonical packed-file credit or Factory accepted-source
claim has been made.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after416_work.py twelve-drive-video-mbcs-ios-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after416_work -v
```
