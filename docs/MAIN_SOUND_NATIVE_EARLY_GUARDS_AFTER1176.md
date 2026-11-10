# PMD/MIDI and sound effects: native early-exit control

The complete `snd_kaja` and `snd_se` physical modules now express the
original control flow with natural early returns. The Kaja dispatcher
returns the incoming AX register if the audio driver is inactive; otherwise
it uses the same fixed PMD and MIDI software interrupt vectors, with byte
flag 1 alone selecting MIDI. A sound effect with no active predecessor is
selected immediately without reading the priority table. Frame-zero effect
playback and the short-circuited active-driver checks use natural truthiness,
while priority ordering, byte postincrement and duration behavior stay intact.

Original TC4/TLINK stage `af1176e` matched both modules across two compiler
rounds: 150 CODE bytes, 20 ordered native fields, three PUBLIC offsets,
complete Japanese MAIN loaded image and ordered MZ relocations. No runtime
DATA or 16-bit register/interrupt ABI was changed.

## Further natural split of the sound update gate (2026-11-10)

`snd_se_update()` now spells out the two independent reasons to skip the
PC-98 PMD service: inactive driver first, no selected effect second. In
native TC4 the two sequential early returns generate exactly the same
short-circuit branch sequence as the previous combined `||` condition.
The frame-zero INT 60h call, priority-indexed expiration and original
byte-frame postfix update do not change. Fresh scoped stage `af1311c`
recompiled **both** `snd_se` and unchanged `snd_kaja` in two original
TC4/TLINK rounds: 150 initialized CODE bytes, 20 ordered fixup fields,
three PUBLICs, complete normal Japanese MAIN image and ordered MZ relocation
vector are unchanged. This is scoped source proof, not whole-game ownership.
