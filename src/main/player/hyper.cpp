// Complete natural TC4J Hyper dispatcher, all ten original near Pascal
// handlers in TH03 MAIN_010_TEXT. No private DATA/BSS emitted.
// Byte packing while reading historical player_stuff_t is required to keep
// target offsets (shot_mode 0x0D, hyper callback 0x64) and near MAIN_01
// pointers exact without any compiler-OMF byte patch.
#pragma codeseg MAIN_010_TEXT main_01
#pragma option -a1
#include "src/main/player/hyper.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2

extern unsigned char round_frame;
extern speed_t player_speed_base;
extern "C" {
void far pascal marisa_hyper_14340(void);
void far pascal ellen_hyper(Subpixel center_x, Subpixel center_y);
void far rikako_chargeshot_cancel(void);
void far pascal rikako_charge_add_private(Subpixel center_x, Subpixel center_y);
}

inline void hyper_speed_up(void)
{
    player_speed_base.aligned.x.v += 0x20;
    player_speed_base.aligned.y.v += 0x20;
    player_speed_base.diagonal.x.v += 0x18;
    player_speed_base.diagonal.y.v += 0x18;
}

inline void hyper_speed_down(unsigned char step_diag)
{
    player_speed_base.aligned.x.v -= 0x10;
    player_speed_base.aligned.y.v -= 0x10;
    player_speed_base.diagonal.x.v -= step_diag;
    player_speed_base.diagonal.y.v -= step_diag;
}

void near pascal hyper_standby(void)
{
    player_cur->shot_mode = SM_1_PAIR;
    if(player_cur->hyper_active) {
        player_cur->hyper = player_cur->hyper_func;
    }
}

void near pascal hyper_reimu(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_REIMU_HYPER;
    hyper_speed_up();
}

void near pascal hyper_mima(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_2_PAIRS;
    player_cur->shot_active = SA_BLOCKED_FOR_THIS_FRAME;
    hyper_speed_up();
}

void near pascal hyper_marisa(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_NONE;
    marisa_hyper_14340();
    hyper_speed_down(0x0C);
}

void near pascal hyper_ellen(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_1_PAIR;
    if((round_frame & 3) == 0) {
        ellen_hyper(player_cur->center.x, player_cur->center.y);
    }
}

void near pascal hyper_kotohime(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_4_PAIRS;
    hyper_speed_up();
}

void near pascal hyper_chiyuri(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_4_PAIRS;
    hyper_speed_up();
}

void near pascal hyper_yumemi(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_4_PAIRS;
    hyper_speed_up();
}

void near pascal hyper_kana(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        return;
    }
    player_cur->shot_mode = SM_4_PAIRS;
    hyper_speed_up();
}

void near pascal hyper_rikako(void)
{
    if(!player_cur->hyper_active) {
        player_cur->hyper = hyper_standby;
        rikako_chargeshot_cancel();
        return;
    }
    if(player_cur->gauge_avail > 0x0FA0) {
        rikako_charge_add_private(player_cur->center.x, player_cur->center.y);
    }
    hyper_speed_down(8);
}
