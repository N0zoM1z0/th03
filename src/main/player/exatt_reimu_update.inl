// Reimu entity iteration and rendering; no storage definitions.
// The second original physical source owns its own entity iteration,
// flight transition, collision and render phases (8 slots per player).
enum reimu_update_state_t {
    REIMU_UPDATE_FREE = 0,
    REIMU_UPDATE_ACTIVE = 1,
    REIMU_UPDATE_FLYING = 2,
    REIMU_UPDATE_APPEARING_END = 0x14,
};

void far pascal exatt_update_reimu(void)
{
    unsigned char angle;
    register exatt_entity_t near *p;
    register int i;
    hitbox_hittest_skip_explosions = true;
    hitbox.radius.x.v = TO_SP(16);
    hitbox.radius.y.v = TO_SP(16);
    hitbox.pid = (1 - pid_current);
    p = &exatt_entities[pid_current][0];

    i = 0;
    for(; i < 8; ++i, p++) {
        if(!p->state) {
            continue;
        }
        if(p->state == REIMU_UPDATE_ACTIVE) {
            p->x += p->velocity_x;
            if((p->x <= 0) || (p->x >= TO_SP(PLAYFIELD_W))) {
                // Original compound negation is codegen-visible:
                // direct = -value failed independently in af765e.
                p->velocity_x *= -1;
                p->x += p->velocity_x;
            }
            p->y += p->velocity_y;
            if(p->y < TO_SP(-24)) {
                // Direct = -value also failed separately for vertical
                // bounce (native negative control af765f).
                p->velocity_y *= -1;
                p->y = TO_SP(-24);
            }
            if(p->y >= TO_SP(PLAYFIELD_H)) {
                p->state = REIMU_UPDATE_FREE;
                continue;
            }
            p->velocity_y++;
            hitbox.origin.center.x.v = p->x;
            hitbox.origin.center.y.v = p->y;
            hitbox_hittest();
            exatt_collmap_set(p->x, p->y);
        } else if(p->state == REIMU_UPDATE_FLYING) {
            exatt_entity_p = p;
            if(exatt_fly_update()) {
                angle = randring_far_next16_and(0x1F);
                angle = ((randring_far_next16_and(1) * 0x60) + angle + 0x80);
                vector2(
                    p->velocity_x, p->velocity_y,
                    angle, ((round_speed / 8) + 0x32)
                );
            }
        } else if(p->state <= REIMU_UPDATE_APPEARING_END) {
            p->state++;
        } else {
            p->state = REIMU_UPDATE_ACTIVE;
        }
    }
    hitbox_hittest_skip_explosions = false;
}

void far pascal exatt_render_reimu(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; ++i, p++) {
        if(p->state) {
            exatt_entity_p = p;
            reimu_exatt_render_one();
            p->frame++;
        }
    }
}

