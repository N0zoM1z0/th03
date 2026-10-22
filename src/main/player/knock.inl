// Select an outward quarter-circle, then decay its motion for 32 frames.
void near pascal player_knockback_update(player_stuff_t near *player)
{
    int vector_x;
    int vector_y;
    if(player->knockback_time == KNOCKBACK_FRAMES) {
        snd_se_play(2);
        player->knockback_angle = randring1_next16_and(0x3F);
        if(player->center.x.v < TO_SP(144)) {
            if(player->center.y.v > TO_SP(184)) {
                player->knockback_angle += 0xC0;
            }
        } else {
            if(player->center.y.v < TO_SP(184)) {
                player->knockback_angle += 0x40;
            } else {
                player->knockback_angle += 0x80;
            }
        }
        player->knockback_length = 64;
    }
    if(player->knockback_time > 32) {
        player->knockback_length -= 2;
        vector2(vector_x, vector_y, player->knockback_angle, player->knockback_length);
        player_velocity.x.v = vector_x;
        player_velocity.y.v = vector_y;
        player_pos_update_and_clamp(player->center);
    } else if(player->knockback_time == 0) {
        player->knockback_active = false;
    }
    player->knockback_time--;
}
