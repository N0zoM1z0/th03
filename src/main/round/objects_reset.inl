void near round_objects_and_counters_reset(void)
{
    shotpair_t near *shotpair = shotpairs;
    for(int i = 0; i < SHOTPAIR_COUNT; i++, shotpair++) {
        shotpair->alive = false;
    }
    efe_t near *efe = efes;
    for(i = 0; i < EFE_COUNT; i++, efe++) {
        efe->flag = EFF_FREE;
    }
    round_frame = 0;
    round_or_result_frame = 0;
    round_reset_flag = 1;
    round_reset_clear_flag = 0;
}
