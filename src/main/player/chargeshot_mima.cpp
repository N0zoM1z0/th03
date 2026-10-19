// Natural semantic hypothesis, not historical source or compiled exactness.
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
#include "src/main/player/mima_gameplay.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
// Observed MAIN_04 code-group relationship; neither function changes ABI.
#pragma samecodeseg bullets_add
#pragma samecodeseg randring_far_next16_and

void far pascal mima_chargeshots_reset(void)
{
    mima_chargeshot_p = &mima_chargeshots[0][0];
    for(int i = 0; i < 30; i++, mima_chargeshot_p++) {
        mima_chargeshot_p->active = 0;
    }
}
void far pascal chargeshot_add_mima(Subpixel center_x, Subpixel center_y)
{
    mima_chargeshot_p = &mima_chargeshots[pid.current][0];
    mima_chargeshot_active[pid.current] = 1;
    mima_chargeshot_frame[pid.current] = 0;
    mima_chargeshot_p->active = 1;
    for(int i = 0; i < 15; i++, mima_chargeshot_p++) {
        if(i != 0) {
            mima_chargeshot_p->active = 0;
        }
        mima_chargeshot_p->x.v = center_x.v;
        mima_chargeshot_p->y.v = center_y.v;
        vector2(mima_chargeshot_p->velocity_x, mima_chargeshot_p->velocity_y,
            mima_chargeshot_angles[i % 6], 176);
        mima_chargeshot_p->unknown_1 = 0;
    }
}
void near pascal mima_chargeshot_activate(unsigned char player, unsigned char slot)
{
    mima_chargeshot_p = &mima_chargeshots[player][slot];
    mima_chargeshot_p->active = 1;
    mima_chargeshot_p->x.v = players[player].center.x.v;
    mima_chargeshot_p->y.v = players[player].center.y.v;
    snd_se_play(13);
}
void far pascal chargeshot_update_mima(void)
{
    unsigned char frame;
    if(mima_chargeshot_active[pid_current] != 0) {
        playfield_clip_negative_radius.x.v = -TO_SP(16);
        playfield_clip_negative_radius.y.v = -TO_SP(16);
        mima_chargeshot_p = &mima_chargeshots[pid_current][0];
        frame = ++mima_chargeshot_frame[pid_current];
        for(int i = 0; i < 15; i++, mima_chargeshot_p++) {
            if(mima_chargeshot_p->active == 0) {
                continue;
            }
            mima_chargeshot_p->x.v += mima_chargeshot_p->velocity_x;
            mima_chargeshot_p->y.v += mima_chargeshot_p->velocity_y;
            if(playfield_clip(mima_chargeshot_p->x, mima_chargeshot_p->y)) {
                mima_chargeshot_p->active = 0;
                if(i == 14) {
                    mima_chargeshot_active[pid_current] = 0;
                }
            }
        }
        if(frame < 60 && (frame % 4) == 0) {
            mima_chargeshot_activate(pid_current, frame / 4);
        }
        players[pid_current].gauge_charged = 0;
    }
}
uint8_t far chargeshot_hittest_mima(void)
{
    unsigned char hits;
    if(mima_chargeshot_active[hitbox.pid] == 0) {
        return 0;
    }
    hits = 0;
    mima_chargeshot_p = &mima_chargeshots[hitbox.pid][0];
    for(int i = 0; i < 15; i++, mima_chargeshot_p++) {
        if(mima_chargeshot_p->active == 0) {
            continue;
        }
        if(mima_chargeshot_p->x.v - TO_SP(16) <= hitbox.right.v &&
           mima_chargeshot_p->x.v + TO_SP(16) >= hitbox.origin.topleft.x.v &&
           mima_chargeshot_p->y.v >= hitbox.origin.topleft.y.v &&
           mima_chargeshot_p->y.v <= hitbox.bottom.v) {
            hitcircles_enemy_add(mima_chargeshot_p->x.v, mima_chargeshot_p->y.v, hitbox.pid);
            hits++;
        }
    }
    return hits;
}
void near pascal mima_chargeshot_sprite_put(int x, int y, int sprite_offset)
{
    x = playfield_fg_x_to_screen(x, pid_current) - 16;
    y = (y >> 4) + 8;
    sprite16_put(x, y, sprite_offset);
}
void far pascal chargeshot_render_mima(void)
{
    sprite16_offset_t sprite_offset;
    if(mima_chargeshot_active[pid_current] != 0) {
        mima_chargeshot_p = &mima_chargeshots[pid_current][0];
        sprite16_clip_set_for_pid(pid_current);
        sprite_offset = pid.so_attack + 0x10;
        sprite16_put_size.set(32, 16);
        for(int i = 0; i < 15; i++, mima_chargeshot_p++) {
            if(mima_chargeshot_p->active == 0) {
                continue;
            }
            mima_chargeshot_sprite_put(mima_chargeshot_p->x.v,
                mima_chargeshot_p->y.v, (i % 3) * 4 + sprite_offset);
        }
    }
}
void near pascal gauge_pattern_mima(unsigned int type)
{
    unsigned char pid_other;
    unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
    if(type == BT_BULLET16_DEFAULT) {
        flag_expected = flag_expected + GBAF_PELLET_TO_BULLET;
    }
    if(gba_flag_active[pid_current] == flag_expected) {
        mima_gauge_angle_step[pid_current] = randring_far_next16_and(1) == 0 ? 249 : 7;
        mima_gauge_angle[pid_current] = 64;
        mima_gauge_frame[pid_current] = 0;
        gba_flag_active[pid_current]++;
        gauge_pattern_timing[pid_current].total_frames = gba_gauge_level[pid_current] + 38;
        gauge_pattern_timing[pid_current].byte_1 = gba_gauge_level[pid_current] * 2 + 24;
        return;
    }
    if(gba_flag_active[pid_current] != flag_expected + 1) {
        return;
    }
    pid_other = 1 - pid_current;
    if((mima_gauge_frame[pid_current] % 8) == 0) {
        bullet_template.type = static_cast<bullet_type_t>(type);
        if(mima_gauge_angle_step[pid_current] > 7) {
            bullet_template.center.x.v = TO_SP(32);
        } else {
            bullet_template.center.x.v = TO_SP(256);
        }
        bullet_template.center.y.v = TO_SP(16);
        bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;
        bullet_template.pid = pid_other;
        bullet_template.angle = mima_gauge_angle[pid_current];
        bullet_template.is_animated = 0;
        bullet_template.group = BG_5_SPREAD_NARROW;
        bomb_center_add(bullet_template.center.x.v, TO_SP(16), pid_other);
        bullets_add();
        if((mima_gauge_frame[pid_current] % 16) != 0) {
            bullet_template.group = BG_RING;
            bullet_template.count = gauge_pattern_timing[pid_current].total_frames;
            bullet_template.speed.v = TO_SP(3) + 6;
            bomb_center_add(bullet_template.center.x.v, TO_SP(16), pid_other);
            bullets_add();
        }
        mima_gauge_angle[pid_current] += mima_gauge_angle_step[pid_current];
        bullet_template.is_animated = 1;
    }
    if(mima_gauge_frame[pid_current] > 64) {
        gba_flag_active[pid_current] = GBAF_NONE;
        palette_restore_for_pid(pid_other);
    }
    mima_gauge_frame[pid_current]++;
}
void far gba_gauge_pattern_pellet_mima(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_mima(BT_PELLET);
    }
}
void far gba_gauge_pattern_bullet_mima(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_mima(BT_BULLET16_DEFAULT);
    }
}
