#ifndef TH03_MAIN_ENEMY_FIREBALL_EXACT_HPP
#define TH03_MAIN_ENEMY_FIREBALL_EXACT_HPP

typedef unsigned char bool;
typedef char int8_t;
typedef int int16_t;
typedef long int32_t;
typedef unsigned char uint8_t;
typedef unsigned int uint16_t;
typedef unsigned long uint32_t;
#define false 0
#define true 1

typedef int pixel_t;
typedef int8_t pixel_delta_8_t;
typedef uint8_t pixel_length_8_t;
typedef int screen_x_t;
typedef int screen_y_t;
typedef int vram_h_t;
typedef unsigned int uvram_byte_amount_t;

typedef unsigned char pid_t;
typedef int16_t pid2;
#define PLAYER_COUNT 2

typedef uint8_t subpixel_length_8_t;
typedef int subpixel_t;
static const subpixel_t SUBPIXEL_FACTOR = 16;
static const char SUBPIXEL_BITS = 4;
#define TO_SP(v) ((v) << SUBPIXEL_BITS)
#define TO_PIXEL(v) ((v) >> SUBPIXEL_BITS)

inline subpixel_t to_sp(float pixel_v)
{
    return static_cast<subpixel_t>(pixel_v * SUBPIXEL_FACTOR);
}

inline subpixel_length_8_t to_sp8(float pixel_v)
{
    return static_cast<subpixel_length_8_t>(to_sp(pixel_v));
}

template <class SubpixelType, class PixelType> class SubpixelBase {
public:
    typedef SubpixelBase<SubpixelType, PixelType> SelfType;
    SubpixelType v;

    SubpixelType operator +(float pixel_v) const
    {
        return (this->v + static_cast<SubpixelType>(to_sp(pixel_v)));
    }

    SubpixelType operator -(const SelfType &other) const
    {
        return (this->v - other.v);
    }

    void operator +=(float pixel_v)
    {
        this->v += static_cast<SubpixelType>(to_sp(pixel_v));
    }

    void operator -=(float pixel_v)
    {
        this->v -= static_cast<SubpixelType>(to_sp(pixel_v));
    }

    void set(float pixel_v)
    {
        v = static_cast<SubpixelType>(to_sp(pixel_v));
    }

    void set(const PixelType &pixel_v)
    {
        v = static_cast<SubpixelType>(TO_SP(pixel_v));
    }

    PixelType to_pixel() const
    {
        return static_cast<PixelType>(TO_PIXEL(v));
    }

    operator SubpixelType() const
    {
        return v;
    }
};

template <class T> struct SPPointBase {
    T x, y;

    void set(float screen_x, float screen_y)
    {
        x.set(screen_x);
        y.set(screen_y);
    }
};

typedef SubpixelBase<subpixel_t, pixel_t> Subpixel;

struct SPPoint : public SPPointBase<Subpixel> {
    void set_long(subpixel_t subpixel_x, subpixel_t subpixel_y)
    {
        reinterpret_cast<uint32_t &>(x) = (
            subpixel_x | (static_cast<uint32_t>(subpixel_y) << 16)
        );
    }
};

typedef subpixel_t playfield_subpixel_t;
typedef Subpixel PlayfieldSubpixel;
typedef SPPoint PlayfieldPoint;

static const int PLAYFIELD_W = 288;
static const int PLAYFIELD_H = 368;
static const int PLAYFIELD_BORDER = 16;
static const screen_x_t PLAYFIELD1_CLIP_LEFT = 0;
static const screen_x_t PLAYFIELD1_CLIP_RIGHT = 319;
static const screen_x_t PLAYFIELD2_CLIP_LEFT = 320;
static const screen_x_t PLAYFIELD2_CLIP_RIGHT = 639;

screen_x_t pascal playfield_fg_x_to_screen(playfield_subpixel_t x, pid2 pid);
inline screen_y_t playfield_fg_y_to_screen(playfield_subpixel_t y, pid2)
{
    return (TO_PIXEL(y) + PLAYFIELD_BORDER);
}
playfield_subpixel_t pascal screen_x_to_playfield(screen_x_t x, pid2 pid);

typedef uint8_t efe_flag_t;
static const efe_flag_t EFF_FREE = 0;
static const efe_flag_t EFF_EXPLOSION_IGNORING_ENEMIES = 9;
static const efe_flag_t EFF_EXPLOSION_HITTING_ENEMIES = 10;
static const int EFE_COUNT = 64;

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

struct fireball_t;
union efe_ptr_t {
    efe_t near *efe;
    fireball_t near *fireball;
};
extern efe_ptr_t efe_p;
extern efe_t efes[EFE_COUNT];
extern bool ef_onehit;

template <class T> inline void efe_subclass_verify(T *)
{
}

enum fireball_variant_t {
    FV_BLUE = 0,
    FV_RED = 1,
    _fireball_variant_t_FORCE_UINT8 = 0xFF
};

enum explosion_hittest_against_t {
    EHA_ENEMY = 0,
    EHA_PELLET = 1,
    EHA_FIREBALL = 2,
    EHA_FIREBALL_BLUE = (EHA_FIREBALL + FV_BLUE),
    EHA_FIREBALL_RED = (EHA_FIREBALL + FV_RED),
    _explosion_hittest_against_t_FORCE_UINT8 = 0xFF
};

extern explosion_hittest_against_t explosion_hittest_against;
extern bool explosion_collision_in_last_hittest;
extern uint8_t explosion_collision_chain_slot;
uint8_t explosions_hittest(void);

enum bomb_flag_t {
    BF_INACTIVE = 0,
    BF_PREPARING = 1,
    BF_ACTIVE = 2
};
extern bomb_flag_t bomb_flag[PLAYER_COUNT];

static const int CHAIN_RING_SIZE = 16;
extern uint8_t chain_ring_p[PLAYER_COUNT];

struct chains_t {
    uint8_t hits[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t pellet_and_fireball_value[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t charge_fireball[PLAYER_COUNT][CHAIN_RING_SIZE];
    uint8_t charge_exatt[PLAYER_COUNT][CHAIN_RING_SIZE];
};
extern chains_t chains;

extern subpixel_length_8_t round_speed;
extern uint16_t round_or_result_frame;

struct player_stuff_t {
    PlayfieldPoint center;
    uint8_t rest[0x80 - sizeof(PlayfieldPoint)];
};
extern player_stuff_t players[PLAYER_COUNT];

extern struct {
    union {
        PlayfieldPoint topleft;
        PlayfieldPoint center;
    } origin;
    PlayfieldPoint radius;
    PlayfieldSubpixel right;
    PlayfieldSubpixel bottom;
    pid_t pid;
} hitbox;

uint8_t hitbox_hittest(void);

typedef int collmap_tile_amount_t;
extern PlayfieldPoint collmap_center;
extern struct {
    collmap_tile_amount_t v;
    void set(pixel_t pixel_v)
    {
        v = (pixel_v / 2);
    }
} collmap_stripe_tile_w;
extern struct {
    collmap_tile_amount_t v;
    void set(pixel_t pixel_v)
    {
        v = (pixel_v / 2);
    }
} collmap_tile_h;
extern pid_t collmap_pid;
void collmap_set_rect_striped(void);

void pascal near gauge_avail_add(pid_t pid, uint8_t charge);
void pascal score_add(uint16_t score, bool pid);
void pascal exatt_add(Subpixel center_x, Subpixel center_y, pid_t pid);

uint16_t pascal near randring2_next16_and(uint16_t mask);
uint16_t pascal near randring2_next16_mod(uint16_t mask);

template <class T> inline bool is_range_a_power_of_two(T min, T max)
{
    return (((max - min) & ((max - min) - 1)) == 0);
}

inline int16_t randring2_next16_mod_ge_lt(int16_t min, int16_t max)
{
    return (min + randring2_next16_mod(max - min));
}

inline int16_t randring2_next16_ge_lt(int16_t min, int16_t max)
{
    if(is_range_a_power_of_two(min, max)) {
        return (min + randring2_next16_and((max - min) - 1));
    }
    return randring2_next16_mod_ge_lt(min, max);
}

inline subpixel_t randring2_next16_ge_lt_sp(float min, float max)
{
    return randring2_next16_ge_lt(to_sp(min), to_sp(max));
}

extern "C" {
void pascal vector2_between_plus(
    int x1,
    int y1,
    int x2,
    int y2,
    unsigned char plus_angle,
    int &ret_x,
    int &ret_y,
    int length
);
}

class VRAMWord {
public:
    unsigned char v;

    void operator =(pixel_t screen_v)
    {
        v = static_cast<unsigned char>(screen_v / 16);
    }
};

extern struct {
    vram_h_t h;
    VRAMWord w;

    void set(pixel_t w_, pixel_t h_)
    {
        w = w_;
        h = (h_ / 2);
    }
} sprite16_put_size;

extern struct {
    screen_x_t left;
    screen_x_t right;

    void reset(void)
    {
        left = PLAYFIELD1_CLIP_LEFT;
        right = PLAYFIELD2_CLIP_RIGHT;
    }
} sprite16_clip;

typedef uvram_byte_amount_t sprite16_offset_t;
extern "C" {
void pascal sprite16_put(
    screen_x_t left,
    screen_y_t top,
    sprite16_offset_t so
);
}

#define BYTE_DOTS 8
#define ROW_SIZE 80
#define XY(x, y) ((y * ROW_SIZE) + (x / BYTE_DOTS))
static const int FIREBALL_CELS = 2;
static const int EXPLOSION_CELS = 4;
static const sprite16_offset_t SO_FIREBALL_FALL = XY(0, 80);
static const sprite16_offset_t SO_FIREBALL_FLY = XY(0, 96);
extern const sprite16_offset_t SO_EXPLOSIONS[][EXPLOSION_CELS];
#define SO_EXPLOSIONS_64X64 SO_EXPLOSIONS[2]

#ifndef static_assert
#define static_assert(condition) ((void)sizeof(char[1 - 2*!(condition)]))
#endif
#ifndef nullptr
#define nullptr 0UL
#endif

extern bool fireball_collision_in_previous_hittest;

#endif
