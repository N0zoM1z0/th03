// Unaccepted complete Marisa owner: charge/gauge physical producer (nine bodies).
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
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

struct marisa_chargeshot_t {
    unsigned char active;
    unsigned char frame;
    playfield_subpixel_t x[12];
    playfield_subpixel_t y[12];
};
struct gauge_pattern_timing_t {
    unsigned char total_frames;
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char byte_3;
};
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
    for(int i = 0; i < 12; i++) {
        marisa_chargeshot_p->x[i] = center_x.v;
        marisa_chargeshot_p->y[i] = center_y.v - TO_SP(16);
    }
    snd_se_play(6);
}

void far pascal marisa_hyper_14340(void)
{
    marisa_chargeshot_p = &marisa_chargeshots[pid.current];
    if(marisa_chargeshot_p->active == 0) {
        marisa_chargeshot_p->active = 1;
        for(int i = 0; i < 12; i++) {
            marisa_chargeshot_p->x[i] = players[pid.current].center.x.v;
            marisa_chargeshot_p->y[i] = players[pid.current].center.y.v - TO_SP(16);
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
    marisa_chargeshot_p->frame++;
    for(int i = 11; i > 0; i--) {
        marisa_chargeshot_p->x[i] = marisa_chargeshot_p->x[i - 1];
        marisa_chargeshot_p->y[i] = marisa_chargeshot_p->y[i - 1] + 24;
    }
    if(marisa_chargeshot_p->frame < 24) {
        marisa_chargeshot_p->x[0] = players[pid_current].center.x.v;
        marisa_chargeshot_p->y[0] = players[pid_current].center.y.v - TO_SP(16);
        return; // The reviewed internal early RETF belongs to this body.
    }
    if(marisa_chargeshot_p->frame > 36) {
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
    for(int i = 0; i < 12; i += 4) {
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
    for(i = 11; i > 6; i--) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> 5) + 8;
        if(previous_x != x) {
            grcg_boxfill(x - 2, 8, x + 1, bottom);
        }
        previous_x = x;
    }
    grcg_settile_1line(GC_RMW, 0xFF00AA55L);
    previous_x = 0;
    for(i = 6; i > 3; i--) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> 5) + 8;
        if(previous_x != x) {
            grcg_boxfill(x - 2, 8, x + 1, bottom);
        }
        previous_x = x;
    }
    grcg_settile_1line(GC_RMW, 0xFF55FF55L);
    previous_x = 0;
    for(i = 3; i > 0; i--) {
        x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[i], pid_current);
        bottom = (marisa_chargeshot_p->y[i] >> 5) + 8;
        if(previous_x != x) {
            grcg_boxfill(x - 2, 8, x + 1, bottom);
        }
        previous_x = x;
    }
    grcg_setcolor(GC_RMW, V_WHITE);
    x = playfield_fg_x_to_screen(marisa_chargeshot_p->x[0], pid_current);
    bottom = (marisa_chargeshot_p->y[0] >> 5) + 8;
    grcg_boxfill(x - 2, 8, x + 1, bottom);
    grcg_off();
    egc_on();
}

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
    if((marisa_gauge_frame[pid_current] % 24) == 8) {
        bomb_center_add(0, marisa_gauge_y[pid_current], pid_other);
    } else if((marisa_gauge_frame[pid_current] % 24) == 20) {
        bomb_center_add(TO_SP(PLAYFIELD_W), marisa_gauge_y[pid_current], pid_other);
    } else if((marisa_gauge_frame[pid_current] % 24) == 0) {
        bullet_template.angle = 0x20;
        bullet_template.center.x.v = 0;
        for(int i = 0; i < 5; i++) {
            bullets_add();
            bullet_template.speed.v -= 6;
        }
        marisa_gauge_y[pid_current] += gauge_pattern_timing[pid_current].total_frames * 16;
    } else if((marisa_gauge_frame[pid_current] % 24) == 12) {
        bullet_template.angle = 0x60;
        bullet_template.center.x.v = TO_SP(PLAYFIELD_W);
        for(int i = 0; i < 5; i++) {
            bullets_add();
            bullet_template.speed.v -= 6;
        }
        marisa_gauge_y[pid_current] += gauge_pattern_timing[pid_current].total_frames * 16;
    }
    if(marisa_gauge_y[pid_current] >= TO_SP(PLAYFIELD_H)) {
        gba_flag_active[pid_current] = GBAF_NONE;
        // ABI hypothesis: pid_t is byte-valued, but Pascal reserves a word.
        // No invented word load or local overlap: probe natural TC4 lowering.
        palette_restore_for_pid(pid_other);
    }
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
