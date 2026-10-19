// Complete natural-source proposal for MAIN load 9778..9AD6.
// Not compiled, linked, accepted, or credited as exact.
#pragma codeseg MAIN_01_TEXT main_01
#include "src/main/round/round_loop.hpp"

unsigned char near round_loop(void)
{
    while(round_quit_requested == 0) {
        collmap_reset();
        round_bullet_template_reset();
        pid_current = 0;
        pid.so_attack = 0;
        round_exatt_update_p1();
        round_boss_update_p1();
        round_player_hook_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_exatt_update_p2();
        round_boss_update_p2();
        round_player_hook_p2();
        round_hitcircles_update();
        round_shots_update();
        pid_current = 0;
        pid.so_attack = 0;
        round_chargeshot_update_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_chargeshot_update_p2();
        hud_start_anim_update();
        round_formations_update();
        round_bullets_update();
        round_enemies_update();
        round_fireballs_update();
        pid_current = 0;
        pid.so_attack = 0;
        round_gauge_pellet_p1();
        round_gauge_bullet_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_gauge_pellet_p2();
        round_gauge_bullet_p2();
        round_CEB2();
        input_mode();
        pid.current = 0;
        round_player_update(input_mp_p1, &players[0]);
        pid.current = 1;
        round_player_update(input_mp_p2, &players[1]);
        round_sound_update();
        if(input_sp & INPUT_CANCEL) {
            round_pause_or_quit();
        }
        round_CA3C();
        round_CB81(0);
        round_CB81(1);
        round_render_hook();
        if(stage_render_timing_flag && !(round_or_result_frame & 1)) {
            goto frame_advance;
        }
        round_egc_on();
        pid_current = 0;
        pid.so_attack = 0;
        round_bomb_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_bomb_p2();
        pid_current = 0;
        pid.so_attack = 0;
        round_boss_render_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_boss_render_p2();
        round_shots_render();
        round_enemies_render();
        round_fireballs_hittest_and_render();
        round_hitcircles_render();
        pid_current = 0;
        pid.so_attack = 0;
        round_exatt_render_p1();
        round_chargeshot_render_p1();
        pid_current = 1;
        pid.so_attack = 40;
        round_exatt_render_p2();
        round_chargeshot_render_p2();
        pid.current = 0;
        round_player_render(&players[0]);
        pid.current = 1;
        round_player_render(&players[1]);
        round_egc_off();
        pid.current = 0;
        round_DF18(&players[0]);
        pid.current = 1;
        round_DF18(&players[1]);
        round_CEE0();
        round_bullets_render();

        if(defeat_flag == DF_BANNER) {
            round_defeat_banner_render();
            if(resident->game_mode == GM_STORY) {
                goto story_result;
            }
            if(players[0].rounds_won >= 2 || players[1].rounds_won >= 2) {
                goto match_result;
            }
            if(round_or_result_frame == 160) {
                goto finish_background;
            }
            if(round_background_complete) {
                goto next_round;
            }
            goto render_hud;

        match_result:
            round_match_result_render();
            if(round_or_result_frame == stage_result_wait_frames) {
                goto finish_background;
            }
            if(round_background_complete) {
                round_score_store_winner(resident->pid_winner);
                return 2; // Target RET 9972: distinct match-completion exit.
            }
            goto render_hud;

        story_result:
            if(resident->pid_winner == 0) {
                goto match_result;
            }
            if(round_or_result_frame == 160) {
            finish_background:
                stage_background_update = round_background_finish;
            } else if(round_background_complete) {
                if(resident->story_lives) {
                    resident->story_lives--;
                next_round:
                    return 1; // Target RET 99A7.
                }
                round_score_store_winner(0);
                return 2; // Target RET 99B0: distinct game-over exit.
            }
        }

    render_hud:
        round_C830();
        round_C8C4();
        round_D52E();
        round_C9FE(0);
        round_C9FE(1);
        hud_start_anim_render();
        round_combos_update_and_render();
        stage_background_update();
        stage_demo_update();
        if(stage_render_timing_flag == 0) {
            while(stage_vsync_wait_frames > round_vsync_count) {
            }
            round_vsync_count = 0;
            stage_vsync_wait_frames = 1;
        } else if(!(round_or_result_frame & 1)) {
            round_vsync_count = 0;
            while(stage_vsync_wait_frames > round_vsync_count) {
            }
            stage_vsync_wait_frames = 2;
        }
        if(palette_changed) {
            round_palette_show();
            palette_changed = 0;
        }
        // Genuine PC-98 page-register writes. Page state remains natural C++.
        // Inline assembly is restricted to hardware I/O, not C++ control flow.
        asm {
            mov dx, 0xA6;
            mov al, page_front;
            out dx, al;
            mov dx, 0xA4;
            mov al, page_back;
            out dx, al;
        }
        page_front = _AL; // OUT leaves the just-shown page value in AL.
        page_back ^= 1;
        round_grcg_setcolor(0xC0, 0);
        _BX = 0x3932;
        round_playfield_clear();
        round_grcg_setcolor(0xC0, 1);
        _BX = 0x395A;
        round_playfield_clear();
        round_grcg_off();

    frame_advance:
        round_frame++;
        round_or_result_frame++;
        round_frame_mod16 = (unsigned char)round_frame & 15;
        round_frame_mod8 = round_frame_mod16 & 7;
        round_frame_mod4 = round_frame_mod8 & 3;
        round_frame_mod2 = round_frame_mod4 & 1;
        if(!(round_or_result_frame & 63)) {
            if(round_speed < 127) {
                round_speed++;
            }
            if(!(round_or_result_frame & 1023)) {
                round_randring_fill();
                if(players[0].hit_damage_next < 6) {
                    players[0].hit_damage_next++;
                }
                if(players[1].hit_damage_next < 6) {
                    players[1].hit_damage_next++;
                }
            }
            if(round_or_result_frame < 2000) {
                players[0].cpu_frame = 0;
                players[1].cpu_frame = 0;
            }
        }
    }
    return 0; // RET 9AD5
}

// Genuine score-transfer dependency at target load A289..A2D0.
// The packed experiment does NOT reproduce the intervening target placement.
#include "compat/rec98/th03/main/score.hpp"

void near pascal round_score_store_winner(int winner)
{
    for(int i = 0; i < SCORE_DIGITS; i++) {
        resident->score_last[winner].digits[i] = score_lebcd[winner].digits[i];
        resident->score_last[1 - winner].digits[i] = 0;
    }
}
