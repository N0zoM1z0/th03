#ifndef TH03_MIMA_GAMEPLAY_CANDIDATE_HPP
#define TH03_MIMA_GAMEPLAY_CANDIDATE_HPP
#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
// Semantic aliases of existing DGROUP storage, never allocations.
struct mima_chargeshot_t {
    unsigned char active;
    unsigned char unknown_1;
    PlayfieldSubpixel x;
    PlayfieldSubpixel y;
    playfield_subpixel_t velocity_x;
    playfield_subpixel_t velocity_y;
};
struct mima_bomb_column_t {
    playfield_subpixel_t x;
    unsigned int sprite_offset;
};
struct gauge_pattern_timing_t {
    unsigned char total_frames;
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char byte_3;
};
extern mima_chargeshot_t mima_chargeshots[PLAYER_COUNT][15];
extern mima_chargeshot_t near *mima_chargeshot_p;
extern unsigned char mima_chargeshot_active[PLAYER_COUNT];
extern unsigned char mima_chargeshot_frame[PLAYER_COUNT];
extern unsigned char mima_chargeshot_angles[6];
extern unsigned char mima_gauge_angle[PLAYER_COUNT];
extern unsigned char mima_gauge_angle_step[PLAYER_COUNT];
extern unsigned char mima_gauge_frame[PLAYER_COUNT];
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];
extern mima_bomb_column_t mima_bomb_columns[PLAYER_COUNT][8];
extern mima_bomb_column_t near *mima_bomb_column_p;
extern "C" {
void far pascal mima_chargeshots_reset(void);
void far pascal chargeshot_add_mima(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_mima(void);
void far pascal chargeshot_render_mima(void);
void far gba_gauge_pattern_pellet_mima(void);
void far gba_gauge_pattern_bullet_mima(void);
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal bomb_explosion_add(int x, int y, int pid);
void far pascal palette_restore_for_pid(pid_t pid);
}
void near pascal mima_chargeshot_activate(unsigned char player, unsigned char slot);
uint8_t far chargeshot_hittest_mima(void);
void near pascal mima_chargeshot_sprite_put(int x, int y, int sprite_offset);
void near pascal gauge_pattern_mima(unsigned int type);
void far mima_bomb_update(void);
void near mima_bomb_columns_render(void);
void far mima_bomb(void);
#endif
