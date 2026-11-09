// Existing player loss timer and round-state update.
enum lose_native_t {
    LOSE_START_FRAME = 48,
    LOSE_START_LEFT = 24,
    LOSE_START_TOP = 8,
    LOSE_RADIUS_STEP = 9,
    LOSE_LAST_FRAME = 255,
    LOSE_PALETTE_NORMAL = 100,
    LOSE_PALETTE_FLASH = 30,
    LOSE_RESET_FRAMES = 2,
    LOSE_SOUND_EXPLOSION = 14,
};
void near pascal player_lose_anim_update(player_stuff_t near *player)
{
    if(player->lose_anim_time == LOSE_START_FRAME) {
        player_lose_left = playfield_fg_x_to_screen(player->center.x.v, pid.current) - LOSE_START_LEFT;
        player_lose_top = player->center.y.to_pixel() - LOSE_START_TOP;
        defeat_flag = DF_EXPLODE;
        snd_se_play(LOSE_SOUND_EXPLOSION);
        damage_all_on[1 - pid.current] = 1;
        player_lose_radius = 0;
    } else {
        player_lose_radius += LOSE_RADIUS_STEP;
    }
    // The original 8-bit alternating shake must retain the mask:
    // a typed %4 emitted different TC4 CODE (af706e).
    if((player->lose_anim_time & 3) < 2) {
        playfield_fg_shift_x[pid.current] = 6;
    } else {
        playfield_fg_shift_x[pid.current] = -6;
    }
    round_reset_flag = LOSE_RESET_FRAMES;
    player->lose_anim_time--;
    if(!player->lose_anim_time) {
        player_lose_left = 0;
        player_lose_top = 0;
        player_lose_radius = 0;
        playfield_fg_shift_x[pid.current] = 0;
        player->lose_anim_time = LOSE_LAST_FRAME;
        PaletteTone = LOSE_PALETTE_NORMAL;
        palette_show();
        defeat_flag = DF_BANNER;
        players[1 - pid.current].rounds_won++;
        resident->pid_winner = 1 - pid.current;
        round_or_result_frame = 0;
        hud_static_rounds_won_put(1 - pid.current);
    } else {
        // The 30-level alternating loss flash is unsigned frame parity,
        // not a signed remainder on the count-down byte.
        PaletteTone = (static_cast<unsigned int>(round_or_result_frame) % 2) * LOSE_PALETTE_FLASH + LOSE_PALETTE_NORMAL;
        palette_show();
    }
}
