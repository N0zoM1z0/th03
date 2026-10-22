// Base sprite pass; the overlay pass handles blink/glow frames separately.
void near pascal player_render(player_stuff_t near *player)
{
    screen_x_t left;
    screen_y_t top;
    sprite16_offset_t sprite;
    if(player->lose_anim_time) {
        if(player->lose_anim_time != 0xFF) {
            player_lose_anim_render(player);
        }
    } else if(player->patnum_glow == 0) {
        sprite16_clip.reset();
        sprite16_put_size.set(32, 64);
        left = playfield_fg_x_to_screen(player->center.x.v, pid.current) - 16;
        top = player->center.y.to_pixel() - 16;
        sprite = 0x2844 + (player->patnum_movement * 4);
        if(pid.current) {
            sprite += 0x0A00;
        }
        sprite16_put(left, top, sprite);
    }
}
