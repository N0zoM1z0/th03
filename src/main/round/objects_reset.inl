void near round_objects_and_counters_reset(void)
{
    // This short original leaf clears every physical shot-pair record.
    // Signed index and near pointer advance AFTER each original store.
    shotpair_t near *shotpair = shotpairs;
    int i = 0;
    while(i < SHOTPAIR_COUNT) {
        shotpair->alive = false;
        ++i;
        shotpair++;
    }
    // Then reset the entire original Enemy/Fireball combined carrier,
    // not just the visible enemy subset. Exact native while (af895a).
    efe_t near *efe = efes;
    i = 0;
    while(i < EFE_COUNT) {
        efe->flag = EFF_FREE;
        ++i;
        efe++;
    }
    round_frame = 0;
    round_or_result_frame = 0;
    round_reset_flag = 1;
    round_reset_clear_flag = 0;
}
