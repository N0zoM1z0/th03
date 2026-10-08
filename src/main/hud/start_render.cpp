// Complete natural C++ candidate for the original 635-byte round intro
// renderer at TH03 0x0BE5D..0x0C0D8. Both PC-98 low-level sprite/VRAM
// helpers are near Pascal dependencies with independently bounded bodies.
#pragma codeseg PLAYER_M_TEXT main_01
#pragma option -a1
#include "src/main/hud/start_render.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#pragma option -a2

struct hud_start_particle_t {
    int x, y, velocity;
    unsigned char angle, active, turn_early, turn_late;
};
typedef char hud_render_particle_size10[(sizeof(hud_start_particle_t)==10)?1:-1];

extern hud_start_particle_t hud_start_particles[128];
extern hud_start_particle_t near *hud_start_particle_p;
extern unsigned char hud_start_flag;
extern unsigned char hud_intro_phase;
extern int hud_intro_frame;
extern int hud_intro_sprite;
extern int hud_intro_x;
extern int hud_intro_destination_x;
extern unsigned char round_id;

void near hud_start_anim_render(void)
{
    register int i;
    if(hud_start_flag == 0) {
        return;
    }
    if(hud_intro_phase == 0) {
        grcg_setcolor(GC_RMW, 15);
        hud_start_particle_p = &hud_start_particles[0];
        i = 0;
        for(; i < 16; i++, hud_start_particle_p++) {
            hud_start_sprite_strip_put(hud_start_particle_p->x,
                hud_start_particle_p->y, hud_intro_sprite, i);
            hud_start_sprite_strip_put(hud_start_particle_p->x + 0x20,
                hud_start_particle_p->y, hud_intro_sprite + 1, i);
            hud_start_sprite_strip_put(hud_start_particle_p->x + 0x40,
                hud_start_particle_p->y, hud_intro_sprite + 2, i);
            hud_start_sprite_strip_put(hud_start_particle_p->x + 0x60,
                hud_start_particle_p->y, hud_intro_sprite + 3, i);
            hud_start_sprite_strip_put(0x220 - hud_start_particle_p->x,
                hud_start_particle_p->y, hud_intro_sprite + 3, i);
            hud_start_sprite_strip_put(0x200 - hud_start_particle_p->x,
                hud_start_particle_p->y, hud_intro_sprite + 2, i);
            hud_start_sprite_strip_put(0x1E0 - hud_start_particle_p->x,
                hud_start_particle_p->y, hud_intro_sprite + 1, i);
            hud_start_sprite_strip_put(0x1C0 - hud_start_particle_p->x,
                hud_start_particle_p->y, hud_intro_sprite, i);
        }
        hud_intro_x = hud_intro_destination_x;
        grcg_off();
    } else if(hud_intro_phase == 1) {
        // Original TC4 control flow places versus first, story second.
        if(resident->game_mode != GM_STORY) {
            if((hud_intro_frame >= 0x18) && (hud_intro_frame < 0x40)) {
                super_put(208, 84, round_id + 34);
                super_put(544, 84, round_id + 34);
            } else if(hud_intro_frame == 0x40) {
                hud_intro_x = 96;
                hud_intro_sprite = 30;
            }
        } else {
            if((hud_intro_frame >= 0x18) && (hud_intro_frame < 0x38)) {
                super_put(208, 84, resident->story_stage + 34);
                super_put(544, 84, resident->story_stage + 34);
            } else if(hud_intro_frame == 0x38) {
                hud_intro_x = 96;
                hud_intro_sprite = 30;
            }
        }
        super_put(hud_intro_x, 84, hud_intro_sprite);
        super_put(hud_intro_x + 32, 84, hud_intro_sprite + 1);
        super_put(hud_intro_x + 64, 84, hud_intro_sprite + 2);
        super_put(hud_intro_x + 96, 84, hud_intro_sprite + 3);
        super_put(hud_intro_x + 320, 84, hud_intro_sprite);
        super_put(hud_intro_x + 352, 84, hud_intro_sprite + 1);
        super_put(hud_intro_x + 384, 84, hud_intro_sprite + 2);
        super_put(hud_intro_x + 416, 84, hud_intro_sprite + 3);
    } else if(hud_intro_phase == 3) {
        grcg_setcolor(GC_RMW, 15);
        asm {
            mov ax, 0A800h
            mov es, ax
        }
        hud_start_particle_p = &hud_start_particles[0];
        i = 0;
        for(; i < 128; i++, hud_start_particle_p++) {
            if(hud_start_particle_p->active != 0) {
                // Preserve the original near Pascal device helper ABI.
                // These are symbolic operations; no raw instruction blobs.
                asm {
                    mov bx, hud_start_particle_p
                    push word ptr [bx]
                    push word ptr [bx+2]
                    call near ptr hud_start_particle_pixel_put
                }
            }
        }
        grcg_off();
    }
}
