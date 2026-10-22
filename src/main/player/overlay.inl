// Player glow and the four-frame charged-gauge ring.
void near pascal player_overlay_render(player_stuff_t near *player)
{
    screen_x_t left;
    vram_y_t top;
    int patnum;
    if(player->lose_anim_time) {
        return;
    }
    if(player->patnum_glow) {
        left = playfield_fg_x_to_screen(player->center.x.v, pid.current) - 16;
        top = (player->center.y.v >> (SUBPIXEL_BITS + 1)) - 8;
        patnum = player->patnum_glow;
        if(pid.current) {
            patnum += 9;
        }
        patnum += player->patnum_movement * 2;
        patnum += player->patnum_movement;
        super_put(left, top, patnum);
    }
    if(player->gauge_charged >= 0x100) {
        if(player->gauge_charged < 0x400) {
            patnum = 44;
        } else if(player->gauge_charged < 0x800) {
            patnum = 48;
        } else if(player->gauge_charged < GAUGE_MAX) {
            patnum = 52;
        } else {
            patnum = 56;
        }
        left = playfield_fg_x_to_screen(player->center.x.v, pid.current) - 16;
        top = (player->center.y.v >> (SUBPIXEL_BITS + 1)) - 15;
        patnum += (round_or_result_frame >> 2) & 3;
        super_put(left, top, patnum);
    }
}
