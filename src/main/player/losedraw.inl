// Near-this Pascal member: one unused player word; DI is the signed16 loop counter.
void near pascal player_stuff_t::lose_render(void)
{
    unsigned char angle;
    sprite16_clip_set_for_pid(pid.current);
    sprite16_put_size.set(48, 48);
    for(_DI = 0, angle = player_lose_radius / 4; (int)_DI < 16; _DI++, angle += 16) {
        player_lose_particle_put(angle, angle + 32);
    }
    for(_DI = 0, angle = 0 - (player_lose_radius / 4); (int)_DI < 16; _DI++, angle += 16) {
        player_lose_particle_put(angle, angle - 32);
    }
    for(_DI = 0, angle = player_lose_radius / 4; (int)_DI < 16; _DI++, angle += 16) {
        player_lose_particle_put(angle, angle);
    }
}
