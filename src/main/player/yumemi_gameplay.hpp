#ifndef TH03_YUMEMI_GAMEPLAY_PROPOSAL_HPP
#define TH03_YUMEMI_GAMEPLAY_PROPOSAL_HPP

#include <stddef.h>
#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

// Target: two consecutive six-byte slots, not a pointer into boss records.
struct yumemi_chargeshot_t {
    unsigned char state; // 0 inactive, 1 rising projectile, 2 expanding effect
    unsigned char frame;
    PlayfieldSubpixel x;
    PlayfieldSubpixel y;
};
typedef char yumemi_chargeshot_size_check[
    (sizeof(yumemi_chargeshot_t) == 6) ? 1 : -1
];

typedef char yumemi_chargeshot_frame_check[(offsetof(yumemi_chargeshot_t, frame) == 1) ? 1 : -1];
typedef char yumemi_chargeshot_x_check[(offsetof(yumemi_chargeshot_t, x) == 2) ? 1 : -1];
typedef char yumemi_chargeshot_y_check[(offsetof(yumemi_chargeshot_t, y) == 4) ? 1 : -1];

// This shared layout already exists in accepted charge/gauge owners.
// For Yumemi, total_frames is used as the ring count, and byte_1 as speed.
// Its other two fields are not accessed by this producer.
struct gauge_pattern_timing_t {
    unsigned char total_frames;
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char byte_3;
};
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];
extern yumemi_chargeshot_t yumemi_chargeshots[PLAYER_COUNT];
extern unsigned char yumemi_gauge_frame[PLAYER_COUNT];

// Shared acquisition state: the boss coordinates are the existing transformed
// boss_target values. They are not the raw center of the current boss record.
extern int boss_active[PLAYER_COUNT];
extern int boss_target_x;
extern int boss_target_y;
extern int ellen_target_x;
extern int ellen_target_y;
extern unsigned char target_formation_marker;

// Two opposite triangles: original semantic angle table, six unsigned bytes.
// This proposal does not allocate or move its original DATA storage.
extern unsigned char yumemi_bomb_triangle_angles[6];

extern "C" {
void far pascal ellen_target_set(pid_t player);
void far pascal yumemi_chargeshots_reset(void);
void far pascal chargeshot_add_yumemi(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_yumemi(void);
void far pascal chargeshot_render_yumemi(void);
void far gba_gauge_pattern_pellet_yumemi(void);
void far gba_gauge_pattern_bullet_yumemi(void);
void far pascal palette_restore_for_pid(pid_t player);
void far pascal bomb_axis_add(int x, int y, int player);
}
uint8_t far chargeshot_hittest_yumemi(void);
void near pascal yumemi_chargeshot_ring_render(
    sprite16_offset_t sprite_offset, int radius, unsigned char y_phase
);
void near pascal gauge_pattern_yumemi(unsigned int type);
void far yumemi_bomb(void);

#endif
