// Existing player loss timer and round-state update.
void near pascal player_lose_anim_update(player_stuff_t near *player)
{
    if(player->lose_anim_time == 48) {
        player_lose_left = playfield_fg_x_to_screen(player->center.x.v, pid.current) - 24;
        player_lose_top = player->center.y.to_pixel() - 8;
        defeat_flag = DF_EXPLODE;
        snd_se_play(14);
        damage_all_on[1 - pid.current] = 1;
        player_lose_radius = 0;
    } else {
        player_lose_radius += 9;
    }
    // The original 8-bit alternating shake must retain the mask:
    // a typed %4 emitted different TC4 CODE (af706e).
    if((player->lose_anim_time & 3) < 2) {
        playfield_fg_shift_x[pid.current] = 6;
    } else {
        playfield_fg_shift_x[pid.current] = -6;
    }
    round_reset_flag = 2;
    player->lose_anim_time--;
    if(!player->lose_anim_time) {
        player_lose_left = 0;
        player_lose_top = 0;
        player_lose_radius = 0;
        playfield_fg_shift_x[pid.current] = 0;
        player->lose_anim_time = 255;
        PaletteTone = 100;
        palette_show();
        defeat_flag = DF_BANNER;
        players[1 - pid.current].rounds_won++;
        resident->pid_winner = 1 - pid.current;
        round_or_result_frame = 0;
        hud_static_rounds_won_put(1 - pid.current);
    } else {
        // The 30-level alternating loss flash is unsigned frame parity,
        // not a signed remainder on the count-down byte.
        PaletteTone = (static_cast<unsigned int>(round_or_result_frame) % 2) * 30 + 100;
        palette_show();
    }
}
