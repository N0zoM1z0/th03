// Natural combined-owner hypothesis, MAIN load 9B0F..A21F, not accepted.
// Real ordinary-play no-op hook, stage setup, then round initialization.
// Original shared translation-unit ownership remains unproved.
#pragma codeseg MAIN_01_TEXT main_01
#pragma option -a-
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/difficul.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/main/score.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/libs/sprite16/sprite16.h"
#include "compat/rec98/th03/main/enemy/efe.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/hud/start.hpp"
#include "compat/rec98/th03/main/hud/warning.hpp"
#include "compat/rec98/th03/main/defeat.hpp"
#pragma option -a2
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th02/formats/bfnt.h"
#include "compat/rec98/th03/snd/snd.h"
#include "src/main/sound/reset.hpp"
#include "src/main/hud/static.hpp"
#include "src/main/enemy/enemy.hpp"
#include <stddef.h>
#include "src/main/round/initialize.hpp"

// Link bindings for existing storage/functions only, never new allocation.
// See bindings.json. Names of previously unnamed state remain hypotheses.
extern unsigned char stage_render_timing_flag;       // DS:659A
extern unsigned int stage_result_wait_frames;    // DS:1188
extern unsigned int demo_frame;                  // DS:1186
extern unsigned char cpu_hit_damage_additional;  // DS:658A
extern unsigned char page_back, page_front;      // DS:658E,658F
extern void (near *stage_demo_update)(void);      // DS:118A
extern void (near *stage_background_update)(void); // DS:2660
extern char stage_lose_bfnt[], stage_round_bfnt[], stage_zikicw_bfnt[];
extern "C" {
void far hflip_lut_generate(void);
void far stage_score_render_cache_reset(void);    // sub_D5A2
void far pascal stage_score_credit_digit_set(unsigned char remaining); // sub_D6C0
void near stage_demo_update_none(void);           // sub_9B0F
void near stage_demo_update_active(void);         // sub_9AD6
void near stage_background_update_none(void);     // sub_B4A3
void near stage_prepare_shot_sprites(void);       // sub_E266
void far stage_palette_show(void);               // sub_A38E
void near pascal set_callbacks_reimu(int pid);
void near pascal set_callbacks_mima(int pid);
void near pascal set_callbacks_marisa(int pid);
void near pascal set_callbacks_ellen(int pid);
void near pascal set_callbacks_kotohime(int pid);
void near pascal set_callbacks_kana(int pid);
void near pascal set_callbacks_rikako(int pid);
void near pascal set_callbacks_chiyuri(int pid);
void near pascal set_callbacks_yumemi(int pid);
}

// Zero-output record contracts, not code-layout constraints.
#define FIELD(T,F,O,S) typedef char setup_##T##_##F[((offsetof(T,F)==O) && (sizeof(((T near *)0)->F)==S)) ? 1 : -1]
FIELD(player_stuff_t, playchar_paletted, 8, 1);
FIELD(player_stuff_t, speed_base, 9, 4);
FIELD(player_stuff_t, gauge_charge_speed, 0x17, 1);
FIELD(player_stuff_t, gauge_avail, 0x1A, 2);
FIELD(player_stuff_t, rounds_won, 0x6C, 1);
FIELD(player_stuff_t, cpu_safety_frames, 0x6E, 2);
FIELD(player_stuff_t, combo_bonus_max, 0x70, 2);
FIELD(player_stuff_t, combo_hits_max, 0x72, 1);
FIELD(resident_t, rank, 0xB, 1);
FIELD(resident_t, is_cpu, 0xE, 2);
FIELD(resident_t, rand, 0x10, 4);
FIELD(resident_t, key_mode, 0x16, 1);
FIELD(resident_t, score_last, 0x18, 16);
FIELD(resident_t, game_mode, 0x28, 1);
FIELD(resident_t, story_stage, 0x33, 1);
FIELD(resident_t, rem_credits, 0x36, 1);
FIELD(resident_t, demo_num, 0x39, 1);
FIELD(PlaycharPalettedOptional, v, 0, 1);
FIELD(score_lebcd_t, digits, 0, 8);
FIELD(playchar_speed_t, motion, 0, 4);
FIELD(playchar_speed_t, gauge_charge, 4, 1);
#undef FIELD
typedef char setup_scalar_abi[(sizeof(int)==2 && sizeof(long)==4) ? 1 : -1];
typedef char setup_player_size[(sizeof(player_stuff_t)==128) ? 1 : -1];
typedef char setup_speed_size[(sizeof(playchar_speed_t)==5) ? 1 : -1];
typedef char setup_resident_size[(sizeof(resident_t)==256) ? 1 : -1];
typedef char setup_near_pointer[(sizeof(unsigned char near *)==2) ? 1 : -1];
typedef char setup_far_pointer[(sizeof(resident_t far *)==4) ? 1 : -1];
typedef char setup_input_callback[(sizeof(input_mode)==4) ? 1 : -1];
typedef char setup_demo_callback[(sizeof(stage_demo_update)==2) ? 1 : -1];
typedef char setup_background_callback[(sizeof(stage_background_update)==2) ? 1 : -1];


// Same existing 32-byte record as the maintained Chiyuri/Marisa owners.
// This declaration creates no storage; only state is touched here.
struct exatt_entity_t {
    unsigned char state, frame;
    int x, y, velocity_x, velocity_y, target_x, boundary_x, duration;
    unsigned char pid, mode, angle, speed;
    int radius;
    unsigned char tail[10];
};
typedef char round_player_size[(sizeof(player_stuff_t) == 128) ? 1 : -1];
typedef char round_enemy_size[(sizeof(efe_t) == 48) ? 1 : -1];
typedef char round_shot_size[(sizeof(shotpair_t) == 14) ? 1 : -1];
typedef char round_exatt_size[(sizeof(exatt_entity_t) == 32) ? 1 : -1];
// Zero-output ABI checks. Offsets/sizes are historical storage contracts,
// not requests for code alignment. A failed check must stop the probe.
#define ROUND_FIELD(T, F, O, S) \
    typedef char round_abi_##T##_##F[ \
        ((offsetof(T, F) == (O)) && (sizeof(((T near *)0)->F) == (S))) ? 1 : -1]
ROUND_FIELD(player_stuff_t, center, 0x0, 4);
ROUND_FIELD(player_stuff_t, is_hit, 0x4, 1);
ROUND_FIELD(player_stuff_t, unused_1, 0x5, 1);
ROUND_FIELD(player_stuff_t, invincibility_time, 0x6, 1);
ROUND_FIELD(player_stuff_t, halfhearts, 0x7, 1);
ROUND_FIELD(player_stuff_t, playchar_paletted, 0x8, 1);
ROUND_FIELD(player_stuff_t, speed_base, 0x9, 4);
ROUND_FIELD(player_stuff_t, shot_mode, 0xD, 1);
ROUND_FIELD(player_stuff_t, patnum_movement, 0xE, 1);
ROUND_FIELD(player_stuff_t, patnum_glow, 0xF, 1);
ROUND_FIELD(player_stuff_t, knockback_time, 0x10, 1);
ROUND_FIELD(player_stuff_t, move_lock_time, 0x11, 1);
ROUND_FIELD(player_stuff_t, knockback_angle, 0x12, 1);
ROUND_FIELD(player_stuff_t, knockback_length, 0x13, 1);
ROUND_FIELD(player_stuff_t, knockback_active, 0x14, 1);
ROUND_FIELD(player_stuff_t, is_cpu, 0x15, 1);
ROUND_FIELD(player_stuff_t, cpu_dodge_strategy, 0x16, 1);
ROUND_FIELD(player_stuff_t, gauge_charge_speed, 0x17, 1);
ROUND_FIELD(player_stuff_t, gauge_charged, 0x18, 2);
ROUND_FIELD(player_stuff_t, gauge_avail, 0x1A, 2);
ROUND_FIELD(player_stuff_t, cpu_charge_at_avail_ring_p, 0x1C, 1);
ROUND_FIELD(player_stuff_t, bombs, 0x1D, 1);
ROUND_FIELD(player_stuff_t, hyper_active, 0x1E, 1);
ROUND_FIELD(player_stuff_t, lose_anim_time, 0x1F, 1);
ROUND_FIELD(player_stuff_t, human_movement_last, 0x20, 2);
ROUND_FIELD(player_stuff_t, shot_active, 0x22, 1);
ROUND_FIELD(player_stuff_t, spell_ready_frames, 0x23, 1);
ROUND_FIELD(player_stuff_t, cpu_charge_at_avail_ring, 0x24, 64);
ROUND_FIELD(player_stuff_t, hyper, 0x64, 2);
ROUND_FIELD(player_stuff_t, hyper_func, 0x66, 2);
ROUND_FIELD(player_stuff_t, chargeshot_add, 0x68, 4);
ROUND_FIELD(player_stuff_t, rounds_won, 0x6C, 1);
ROUND_FIELD(player_stuff_t, unused_2, 0x6D, 1);
ROUND_FIELD(player_stuff_t, cpu_safety_frames, 0x6E, 2);
ROUND_FIELD(player_stuff_t, combo_bonus_max, 0x70, 2);
ROUND_FIELD(player_stuff_t, combo_hits_max, 0x72, 1);
ROUND_FIELD(player_stuff_t, hit_damage_next, 0x73, 1);
ROUND_FIELD(player_stuff_t, cpu_frame, 0x74, 2);
ROUND_FIELD(player_stuff_t, gauge_attacks_fired, 0x76, 1);
ROUND_FIELD(player_stuff_t, boss_attacks_fired, 0x77, 1);
ROUND_FIELD(player_stuff_t, boss_attacks_reversed, 0x78, 1);
ROUND_FIELD(player_stuff_t, boss_panics_fired, 0x79, 1);
ROUND_FIELD(player_stuff_t, padding, 0x7A, 6);
ROUND_FIELD(resident_t, id, 0x0, 11);
ROUND_FIELD(resident_t, rank, 0xB, 1);
ROUND_FIELD(resident_t, playchar_paletted, 0xC, 2);
ROUND_FIELD(resident_t, is_cpu, 0xE, 2);
ROUND_FIELD(resident_t, rand, 0x10, 4);
ROUND_FIELD(resident_t, unused_1, 0x14, 1);
ROUND_FIELD(resident_t, bgm_mode, 0x15, 1);
ROUND_FIELD(resident_t, key_mode, 0x16, 1);
ROUND_FIELD(resident_t, pid_winner, 0x17, 1);
ROUND_FIELD(resident_t, score_last, 0x18, 16);
ROUND_FIELD(resident_t, game_mode, 0x28, 1);
ROUND_FIELD(resident_t, story_opponents, 0x29, 9);
ROUND_FIELD(resident_t, unused_2, 0x32, 1);
ROUND_FIELD(resident_t, story_stage, 0x33, 1);
ROUND_FIELD(resident_t, story_lives, 0x34, 1);
ROUND_FIELD(resident_t, show_score_menu, 0x35, 1);
ROUND_FIELD(resident_t, rem_credits, 0x36, 1);
ROUND_FIELD(resident_t, op_animation_fast, 0x37, 1);
ROUND_FIELD(resident_t, skill, 0x38, 1);
ROUND_FIELD(resident_t, demo_num, 0x39, 1);
ROUND_FIELD(resident_t, unused_3, 0x3A, 198);
ROUND_FIELD(efe_t, flag, 0x0, 1);
ROUND_FIELD(efe_t, frame, 0x1, 1);
ROUND_FIELD(efe_t, center, 0x2, 4);
ROUND_FIELD(efe_t, explosion_max_enemy_hits_half, 0x6, 1);
ROUND_FIELD(efe_t, val1, 0x7, 1);
ROUND_FIELD(efe_t, pid, 0x8, 1);
ROUND_FIELD(efe_t, size_pixels, 0x9, 1);
ROUND_FIELD(efe_t, val2, 0xA, 18);
ROUND_FIELD(efe_t, chain_slot, 0x1C, 1);
ROUND_FIELD(efe_t, val3, 0x1D, 5);
ROUND_FIELD(efe_t, padding, 0x22, 14);
ROUND_FIELD(shotpair_t, alive, 0x0, 1);
ROUND_FIELD(shotpair_t, unused_1, 0x1, 1);
ROUND_FIELD(shotpair_t, topleft, 0x2, 4);
ROUND_FIELD(shotpair_t, velocity_y, 0x6, 2);
ROUND_FIELD(shotpair_t, so_pid, 0x8, 2);
ROUND_FIELD(shotpair_t, so_anim, 0xA, 1);
ROUND_FIELD(shotpair_t, unused_2, 0xB, 1);
ROUND_FIELD(shotpair_t, pid, 0xC, 1);
ROUND_FIELD(shotpair_t, unused_3, 0xD, 1);
ROUND_FIELD(PlayfieldPoint, x, 0x0, 2);
ROUND_FIELD(PlayfieldPoint, y, 0x2, 2);
ROUND_FIELD(SPPoint8, x, 0x0, 1);
ROUND_FIELD(SPPoint8, y, 0x1, 1);
ROUND_FIELD(speed_t, aligned, 0x0, 2);
ROUND_FIELD(speed_t, diagonal, 0x2, 2);
ROUND_FIELD(exatt_entity_t, state, 0x0, 1);
ROUND_FIELD(exatt_entity_t, frame, 0x1, 1);
ROUND_FIELD(exatt_entity_t, x, 0x2, 2);
ROUND_FIELD(exatt_entity_t, y, 0x4, 2);
ROUND_FIELD(exatt_entity_t, velocity_x, 0x6, 2);
ROUND_FIELD(exatt_entity_t, velocity_y, 0x8, 2);
ROUND_FIELD(exatt_entity_t, target_x, 0xA, 2);
ROUND_FIELD(exatt_entity_t, boundary_x, 0xC, 2);
ROUND_FIELD(exatt_entity_t, duration, 0xE, 2);
ROUND_FIELD(exatt_entity_t, pid, 0x10, 1);
ROUND_FIELD(exatt_entity_t, mode, 0x11, 1);
ROUND_FIELD(exatt_entity_t, angle, 0x12, 1);
ROUND_FIELD(exatt_entity_t, speed, 0x13, 1);
ROUND_FIELD(exatt_entity_t, radius, 0x14, 2);
ROUND_FIELD(exatt_entity_t, tail, 0x16, 10);
#undef ROUND_FIELD
typedef char round_resident_size[(sizeof(resident_t) == 256) ? 1 : -1];
typedef char round_point_size[(sizeof(PlayfieldPoint) == 4) ? 1 : -1];
typedef char round_speed_size[(sizeof(speed_t) == 4) ? 1 : -1];
typedef char round_near_pointer_size[(sizeof(player_stuff_t near *) == 2) ? 1 : -1];
typedef char round_far_pointer_size[(sizeof(resident_t far *) == 4) ? 1 : -1];
typedef char round_scalar_abi[(sizeof(int) == 2 && sizeof(long) == 4 && sizeof(bool) == 1) ? 1 : -1];
typedef char round_gba_flag_size[(sizeof(gba_flag_t) == 1) ? 1 : -1];
typedef char round_hud_flag_size[(sizeof(hud_start_flag_t) == 1) ? 1 : -1];
typedef char round_warning_flag_size[(sizeof(warning_flag_t) == 1) ? 1 : -1];
typedef char round_defeat_flag_size[(sizeof(defeat_flag) == 1) ? 1 : -1];

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern int boss_active[PLAYER_COUNT];
// Inferred transition semantics; aliases of existing DS:2662/2663 only.
extern unsigned char playfield_transition_frame;
extern unsigned char playfield_transition_midpoint_reached;
// Existing initialized words DS:0090..0107, ten rows of six words.
// The valid story stages normally use rows 0..8; row 9 is retained storage.
extern const unsigned int story_cpu_safety_frames[10][6];
extern unsigned int combo_points_for_boss_attack;

// Existing functions, not placeholder implementations. Explicitly preserve
// the near C++ random-ring call and far C++ bullet/formation calls.
void near randring_fill(void);
void far bullets_reset(void);
extern "C" {
void near round_objects_and_counters_reset(void); // existing sub_E313
void far pascal reimu_chargeshots_reset(void);
void far pascal mima_chargeshots_reset(void);
void far pascal marisa_chargeshot_state_reset(void);
void far pascal chargeshots_reset_ellen(void);
void far pascal exatt_ellen_slots_init(void);
int far pascal IRand(void);
}


// Real callback selected for ordinary play, called indirectly each frame.
// Empty behavior is intentional; no code or alignment bytes are prescribed.
extern "C" void near stage_demo_update_none(void)
{
}

void near stage_setup(void)
{
    int playchar;
    long safety_frames;
    unsigned char near *speed;
    int i;
    player_stuff_t near *player;

    random_seed = resident->rand;
    text_fillca(' ', (TX_BLACK | TX_REVERSE));
    graph_copy_page(0);
    enemy_formations_load();
    round_id = 0;
    round_initialize();
    hflip_lut_generate();
    stage_score_render_cache_reset();
    stage_render_timing_flag = 0;
    if(resident->story_stage < 8) {
        stage_result_wait_frames = 320;
    } else {
        stage_result_wait_frames = 460;
    }
    if(resident->game_mode == GM_STORY) {
        for(i = 0; i < SCORE_DIGITS; i++) {
            score_lebcd[0].digits[i] = resident->score_last[0].digits[i];
        }
        switch(resident->story_stage) {
        case 0: case 1: cpu_hit_damage_additional = 3; break;
        case 2: case 3: cpu_hit_damage_additional = 2; break;
        case 4: case 5: cpu_hit_damage_additional = 1; break;
        default: cpu_hit_damage_additional = 0; break;
        }
        gba_gauge_level[0] = resident->story_stage + 1;
        gba_gauge_level[1] = resident->story_stage + 1;
        extends_gained = score_lebcd[0].digits[6];
        if(extends_gained >= EXTENDS_MAX || score_lebcd[0].digits[7] != 0) {
            extends_gained = EXTENDS_DISABLE;
        }
        stage_score_credit_digit_set(resident->rem_credits);
    } else {
        if(resident->is_cpu[1] && resident->is_cpu[0]) {
            safety_frames = 65535L;
        } else {
            switch(resident->rank) {
            case 0: safety_frames = 1000L; break;
            case 1: safety_frames = 1900L; break;
            case 2: safety_frames = 4000L; break;
            case 3: safety_frames = 65535L; break;
            }
        }
        // No synthetic default: the target leaves the local undefined for
        // invalid ranks. Valid configuration ranks are 0..3.
        players[1].cpu_safety_frames = players[0].cpu_safety_frames = safety_frames;
        gba_gauge_level[0] = GBA_GAUGE_LEVEL_MIN;
        gba_gauge_level[1] = GBA_GAUGE_LEVEL_MIN;
        extends_gained = EXTENDS_DISABLE;
        cpu_hit_damage_additional = 0;
        stage_score_credit_digit_set(3);
    }
    for(player = players, i = 0; i < PLAYER_COUNT; i++, player++) {
        player->rounds_won = 0;
        player->gauge_avail = (64 << 4);
        player->combo_hits_max = 0;
        player->combo_bonus_max = 0;
    }
    if(resident->demo_num == 0) {
        stage_demo_update = stage_demo_update_none;
    } else {
        demo_frame = 0;
        stage_demo_update = stage_demo_update_active;
        round_speed = (4 << 4);
        bullet_base_speed.v = 0;
        gba_boss_level = 8;
        gba_gauge_level[0] = 9;
        gba_gauge_level[1] = 9;
    }
    stage_background_update = stage_background_update_none;
    if(resident->demo_num != 0) {
        input_mode = input_mode_attract;
    } else if(resident->is_cpu[1] && resident->is_cpu[0]) {
        input_mode = input_mode_cpu_vs_cpu;
    } else if(resident->is_cpu[1]) {
        input_mode = input_mode_1p_vs_cpu;
    } else if(resident->is_cpu[0]) {
        input_mode = input_mode_cpu_vs_1p;
    } else if(resident->key_mode == KM_KEY_KEY) {
        input_mode = input_mode_key_vs_key;
    } else if(resident->key_mode == KM_JOY_KEY) {
        input_mode = input_mode_joy_vs_key;
    } else {
        input_mode = input_mode_key_vs_joy;
    }
    for(i = 0; i < PLAYER_COUNT; i++) {
        playchar = (players[i].playchar_paletted.v - 1) / 2;
        speed = (unsigned char near *)&PLAYCHAR_SPEEDS[playchar];
        player = &players[i];
        player->speed_base.aligned.x.v = *speed++;
        player->speed_base.aligned.y.v = *speed++;
        player->speed_base.diagonal.x.v = *speed++;
        player->speed_base.diagonal.y.v = *speed++;
        player->gauge_charge_speed = *speed;
        switch(playchar) {
        case 0: set_callbacks_reimu(i); break;
        case 1: set_callbacks_mima(i); break;
        case 2: set_callbacks_marisa(i); break;
        case 3: set_callbacks_ellen(i); break;
        case 4: set_callbacks_kotohime(i); break;
        case 5: set_callbacks_kana(i); break;
        case 6: set_callbacks_rikako(i); break;
        case 7: set_callbacks_chiyuri(i); break;
        case 8: set_callbacks_yumemi(i); break;
        }
    }
    super_entry_bfnt(stage_lose_bfnt);
    super_entry_bfnt(stage_round_bfnt);
    super_entry_bfnt(stage_zikicw_bfnt);
    stage_prepare_shot_sprites();
    stage_palette_show();
    graph_200line(0);
    sprite16_sprites_commit();
    page_back = 0;
    page_front = 1;
    _DX = 0xA6;
    _AL = 0;
    asm out dx, al;
    _DX = 0xA4;
    _AL = 1;
    asm out dx, al;
    snd_se_reset();
    hud_wipe();
    hud_static_put();
    grc_setclip(0, 0, (RES_X - 1), (SPRITE16_RES_Y - 1));
    snd_kaja_func(KAJA_SONG_PLAY, 0);
}

void near round_initialize(void)
{
    int i;
    long safety_frames;
    player_stuff_t near *player;
    int pid;

    boss_active[0] = 0;
    boss_active[1] = 0;
    ef_onehit = false;
    playfield_transition_frame = 0;
    playfield_transition_midpoint_reached = 0;
    enemy_speed = 0;
    round_objects_and_counters_reset();
    randring_fill();
    bullets_reset();
    for(pid = 0; pid < EFE_COUNT; pid++) {
        efes[pid].flag = EFF_FREE;
    }
    for(pid = 0; pid < 16; pid++) {
        exatt_entities[0][pid].state = 0;
        exatt_entities[1][pid].state = 0;
    }
    for(pid = 0; pid < SHOTPAIR_COUNT; pid++) {
        shotpairs[pid].alive = false;
    }
    reimu_chargeshots_reset();
    mima_chargeshots_reset();
    marisa_chargeshot_state_reset();
    chargeshots_reset_ellen();
    exatt_ellen_slots_init();

    if(resident->game_mode == GM_STORY) {
        pid = (round_id - resident->rem_credits + 3);
        if(pid > 5) {
            pid = 5;
        }
        // No invented lower clamp: original assumes this index is valid.
        safety_frames = story_cpu_safety_frames[resident->story_stage][pid];
        switch(resident->rank) {
        case 0: safety_frames /= 3; break;
        case 2: safety_frames *= 2; break;
        case 3: safety_frames *= 3; safety_frames += 500; break;
        }
        if(safety_frames > 65535L) {
            safety_frames = 65535L;
        }
        players[1].cpu_safety_frames = safety_frames;
    }

    switch(resident->rank) {
    case 0: // Easy
        round_speed = (round_id << 4);
        bullet_base_speed.v = 0;
        gba_boss_level = (resident->story_stage / 2 + round_id);
        if(resident->game_mode != GM_STORY) {
            gba_gauge_level[0]++;
            gba_gauge_level[1]++;
        }
        break;
    case 1: // Normal
        round_speed = (round_id << 5);
        bullet_base_speed.v = 0;
        gba_boss_level = (resident->story_stage + round_id * 2);
        if(resident->game_mode != GM_STORY) {
            gba_gauge_level[0] += 2;
            gba_gauge_level[1] += 2;
        }
        break;
    case 2: // Hard
        round_speed = ((round_id << 5) + (2 << 4));
        bullet_base_speed.v = 8;
        gba_boss_level = (resident->story_stage + round_id * 2 + 2);
        if(resident->game_mode != GM_STORY) {
            gba_gauge_level[0] += 2;
            gba_gauge_level[1] += 2;
        }
        break;
    case 3: // Lunatic
        round_speed = (6 << 4);
        bullet_base_speed.v = ((1 << 4) + 8);
        gba_boss_level = (resident->story_stage + round_id * 2 + 8);
        if(resident->game_mode != GM_STORY) {
            gba_gauge_level[0] += 4;
            gba_gauge_level[1] += 4;
        }
        break;
    }
    if(round_speed >= (ROUND_SPEED_MAX + 1)) {
        round_speed = ROUND_SPEED_MAX;
    }
    if(gba_boss_level > GBA_BOSS_LEVEL_MAX) {
        gba_boss_level = GBA_BOSS_LEVEL_MAX;
    }
    if(gba_gauge_level[0] > GBA_GAUGE_LEVEL_MAX) {
        gba_gauge_level[0] = GBA_GAUGE_LEVEL_MAX;
    }
    if(gba_gauge_level[1] > GBA_GAUGE_LEVEL_MAX) {
        gba_gauge_level[1] = GBA_GAUGE_LEVEL_MAX;
    }
    gba_boss_launched_by = PID_NONE;
    defeat_flag = DF_NONE;
    hud_start_flag = HSF_INIT;
    combo_points_for_boss_attack = 5120;
    round_frame_mod16 = 0;
    round_frame_mod8 = 0;
    round_frame_mod4 = 0;
    round_frame_mod2 = 0;

    player = players;
    for(pid = 0; pid < PLAYER_COUNT; pid++, player++) {
        enemies_alive[pid] = 0;
        player->playchar_paletted = resident->playchar_paletted[pid];
        player->is_cpu = resident->is_cpu[pid];
        player->is_hit = false;
        player->unused_1 = 0;
        player->invincibility_time = ROUND_START_INVINCIBILITY_FRAMES;
        player->is_hit = false; // Repeated by the original initializer.
        player->shot_mode = SM_1_PAIR;
        player->halfhearts = HALFHEARTS_MAX;
        player->knockback_time = 0;
        player->move_lock_time = 0;
        player->knockback_active = false;
        player->center.x.v = ((PLAYFIELD_W / 2) << 4);
        player->center.y.v = ((PLAYFIELD_H - 32) << 4);
        player->gauge_charged = 0;
        player->shot_active = SA_ENABLED;
        player->hit_damage_next = 1;
        for(i = 0; i < CHARGE_AT_AVAIL_RING_SIZE; i++) {
            player->cpu_charge_at_avail_ring[i] = (((IRand() & 3) << 6) + 0x3F);
        }
        player->cpu_charge_at_avail_ring_p = 0;
        player->bombs = 2;
        player->lose_anim_time = 0;
        player->hyper_active = 0;
        player->cpu_frame = 0;
        player->gauge_attacks_fired = 0;
        player->boss_attacks_fired = 0;
        player->boss_attacks_reversed = 0;
        player->boss_panics_fired = 0;
        gba_flag_active[pid] = GBAF_NONE;
        playfield_fg_shift_x[pid] = 0;
        damage_all_on[pid] = false;
        warning_flag[pid] = WF_NONE;
    }
    enemy_formations_randomize();
}
