// MAIN load 9778..9AD6. Names are inferred; existing storage stays external.
#pragma codeseg PLAYFLD_TEXT main_01
// Speed code generation preserves the separate match and game-over exits.
#pragma option -G
#include "src/main/round/round_loop.hpp"

unsigned char near round_loop(void)
{
    while(!round_quit_requested) {
        collmap_reset();
        bullet_template_reset_stuff();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        round_exatt_update_p1();
        gba_boss_update[0]();
        round_player_hook_p1();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        round_exatt_update_p2();
        gba_boss_update[1]();
        round_player_hook_p2();
        hitcircles_update();
        shots_update();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        chargeshot_update[0]();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        chargeshot_update[1]();
        hud_start_anim_update();
        enemy_formations_update();
        bullets_update();
        enemies_update();
        fireballs_update();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        gba_gauge_pattern_pellet[0]();
        gba_gauge_pattern_bullet[0]();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        gba_gauge_pattern_pellet[1]();
        gba_gauge_pattern_bullet[1]();
        player_effects_update();
        input_mode();
        pid.current = ROUND_PLAYER_LEFT;
        player_state_update(input_mp_p1, &players[0]);
        pid.current = ROUND_PLAYER_RIGHT;
        player_state_update(input_mp_p2, &players[1]);
        snd_se_update();
        if(input_sp & INPUT_CANCEL) {
            round_pause_or_quit();
        }
        round_CA3C();
        round_CB81(0);
        round_CB81(1);
        round_render_hook();
        // The unsigned-word even/odd cadence CAN use natural `%2`.
        // Keep this original goto frame_advance and all page flip calls.
        if(stage_render_timing_flag && !(round_or_result_frame % 2)) {
            goto frame_advance;
        }
        egc_on();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        round_bomb_p1();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        round_bomb_p2();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        gba_boss_render[0]();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        gba_boss_render[1]();
        shots_render();
        enemies_render();
        fireballs_hittest_and_render();
        hitcircles_render();
        pid_current = ROUND_PLAYER_LEFT;
        pid.so_attack = ROUND_SPRITE_BASE_LEFT;
        round_exatt_render_p1();
        chargeshot_render[0]();
        pid_current = ROUND_PLAYER_RIGHT;
        pid.so_attack = ROUND_SPRITE_BASE_RIGHT;
        round_exatt_render_p2();
        chargeshot_render[1]();
        pid.current = ROUND_PLAYER_LEFT;
        player_render(&players[0]);
        pid.current = ROUND_PLAYER_RIGHT;
        player_render(&players[1]);
        egc_off();
        pid.current = ROUND_PLAYER_LEFT;
        player_overlay_render(&players[0]);
        pid.current = ROUND_PLAYER_RIGHT;
        player_overlay_render(&players[1]);
        player_effects_render();
        bullets_render();

        if(defeat_flag == DF_BANNER) {
            round_defeat_banners_render();
            if(resident->game_mode == GM_STORY) {
                goto story_result;
            }
            if(players[0].rounds_won >= ROUND_VICTORY_ROUNDS || players[1].rounds_won >= ROUND_VICTORY_ROUNDS) {
                goto match_result;
            }
            if(round_or_result_frame == ROUND_RESULT_FINISH_BACKGROUND_AT) {
                goto finish_background;
            }
            if(playfield_transition_midpoint) {
                goto next_round;
            }
            goto render_hud;

        match_result:
            round_match_result_render();
            if(round_or_result_frame == stage_result_wait_frames) {
                goto finish_background;
            }
            if(playfield_transition_midpoint) {
                round_score_commit(resident->pid_winner);
                return ROUND_LOOP_END_MATCH; // Target RET 9972: distinct match-completion exit.
            }
            goto render_hud;

        story_result:
            if(resident->pid_winner == 0) {
                goto match_result;
            }
            if(round_or_result_frame == ROUND_RESULT_FINISH_BACKGROUND_AT) {
            finish_background:
                stage_background_update = stage_demo_finish;
            } else if(playfield_transition_midpoint) {
                if(resident->story_lives) {
                    resident->story_lives--;
                next_round:
                    return ROUND_LOOP_PLAY_NEXT; // Target RET 99A7.
                }
                round_score_commit(0);
                return ROUND_LOOP_END_MATCH; // Target RET 99B0: distinct game-over exit.
            }
        }

    render_hud:
        round_C830();
        round_C8C4();
        score_hud_render();
        round_C9FE(0);
        round_C9FE(1);
        hud_start_anim_render();
        combos_update_and_render();
        stage_background_update();
        stage_demo_update();
        if(!stage_render_timing_flag) {
            while(round_reset_flag > vsync_Count1) {
            }
            vsync_Count1 = 0;
            round_reset_flag = 1;
        } else if(!(round_or_result_frame % 2)) {
            vsync_Count1 = 0;
            while(round_reset_flag > vsync_Count1) {
            }
            round_reset_flag = 2;
        }
        if(palette_changed) {
            palette_show();
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
        // Preserve AL from the hardware OUT (the byte for the old back page).
        // Direct C++ page_back reload emits an additional MOV AL,memory
        // and shifts the original scheduler by two bytes (af785b).
        page_front = _AL;
        page_back ^= 1;
        grcg_setcolor(0xC0, 0);
        _BX = 0x3932;
        round_playfield_clear();
        grcg_setcolor(0xC0, 1);
        _BX = 0x395A;
        round_playfield_clear();
        grcg_off();

    frame_advance:
        // Both original global 16-bit clocks admit natural prefix
        // (af923f); these differ from the byte speed and scratch
        // frame-mask counters below.
        ++round_frame;
        ++round_or_result_frame;
        // Preserve original byte-frame &15: replacing with %16
        // changed real TC4 CODE (af923h), unlike word-valued modulo.
        round_frame_mod16 = (unsigned char)round_frame & 15;
        round_frame_mod8 = round_frame_mod16 & 7;
        round_frame_mod4 = round_frame_mod8 & 3;
        round_frame_mod2 = round_frame_mod4 & 1;
        if(!(round_or_result_frame & ROUND_SPEED_UPDATE_MASK)) {
            if(round_speed < ROUND_ENTRY_SPEED_MAX) {
                // Keep original mutable speed byte postfix: changing it
                // to prefix changes native original CODE (af923i).
                round_speed++;
            }
            if(!(round_or_result_frame & ROUND_RANDOM_REFILL_MASK)) {
                randring_fill();
                if(players[0].hit_damage_next < 6) {
                    players[0].hit_damage_next++;
                }
                if(players[1].hit_damage_next < 6) {
                    players[1].hit_damage_next++;
                }
            }
            if(round_or_result_frame < ROUND_CPU_RESET_WINDOW_END) {
                players[0].cpu_frame = 0;
                players[1].cpu_frame = 0;
            }
        }
    }
    return ROUND_LOOP_RETURN_TO_OP; // RET 9AD5
}
