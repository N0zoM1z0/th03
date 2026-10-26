// Contiguous player core and stage-shot preparation: D6D4..E313.
// Complete functions share one native record stream; no synthetic prefix.
#pragma codeseg MAIN_010_TEXT main_01
#pragma option -a1
#include "src/main/player/state.hpp"
#include "src/main/player/shotroot.hpp"
#pragma option -a2

#pragma option -G- -a2
#pragma option -G
#include "src/main/player/move.inl"
#pragma option -G- -a2
#include "src/main/player/hyper.inl"
#pragma option -G- -a2
#include "src/main/player/state.inl"
#pragma option -G- -a2
#include "src/main/player/stuff.inl"
#pragma option -G- -a2
#include "src/main/player/shot_sprites.inl"
