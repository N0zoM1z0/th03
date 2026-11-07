// Complete current natural C++ for the original physical Yumemi gameplay
// owner in PELLET_PUT, MAIN_04 group. Genuine original TC4 and normal MAIN
// native link are exact; canonical packed-game Factory remains separate.
// The first function also provides the shared target acquisition service.
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

// Two sentinels in the actual formation-index byte: the boss target
// takes precedence, while 255 denotes no usable enemy formation.
enum yumemi_target_marker_t {
    YUME_TARGET_BOSS = 254,
    YUME_TARGET_NO_FORMATION = 255,
    YUME_TARGET_FIRST_FORMATION = 0,
    YUME_TARGET_FALLBACK_X = TO_SP(144),
    YUME_TARGET_FALLBACK_Y = TO_SP(300),
    YUME_TARGET_ENEMY_X_BIAS = TO_SP(16),
    YUME_TARGET_ENEMY_Y_BIAS = TO_SP(110),
};

void far pascal ellen_target_set(pid_t player)
{
    unsigned char formation = YUME_TARGET_NO_FORMATION;
    if(boss_active[player]) {
        target_formation_marker = YUME_TARGET_BOSS;
        ellen_target_x = boss_target_x;
        ellen_target_y = boss_target_y;
        return;
    }

    enemy_t near *p = reinterpret_cast<enemy_t near *>(&efes[0]);
    for(int i = 0; i < TARGET_ENEMY_COUNT; ++i, p++) {
        if(p->flag != EF_RUNNING_SPAWNED || p->pid != player ||
           p->center.x.v < 0 || p->center.x.v > TO_SP(PLAYFIELD_W) ||
           p->center.y.v < 0 ||
           p->center.y.v > TO_SP(PLAYFIELD_H + PLAYFIELD_BORDER) ||
           p->formation_i >= formation) {
            continue;
        }
        formation = p->formation_i;
        efe_p.enemy = p;
        if(formation == YUME_TARGET_FIRST_FORMATION) {
            break;
        }
    }
    if(formation == YUME_TARGET_NO_FORMATION) {
        ellen_target_x = YUME_TARGET_FALLBACK_X;
        ellen_target_y = YUME_TARGET_FALLBACK_Y;
        target_formation_marker = YUME_TARGET_NO_FORMATION;
        return;
    }

    ellen_target_x = efe_p.enemy->center.x.v - YUME_TARGET_ENEMY_X_BIAS;
    ellen_target_y = efe_p.enemy->center.y.v + YUME_TARGET_ENEMY_Y_BIAS;
    target_formation_marker = formation;
    if(ellen_target_x <= 0 || ellen_target_x >= TO_SP(PLAYFIELD_W) ||
       ellen_target_y <= 0 ||
       ellen_target_y >= TO_SP(PLAYFIELD_H + PLAYFIELD_BORDER)) {
        // The selected formation marker survives this fallback. These
        // are original signed-16-bit target coordinates (af856g).
        ellen_target_x = YUME_TARGET_FALLBACK_X;
        ellen_target_y = YUME_TARGET_FALLBACK_Y;
    }
}

// The charged projectile changes to its blooming hitbox at frame 64.
// The ring renderer has separate eight-frame radii/phase intervals.
enum yumemi_chargeshot_phase_t {
    YUME_CHARGE_INACTIVE = 0,
    YUME_CHARGE_FLYING = 1,
    YUME_CHARGE_BLOOMING = 2,
    YUME_CHARGE_EFFECT_START = 24,
    YUME_CHARGE_LIFETIME = 64,
    YUME_RENDER_RING_8 = 8,
    YUME_RENDER_RING_16 = 16,
    YUME_RENDER_RING_24 = 24,
    YUME_RENDER_RING_32 = 32,
    YUME_RENDER_RING_40 = 40,
    YUME_RENDER_RING_48 = 48,
    YUME_RENDER_RING_56 = 56,
    YUME_RENDER_RING_64 = 64,
    YUME_RING_SPRITES_PER_WAVE = 16,
    YUME_GAUGE_VOLLEY_PERIOD = 8,
    YUME_CHARGE_FLY_SPEED = TO_SP(4),
    YUME_CHARGE_FLY_HIT_MARGIN = TO_SP(8),
    YUME_CHARGE_BLOOM_HIT_MARGIN = TO_SP(56),
    YUME_RING_CENTER_OFFSET = TO_SP(16),
    YUME_RING_SCREEN_TOP_OFFSET = 16,
};

void far pascal yumemi_chargeshots_reset(void)
{
    yumemi_chargeshots[0].state = YUME_CHARGE_INACTIVE;
    yumemi_chargeshots[1].state = YUME_CHARGE_INACTIVE;
}

void far pascal chargeshot_add_yumemi(Subpixel center_x, Subpixel center_y)
{
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid.current];
    p->state = YUME_CHARGE_FLYING;
    p->frame = 0;
    p->x.v = center_x.v;
    p->y.v = center_y.v;
}

void far pascal chargeshot_update_yumemi(void)
{
    unsigned char frame;
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid_current];
    if(!p->state) {
        return;
    }
    frame = ++p->frame;
    if(p->state == YUME_CHARGE_FLYING) {
        p->y.v -= YUME_CHARGE_FLY_SPEED;
        if(frame >= YUME_CHARGE_LIFETIME || p->y.v <= 0) {
            p->state = YUME_CHARGE_BLOOMING;
            p->frame = 0;
            snd_se_play(7);
        }
    } else {
        // This native byte-frame equality cannot be replaced by !(&1),
        // which changed actual TC4 CODE (rejected af776d).
        if(frame >= YUME_CHARGE_EFFECT_START && (frame % 2) == 0) {
            snd_se_play(15);
        }
        if(frame >= YUME_CHARGE_LIFETIME) {
            p->state = YUME_CHARGE_INACTIVE;
        }
    }
    players[pid_current].gauge_charged = 0;
}

uint8_t far chargeshot_hittest_yumemi(void)
{
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[hitbox.pid];
    if(!p->state) {
        return 0;
    }
    if(p->state == YUME_CHARGE_FLYING) {
        if(p->x.v - YUME_CHARGE_FLY_HIT_MARGIN <= hitbox.right.v &&
           p->x.v + YUME_CHARGE_FLY_HIT_MARGIN >= hitbox.origin.topleft.x.v &&
           p->y.v - YUME_CHARGE_FLY_HIT_MARGIN <= hitbox.bottom.v &&
           p->y.v + YUME_CHARGE_FLY_HIT_MARGIN >= hitbox.origin.topleft.y.v) {
            p->state = YUME_CHARGE_BLOOMING;
            p->frame = 0;
            snd_se_play(7);
        }
        // Triggering the effect itself does not report a hit.
        return 0;
    }
    if(p->x.v - YUME_CHARGE_BLOOM_HIT_MARGIN <= hitbox.right.v &&
       p->x.v + YUME_CHARGE_BLOOM_HIT_MARGIN >= hitbox.origin.topleft.x.v &&
       p->y.v - YUME_CHARGE_BLOOM_HIT_MARGIN <= hitbox.bottom.v &&
       p->y.v + YUME_CHARGE_BLOOM_HIT_MARGIN >= hitbox.origin.topleft.y.v) {
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
    center_x = p->x.v - YUME_RING_CENTER_OFFSET;
    center_y = p->y.v - YUME_RING_CENTER_OFFSET;
    // One ring contains sixteen actual sprite calls, with two independently
    // advanced local carriers. The natural while emits native-exact CODE
    // (af856a), but naming the live byte `angle += 16` changes it (af856b).
    i = 0;
    angle = (frame << 1);
    while(i < YUME_RING_SPRITES_PER_WAVE) {
        left = polar(center_x, radius, CosTable8[angle]);
        top = polar(
            center_y, radius, SinTable8[static_cast<unsigned char>(angle + y_phase)]
        );
        left = playfield_fg_x_to_screen(left, pid_current);
        top = (top >> 4) + YUME_RING_SCREEN_TOP_OFFSET;
        sprite16_put(left, top, sprite_offset);
        ++i;
        angle += 16;
    }
}

void far pascal chargeshot_render_yumemi(void)
{
    int left;
    int top;
    unsigned char frame;
    sprite16_offset_t sprite_offset;
    yumemi_chargeshot_t near *p = &yumemi_chargeshots[pid_current];
    if(!p->state) {
        return;
    }
    sprite16_put_size.set(32, 32); // Stored VRAM height is 16 rows.
    sprite16_clip_set_for_pid(pid_current);
    sprite_offset = pid.so_attack + 0xC80;
    frame = p->frame;
    // Original byte phase is deliberately masked here. Natural byte
    // `% 2` produces a different TC4 object (af856d), unlike the Gauge
    // division predicate below.
    if(frame & 1) {
        sprite_offset += 4;
    }
    if(p->state == YUME_CHARGE_FLYING) {
        left = playfield_fg_x_to_screen(p->x.v, pid_current) - 16;
        top = p->y.v >> 4;
        sprite16_put(left, top, sprite_offset);
        return;
    }

    sprite_offset += 0x500;
    if(frame < YUME_RENDER_RING_8) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP(frame * 8), 0);
    } else if(frame < YUME_RENDER_RING_16) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 7) * 8), 32);
    } else if(frame < YUME_RENDER_RING_24) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 15) * 8), 224);
    } else if(frame < YUME_RENDER_RING_32) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 24) * 8), 0);
    } else if(frame < YUME_RENDER_RING_40) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 31) * 8), 32);
    } else if(frame < YUME_RENDER_RING_48) {
        yumemi_chargeshot_ring_render(sprite_offset, TO_SP((frame - 39) * 8), 224);
    } else if(frame < YUME_RENDER_RING_64) {
        if(frame < YUME_RENDER_RING_56) {
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

// The original two interleaved triangular Gauge barrages are emitted
// at these eight fixed frame counters. TC4 owns the switch jump table.
enum yumemi_gauge_volley_t {
    YUME_GAUGE_FIRST = 0,
    YUME_GAUGE_SECOND = 8,
    YUME_GAUGE_THIRD = 16,
    YUME_GAUGE_FOURTH = 24,
    YUME_GAUGE_FIFTH = 32,
    YUME_GAUGE_SIXTH = 40,
    YUME_GAUGE_SEVENTH = 48,
    YUME_GAUGE_FINAL = 56,
};

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
    // Original byte-clock division remains `%8`: direct &7 changed
    // original CODE by six bytes in native af776a. The natural
    // `if(!(byte_frame % 8))` truth spelling is exact (af856f).
    if(!(yumemi_gauge_frame[pid_current] % YUME_GAUGE_VOLLEY_PERIOD)) {
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
        case YUME_GAUGE_FIRST:
            x = TO_SP(144); y = TO_SP(32);
            break;
        case YUME_GAUGE_SECOND:
            x = TO_SP(96); y = TO_SP(80);
            break;
        case YUME_GAUGE_THIRD:
            x = TO_SP(192); y = TO_SP(80);
            bullet_template.center.x.v = TO_SP(144);
            bullet_template.center.y.v = TO_SP(32);
            break;
        case YUME_GAUGE_FOURTH:
            x = TO_SP(96); y = TO_SP(56);
            bullet_template.center.x.v = TO_SP(96);
            bullet_template.center.y.v = TO_SP(80);
            break;
        case YUME_GAUGE_FIFTH:
            x = TO_SP(192); y = TO_SP(56);
            bullet_template.center.x.v = TO_SP(192);
            bullet_template.center.y.v = TO_SP(80);
            break;
        case YUME_GAUGE_SIXTH:
            x = TO_SP(144); y = TO_SP(104);
            bullet_template.center.x.v = TO_SP(96);
            bullet_template.center.y.v = TO_SP(56);
            break;
        case YUME_GAUGE_SEVENTH:
            bullet_template.center.x.v = TO_SP(192);
            bullet_template.center.y.v = TO_SP(56);
            break;
        case YUME_GAUGE_FINAL:
            bullet_template.center.x.v = TO_SP(144);
            bullet_template.center.y.v = TO_SP(104);
            gba_flag_active[pid_current] = GBAF_NONE;
            palette_restore_for_pid(player_other);
            break;
        }
        // x and y are only consumed on cases 0 through 40, which assign both.
        // The INIT/ACTIVE state machine ends at 56, so no later case executes.
        if(yumemi_gauge_frame[pid_current] <= YUME_GAUGE_SIXTH) {
            bomb_axis_add(x, y, player_other);
        }
        if(yumemi_gauge_frame[pid_current] >= YUME_GAUGE_THIRD) {
            bullets_add();
        }
    }
    yumemi_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_yumemi(void)
{
    if(gba_flag_active[pid_current]) {
        gauge_pattern_yumemi(BT_PELLET);
    }
}

void far gba_gauge_pattern_bullet_yumemi(void)
{
    if(gba_flag_active[pid_current]) {
        gauge_pattern_yumemi(BT_BULLET16_DEFAULT);
    }
}
