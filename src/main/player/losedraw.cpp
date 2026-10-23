// Candidate renderer: original SI/DI preservation is still unresolved.
#pragma codeseg PLAYER_M_TEXT main_01
#pragma option -G-
#include "src/main/player/lose.hpp"

void near pascal player_lose_anim_render(player_stuff_t near *unused_player)
{
    unsigned char angle;
    register int i;
    sprite16_clip_set_for_pid(pid.current);
    sprite16_put_size.set(48, 48);
    for(i = 0, angle = player_lose_radius / 4; i < 16; i++, angle += 16) {
        player_lose_particle_put(angle, angle + 32);
    }
    for(i = 0, angle = 0 - (player_lose_radius / 4); i < 16; i++, angle += 16) {
        player_lose_particle_put(angle, angle - 32);
    }
    for(i = 0, angle = player_lose_radius / 4; i < 16; i++, angle += 16) {
        player_lose_particle_put(angle, angle);
    }
}
