// Natural Turbo C++ reconstruction of the complete 215-byte MAIN_06_TEXT
// shared Extra Attack flight CODE owner. The original 32-byte entity layout
// and global state remain in the frozen carrier; this source emits no private
// BSS. Acceptance is bounded to the verified CODE extent and producer order.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_shared.hpp"
#include "src/main/math/vector_far.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/difficul.hpp"

#pragma option -a2

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

extern exatt_entity_t near *exatt_entity_p;

unsigned char near cdecl exatt_fly_update(void)
{
    register exatt_entity_t near *p = exatt_entity_p;
    register int next_x = p->x;
    next_x += p->velocity_x;

    if(exatt_entity_p->pid != 0) {
        goto negative_direction;
    }
    if(p->boundary_x > next_x) {
        goto moving;
    }

arrived:
    p->x = p->target_x;
    p->state = 3;
    p->pid = (1 - pid_current);
    return 1;

negative_direction:
    if(p->boundary_x >= next_x) {
        goto arrived;
    }

moving:
    p->x = next_x;
    p->y += p->velocity_y;
    return 0;
}

void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y, unsigned char pid_, int speed
)
{
    register int screen_target_x = target_x;
    register exatt_entity_t near *p = exatt_entity_p;

    p->state = 2;
    p->frame = 0;
    p->x = x;
    p->y = y;
    p->pid = pid_;

    x = playfield_fg_x_to_screen(x, pid_);
    p->target_x = screen_target_x;
    screen_target_x = playfield_fg_x_to_screen(
        screen_target_x, (1 - pid_)
    );
    vector2_between_plus(
        TO_SP(x), y, TO_SP(screen_target_x), target_y,
        0, p->velocity_x, p->velocity_y, ((round_speed / 4) + speed)
    );
    p->boundary_x = screen_x_to_playfield(screen_target_x, pid_);
}
