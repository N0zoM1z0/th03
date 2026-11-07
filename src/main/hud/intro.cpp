// MAIN load BB12..C0D8: one original-compiler producer for the full round intro.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/hud/intro.hpp"

// One original physical HUD intro TU owns the large particle update,
// drawing state machine and two low-level pixel/strip writers.
enum hud_intro_state_t {
    HUD_INTRO_STOPPED = 0,
    HUD_INTRO_RESET_REQUEST = 1,
    HUD_INTRO_RUNNING = 2,
    HUD_PHASE_SLIDE = 0,
    HUD_PHASE_BANNER = 1,
    HUD_PHASE_CREATE_STARS = 2,
    HUD_PHASE_MOVE_STARS = 3,
};
enum hud_intro_capacity_t {
    HUD_SLIDE_STRIPS = 16,
    HUD_STARS_PER_SIDE = 64,
    HUD_TOTAL_STARS = 128,
};
#include "src/main/hud/start_anim.inl"
#include "src/main/hud/start_lowlevel.inl"
#include "src/main/hud/start_render.inl"
