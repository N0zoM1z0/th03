void near hud_start_anim_update(void)
{
    int speed_y;
    signed char turn;
    register int i;
    register int x;

    if(hud_start_flag == HUD_INTRO_RESET_REQUEST) {
        hud_intro_frame = 0;
        hud_start_particle_p = &hud_start_particles[0];
        x = -0x120;
        speed_y = 0x54;
        for(i = 0; i < HUD_SLIDE_STRIPS; ++i, ++hud_start_particle_p, speed_y++, x += 8) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = speed_y;
            hud_start_particle_p->velocity = 8;
            hud_start_particle_p->active = 1;
        }
        hud_intro_phase = HUD_PHASE_SLIDE;
        if(resident->game_mode == GM_STORY) {
            hud_intro_sprite = 0x16;
        } else {
            hud_intro_sprite = 0x1A;
        }
        hud_start_flag = HUD_INTRO_RUNNING;
        hud_intro_x = 0;
    }
    // Finish exactly one active animation phase per update; even when
    // its state advances, the next phase does not run on the same tick.
    if(hud_intro_phase == HUD_PHASE_SLIDE) {
        hud_start_particle_p = &hud_start_particles[0];
        for(i = 0; i < HUD_SLIDE_STRIPS; ++i, ++hud_start_particle_p) {
            if(hud_start_particle_p->active) {
                asm { mov bx, hud_start_particle_p }
                ((hud_start_particle_t near *)_BX)->x +=
                    ((hud_start_particle_t near *)_BX)->velocity;
                if(((hud_start_particle_t near *)_BX)->active == 1) {
                    if(((hud_start_particle_t near *)_BX)->x >= 0x60) {
                        ((hud_start_particle_t near *)_BX)->active = 2;
                    }
                } else {
                    if(hud_start_particle_p->x <= 0x40) {
                        hud_start_particle_p->x = 0x40;
                        hud_start_particle_p->active = 0;
                        if(i == 0) {
                            hud_intro_phase = 1;
                        }
                    } else {
                        hud_start_particle_p->velocity--;
                    }
                }
            }
        }
        return;
    }
    if(hud_intro_phase == HUD_PHASE_BANNER) {
        hud_intro_frame++;
        if(hud_intro_frame > 0x56) {
            hud_intro_phase++;
        }
        return;
    }
    if(hud_intro_phase == HUD_PHASE_CREATE_STARS) {
        hud_start_particle_p = &hud_start_particles[0];
        x = 0x600;
        for(i = 0; i < HUD_STARS_PER_SIDE; ++i, ++hud_start_particle_p, x += 0x20) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = randring1_next16_and(0x01FF) + 0x0A80;
            hud_start_particle_p->angle = static_cast<unsigned char>(randring1_next16());
            hud_start_particle_p->turn_early = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->turn_late = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->active = 1;
        }
        x = 0x1A00;
        for(i = 0; i < HUD_STARS_PER_SIDE; ++i, ++hud_start_particle_p, x += 0x20) {
            hud_start_particle_p->x = x;
            hud_start_particle_p->y = randring1_next16_and(0x01FF) + 0x0A80;
            hud_start_particle_p->angle = static_cast<unsigned char>(randring1_next16());
            hud_start_particle_p->turn_early = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->turn_late = static_cast<unsigned char>(IRand() % 3);
            hud_start_particle_p->active = 1;
        }
        hud_intro_phase++;
        hud_intro_frame = 0;
        return;
    }
    if(hud_intro_phase == HUD_PHASE_MOVE_STARS) {
        hud_intro_frame++;
        if(hud_intro_frame >= 0x40) {
            hud_intro_phase++;
        }
        hud_start_particle_p = &hud_start_particles[0];
        for(i = 0; i < HUD_TOTAL_STARS; ++i, ++hud_start_particle_p) {
            if(hud_start_particle_p->active) {
                asm { mov bx, hud_start_particle_p }
                x = polar(0, 80, CosTable8[((hud_start_particle_t near *)_BX)->angle]);
                speed_y = polar(0, 80, SinTable8[hud_start_particle_p->angle]);
                hud_start_particle_p->x += x;
                hud_start_particle_p->y += speed_y;
                if(
                    (hud_start_particle_p->x < 0) ||
                    (hud_start_particle_p->x >= 0x2700) ||
                    (hud_start_particle_p->y < 0) ||
                    (hud_start_particle_p->y >= 0x1800)
                ) {
                    hud_start_particle_p->active = 0;
                } else {
                    turn = (hud_intro_frame < 0x20)
                        ? hud_start_particle_p->turn_early
                        : hud_start_particle_p->turn_late;
                    turn--;
                    hud_start_particle_p->angle += (turn << 2);
                }
            }
        }
    } else {
        hud_start_flag = HUD_INTRO_STOPPED;
    }
}
