// Lose update and particles at MAIN load C0D8..C248. Names are inferred.
#pragma codeseg PLAYER_M_TEXT main_01
#pragma option -G
#include "src/main/player/lose.hpp"
#pragma samecodeseg playfield_fg_x_to_screen

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
    if((player->lose_anim_time & 3) < 2) {
        playfield_fg_shift_x[pid.current] = 6;
    } else {
        playfield_fg_shift_x[pid.current] = -6;
    }
    round_reset_flag = 2;
    player->lose_anim_time--;
    if(player->lose_anim_time == 0) {
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
        PaletteTone = (round_or_result_frame & 1) * 30 + 100;
        palette_show();
    }
}


#pragma option -G-
void near pascal player_lose_particle_put(unsigned char angle_x, unsigned char angle_y)
{
    int left;
    int top;
    left = polar(player_lose_left, player_lose_radius, CosTable8[angle_x])
        + playfield_fg_shift_x[pid.current];
    top = polar(player_lose_top, player_lose_radius, SinTable8[angle_y]);
    sprite16_put(left, top, 0x34B4);
}
