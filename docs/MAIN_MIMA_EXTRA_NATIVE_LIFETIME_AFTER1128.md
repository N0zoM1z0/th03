# Mima Extra Attack: native six-slot loop lifetimes

The full `ex_mima` owner has natural `for` headers for all three six-slot
allocation, motion/collision and rendering passes. Each advances the original
near entity pointer with prefix `++p`; the allocation and rendering indices
initialize at first use in their loop headers. These changes preserve the
active bounce, signed velocity negation, flight transition and the distinct
byte-duration render path.

Original TC4/TLINK `af1128c` matched the complete 727 CODE bytes, 44 ordered
native fields and Japanese MAIN image/relocations twice. `af1128a` narrowed
all three index lifetimes together and changed CODE; isolated `af1128d`
confirmed that the update's signed `i` must retain its wider local lifetime.
The accepted pointer and outer-index changes stay.
