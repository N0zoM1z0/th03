# DOS launcher: exact PI and MRS cleanup before far execl

The complete 79-byte `execl` physical owner frees the primary PI slot,
releases the separate sprite/VRAM assets, resets the video and driver state,
and frees MRS archives 0 and 1 before the far-Pascal game shutdown and DOS
handoff. The PI slot is now a named compile-time constant, matching the
already-named MRS indices. Both MRS calls must remain separate: replacing
them with a loop changes the original instruction stream. The final
`execl` vararg is an explicit **far null pointer** (four bytes in the
original large memory model); an integer literal would change its ABI.

Stage `af1181b` matched 79 original CODE bytes, 11 ordered native fields,
the PUBLIC and complete Japanese MAIN image/relocations in both original
TC4/TLINK rounds.
