// Natural complete-function proposal from the attested TH03 target.
// Complete reviewed source; full-link acceptance pending. Owner: PELLET_PUT,
// MAIN_04 group. The first function is shared target acquisition.
#pragma codeseg PELLET_PUT main_04
#pragma option -a1
#include "src/main/player/yumemi_gameplay.hpp"
#include "src/main/enemy/target_record.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

// Real MAIN_04 code-group relationship. Target NOP/PUSH CS/CALL-near is
// linker relaxation of the far bullets_add ABI, not a near-return function.
#pragma samecodeseg bullets_add

void far pascal ellen_target_set(pid_t player)
{
    unsigned char formation = 255;
    if(boss_active[player] != 0) {
        target_formation_marker = 254;
        ellen_target_x = boss_target_x;
        ellen_target_y = boss_target_y;
        return;
    }

    enemy_t near *p = reinterpret_cast<enemy_t near *>(&efes[0]);
    for(int i = 0; i < TARGET_ENEMY_COUNT; i++, p++) {
        if(p->flag != EF_RUNNING_SPAWNED || p->pid != player ||
           p->center.x.v < 0 || p->center.x.v > TO_SP(PLAYFIELD_W) ||
           p->center.y.v < 0 ||
           p->center.y.v > TO_SP(PLAYFIELD_H + PLAYFIELD_BORDER) ||
           p->formation_i >= formation) {
            continue;
        }
        formation = p->formation_i;
        efe_p.enemy = p;
        if(formation == 0) {
            break;
        }
    }
    if(formation == 255) {
        ellen_target_x = TO_SP(144);
        ellen_target_y = TO_SP(300);
        target_formation_marker = 255;
        return;
    }

    ellen_target_x = efe_p.enemy->center.x.v - TO_SP(16);
    ellen_target_y = efe_p.enemy->center.y.v + TO_SP(110);
    target_formation_marker = formation;
    if(ellen_target_x <= 0 || ellen_target_x >= TO_SP(PLAYFIELD_W) ||
       ellen_target_y <= 0 ||
       ellen_target_y >= TO_SP(PLAYFIELD_H + PLAYFIELD_BORDER)) {
        // The formation marker remains selected, even after this fallback.
        ellen_target_x = TO_SP(144);
        ellen_target_y = TO_SP(300);
    }
}

void far pascal yumemi_chargeshots_reset(void)
{
    yumemi_chargeshots[0].state = 0;
    yumemi_chargeshots[1].state = 0;
}

void far pascal chargeshot_add_yumemi(Subpixel center_x, Subpixel center_y)
{
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid.current];
    p->state = 1;
    p->frame = 0;
    p->x.v = center_x.v;
    p->y.v = center_y.v;
}

void far pascal chargeshot_update_yumemi(void)
{
    unsigned char frame;
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid_current];
    if(p->state == 0) {
        return;
    }
    frame = ++p->frame;
    if(p->state == 1) {
        p->y.v -= TO_SP(4);
        if(frame >= 64 || p->y.v <= 0) {
            p->state = 2;
            p->frame = 0;
            snd_se_play(7);
        }
    } else {
        if(frame >= 24 && (frame % 2) == 0) {
            snd_se_play(15);
        }
        if(frame >= 64) {
            p->state = 0;
        }
    }
    players[pid_current].gauge_charged = 0;
}

uint8_t far chargeshot_hittest_yumemi(void)
{
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[hitbox.pid];
    if(p->state == 0) {
        return 0;
    }
    if(p->state == 1) {
        if(p->x.v - TO_SP(8) <= hitbox.right.v &&
           p->x.v + TO_SP(8) >= hitbox.origin.topleft.x.v &&
           p->y.v - TO_SP(8) <= hitbox.bottom.v &&
           p->y.v + TO_SP(8) >= hitbox.origin.topleft.y.v) {
            p->state = 2;
            p->frame = 0;
            snd_se_play(7);
        }
        // Triggering the effect itself does not report a hit.
        return 0;
    }
    if(p->x.v - TO_SP(56) <= hitbox.right.v &&
       p->x.v + TO_SP(56) >= hitbox.origin.topleft.x.v &&
       p->y.v - TO_SP(56) <= hitbox.bottom.v &&
       p->y.v + TO_SP(56) >= hitbox.origin.topleft.y.v) {
        hitcircles_enemy_add(
            hitbox.origin.topleft.x.v, hitbox.origin.topleft.y.v, hitbox.pid
        );
        return 1;
    }
    return 0;
}

void near pascal yumemi_chargeshot_ring_render(
    sprite16_offset_t sprite_offset, int radius, unsigned char y_phase
)
{
    int left;
    int top;
    int i;
    int center_x;
    int center_y;
    unsigned char frame;
    unsigned char angle;
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid_current];
    frame = p->frame;
    center_x = p->x.v - TO_SP(16);
    center_y = p->y.v - TO_SP(16);
    for(i = 0, angle = frame * 2; i < 16; i++, angle += 16) {
        left = polar(center_x, radius, CosTable8[angle]);
        top = polar(
            center_y, radius, SinTable8[static_cast<unsigned char>(angle + y_phase)]
        );
        left = playfield_fg_x_to_screen(left, pid_current);
        top = (top >> 4) + 16;
        sprite16_put(left, top, sprite_offset);
    }
}

void far pascal chargeshot_render_yumemi(void)
{
    int left;
    int top;
    unsigned char frame;
    sprite16_offset_t sprite_offset;
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid_current];
    if(p->state == 0) {
        return;
    }
    sprite16_put_size.set(32, 32); // Stored VRAM height is 16 rows.
    sprite16_clip_set_for_pid(pid_current);
    sprite_offset = pid.so_attack + 0xC80;
    frame = p->frame;
    if(frame & 1) {
        sprite_offset += 4;
    }
    if(p->state == 1) {
        left = playfield_fg_x_to_screen(p->x.v, pid_current) - 16;
        top = p->y.v >> 4;
        sprite16_put(left, top, sprite_offset);
        return;
    }

    sprite_offset += 0x500;
    if(frame < 8) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP(frame * 8), 0);
    } else if(frame < 16) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 7) * 8), 32);
    } else if(frame < 24) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 15) * 8), 224);
    } else if(frame < 32) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 24) * 8), 0);
    } else if(frame < 40) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 31) * 8), 32);
    } else if(frame < 48) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 39) * 8), 224);
    } else if(frame < 64) {
        if(frame < 56) {
            yumemi_chargeshot_ring_render(
                sprite_offset, TO_SP((frame - 47) * 8), 32
            );
            yumemi_chargeshot_ring_render(
                sprite_offset, TO_SP((frame - 47) * 8), 224
            );
        }
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 48) * 8), 0);
    }
}

void near pascal gauge_pattern_yumemi(unsigned int type)
{
    unsigned char player_other;
    unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
    int x;
    int y;
    if(type == BT_BULLET16_DEFAULT) {
        flag_expected = flag_expected + GBAF_PELLET_TO_BULLET;
    }
    if(gba_flag_active[pid_current] == flag_expected) {
        yumemi_gauge_frame[pid_current] = 0;
        gba_flag_active[pid_current]++;
        gauge_pattern_timing[pid_current].total_frames =
            gba_gauge_level[pid_current] + 24;
        gauge_pattern_timing[pid_current].byte_1 =
            gba_gauge_level[pid_current] + 32;
        return;
    }
    if(gba_flag_active[pid_current] != flag_expected + 1) {
        return;
    }
    player_other = 1 - pid_current;
    if((yumemi_gauge_frame[pid_current] % 8) == 0) {
        bullet_template.type = static_cast<bullet_type_t>(type);
        bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;
        bullet_template.pid = player_other;
        bullet_template.angle = 0;
        bullet_template.group = BG_RING_AIMED;
        bullet_template.count = gauge_pattern_timing[pid_current].total_frames;
        // The two interleaved triangles are laid out explicitly. This natural
        // switch owns the original 32-byte value/jump table; no table bytes
        // are copied into source or used to constrain compiler output.
        switch(yumemi_gauge_frame[pid_current]) {
        case 0:
            x = TO_SP(144); y = TO_SP(32);
            break;
        case 8:
            x = TO_SP(96); y = TO_SP(80);
            break;
        case 16:
            x = TO_SP(192); y = TO_SP(80);
            bullet_template.center.x.v = TO_SP(144);
            bullet_template.center.y.v = TO_SP(32);
            break;
        case 24:
            x = TO_SP(96); y = TO_SP(56);
            bullet_template.center.x.v = TO_SP(96);
            bullet_template.center.y.v = TO_SP(80);
            break;
        case 32:
            x = TO_SP(192); y = TO_SP(56);
            bullet_template.center.x.v = TO_SP(192);
            bullet_template.center.y.v = TO_SP(80);
            break;
        case 40:
            x = TO_SP(144); y = TO_SP(104);
            bullet_template.center.x.v = TO_SP(96);
            bullet_template.center.y.v = TO_SP(56);
            break;
        case 48:
            bullet_template.center.x.v = TO_SP(192);
            bullet_template.center.y.v = TO_SP(56);
            break;
        case 56:
            bullet_template.center.x.v = TO_SP(144);
            bullet_template.center.y.v = TO_SP(104);
            gba_flag_active[pid_current] = GBAF_NONE;
            palette_restore_for_pid(player_other);
            break;
        }
        // x and y are only consumed on cases 0 through 40, which assign both.
        // The INIT/ACTIVE state machine ends at 56, so no later case executes.
        if(yumemi_gauge_frame[pid_current] <= 40) {
            bomb_axis_add(x, y, player_other);
        }
        if(yumemi_gauge_frame[pid_current] >= 16) {
            bullets_add();
        }
    }
    yumemi_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_yumemi(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_yumemi(BT_PELLET);
    }
}

void far gba_gauge_pattern_bullet_yumemi(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_yumemi(BT_BULLET16_DEFAULT);
    }
}
