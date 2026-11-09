void near round_objects_and_counters_reset(void)
{
    // Clear all physical shotpairs with signed-index and near-pointer
    // advancement after each original alive-flag store.
    shotpair_t near *shotpair = shotpairs;
    int i;
    for(i = 0; i < SHOTPAIR_COUNT; ++i, ++shotpair) {
        shotpair->alive = false;
    }
    // Reset the entire Enemy/Fireball shared carrier, not only visible
    // enemies; the original two traversals reuse the same signed index.
    efe_t near *efe = efes;
    for(i = 0; i < EFE_COUNT; ++i, ++efe) {
        efe->flag = EFF_FREE;
    }
    round_frame = 0;
    round_or_result_frame = 0;
    round_reset_flag = 1;
    round_reset_clear_flag = 0;
}
