# Yumemi BOSS: attack phase exits and native rendering guards

The full `ba_yumem` owner now expresses ring and aimed-shot warmup as
independent early-return guards after the warning, with no change to random
selection or projectile emission. The complete intro state handles unfinished
frames with an early return; ring, aimed, cross and rain volleys use natural
remainder truth tests. The main renderer uses byte-state truthiness for
hit/mode checks and for the beam/circle distinction.

Original TC4/TLINK `af1130c` reproduced all 2,358 original CODE bytes, 343
ordered native fields and the Japanese MAIN image/relocations in two rounds.
At `af1130d`, replacing the original signed random-direction ternary with a
structured if/else changed native CODE, so its original source form remains.
