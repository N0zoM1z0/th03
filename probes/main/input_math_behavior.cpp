// Isolated DOS behavior probe. Hardware collaborators are explicit test doubles.
#include <stdio.h>
#include "input.hpp"
#include "polar.hpp"

int js_bexist;
unsigned int js_stat[2];
input_t input_mp_p1, input_mp_p2, input_sp;
static unsigned int senses, joystick_senses, delays;
static unsigned int release_until, press_at;
static input_t keyboard_sp, keyboard_p1, keyboard_p2;

int far pascal js_sense(void)
{
    joystick_senses++;
    return 0;
}

void far pascal frame_delay(int frames)
{
    delays += frames;
}

void far __cdecl input_reset_sense_key_held(void)
{
    senses++;
    input_sp = keyboard_sp;
    input_mp_p1 = keyboard_p1;
    input_mp_p2 = keyboard_p2;
    if(press_at) {
        input_sp = (senses <= release_until || senses >= press_at) ? INPUT_OK : 0;
        input_mp_p1 = input_mp_p2 = 0;
    }
}

static void reset(void)
{
    senses = joystick_senses = delays = 0;
    release_until = press_at = 0;
    keyboard_sp = 1;
    keyboard_p1 = 2;
    keyboard_p2 = 4;
    js_bexist = 0;
    js_stat[0] = 8;
}

#define CHECK(condition) if(!(condition)) { printf("FAIL line %d\n", __LINE__); return 1; }

int main(void)
{
    CHECK(sizeof(int) == 2 && sizeof(long) == 4);
    CHECK(polar(100, 256, 256) == 356);
    CHECK(polar(100, -256, 256) == -156);
    CHECK(polar(0, -1, 1) == -1);
    CHECK(polar(0, 1, 255) == 0);
    CHECK(polar(0, -1, -256) == 1);
    CHECK(polar(32767, 1, 256) == -32768);

    reset(); input_mode_interface();
    CHECK(input_sp == 3 && joystick_senses == 0);
    reset(); js_bexist = 1; input_mode_interface();
    CHECK(input_sp == 11 && joystick_senses == 1);
    reset(); js_bexist = 1; input_mode_key_vs_key();
    CHECK(input_sp == 1 && input_mp_p1 == 2 && input_mp_p2 == 4 && !joystick_senses);
    reset(); input_mode_joy_vs_key();
    CHECK(input_mp_p1 == 2 && input_mp_p2 == 4);
    reset(); js_bexist = 1; input_mode_joy_vs_key();
    CHECK(input_mp_p1 == 8 && input_mp_p2 == 1);
    reset(); js_bexist = 1; input_mode_key_vs_joy();
    CHECK(input_mp_p1 == 1 && input_mp_p2 == 8);
    reset(); js_bexist = 1; input_mode_1p_vs_cpu();
    CHECK(input_mp_p1 == 11 && input_mp_p2 == 0);
    reset(); js_bexist = 1; input_mode_cpu_vs_1p();
    CHECK(input_mp_p1 == 0 && input_mp_p2 == 11);
    reset(); keyboard_sp = INPUT_OK | 1; input_mode_cpu_vs_cpu();
    CHECK(input_sp == INPUT_CANCEL && !input_mp_p1 && !input_mp_p2);
    reset(); input_mode_cpu_vs_cpu();
    CHECK(input_sp == 1 && !input_mp_p1 && !input_mp_p2);
    reset(); js_bexist = 1; input_mode_attract();
    CHECK(input_sp == 11 && !input_mp_p1 && !input_mp_p2);

    reset(); release_until = 2; press_at = 6; input_wait_for_change(10);
    CHECK(senses == 6 && delays == 4);
    reset(); keyboard_sp = keyboard_p1 = 0; input_wait_for_change(3);
    CHECK(senses == 4 && delays == 3);
    reset(); release_until = 2; press_at = 10003; input_wait_for_change(0);
    CHECK(senses == 10003 && delays == 10001);
    reset(); release_until = 2; press_at = 10003; input_wait_for_change(9999);
    CHECK(senses == 10003 && delays == 10001);
    reset(); release_until = 2; press_at = 6; input_wait_for_change(-1);
    CHECK(senses == 3 && delays == 2);
    puts("TH03 input/math behavior PASS");
    return 0;
}
