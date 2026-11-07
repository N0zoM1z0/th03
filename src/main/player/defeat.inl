// Existing defeat banners and frame-dependent winner bounce.
void near round_defeat_banners_render(void)
{
    register int left;
    register int top;
    int frame_mod_32;
    left = round_defeated_player * 320 + 96;
    super_put(left, 40, 18);
    super_put(left + 64, 40, 19);
    left = (1 - round_defeated_player) * 320 + 96;
    // Winner banner bounces with exactly sixteen frames per half-cycle.
    frame_mod_32 = (static_cast<unsigned int>(round_or_result_frame) % 32);
    if(frame_mod_32 < 16) {
        top = frame_mod_32 + 32;
    } else {
        top = 64 - frame_mod_32;
    }
    super_put(left, top, 20);
    super_put(left + 64, top, 21);
}
