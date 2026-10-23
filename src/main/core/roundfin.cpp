// MAIN load A21F..A2D0. Existing storage and foreign services remain external.
#pragma codeseg PLAYFLD_TEXT main_01
#include "src/main/player/lose.hpp"
#include "src/main/player/hyper.hpp"
#include "compat/rec98/th03/main/hud/static.hpp"

extern unsigned char round_id;
typedef char round_score_layout[(offsetof(resident_t, score_last) == 0x18 &&
    sizeof(score_lebcd_t) == 8) ? 1 : -1];
extern void (far *round_background_reset)(void);
extern "C" {
void near round_prepare_players(void);
void far round_objects_for_next(void);
void far snd_se_reset(void);
extern score_lebcd_t score_p1[2];
}
#pragma samecodeseg hud_wipe
#pragma samecodeseg round_objects_for_next
#pragma samecodeseg hud_static_put

extern "C" void near round_start_next(void)
{
    grcg_setcolor(GC_RMW, 2);
    grc_setclip(0, 0, 639, 199);
    graph_accesspage(1);
    grcg_fill();
    graph_accesspage(0);
    grcg_fill();
    graph_showpage(1);
    grcg_off();
    round_id++;
    round_prepare_players();
    round_background_reset();
    players[0].hyper = hyper_standby;
    players[1].hyper = hyper_standby;
    snd_se_reset();
    hud_wipe();
    round_objects_for_next();
    hud_static_put();
}

void near pascal round_score_commit(register unsigned int player)
{
    for(_CX = 0; (int)_CX < SCORE_DIGITS; _CX++) {
        resident->score_last[player].digits[_CX] = score_p1[player].digits[_CX];
        resident->score_last[1 - player].digits[_CX] = 0;
    }
}
