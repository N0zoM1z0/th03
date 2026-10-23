// MAIN A44C..B37C: resource loading and all nine character callback sets.
// Historical names and translation-unit grouping remain inferred.
#pragma codeseg HITCIRC_TEXT main_01
#pragma option -a1
#include "src/main/player/stuff.hpp"
#pragma option -a2
#include "src/main/player/exatt.hpp"
#include "src/main/player/character_setup.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "src/main/player/hyper.hpp"
#include "src/main/formats/mrs.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include <stddef.h>
extern const char character_filename_template[12];
typedef void (far *callback_void_t)(void);
extern callback_void_t round_player_hook_p1, round_player_hook_p2;
extern callback_void_t round_bomb_p1, round_bomb_p2;
extern callback_void_t main_background_init, round_render_hook, round_background_reset;
void far background_chain1_init(void);
void far background_chain1_accelerate(void);
void far background_chain2_init(void);
void far background_chain2_accelerate(void);
void far background_velocity_reset(void);
void far shared_bomb_lifecycle_update(void);
extern "C" void far stage_palette_backup(void);
#pragma samecodeseg stage_palette_backup
#define DECLARE_CHARACTER(c) \
extern "C" { \
void far pascal exatt_add_##c(int x, int y, unsigned char pid); \
void far pascal exatt_update_##c(void); \
void far pascal exatt_render_##c(void); \
void far pascal chargeshot_add_##c(Subpixel center_x, Subpixel center_y); \
void far pascal chargeshot_update_##c(void); \
void far pascal chargeshot_render_##c(void); \
void far gba_gauge_pattern_pellet_##c(void); \
void far gba_gauge_pattern_bullet_##c(void); \
void far pascal boss_##c##_template_init(int pid); \
void far gba_boss_update_##c(void); \
void far gba_boss_render_##c(void); \
} \
uint8_t far chargeshot_hittest_##c(void); \
void far c##_bomb(void);
DECLARE_CHARACTER(reimu)
DECLARE_CHARACTER(mima)
DECLARE_CHARACTER(marisa)
DECLARE_CHARACTER(ellen)
DECLARE_CHARACTER(kotohime)
DECLARE_CHARACTER(kana)
DECLARE_CHARACTER(rikako)
DECLARE_CHARACTER(chiyuri)
DECLARE_CHARACTER(yumemi)
#undef DECLARE_CHARACTER
void far reimu_bomb_update(void);
void far mima_bomb_update(void);
void far ellen_bomb_update(void);

// Four-byte callback addresses, existing 128-byte player records only.
typedef char callback_shapes[(sizeof(player_stuff_t) == 128 &&
    offsetof(player_stuff_t, playchar_paletted) == 8 &&
    offsetof(player_stuff_t, hyper) == 0x64 &&
    offsetof(player_stuff_t, hyper_func) == 0x66 &&
    offsetof(player_stuff_t, chargeshot_add) == 0x68 &&
    sizeof(exatt_funcs_t) == 12 && sizeof(callback_void_t) == 4 &&
    sizeof(nearfunc_t_near) == 2) ? 1 : -1];
extern "C" void near pascal character_sprite_pair_load(int slot, char far *fn)
{
    super_entry_bfnt(fn);
    fn[2]='e'; fn[3]='x'; fn[5]='m'; fn[6]='r'; fn[7]='s';
    mrs_load(slot,fn);
    fn[2]='b'; fn[3]='m';
    mrs_load(slot+2,fn);
}
extern "C" void near character_sprites_finalize(void)
{
    mrs_hflip(1);
    mrs_hflip(3);
    respal_get_palettes();
    palette_show();
    stage_palette_backup();
}
extern "C" void near pascal character_resources_load(int pid, int resource)
{
    char fn[12];
    for(int i=0; i<12; i++) {
        fn[i]=character_filename_template[i];
    }
    resource -= (players[pid].playchar_paletted.v & 1);
    if(resource>=10) {
        fn[0] += resource / 10;
        resource %= 10;
    }
    fn[1] += resource;
    character_sprite_pair_load(pid, fn);
}
// No-argument Pascal/C callbacks share the far zero-argument stack ABI.
#define BIND_CHARACTER(c, p, hook, bomb, bomb_update) \
    exatt_funcs[p].add = exatt_add_##c; \
    exatt_funcs[p].update = (callback_void_t)exatt_update_##c; \
    exatt_funcs[p].render = (callback_void_t)exatt_render_##c; \
    players[p].chargeshot_add = chargeshot_add_##c; \
    chargeshot_update[p] = chargeshot_update_##c; \
    chargeshot_render[p] = chargeshot_render_##c; \
    chargeshot_hittest[p] = chargeshot_hittest_##c; \
    gba_gauge_pattern_pellet[p] = (farfunc_t_near)gba_gauge_pattern_pellet_##c; \
    gba_gauge_pattern_bullet[p] = (farfunc_t_near)gba_gauge_pattern_bullet_##c; \
    gba_boss_update[p] = (farfunc_t_near)gba_boss_update_##c; \
    gba_boss_render[p] = (farfunc_t_near)gba_boss_render_##c; \
    hook = bomb_update; \
    bomb = c##_bomb; \
    players[p].hyper_func = hyper_##c; \
    players[p].hyper = hyper_standby;

#define DEFINE_CHARACTER(c, resource, chain, bomb_update) \
extern "C" void near pascal set_callbacks_##c(int pid) \
{ \
    character_resources_load(pid, resource); \
    if(pid == 0) { \
        BIND_CHARACTER(c, 0, round_player_hook_p1, round_bomb_p1, bomb_update) \
    } else { \
        BIND_CHARACTER(c, 1, round_player_hook_p2, round_bomb_p2, bomb_update) \
        character_sprites_finalize(); \
    } \
    main_background_init = background_chain##chain##_init; \
    round_render_hook = background_chain##chain##_accelerate; \
    round_background_reset = background_velocity_reset; \
    boss_##c##_template_init(pid); \
}
DEFINE_CHARACTER(reimu, 1, 1, reimu_bomb_update)
DEFINE_CHARACTER(mima, 3, 1, mima_bomb_update)
DEFINE_CHARACTER(marisa, 5, 2, shared_bomb_lifecycle_update)
DEFINE_CHARACTER(ellen, 7, 2, ellen_bomb_update)
DEFINE_CHARACTER(kotohime, 9, 2, shared_bomb_lifecycle_update)
DEFINE_CHARACTER(kana, 11, 2, shared_bomb_lifecycle_update)
DEFINE_CHARACTER(rikako, 13, 1, shared_bomb_lifecycle_update)
DEFINE_CHARACTER(chiyuri, 15, 2, shared_bomb_lifecycle_update)
DEFINE_CHARACTER(yumemi, 17, 2, shared_bomb_lifecycle_update)
#undef DEFINE_CHARACTER
#undef BIND_CHARACTER
