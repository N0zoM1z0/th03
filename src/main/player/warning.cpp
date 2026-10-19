// Complete pause, gauge, portrait, flash and warning-state source cohort.
// Source-present only; see docs/reconstruction/MAIN_PLAYER_WARNING_REVIEW.md.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/player/warning.hpp"

void near round_pause_or_quit(void)
{
    if(resident->is_cpu[0] && resident->is_cpu[1]) {
        palette_black_out(1);
        round_quit_requested = 1;
        return;
    }
    snd_se_reset();
    snd_se_play(21);
    snd_se_update();
    while(input_sp != INPUT_NONE) {
        input_reset_sense_key_held();
        frame_delay(1);
    }
    for(;;) {
        input_reset_sense_key_held();
        if(input_sp & INPUT_Q) {
            round_quit_requested = 1;
            return;
        }
        if(input_sp & INPUT_CANCEL) break;
        frame_delay(1);
    }
    while(input_sp != INPUT_NONE) {
        input_reset_sense_key_held();
        frame_delay(1);
    }
    snd_se_reset();
    snd_se_play(21);
    snd_se_update();
}

void near round_C830(void)
{
    register int color;
    egc_on();
    asm { call near ptr hud_gauge_highlights_restore }
    egc_off();
    if(players[0].hyper_active && (round_or_result_frame & 1)) {
        color = players[0].gauge_avail >> 10;
        if(color == 1) color = 8;
        else if(color == 2) color = 12;
        else color = 6;
        grcg_setcolor(GC_RMW, color);
        asm {
            mov bx, 0232h
            call near ptr hud_gauge_highlight_fill
            xor ax, ax
            out 07Ch, ax
        }
    }
    if(players[1].hyper_active && (round_or_result_frame & 1)) {
        color = players[1].gauge_avail >> 10;
        if(color == 1) color = 8;
        else if(color == 2) color = 12;
        else color = 6;
        grcg_setcolor(GC_RMW, color);
        asm {
            mov bx, 025Ah
            call near ptr hud_gauge_highlight_fill
            xor ax, ax
            out 07Ch, ax
        }
    }
}

void near round_C8C4(void)
{
    unsigned char color;
    unsigned int charged_p1 = players[0].gauge_charged >> 4;
    register int available_p1 = players[0].gauge_avail >> 4;
    unsigned int charged_p2 = players[1].gauge_charged >> 4;
    register int available_p2 = players[1].gauge_avail >> 4;
    available_p1 -= static_cast<int>(charged_p1);
    if(available_p1 > 0) {
        if(!players[0].hyper_active || (round_or_result_frame & 1))
            grcg_setcolor(GC_RMW, 9);
        else grcg_setcolor(GC_RMW, 15);
        // Genuine B3F6 input contract; do not name C locals inside asm.
        _DX = charged_p1 + 32;
        _BX = available_p1;
        asm { call near ptr hud_gauge_bar_fill }
    }
    available_p2 -= static_cast<int>(charged_p2);
    if(available_p2 > 0) {
        if(!players[1].hyper_active || (round_or_result_frame & 1))
            grcg_setcolor(GC_RMW, 9);
        else grcg_setcolor(GC_RMW, 15);
        // Genuine B3F6 input contract; do not name C locals inside asm.
        _DX = charged_p2 + 352;
        _BX = available_p2;
        asm { call near ptr hud_gauge_bar_fill }
    }
    // Reload for this phase: B3F6 destroys CX, while grcg_setcolor preserves it.
    _CX = charged_p1;
    if(_CX) {
        if(_CX < 64) color = 15;
        else if(_CX < 128) color = 10;
        else if(_CX < 192) color = 8;
        else if(_CX < 255) color = 6;
        else color = 12;
        grcg_setcolor(GC_RMW, color);
        _DX = 32;
        _BX = _CX;
        asm { call near ptr hud_gauge_bar_fill }
    }
    // Reload for this phase: B3F6 destroys CX, while grcg_setcolor preserves it.
    _CX = charged_p2;
    if(_CX) {
        if(_CX < 64) color = 15;
        else if(_CX < 128) color = 10;
        else if(_CX < 192) color = 8;
        else if(_CX < 255) color = 6;
        else color = 12;
        grcg_setcolor(GC_RMW, color);
        _DX = 352;
        _BX = _CX;
        asm { call near ptr hud_gauge_bar_fill }
    }
    asm {
        xor ax, ax
        out 07Ch, ax
    }
}

void far pascal round_C9FE(pid_t player)
{
    register int left;
    if(warning_flag[player] != WF_PORTRAIT) return;
    left = PLAYFIELD_LEFT;
    if(player != 0) left += PLAYFIELD_W_BORDERED;
    mrs_put_8(left, PLAYFIELD_TOP, player);
    warning_flag[player] = WF_FLASH_WHITE;
}

void far round_CA3C(void)
{
    register int frame;
    if(warning_flag[0] != WF_FLASH_WHITE &&
       warning_flag[1] != WF_FLASH_WHITE) return;
    snd_se_reset();
    snd_se_play(19);
    snd_se_update();
    hud_static_gauge_levels_put(0);
    hud_static_gauge_levels_put(1);
    if(warning_flag[0] == WF_FLASH_WHITE) {
        warning_flag[0] = WF_FLASH_RED;
        warning_text_put(0, TX_WHITE);
    }
    if(warning_flag[1] == WF_FLASH_WHITE) {
        warning_flag[1] = WF_FLASH_RED;
        warning_text_put(1, TX_WHITE);
    }
    for(frame = 0; frame < 27; frame++) {
        input_reset_sense_key_held();
        if(input_sp & INPUT_CANCEL) round_pause_or_quit();
        frame_delay(1);
        PaletteTone = 100 + (frame & 1) * 50;
        palette_show();
    }
}

void near pascal warning_text_put(pid_t player, unsigned int attribute)
{
    register unsigned int x = 4;
    if(player == 0) x += 40;
    gaiji_putsa(x, 11, warning_title_top, attribute);
    gaiji_putsa(x, 12, warning_title_middle, attribute);
    gaiji_putsa(x, 13, warning_title_bottom, attribute);
    x += 4;
    gaiji_putsa(x, 14, warning_forced_to_evade, attribute);
    if(gba_flag_next[player] != GBAF_BOSS) {
        gaiji_putsa(x + 2, 15, warning_gauge_level, attribute);
        gaiji_putca(x + 19, 15, gba_gauge_level[player] + 0x1F, TX_WHITE);
    } else {
        gaiji_putsa(x + 2, 15, warning_boss_level, attribute);
        gaiji_putca(x + 19, 15, gba_boss_level + 0x1F, TX_WHITE);
    }
    gaiji_putsa(x, 16, warning_life_in_peril, attribute);
}

// Local unsigned-byte representation view of the existing one-byte array.
// No new allocation, symbol, global enum change, or widened access.
#define warning_flag_bytes (reinterpret_cast<unsigned char near *>(warning_flag))

void far pascal round_CB81(pid_t player)
{
    unsigned int x;
    pid_t attacked = 1 - player;
    register unsigned int i;
    register unsigned int attribute_or_y;
    if(warning_flag_bytes[player] >= WF_FLASH_RED) {
        if(warning_flag_bytes[player] == WF_FLASH_RED)
            warning_brightness[player] = 0;
        if(warning_flag_bytes[player] < WF_FLASH_RED_END) {
            if(warning_flag_bytes[player] < (WF_FLASH_RED + 15))
                warning_brightness[player] += 13;
            else warning_brightness[player] -= 13;
            warning_flag_bytes[player]++;
            attribute_or_y = 1;
            if(warning_flag_bytes[player] & 1) {
                if(gba_flag_next[player] == GBAF_GAUGE_PELLET_INIT)
                    attribute_or_y = 0xA1;
                else if(gba_flag_next[player] == GBAF_GAUGE_BULLET_INIT)
                    attribute_or_y = 0x61;
                else attribute_or_y = 0x41;
                palette_restore_for_pid(attacked);
            } else {
                if(gba_flag_next[player] == GBAF_GAUGE_PELLET_INIT)
                    Palettes[attacked].c.b = 120;
                else if(gba_flag_next[player] == GBAF_GAUGE_BULLET_INIT) {
                    Palettes[attacked].c.r = 120;
                    Palettes[attacked].c.b = 120;
                } else Palettes[attacked].c.r = 120;
                palette_changed = true;
            }
            warning_text_put(player, attribute_or_y);
        } else {
            x = 4;
            if(attacked == 1) x += 40;
            i = 0;
            attribute_or_y = 11;
            while(i < 6) {
                text_putsa(x, attribute_or_y, warning_clear_line, TX_WHITE);
                i++;
                attribute_or_y++;
            }
            palette_restore_for_pid(attacked);
            warning_flag_bytes[player] = WF_NONE;
            gba_flag_active[player] = gba_flag_next[player];
            warning_brightness[player] = 0;
            warning_fading_out[player] = 0;
        }
    }
    // Deliberate fall-through: first active tick runs in the completion call.
    if(gba_flag_active[player] != GBAF_NONE) {
        if(warning_fading_out[player] == 0) {
            warning_brightness[player] += 4;
            if(warning_brightness[player] >= 0x90)
                warning_fading_out[player] = 1;
        } else {
            warning_brightness[player] -= 4;
            if(warning_brightness[player] <= 0)
                warning_fading_out[player] = 0;
        }
        Palettes[attacked].c.r = warning_brightness[player];
        palette_changed = true;
    }
}

#undef warning_flag_bytes
