// Reimu spawn, render and collision helpers in physical function order.
// Byte-sized original projectile slots and their fixed spawn geometry.
// These are compile-time values, not a new storage owner.
enum reimu_exatt_native_t {
    REIMU_EXATT_SLOTS = 8,
    REIMU_EXATT_SPAWN_X_RANGE = 0x1200,
    REIMU_EXATT_SPAWN_Y_MASK = 0x7FF,
    REIMU_EXATT_FLY_SPEED_BONUS = 0x5A,
    REIMU_EXATT_ORBIT_SPEED = 0x50,
    REIMU_EXATT_COLLISION_MAIN_WIDTH = 16,
    REIMU_EXATT_COLLISION_MAIN_HEIGHT = 32,
    REIMU_EXATT_COLLISION_SIDE_WIDTH = 8,
    REIMU_EXATT_COLLISION_SIDE_HEIGHT = 16,
    REIMU_EXATT_COLLISION_LEFT_OFFSET = TO_SP(12),
    REIMU_EXATT_COLLISION_RIGHT_STEP = TO_SP(24),
};

void far pascal exatt_add_reimu(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    for(register int i = 0; i < REIMU_EXATT_SLOTS; ++i, ++p) {
        if(!p->state) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(REIMU_EXATT_SPAWN_X_RANGE),
                randring_far_next16_and(REIMU_EXATT_SPAWN_Y_MASK),
                pid_, REIMU_EXATT_FLY_SPEED_BONUS
            );
            return;
        }
    }
}

void far pascal reimu_extra_add(int x, int y, unsigned char angle_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    for(register int i = 0; i < REIMU_EXATT_SLOTS; ++i, ++p) {
        if(!p->state) {
            p->state = REIMU_FLY_STATE_ACTIVE;
            p->frame = 0;
            p->x = x;
            p->y = y;
            p->pid = (1 - pid_current);
            vector2(p->velocity_x, p->velocity_y, angle_, REIMU_EXATT_ORBIT_SPEED);
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
    sprite16_clip.reset();
    sprite16_put_size.set(48, 48);
    register sprite16_offset_t sprite_offset = 0x1930;
    sprite_offset += ((frame / 4) % 3) * 6;
    sprite16_put(left - 24, top - 24, sprite_offset);
}

void near reimu_exatt_render_one(void)
{
    register exatt_entity_t near *p = exatt_entity_p;
    screen_x_t left = playfield_fg_x_to_screen(p->x, p->pid);
    screen_y_t top = (p->y >> 4) + 16;
    sprite16_put_size.set(48, 48);
    if(pid_current == 1) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }

    if(REIMU_FLY_STATE_ACTIVE == p->state) {
        register sprite16_offset_t sprite_offset = pid.so_attack + 0x280;
        unsigned char phase = (p->frame / 4);
        if((phase & 3) == 1) {
            sprite_offset += 6;
        } else if(phase & 3) {
            sprite_offset += 0x780 + ((phase & 1) * 6);
        }
        sprite16_put(left - 24, top - 24, sprite_offset);
        return;
    }
    if(REIMU_FLY_STATE_FLYING == p->state) {
        exatt_render_state2(left, top, *reinterpret_cast<unsigned int near *>(&p->frame));
    } else {
        exatt_render_state_other(left, top, *reinterpret_cast<unsigned int near *>(&p->state));
    }
}

void near pascal exatt_collmap_set(int x, int y)
{
    collmap_center.x.v = x;
    collmap_center.y.v = y;
    collmap_stripe_tile_w.set(REIMU_EXATT_COLLISION_MAIN_WIDTH);
    collmap_tile_h.set(REIMU_EXATT_COLLISION_MAIN_HEIGHT);
    collmap_pid = (1 - pid_current);
    collmap_set_rect_striped();

    collmap_center.x.v -= REIMU_EXATT_COLLISION_LEFT_OFFSET;
    collmap_stripe_tile_w.set(REIMU_EXATT_COLLISION_SIDE_WIDTH);
    collmap_tile_h.set(REIMU_EXATT_COLLISION_SIDE_HEIGHT);
    collmap_set_rect_striped();

    collmap_center.x.v += REIMU_EXATT_COLLISION_RIGHT_STEP;
    collmap_set_rect_striped();
}

