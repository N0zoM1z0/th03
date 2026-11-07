// Complete current source-native Marisa Chargeshot/Gauge (nine real
// original functions), retaining true PC-98 GRCG and segmented ABI.
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
#include <stddef.h>
#include "src/main/player/chargeshot_marisa.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// HITBOX_TEXT and BULLET_TEXT share the verified MAIN_04 CS frame.
// Supply that relationship to TC4/TLINK; bullets_add keeps its far ABI.
#pragma samecodeseg bullets_add

// Marisa's single physical beam per player records a 12-point
// vertical history, drawn in three overlapping GRCG pattern bands.
enum marisa_charge_layout_t {
    MARISA_CHARGE_HISTORY = 12,
    MARISA_CHARGE_LAST_SAMPLE = 11,
    MARISA_CHARGE_INITIAL_TAIL_END = 24,
    MARISA_CHARGE_FINISH_AFTER = 36,
    MARISA_CHARGE_GRCG_FIRST_BAND_END = 6,
    MARISA_CHARGE_GRCG_SECOND_BAND_END = 3,
    MARISA_CHARGE_HIT_STEP = 4,
    MARISA_CHARGE_HISTORY_Y_DROP = 24,
    MARISA_CHARGE_START_Y_OFFSET = TO_SP(16),
    MARISA_GRCG_Y_SHIFT = 5,
    MARISA_GRCG_TOP_Y = 8,
    MARISA_GRCG_LEFT_EDGE_DELTA = 2,
    MARISA_GRCG_RIGHT_EDGE_DELTA = 1,
};

struct marisa_chargeshot_t {
    unsigned char active;
    unsigned char frame;
    playfield_subpixel_t x[MARISA_CHARGE_HISTORY];
    playfield_subpixel_t y[MARISA_CHARGE_HISTORY];
};
typedef char marisa_charge_stride_is_50[
    (sizeof(marisa_chargeshot_t) == 50) ? 1 : -1
];
typedef char marisa_charge_x_at_02[
    (offsetof(marisa_chargeshot_t, x) == 2) ? 1 : -1
];
typedef char marisa_charge_y_at_1a[
    (offsetof(marisa_chargeshot_t, y) == 0x1A) ? 1 : -1
];

struct gauge_pattern_timing_t {
    unsigned char total_frames;
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char byte_3;
};
typedef char marisa_gauge_timing_is_4[
    (sizeof(gauge_pattern_timing_t) == 4) ? 1 : -1
];

// Proposed semantic aliases only: no allocation, no absolute pointer casts.
extern marisa_chargeshot_t marisa_chargeshots[PLAYER_COUNT];
extern marisa_chargeshot_t near *marisa_chargeshot_p;
extern int marisa_gauge_y[PLAYER_COUNT];
extern unsigned char marisa_gauge_frame[PLAYER_COUNT];
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];
extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far pascal marisa_chargeshot_state_reset(void)
{
    marisa_chargeshots[0].active = 0;
    marisa_chargeshots[1].active = 0;
}

void far pascal chargeshot_add_marisa(Subpixel center_x, Subpixel center_y)
{
    marisa_chargeshot_p = &marisa_chargeshots[pid.current];
    marisa_chargeshot_p->active = 1;
    marisa_chargeshot_p->frame = 0;
    players[pid.current].shot_active = SA_DISABLED;
    // All twelve original 16-bit X/Y history slots are initialized.
    int i = 0;
    while(i < MARISA_CHARGE_HISTORY) {
        marisa_chargeshot_p->x[i] = center_x.v;
        marisa_chargeshot_p->y[i] = center_y.v - MARISA_CHARGE_START_Y_OFFSET;
        ++i;
    }
    snd_se_play(6);
}

void far pascal marisa_hyper_14340(void)
{
    marisa_chargeshot_p = &marisa_chargeshots[pid.current];
    // The original byte-active guard naturally spells ==0 under
    // original TC4 (af920a), without changing its early return.
    if(marisa_chargeshot_p->active == 0) {
        marisa_chargeshot_p->active = 1;
        int i = 0;
        while(i < MARISA_CHARGE_HISTORY) {
            marisa_chargeshot_p->x[i] = players[pid.current].center.x.v;
            marisa_chargeshot_p->y[i] = players[pid.current].center.y.v - MARISA_CHARGE_START_Y_OFFSET;
            ++i;
        }
        snd_se_play(6);
    }
    marisa_chargeshot_p->frame = 16;
    players[pid.current].shot_active = SA_DISABLED;
}

void far pascal chargeshot_update_marisa(void)
{
    marisa_chargeshot_p = &marisa_chargeshots[pid_current];
    if(marisa_chargeshot_p->active == 0) {
        return;
    }
    players[pid_current].gauge_charged = 0;
    // Keep native byte postfix: original TC4 also rejected prefix
    // in fresh af868g (independently of older after769 evidence).
    // Keep the byte shot-frame postfix: prefix produced nonoriginal
    // code (af920c), independently of historical compiler notes.
    marisa_chargeshot_p->frame++;
    // Shift history from sample 11 down to 1 before replacing its head.
    // The descending while preserves the original signed subpixel delay.
    int i = MARISA_CHARGE_LAST_SAMPLE;
    while(i > 0) {
        marisa_chargeshot_p->x[i] = marisa_chargeshot_p->x[i - 1];
        marisa_chargeshot_p->y[i] = marisa_chargeshot_p->y[i - 1] + MARISA_CHARGE_HISTORY_Y_DROP;
        --i;
    }
    // The signed/byte initial-tail cutoff can have its operands
    // reversed with exact native TC4 codegen (af920g).
    if(MARISA_CHARGE_INITIAL_TAIL_END > marisa_chargeshot_p->frame) {
        marisa_chargeshot_p->x[0] = players[pid_current].center.x.v;
        marisa_chargeshot_p->y[0] = players[pid_current].center.y.v - MARISA_CHARGE_START_Y_OFFSET;
        return; // The reviewed internal early RETF belongs to this body.
    }
    if(marisa_chargeshot_p->frame > MARISA_CHARGE_FINISH_AFTER) {
        players[pid_current].shot_active = SA_ENABLED;
        marisa_chargeshot_p->active = 0;
    }
}

uint8_t far chargeshot_hittest_marisa(void)
{
    unsigned char hit;
    marisa_chargeshot_p = &marisa_chargeshots[hitbox.pid];
    if(marisa_chargeshot_p->active == 0) {
        return 0;
    }
    hit = 0;
    // Collision examines samples 0, 4 and 8, not all 12 visible
    // samples; a hit breaks before the next index increment.
    int i = 0;
    while(i < MARISA_CHARGE_HISTORY) {
        if(
            (marisa_chargeshot_p->x[i] >= hitbox.origin.topleft.x.v) &&
            (marisa_chargeshot_p->x[i] <= hitbox.right.v) &&
            (marisa_chargeshot_p->y[i] >= hitbox.origin.topleft.y.v)
        ) {
            hitcircles_enemy_add(
                marisa_chargeshot_p->x[i],
                hitbox.origin.topleft.y.v + hitbox.radius.y.v, hitbox.pid
            );
            hit = 1;
            break;
        }
        i += MARISA_CHARGE_HIT_STEP;
    }
    return hit;
}

void far pascal chargeshot_render_marisa(void)
{
    int bottom;
    int previous_x;
    int i;
    int x;
    marisa_chargeshot_p = &marisa_chargeshots[pid_current];
    if(marisa_chargeshot_p->active == 0) {
        return;
    }
    egc_off();
    grcg_settile_1line(GC_RMW, 0xAA0055AAL);
    previous_x = 0;
    // The complete original GRCG beam paints 11..7, 6..4 and 3..1
    // history samples in independent hardware tile/clip passes, resetting
    // previous X between each. The signed coordinate >>5 must remain:
    // replacing four uses with /32 changed actual TC4 CODE in af920d,
    // and signed negative rounding differs as well.
    i = MARISA_CHARGE_LAST_SAMPLE;
    while(i > MARISA_CHARGE_GRCG_FIRST_BAND_END) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> MARISA_GRCG_Y_SHIFT) + MARISA_GRCG_TOP_Y;
        if(previous_x != x) {
            grcg_boxfill(
                x - MARISA_GRCG_LEFT_EDGE_DELTA, MARISA_GRCG_TOP_Y,
                x + MARISA_GRCG_RIGHT_EDGE_DELTA, bottom
            );
        }
        previous_x = x;
        --i;
    }
    grcg_settile_1line(GC_RMW, 0xFF00AA55L);
    previous_x = 0;
    i = MARISA_CHARGE_GRCG_FIRST_BAND_END;
    while(i > MARISA_CHARGE_GRCG_SECOND_BAND_END) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> MARISA_GRCG_Y_SHIFT) + MARISA_GRCG_TOP_Y;
        if(previous_x != x) {
            grcg_boxfill(
                x - MARISA_GRCG_LEFT_EDGE_DELTA, MARISA_GRCG_TOP_Y,
                x + MARISA_GRCG_RIGHT_EDGE_DELTA, bottom
            );
        }
        previous_x = x;
        --i;
    }
    grcg_settile_1line(GC_RMW, 0xFF55FF55L);
    previous_x = 0;
    i = MARISA_CHARGE_GRCG_SECOND_BAND_END;
    while(i > 0) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> MARISA_GRCG_Y_SHIFT) + MARISA_GRCG_TOP_Y;
        if(previous_x != x) {
            grcg_boxfill(
                x - MARISA_GRCG_LEFT_EDGE_DELTA, MARISA_GRCG_TOP_Y,
                x + MARISA_GRCG_RIGHT_EDGE_DELTA, bottom
            );
        }
        previous_x = x;
        --i;
    }
    grcg_setcolor(GC_RMW, V_WHITE);
    x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[0], pid_current);
    bottom = (marisa_chargeshot_p->y[0] >> MARISA_GRCG_Y_SHIFT) + MARISA_GRCG_TOP_Y;
    grcg_boxfill(
        x - MARISA_GRCG_LEFT_EDGE_DELTA, MARISA_GRCG_TOP_Y,
        x + MARISA_GRCG_RIGHT_EDGE_DELTA, bottom
    );
    grcg_off();
    egc_on();
}

// Two alternating five-shot side volleys per 24 frames, with warnings
// at 8 and 20. The gauge moves downward in the *original* signed
// subpixel increments, not a newly normalized pixel coordinate.
enum marisa_gauge_phase_t {
    MARISA_GAUGE_PERIOD = 24,
    MARISA_GAUGE_LEFT_FIRE = 0,
    MARISA_GAUGE_LEFT_WARN = 8,
    MARISA_GAUGE_RIGHT_FIRE = 12,
    MARISA_GAUGE_RIGHT_WARN = 20,
    MARISA_GAUGE_VOLLEY_COUNT = 5,
};

void near pascal gauge_pattern_marisa(bullet_type_t type)
{
    unsigned char pid_other;
    unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
    if(type == BT_BULLET16_DEFAULT) {
        flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
    }
    if(gba_flag_active[pid_current] == flag_expected) {
        marisa_gauge_y[pid_current] = -(int)randring2_next16_and(31) * 16;
        marisa_gauge_frame[pid_current] = 0;
        gba_flag_active[pid_current]++;
        gauge_pattern_timing[pid_current].total_frames = 48 - gba_gauge_level[pid_current];
        return;
    }
    if(gba_flag_active[pid_current] != flag_expected + 1) {
        return;
    }
    bullet_template.type = type;
    bullet_template.center.y.v = marisa_gauge_y[pid_current];
    pid_other = 1 - pid_current;
    bullet_template.pid = pid_other;
    bullet_template.speed.v = 56;
    bullet_template.group = BG_1;
    // All four original byte-frame phases keep their distinct order:
    // left warning, right warning, left volley, right volley. Equality
    // operand reversal is native-exact (af920b/f), but event ordering
    // and original RNG and bomb warning calls must not be collapsed.
    if(MARISA_GAUGE_LEFT_WARN == (marisa_gauge_frame[pid_current] % MARISA_GAUGE_PERIOD)) {
        bomb_center_add(0, marisa_gauge_y[pid_current], pid_other);
    } else if(MARISA_GAUGE_RIGHT_WARN == (marisa_gauge_frame[pid_current] % MARISA_GAUGE_PERIOD)) {
        bomb_center_add(TO_SP(PLAYFIELD_W), marisa_gauge_y[pid_current], pid_other);
    // This is the one *zero-remainder* 24-frame phase. Native TC4
    // accepts if(!remainder), unlike some other byte-value masks.
    } else if(!(marisa_gauge_frame[pid_current] % MARISA_GAUGE_PERIOD)) {
        bullet_template.angle = 0x20;
        bullet_template.center.x.v = 0;
        // The original mutable speed -=6 must remain literal: a
        // fresh real TC4 compile rejected the named constant (af868f).
        int i = 0;
        while(i < MARISA_GAUGE_VOLLEY_COUNT) {
            bullets_add();
            bullet_template.speed.v -= 6;
            ++i;
        }
        marisa_gauge_y[pid_current] +=
            (gauge_pattern_timing[pid_current].total_frames << 4);
    } else if(MARISA_GAUGE_RIGHT_FIRE == (marisa_gauge_frame[pid_current] % MARISA_GAUGE_PERIOD)) {
        bullet_template.angle = 0x60;
        bullet_template.center.x.v = TO_SP(PLAYFIELD_W);
        int i = 0;
        while(i < MARISA_GAUGE_VOLLEY_COUNT) {
            bullets_add();
            bullet_template.speed.v -= 6;
            ++i;
        }
        marisa_gauge_y[pid_current] +=
            (gauge_pattern_timing[pid_current].total_frames << 4);
    }
    if(marisa_gauge_y[pid_current] >= TO_SP(PLAYFIELD_H)) {
        gba_flag_active[pid_current] = GBAF_NONE;
        // ABI hypothesis: pid_t is byte-valued, but Pascal reserves a word.
        // No invented word load or local overlap: probe natural TC4 lowering.
        palette_restore_for_pid(pid_other);
    }
    // This mutable byte timing must retain postfix: prefix changed
    // original CODE in the fresh af920e trial.
    marisa_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_marisa(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_marisa(BT_PELLET);
    }
}
void far gba_gauge_pattern_bullet_marisa(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_marisa(BT_BULLET16_DEFAULT);
    }
}
