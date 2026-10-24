// One 664-byte native PLAYER_M producer in physical function order.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/player/lose.hpp"
#pragma samecodeseg playfield_fg_x_to_screen
#pragma option -G
#include "src/main/player/lose_update.inl"
#pragma option -G-
#include "src/main/player/lose_particle.inl"
#include "src/main/player/losedraw.inl"
#include "src/main/player/defeat.inl"
