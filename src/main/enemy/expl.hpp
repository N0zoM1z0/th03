#ifndef TH03_MAIN_ENEMY_EXPL_HPP
#define TH03_MAIN_ENEMY_EXPL_HPP

typedef unsigned char uint8_t;
typedef char int8_t;
typedef unsigned int uint16_t;
typedef unsigned char pid_t;
typedef unsigned char bool;
#define false 0
#define true 1
typedef unsigned char pixel_length_8_t;

struct Subpixel {
    int v;
};

struct PlayfieldPoint {
    Subpixel x;
    Subpixel y;
};

typedef uint8_t efe_flag_t;

static const efe_flag_t EFF_EXPLOSION_IGNORING_ENEMIES = 9;
static const efe_flag_t EFF_EXPLOSION_HITTING_ENEMIES = 10;
static const int EFE_COUNT = 64;
static const int PLAYER_COUNT = 2;
static const int CHAIN_RING_SIZE = 16;

struct efe_t {
    efe_flag_t flag;
    uint8_t frame;
    PlayfieldPoint center;
    uint8_t explosion_max_enemy_hits_half;
    int8_t val1;
    pid_t pid;
    pixel_length_8_t size_pixels;
    int8_t val2[18];
    uint8_t chain_slot;
    int8_t val3[5];
    int8_t padding[14];
};

enum explosion_hittest_against_t {
    EHA_ENEMY = 0,
    EHA_PELLET = 1,
    EHA_FIREBALL = 2,
    EHA_FIREBALL_BLUE = 2,
    EHA_FIREBALL_RED = 3,

    _explosion_hittest_against_t_FORCE_UINT8 = 0xFF
};

struct chains_t {
    uint8_t hits[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t pellet_and_fireball_value[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t charge_fireball[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t charge_exatt[PLAYER_COUNT][CHAIN_RING_SIZE];
};

struct hitbox_t {
    union {
        PlayfieldPoint topleft;
        PlayfieldPoint center;
    } origin;
    PlayfieldPoint radius;
    Subpixel right;
    Subpixel bottom;
    pid_t pid;
};

extern efe_t efes[EFE_COUNT];
extern explosion_hittest_against_t explosion_hittest_against;
extern bool explosion_collision_in_last_hittest;
extern uint8_t explosion_collision_chain_slot;
extern chains_t chains;
extern hitbox_t hitbox;
extern uint8_t round_speed;

void far pascal score_add(uint16_t score, uint8_t pid);
void near pascal gauge_avail_add(pid_t pid, uint8_t charge);
uint16_t near pascal combo_add(pid_t pid, uint8_t chain_slot, uint16_t bonus);
void near pascal fire_point_based_boss_attack_or_panic(
    uint16_t points, pid_t pid
);
void near pascal explosion_collision_chain_slot_fire_charged_fireball(
    pid_t pid, efe_t near *efe
);

uint8_t far __cdecl explosions_hittest(void);

#endif
