// Source-native original Marisa full Bomb state-machine physical producer.
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
#include "src/main/player/chargeshot_marisa.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

extern SPPoint marisa_bomb_point;
// Existing hardware helper consumes BX as a VRAM offset.
extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

// Original Marisa Bomb: 64-frame full-screen palette flash followed by
// 64 frames of sprite movement and randomized explosions, then fade.
enum marisa_bomb_phase_t {
    MARISA_BOMB_PALETTE_END = 64,
    MARISA_BOMB_SHAKE_END = 128,
    MARISA_BOMB_EXPLOSION_PERIOD = 8,
    MARISA_BOMB_SPRITE_WIDTH = 48,
    MARISA_BOMB_SPRITE_HEIGHT = 48,
    MARISA_BOMB_SPRITE_OFFSET = 0xF16,
    MARISA_BOMB_SPRITE_ANIM_OFFSET = 6,
    MARISA_BOMB_SPRITE_CENTER_OFFSET = 24,
    MARISA_BOMB_PHASE_PALETTE_WHITE = 255,
    MARISA_BOMB_PHASE_PALETTE_STEP = 8,
};

void far marisa_bomb(void)
{
    unsigned char frame;
    unsigned char color;
    int left;
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    egc_off();
    frame = bomb_frame[pid_current];
    if(frame < MARISA_BOMB_PALETTE_END) {
        grcg_setcolor(GC_RMW, pid_current);
        // Real hardware ABI, not register allocation tuning: the existing
        // named helper consumes BX as a VRAM offset. Reference sub_B39E
        // calls sub_B37C, which copies BX to DI before filling VRAM.
        // Independently revalidate this caller/helper chain against target.
        _BX = 0x3932;
        if(pid_current) {
            _BX += 40;
        }
        bomb_bg_fill();
        grcg_off();
        color = 0 - (frame * 4);
        Palettes[pid_current].c.r = color;
        Palettes[pid_current].c.g = color;
        Palettes[pid_current].c.b = color;
        palette_changed = true;
    } else if(frame < MARISA_BOMB_SHAKE_END) {
        if((static_cast<unsigned int>(frame) % 2) != 0) {
            snd_se_play(16);
        }
        // The original bitmask must remain: equal-valued unsigned %4
        // was native-code-unequal in the two shake/sprite tests (af688d).
        if((frame & 3) < 2) {
            playfield_fg_shift_x[pid_current] = 4;
            left = 16;
        } else {
            playfield_fg_shift_x[pid_current] = -4;
            left = 8;
        }
        if(pid_current) {
            left += PLAYFIELD_W_BORDERED;
        }
        // TC4 caller-lowering compatibility, as in the maintained bomb owners.
        // Preserve the byte bool formal and zero-extend its word stack carrier;
        // this is not an AX-parameter ABI or a claim about original source text.
        mrs_put_noalpha_8(left, PLAYFIELD_TOP, pid_current + 2, (_AX = pid_current));
        if(!(frame % MARISA_BOMB_EXPLOSION_PERIOD)) {
            marisa_bomb_point.x.v = randring2_next16_mod(TO_SP(PLAYFIELD_W));
            marisa_bomb_point.y.v = randring2_next16_mod(TO_SP(PLAYFIELD_H));
            bomb_explosion_add(marisa_bomb_point.x.v, marisa_bomb_point.y.v, pid_current);
            marisa_bomb_point.x.v = playfield_fg_x_to_screen(marisa_bomb_point.x.v, pid_current);
            marisa_bomb_point.y.v = (marisa_bomb_point.y.v >> 4) + 16;
        }
    } else {
        playfield_fg_shift_x[pid_current] = 0;
        color = MARISA_BOMB_PHASE_PALETTE_WHITE - (frame * MARISA_BOMB_PHASE_PALETTE_STEP);
        Palettes[pid_current].c.r = color;
        Palettes[pid_current].c.g = color;
        Palettes[pid_current].c.b = color;
        palette_changed = true;
    }
    egc_on();
    if(frame < MARISA_BOMB_PALETTE_END || frame >= MARISA_BOMB_SHAKE_END) {
        return;
    }
    sprite16_put_size.set(MARISA_BOMB_SPRITE_WIDTH, MARISA_BOMB_SPRITE_HEIGHT);
    sprite16_clip.reset();
    sprite16_offset_t sprite_offset = pid.so_attack + MARISA_BOMB_SPRITE_OFFSET;
    if((frame & 3) < 2) {
        sprite_offset += MARISA_BOMB_SPRITE_ANIM_OFFSET;
    }
    sprite16_put(marisa_bomb_point.x.v - MARISA_BOMB_SPRITE_CENTER_OFFSET, marisa_bomb_point.y.v - MARISA_BOMB_SPRITE_CENTER_OFFSET, sprite_offset);
}
