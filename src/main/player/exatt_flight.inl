// Shared MAIN_06 flight functions; no storage definitions.
unsigned char near cdecl exatt_fly_update(void)
{
    register exatt_entity_t near *p = exatt_entity_p;
    register int next_x = p->x;
    next_x += p->velocity_x;

    if(exatt_entity_p->pid != 0) {
        goto negative_direction;
    }
    if(p->boundary_x > next_x) {
        goto moving;
    }

arrived:
    p->x = p->target_x;
    p->state = 3;
    p->pid = (1 - pid_current);
    return 1;

negative_direction:
    if(p->boundary_x >= next_x) {
        goto arrived;
    }

moving:
    p->x = next_x;
    p->y += p->velocity_y;
    return 0;
}

void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y, unsigned char pid_, int speed
)
{
    register int screen_target_x = target_x;
    register exatt_entity_t near *p = exatt_entity_p;

    p->state = 2;
    p->frame = 0;
    p->x = x;
    p->y = y;
    p->pid = pid_;

    x = playfield_fg_x_to_screen(x, pid_);
    p->target_x = screen_target_x;
    screen_target_x = playfield_fg_x_to_screen(
        screen_target_x, (1 - pid_)
    );
    vector2_between_plus(
        TO_SP(x), y, TO_SP(screen_target_x), target_y,
        0, p->velocity_x, p->velocity_y, ((round_speed / 4) + speed)
    );
    p->boundary_x = screen_x_to_playfield(screen_target_x, pid_);
}
