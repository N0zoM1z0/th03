// Existing polar-to-sprite particle helper.
void near pascal player_lose_particle_put(unsigned char angle_x, unsigned char angle_y)
{
    int left;
    int top;
    left = polar(player_lose_left, player_lose_radius, CosTable8[angle_x])
        + playfield_fg_shift_x[pid.current];
    top = polar(player_lose_top, player_lose_radius, SinTable8[angle_y]);
    sprite16_put(left, top, 0x34B4);
}
