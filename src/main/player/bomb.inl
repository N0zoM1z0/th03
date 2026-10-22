// Drops a bomb, or starts a full-gauge hyper when no bombs remain.
extern "C" void near pascal player_bomb(player_stuff_t near *player)
{
    if(bomb_flag[pid.current] != BF_INACTIVE || player->hyper_active) {
        return;
    }
    if(player->bombs) {
        bomb_flag[pid.current] = BF_PREPARING;
        player->bombs--;
        player->invincibility_time = BOMB_FRAMES;
        hud_static_bombs_put(pid.current);
    } else {
        if(player->gauge_avail < GAUGE_MAX) {
            return;
        }
        damage_all_on[pid.current] = true;
        snd_se_play(7);
        player->hyper_active = player->playchar_paletted.v;
        bomb_explosion_add(player->center.x.v, player->center.y.v, pid.current);
    }
    story_skill_decrement();
}
