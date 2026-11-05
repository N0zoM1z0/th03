# Original strstreambuf underflow, NEC GOTOXY and far strnset — after424

Three previously contextual Japanese Borland `CL.LIB` members are now
maintained as natural 8086 source in `src/mainl/crt/`:
`srbuflow` (original index 849, **188 CODE bytes**), `cnecgtxy`
(index 541, **74 bytes**) and `fstrnset` (index 453, **58 bytes**).
The first is the complete C++ `strstreambuf::underflow` function, with
original get/put span checks, EOF returns, two distinct genuine far
`streambuf::setg` paths and the original 16-bit C++ ABI. The second is the
actual PC-98 `__NEC_GOTOXY` operation, with a physical 0000:071C/0710
cursor update and saved interrupt flags on the direct path, or genuine
NEC video service calls on the BIOS path; it preserves `retf 4` and the
frame distinctions for the video imports. The final member clips the
character count to the actual far string length and delegates to the
real far memory-fill helper, returning the original far pointer.

All **320 original CODE bytes** and all **eight logical OMF FIXUPP fields**
match the actual original members, including segment sizes, original
GROUPs, public offsets, ordered imports and individual frame/target/addend.
`cnecgtxy` also preserves all four *literal ordered* Borland FIXUPPs;
`srbuflow` and `fstrnset` emit the same logical fields in TASM's
ascending rather than Borland's descending record chronology. Neither
literal FIXUPP equality for those members nor full Borland OBJ serialization
is claimed. No original CODE byte arrays or binary patches are involved.

The after424 native builder validates its unchanged after423 source-bound
parent and runs two fresh TASM/TLIB/TLINK rounds, retaining full raw
OBJ/LIB/EXE/MAP and logs. Both complete Japanese decoded MAINL EXE/MAP
are byte-for-byte original-equal (67,372-byte EXE and 677 ordered DOS MZ
relocations). Working CRT reaches **620/893** source-linked original members
and **170,101 original-equal CODE bytes**, with **273** contextual vendor
members. This is not a full cold replay or Factory acceptance.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after424_work.py strstreambuf-nec-and-far-string
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after424_work -v
```
