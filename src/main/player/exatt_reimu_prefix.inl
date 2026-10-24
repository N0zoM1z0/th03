// Reimu spawn, render and collision helpers in physical function order.
void far pascal exatt_add_reimu(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(0x1200),
                randring_far_next16_and(0x7FF),
                pid_, 0x5A
            );
            return;
        }
    }
}

void far pascal reimu_extra_add(int x, int y, unsigned char angle_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            p->state = 1;
            p->frame = 0;
            p->x = x;
            p->y = y;
            p->pid = (1 - pid_current);
            vector2(p->velocity_x, p->velocity_y, angle_, 0x50);
            return;
        }
    }
}

void near pascal exatt_render_state2(
    screen_x_t left, screen_y_t top, unsigned char frame
)
{
    register sprite16_offset_t sprite_offset;
    if((frame & 1) == 0) {
        sprite_offset = 0x1928;
        if((frame & 7) <= 3) {
            sprite_offset += 4;
        }
        sprite16_put_size.set(32, 32);
        sprite16_clip.reset();
        sprite16_put(left - 16, top - 16, sprite_offset);
    }
}

void near pascal exatt_render_state_other(
    screen_x_t left, screen_y_t top, unsigned char frame
)
{
    register sprite16_offset_t sprite_offset;
    sprite16_clip.reset();
    sprite16_put_size.set(48, 48);
    sprite_offset = 0x1930;
    sprite_offset += ((frame / 4) % 3) * 6;
    sprite16_put(left - 24, top - 24, sprite_offset);
}

void near reimu_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    unsigned char phase;
    register exatt_entity_t near *p = exatt_entity_p;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    sprite16_put_size.set(48, 48);
    if(pid_current == 1) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }

    if(p->state == 1) {
        sprite_offset = (pid.so_attack + 0x280);
        phase = (p->frame / 4);
        if((phase & 3) == 1) {
            sprite_offset += 6;
        } else if((phase & 3) != 0) {
            sprite_offset += (0x780 + ((phase & 1) * 6));
        }
        sprite16_put(left - 24, top - 24, sprite_offset);
        return;
    }
    if(p->state == 2) {
        exatt_render_state2(left, top, *(unsigned int near *)&p->frame);
    } else {
        exatt_render_state_other(left, top, *(unsigned int near *)&p->state);
    }
}

void near pascal exatt_collmap_set(int x, int y)
{
    collmap_center.x.v = x;
    collmap_center.y.v = y;
    collmap_stripe_tile_w.set(16);
    collmap_tile_h.set(32);
    collmap_pid = (1 - pid_current);
    collmap_set_rect_striped();

    collmap_center.x.v -= TO_SP(12);
    collmap_stripe_tile_w.set(8);
    collmap_tile_h.set(16);
    collmap_set_rect_striped();

    collmap_center.x.v += TO_SP(24);
    collmap_set_rect_striped();
}

