#ifndef TH03_MAIN_PLAYER_EXATT_ENTITY_HPP
#define TH03_MAIN_PLAYER_EXATT_ENTITY_HPP

#include <stddef.h>

// Existing shared entity storage stays in the root DATA/BSS owner.
// TC4 aligns nested unions to 2 under -a2, introducing artificial padding.
// The original shared 32-byte entity is byte-packed; restore caller packing.
#pragma option -a1
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
    // The 0x11 byte has different meanings in different character scripts:
    // a signed angular step for Ellen and a projectile kind for Kotohime.
    // These are alternative views of one physical byte, not two fields.
    union {
        unsigned char unclassified;
        signed char ellen_spin_delta;
        unsigned char kotohime_extra_mode;
    } character_mode;
    unsigned char angle;
    unsigned char speed;
    int radius;
    // Byte 0x17 is a per-character mode bit in Rikako's projectiles.
    // The other characters must still be free to interpret the whole
    // 0x16..0x1F tail without adopting Rikako's meaning.
    union {
        unsigned char raw[10];
        struct {
            unsigned char unclassified_16;
            unsigned char homing_disabled; // +0x17: 0 = adjust angle toward rival
            unsigned char unclassified_18_to_1f[8];
        } rikako;
    } character;
};
#pragma option -a2
typedef char exatt_entity_size_must_be_20[(sizeof(exatt_entity_t) == 0x20) ? 1 : -1];
typedef char exatt_entity_mode_offset_must_be_11[
    (offsetof(exatt_entity_t, character_mode) == 0x11) ? 1 : -1
];
typedef char exatt_entity_character_offset_must_be_16[
    (offsetof(exatt_entity_t, character) == 0x16) ? 1 : -1
];
typedef char exatt_entity_rikako_flag_offset_must_be_17[
    (offsetof(exatt_entity_t, character.rikako.homing_disabled) == 0x17) ? 1 : -1
];

#endif
