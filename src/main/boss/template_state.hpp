#ifndef TH03_MAIN_BOSS_TEMPLATE_STATE_HPP
#define TH03_MAIN_BOSS_TEMPLATE_STATE_HPP

#include <stddef.h>

// The original 32-byte per-player BOSS template/state. All nine BOSS TUs
// and the shared controller refer to this SAME physical DGROUP storage.
// Characters interpret the trailing 0x18..0x1F bytes differently; none of
// those alternative views may change the original object stride.
struct boss_template_state_t {
    int center_x;                     // +00
    int center_y;                     // +02
    int scratch_x;                    // +04
    int scratch_y;                    // +06
    int velocity_x;                   // +08
    int velocity_y;                   // +0A
    int hp;                           // +0C
    sprite16_offset_t sprite_offset;  // +0E
    unsigned char hit;                // +10
    unsigned char mode;               // +11
    unsigned char angle;              // +12
    unsigned char pattern_i;          // +13
    unsigned char pattern_count;      // +14
    unsigned char render_mode;        // +15
    unsigned char render_frame;       // +16
    unsigned char move_phase;         // +17
    unsigned int effect_radius;       // +18
    signed char spin_delta;           // +1A: Rikako's signed mode
    unsigned char tail[5];            // +1B..+1F: other character views
};

typedef char boss_template_size_is_32[(sizeof(boss_template_state_t) == 32) ? 1 : -1];
typedef char boss_template_sprite_offset_is_0e[
    (offsetof(boss_template_state_t, sprite_offset) == 0x0E) ? 1 : -1
];
typedef char boss_template_mode_offset_is_11[
    (offsetof(boss_template_state_t, mode) == 0x11) ? 1 : -1
];
typedef char boss_template_radius_offset_is_18[
    (offsetof(boss_template_state_t, effect_radius) == 0x18) ? 1 : -1
];
typedef char boss_template_spin_offset_is_1a[
    (offsetof(boss_template_state_t, spin_delta) == 0x1A) ? 1 : -1
];

#endif
