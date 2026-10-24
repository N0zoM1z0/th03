#ifndef TH03_MAIN_PLAYER_EXATT_ENTITY_HPP
#define TH03_MAIN_PLAYER_EXATT_ENTITY_HPP

// Existing shared entity storage stays in the root DATA/BSS owner.
struct exatt_entity_t {
    unsigned char state;
    unsigned char frame;
    int x;
    int y;
    int velocity_x;
    int velocity_y;
    int target_x;
    int boundary_x;
    int duration;
    unsigned char pid;
    unsigned char unknown_11;
    unsigned char angle;
    unsigned char speed;
    int radius;
    unsigned char tail[10];
};
typedef char exatt_entity_size_must_be_20[(sizeof(exatt_entity_t) == 0x20) ? 1 : -1];

#endif
