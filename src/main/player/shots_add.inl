void near player_shots_add(void)
{
    int i;
    Subpixel left;
    Subpixel top;
    int pair;
    player_stuff_t near *player = &players[pid.current];
    shotpair_t near *shotpair;

    top.v = player->center.y.v;
    if(player->shot_mode == SM_NONE) {
        return;
    }
    if(player->shot_mode == SM_4_PAIRS) {
        left.v = player->center.x.v + to_sp(-64.0f);
        pair = 0;
    } else if(player->shot_mode == SM_2_PAIRS) {
        left.v = player->center.x.v + to_sp(-32.0f);
        pair = 2;
    } else if(player->shot_mode == SM_1_PAIR) {
        left.v = player->center.x.v + to_sp(-16.0f);
        pair = 3;
    } else if(player->shot_mode == SM_REIMU_HYPER) {
        left.v = player->center.x.v + to_sp(-24.0f);
        top.v -= to_sp(1.0f);
        reimu_hyper_shot_add(left, top);
        left.v += to_sp(48.0f);
        reimu_hyper_shot_add(left, top);
        left.v = player->center.x.v + to_sp(-16.0f);
        pair = 3;
    }

    // Invalid shot modes retain the original uninitialized-local behavior.
    shotpair = shotpairs;
    snd_se_play(1);
    while(left.v <= to_sp(-32.0f)) {
        left.v += to_sp(32.0f);
        pair++;
    }
    for(i = 0; i < SHOTPAIR_COUNT; i++, shotpair++) {
        if(!shotpair->alive) {
            shotpair->alive = true;
            shotpair->unused_1 = 0;
            shotpair->topleft.x.v = left.v;
            shotpair->topleft.y.v = top.v;
            shotpair->velocity_y.v = to_sp(SHOT_VELOCITY);
            shotpair->so_pid = (pid.current == 0) ? 0 : SHOT_SO_PID;
            shotpair->so_anim = 0;
            shotpair->pid = pid.current;
            pair++;
            if(pair >= 4) {
                break;
            }
            left.v += to_sp(32.0f);
            if(left.v >= to_sp(PLAYFIELD_W)) {
                break;
            }
        }
    }
}
