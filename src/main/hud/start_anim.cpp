// Complete 688-byte TH03 round-intro state update candidate. All init,
// particle motion, randomized burst, polar phase, and exit paths are present.
#pragma codeseg PLAYER_M_TEXT main_01
#pragma option -a1
#include "src/main/hud/start_anim.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "src/main/math/randring_getters.hpp"
#include "src/main/math/polar.hpp"
#pragma option -a2

struct hud_start_particle_t {
    int x, y, velocity;
    unsigned char angle, active, turn_early, turn_late;
};
typedef char hud_start_particle_size10[(sizeof(hud_start_particle_t)==10)?1:-1];

extern hud_start_particle_t hud_start_particles[128];
extern hud_start_particle_t near *hud_start_particle_p;
extern unsigned char hud_start_flag;
extern unsigned char hud_intro_phase;
extern int hud_intro_frame;
extern int hud_intro_sprite;
extern int hud_intro_x;
extern int CosTable8[256], SinTable8[256];
extern "C" int far pascal IRand(void);

void near hud_start_anim_update(void)
{
    int speed_y;
    signed char turn;
    register int i;
    register int x;

    if(hud_start_flag == 1) {
        hud_intro_frame = 0;
        hud_start_particle_p = &hud_start_particles[0];
        x = -0x120;
        speed_y = 0x54;
        i = 0;
        for(; i < 16; i++, hud_start_particle_p++, speed_y++, x += 8) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = speed_y;
            hud_start_particle_p->velocity = 8;
            hud_start_particle_p->active = 1;
        }
        hud_intro_phase = 0;
        if(resident->game_mode == GM_STORY) {
            hud_intro_sprite = 0x16;
        } else {
            hud_intro_sprite = 0x1A;
        }
        hud_start_flag = 2;
        hud_intro_x = 0;
    }
    if(hud_intro_phase == 0) {
        hud_start_particle_p = &hud_start_particles[0];
        i = 0;
        for(; i < 16; i++, hud_start_particle_p++) {
            if(hud_start_particle_p->active != 0) {
                asm { mov bx, hud_start_particle_p }
                ((hud_start_particle_t near *)_BX)->x +=
                    ((hud_start_particle_t near *)_BX)->velocity;
                if(((hud_start_particle_t near *)_BX)->active == 1) {
                    if(((hud_start_particle_t near *)_BX)->x >= 0x60) {
                        ((hud_start_particle_t near *)_BX)->active = 2;
                    }
                } else {
                    if(hud_start_particle_p->x <= 0x40) {
                        hud_start_particle_p->x = 0x40;
                        hud_start_particle_p->active = 0;
                        if(i == 0) {
                            hud_intro_phase = 1;
                        }
                    } else {
                        hud_start_particle_p->velocity--;
                    }
                }
            }
        }
    } else if(hud_intro_phase == 1) {
        hud_intro_frame++;
        if(hud_intro_frame > 0x56) {
            hud_intro_phase++;
        }
    } else if(hud_intro_phase == 2) {
        hud_start_particle_p = &hud_start_particles[0];
        x = 0x600;
        i = 0;
        for(; i < 64; i++, hud_start_particle_p++, x += 0x20) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = randring1_next16_and(0x01FF) + 0x0A80;
            hud_start_particle_p->angle = static_cast<unsigned char>(randring1_next16());
            hud_start_particle_p->turn_early = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->turn_late = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->active = 1;
        }
        x = 0x1A00;
        i = 0;
        for(; i < 64; i++, hud_start_particle_p++, x += 0x20) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = randring1_next16_and(0x01FF) + 0x0A80;
            hud_start_particle_p->angle = static_cast<unsigned char>(randring1_next16());
            hud_start_particle_p->turn_early = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->turn_late = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->active = 1;
        }
        hud_intro_phase++;
        hud_intro_frame = 0;
    } else if(hud_intro_phase == 3) {
        hud_intro_frame++;
        if(hud_intro_frame >= 0x40) {
            hud_intro_phase++;
        }
        hud_start_particle_p = &hud_start_particles[0];
        i = 0;
        for(; i < 128; i++, hud_start_particle_p++) {
            if(hud_start_particle_p->active != 0) {
                asm { mov bx, hud_start_particle_p }
                x = polar(0, 80, CosTable8[((hud_start_particle_t near *)_BX)->angle]);
                speed_y = polar(0, 80, SinTable8[hud_start_particle_p->angle]);
                hud_start_particle_p->x += x;
                hud_start_particle_p->y += speed_y;
                if(
                    (hud_start_particle_p->x < 0) ||
                    (hud_start_particle_p->x >= 0x2700) ||
                    (hud_start_particle_p->y < 0) ||
                    (hud_start_particle_p->y >= 0x1800)
                ) {
                    hud_start_particle_p->active = 0;
                } else {
                    turn = (hud_intro_frame < 0x20)
                        ? hud_start_particle_p->turn_early
                        : hud_start_particle_p->turn_late;
                    turn--;
                    hud_start_particle_p->angle += (turn << 2);
                }
            }
        }
    } else {
        hud_start_flag = 0;
    }
}
