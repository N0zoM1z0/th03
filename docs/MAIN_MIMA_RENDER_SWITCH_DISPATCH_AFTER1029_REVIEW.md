# TH03 MAIN Mima renderer: switch-dispatch alternative

The 305-byte `mima_render_main()` now uses independent early-return `if`
guards for the hit, Particle, Expand, Flash and Trail paths. A natural
`switch(boss_render_mode)` rewrite was also tested in stage `af1029i`, keeping
the same case bodies and the Trail-to-Particle `goto`.

The complete `ba_mima` CODE comparison failed, so the switch form was reverted.
The original compiler does not emit the same instruction sequence for this
four-value mode dispatch when written as a switch. Keep the independent guards
from `af1029g`; their full-owner and MAIN-image comparison passes.
