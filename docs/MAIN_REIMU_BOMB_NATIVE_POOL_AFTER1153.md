# Reimu Bomb and shared lifecycle: physical 32-slot controller

The shared Bomb lifecycle and Reimu's complete particle controller retain
their separate update, rendering and palette phases. Both live 32-slot
passes now advance the near particle pointer with a natural prefix `++`.
The render sprite offset initializes at first use, and named geometry
captures the exact clip boundary, respawn height, falling acceleration,
random initial velocity and sprite placement constants.

Original TC4/TLINK stage `af1153d` matches all 925 CODE bytes, 104 ordered
native fields and the Japanese MAIN image/relocations in both rounds.
Narrowing the renderer's `left` and `top` scratch into the live branch
(`af1153c`) changed CODE, so those existing locals retain their original
lifetime. The original EGC/GRCG and BX caller conventions are unchanged.
