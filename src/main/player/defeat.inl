// Existing defeat banners and frame-dependent winner bounce.
enum lose_banner_t {
    LOSE_BANNER_PLAYER_STRIDE = 320,
    LOSE_BANNER_LEFT = 96,
    LOSE_BANNER_TOP = 40,
    LOSE_BANNER_PANEL_STEP = 64,
    LOSE_BANNER_BOUNCE_PERIOD = 32,
    LOSE_BANNER_BOUNCE_HALF = 16,
    LOSE_BANNER_BOUNCE_BASE = 32,
    LOSE_BANNER_BOUNCE_PEAK = 64,
    LOSE_BANNER_LEFT_CEL = 18,
    LOSE_BANNER_RIGHT_CEL = 19,
    LOSE_BANNER_WIN_CEL = 20,
    LOSE_BANNER_WIN_NEXT = 21,
};
void near round_defeat_banners_render(void)
{
    register int left;
    register int top;
    left = round_defeated_player * LOSE_BANNER_PLAYER_STRIDE + LOSE_BANNER_LEFT;
    super_put(left, LOSE_BANNER_TOP, LOSE_BANNER_LEFT_CEL);
    super_put(left + LOSE_BANNER_PANEL_STEP, LOSE_BANNER_TOP, LOSE_BANNER_RIGHT_CEL);
    left = (1 - round_defeated_player) * LOSE_BANNER_PLAYER_STRIDE + LOSE_BANNER_LEFT;
    // Winner banner bounces with exactly sixteen frames per half-cycle.
    int frame_mod_32 = (static_cast<unsigned int>(round_or_result_frame) % LOSE_BANNER_BOUNCE_PERIOD);
    if(frame_mod_32 < LOSE_BANNER_BOUNCE_HALF) {
        top = frame_mod_32 + LOSE_BANNER_BOUNCE_BASE;
    } else {
        top = LOSE_BANNER_BOUNCE_PEAK - frame_mod_32;
    }
    super_put(left, top, LOSE_BANNER_WIN_CEL);
    super_put(left + LOSE_BANNER_PANEL_STEP, top, LOSE_BANNER_WIN_NEXT);
}
