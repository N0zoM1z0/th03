// Candidate for the five MAIN_010 root procedures, load DA43..E0F7.
#pragma option -G
#include "src/main/player/state.hpp"
// These far APIs share MAIN_01; preserve their original far/Pascal contracts.
#pragma samecodeseg hitcircles_player_add
#pragma samecodeseg hud_static_halfhearts_put
#pragma samecodeseg hud_static_bombs_put
#pragma samecodeseg bomb_explosion_add
#include "src/main/player/update.inl"
#include "src/main/player/render.inl"
#include "src/main/player/overlay.inl"
#include "src/main/player/knock.inl"
#include "src/main/player/bomb.inl"
