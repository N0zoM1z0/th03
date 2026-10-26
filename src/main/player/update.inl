// Target-derived player state machine, load DA43..DE95 (1,106 bytes).
// Current core.cpp producer binds shot_release_frames[2] at DS:4B9C.
// Ownership excludes callees, shared storage, and adjacent player procedures.
void near pascal player_state_update(input_t input_raw, player_stuff_t near *player_raw)
{
    register player_stuff_t near *player;
    register input_t input = input_raw;
    int charged;
    input_t movement;
    unsigned char work;
    bool first_attempt;

    player = player_raw;
    player_cur = &players[pid.current];
    if(player->invincibility_time) {
        player->invincibility_time--;
    }
    if(damage_all_on[pid.current]) {
        damage_all_on[pid.current]--;
    }
    if(defeat_flag != DF_BANNER) {
        if(player->lose_anim_time == 0) {
            player_speed_base.aligned.x.v = player->speed_base.aligned.x.v;
            player_speed_base.aligned.y.v = player->speed_base.aligned.y.v;
            player_speed_base.diagonal.x.v = player->speed_base.diagonal.x.v;
            player_speed_base.diagonal.y.v = player->speed_base.diagonal.y.v;
            player->hyper();
            if(player->move_lock_time == 0) {
                if(!player->is_cpu) {
                    movement = input & INPUT_MOVEMENT;
                    first_attempt = true;
                    for(;;) {
                        work = player_move(movement);
                        if(work == MOVE_INVALID && first_attempt) {
                            if(player->human_movement_last != movement) {
                                movement &= ~player->human_movement_last;
                                first_attempt = false;
                                continue;
                            }
                            break;
                        }
                        if(work == MOVE_VALID) {
                            player_pos_update_and_clamp(player->center);
                        }
                        break;
                    }
                    if(first_attempt) {
                        player->human_movement_last = movement;
                    }
                } else {
                    player->cpu_frame++;
                    player_cpu_update(player);
                    if(target_formation_marker == 0) {
                        work = 6;
                    } else if(target_formation_marker == 255) {
                        work = 32;
                    } else if(target_formation_marker == 254) {
                        work = 7;
                    } else {
                        work = 10;
                    }
                    if((round_or_result_frame % work) == 0) {
                        shot_release_frames[pid.current] = 4;
                        input = INPUT_SHOT;
                    }
                    target_formation_marker = 0;
                    if(!player->is_hit) {
                        if(player->bombs || player->halfhearts > 3) {
                            if(player->cpu_charge_at_avail_ring[player->cpu_charge_at_avail_ring_p]
                                    < (player->gauge_avail >> 4)
                                || player->gauge_avail == GAUGE_MAX) {
                                shot_release_frames[pid.current] = 0;
                                input = INPUT_SHOT;
                                if(player->gauge_charged >= player->gauge_avail) {
                                    shot_release_frames[pid.current] = 4;
                                    input = 0;
                                    player->cpu_charge_at_avail_ring_p++;
                                    if(player->cpu_charge_at_avail_ring_p >= CHARGE_AT_AVAIL_RING_SIZE) {
                                        player->cpu_charge_at_avail_ring_p = 0;
                                    }
                                }
                            }
                        }
                    } else {
                        player->is_hit = false;
                        shot_release_frames[pid.current] = 4;
                        input = 0;
                    }
                }
            } else {
                player->move_lock_time--;
            }

            // The observed work byte is reused as the collision-suppression flag.
            work = false;
            if(player->knockback_active) {
                player_knockback_update(player);
                player->gauge_charged = 0;
                player->cpu_frame = 0;
                work = true;
            } else if(shot_release_frames[pid.current] <= 2 && !player->hyper_active) {
                if(player->gauge_charged < player->gauge_avail) {
                    player->gauge_charged += player->gauge_charge_speed;
                    if(player->gauge_charged > player->gauge_avail) {
                        player->gauge_charged = player->gauge_avail;
                        player->spell_ready_frames = 0;
                    }
                    if(player->gauge_charged == 0x180) {
                        snd_se_play(9);
                    }
                } else {
                    player->spell_ready_frames++;
                    if(player->spell_ready_frames >= SPELL_AUTOFIRE_FRAMES) {
                        goto fire_charge;
                    }
                }
            } else if(shot_release_frames[pid.current] <= 4) {
fire_charge:
                charged = player->gauge_charged;
                if(charged >= 0x400) {
                    player->chargeshot_add(player->center.x, player->center.y);
                    if(charged >= 0x800) {
                        warning_flag[pid.current] = WF_PORTRAIT;
                        if(charged >= GAUGE_MAX) {
                            if(gba_boss_launched_by == pid.current) {
                                goto fire_gauge_bullet;
                            }
                            gba_flag_next[pid.current] = GBAF_BOSS;
                            player->gauge_avail = 0x400;
                            if(gba_boss_level < GBA_BOSS_LEVEL_MAX) {
                                gba_boss_level++;
                            }
                            combo_points_for_boss_attack += 10240;
                            if(gba_boss_launched_by == 255) {
                                player->boss_attacks_fired++;
                            } else {
                                player->boss_attacks_reversed++;
                            }
                        } else if(charged >= 0xC00) {
fire_gauge_bullet:
                            player->gauge_attacks_fired++;
                            gba_flag_next[pid.current] = GBAF_GAUGE_BULLET_INIT;
                            player->gauge_avail -= 0x800;
                            if(gba_gauge_level[pid.current] < GBA_GAUGE_LEVEL_MAX) {
                                gba_gauge_level[pid.current]++;
                            }
                        } else {
                            player->gauge_attacks_fired++;
                            gba_flag_next[pid.current] = GBAF_GAUGE_PELLET_INIT;
                            player->gauge_avail -= 0x400;
                            if(gba_gauge_level[pid.current] < GBA_GAUGE_LEVEL_MAX) {
                                gba_gauge_level[pid.current]++;
                            }
                        }
                    }
                    player->invincibility_time += 6;
                    work = true;
                }
                player->gauge_charged = 0;
            }
            if(player->shot_active == SA_BLOCKED_FOR_THIS_FRAME) {
                input = 0;
            }
            if(player->move_lock_time == 0 && player->shot_active != SA_DISABLED) {
                if(((input & INPUT_SHOT) || player->shot_active == SA_BLOCKED_FOR_THIS_FRAME)
                    && shot_release_frames[pid.current] > 2) {
                    player_shots_add();
                    shot_release_frames[pid.current] = 0;
                } else if(!(input & INPUT_SHOT) && shot_release_frames[pid.current] < 8) {
                    shot_release_frames[pid.current]++;
                }
                if(input & INPUT_BOMB) {
                    player_bomb(player);
                }
                if(player->shot_active == SA_BLOCKED_FOR_THIS_FRAME) {
                    player->shot_active = SA_ENABLED;
                }
            }
            if(player->hyper_active) {
                if(player->gauge_avail > 0x400) {
                    player->gauge_avail -= 6;
                } else {
                    player->hyper_active = false;
                    player->gauge_avail = 0x400;
                }
                work = true;
            }
            if(defeat_flag == DF_NONE && !work) {
                player_hittest(4);
                if(player->is_hit) {
                    if(player->halfhearts) {
                        hitcircles_player_add(player->center.x.v, player->center.y.v, pid.current);
                        player->halfhearts = player->halfhearts - players_hit_damage_update(*player);
                        if(player->halfhearts < 0) {
                            player->halfhearts = 0;
                        }
                        if(player->halfhearts == 0) {
                            player->lose_anim_time = 48;
                            round_defeated_player = pid.current;
                        } else {
                            player->knockback_active = true;
                            player->knockback_time = KNOCKBACK_FRAMES;
                            player->invincibility_time = MISS_INVINCIBILITY_FRAMES;
                            player->move_lock_time = 64;
                        }
                        hud_static_halfhearts_put(pid.current);
                    }
                    player->is_hit = false;
                }
            }
        } else if(player->lose_anim_time != 255) {
            player_lose_anim_update(player);
        }
    }
    if(player_velocity.x.v == 0) {
        player->patnum_movement = 0;
    } else if(player_velocity.x.v < 0) {
        player->patnum_movement = 1;
    } else {
        player->patnum_movement = 2;
    }
    player->patnum_glow = 0;
    if(page_back) {
        if(player->hyper_active) {
            player->patnum_glow = 2;
        } else if(player->invincibility_time) {
            player->patnum_glow = 1;
        }
    }
}
