// Bounded result-statistics bodies within the original P_SHOT code segment.
void near pascal round_result_number_put(int x, int y, int value)
{
    if(value >= 10) {
        if(value >= 100) {
            gaiji_putca(x + 18, (y + 96) / 16, (value / 100) + gb_0, TX_WHITE);
            value %= 100;
        }
        gaiji_putca(x + 20, (y + 96) / 16, (value / 10) + gb_0, TX_WHITE);
        value %= 10;
    }
    gaiji_putca(x + 22, (y + 96) / 16, value + gb_0, TX_WHITE);
}

void near round_match_result_render(void)
{
    int winner = 1 - round_defeated_player;
    long value;
    int x = 4;
    player_stuff_t near *player;
    if(winner != 0) {
        x += 40;
    }
    if((round_or_result_frame & 7) == 1) {
        text_putsa(x, 8, result_label_combo, TX_WHITE);
        text_putsa(x, 10, result_label_gauge, TX_WHITE);
        text_putsa(x, 12, result_label_boss, TX_WHITE);
        text_putsa(x, 14, result_label_reversal, TX_WHITE);
        text_putsa(x, 16, result_label_panic, TX_WHITE);
        text_putsa(x, 20, result_label_total, TX_WHITE);
        if(resident->story_stage < 8) {
            text_putsa(x, 6, result_label_winner, TX_WHITE);
        } else {
            text_putsa(x, 6, result_label_clear, TX_WHITE);
            text_putsa(x, 18, result_label_lives, TX_WHITE);
        }
        player = &players[winner];
        if(round_or_result_frame == 1) {
            defeat_combo_hits_max = player->combo_hits_max;
            defeat_gauge_attacks_fired = player->gauge_attacks_fired;
            defeat_boss_attacks_fired = player->boss_attacks_fired;
            defeat_boss_attacks_reversed = player->boss_attacks_reversed;
            defeat_boss_panics_fired = player->boss_panics_fired;
            result_bonus_remaining = (long)defeat_combo_hits_max * 1000;
            result_bonus_remaining += (long)defeat_gauge_attacks_fired * 10000;
            result_bonus_remaining += (long)defeat_boss_attacks_fired * 15000;
            result_bonus_remaining += (long)defeat_boss_attacks_reversed * 20000;
            result_bonus_remaining += (long)defeat_boss_panics_fired * 30000;
            if(resident->story_stage == 8) {
                result_lives_remaining = resident->story_lives;
                result_bonus_remaining += (long)result_lives_remaining * 100000L;
                extends_gained = 255;
            }
            value = result_bonus_remaining / 192;
            if(value > 65535UL) {
                result_bonus_step = 65535U;
            } else {
                result_bonus_step = (unsigned int)value;
            }
            value = result_bonus_remaining;
            result_bonus_low = value % 10000;
            result_bonus_high = value / 10000;
        }
        round_result_number_put(x, 32, defeat_combo_hits_max);
        round_result_number_put(x, 64, defeat_gauge_attacks_fired);
        round_result_number_put(x, 96, defeat_boss_attacks_fired);
        round_result_number_put(x, 128, defeat_boss_attacks_reversed);
        round_result_number_put(x, 160, defeat_boss_panics_fired);
        if(resident->story_stage == 8) {
            round_result_number_put(x, 192, result_lives_remaining);
        }
    }

    x *= 8;
    hud_dynamic_5_digit_points_put(x + 216, 64, 1000, 15);
    hud_dynamic_5_digit_points_put(x + 216, 80, 10000, 15);
    hud_dynamic_5_digit_points_put(x + 216, 96, 15000, 15);
    hud_dynamic_5_digit_points_put(x + 216, 112, 20000, 15);
    hud_dynamic_5_digit_points_put(x + 216, 128, 30000, 15);
    if(resident->story_stage == 8) {
        hud_dynamic_5_digit_points_put(x + 208, 144, 10000, 15);
        hud_dynamic_5_digit_points_put(x + 216, 144, 0, 15);
    }
    if(result_bonus_low != 0) {
        hud_dynamic_5_digit_points_put(x + 216, 160, result_bonus_low, 12);
    } else {
        hud_dynamic_5_digit_points_put(x + 216, 160, 0, 12);
        hud_dynamic_5_digit_points_put(x + 200, 160, 0, 12);
        hud_dynamic_5_digit_points_put(x + 192, 160, 0, 12);
    }
    round_result_high_digits_put(x + 184, 160, result_bonus_high, 12);
    if((long)result_bonus_step < result_bonus_remaining) {
        score_add(result_bonus_step, winner);
        result_bonus_remaining -= result_bonus_step;
    } else if(result_bonus_remaining > 0) {
        score_add((unsigned int)result_bonus_remaining, winner);
        result_bonus_remaining = 0;
    }
}
