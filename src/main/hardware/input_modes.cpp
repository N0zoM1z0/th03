#pragma option -zCSHARED

#include "src/main/hardware/input.hpp"

// Each expansion senses the joystick only when the driver reports one.
#define merge_joystick(destination) \
    if(js_bexist) { \
        js_sense(); \
        destination |= js_stat[0]; \
    }

void far pascal input_mode_interface(void)
{
    input_reset_sense_key_held();
    merge_joystick(input_sp);
    input_sp |= input_mp_p1;
}

void far pascal input_mode_key_vs_key(void)
{
    input_reset_sense_key_held();
}

void far pascal input_mode_joy_vs_key(void)
{
    input_reset_sense_key_held();
    if(js_bexist) {
        js_sense();
        input_mp_p1 = js_stat[0];
        input_mp_p2 = input_sp;
    }
}

void far pascal input_mode_key_vs_joy(void)
{
    input_reset_sense_key_held();
    if(js_bexist) {
        js_sense();
        input_mp_p2 = js_stat[0];
        input_mp_p1 = input_sp;
    }
}

void far pascal input_mode_1p_vs_cpu(void)
{
    input_reset_sense_key_held();
    input_mp_p1 |= input_sp;
    merge_joystick(input_mp_p1);
    input_mp_p2 = INPUT_NONE;
}

void far pascal input_mode_cpu_vs_1p(void)
{
    input_reset_sense_key_held();
    input_mp_p2 = input_sp | input_mp_p1;
    merge_joystick(input_mp_p2);
    input_mp_p1 = INPUT_NONE;
}

void far pascal input_mode_cpu_vs_cpu(void)
{
    input_reset_sense_key_held();
    if((input_sp & INPUT_CANCEL) || (input_sp & INPUT_OK)) {
        input_sp = INPUT_CANCEL;
    }
    input_mp_p1 = INPUT_NONE;
    input_mp_p2 = INPUT_NONE;
}

void far pascal input_mode_attract(void)
{
    input_reset_sense_key_held();
    merge_joystick(input_sp);
    input_sp |= input_mp_p1;
    input_mp_p1 = INPUT_NONE;
    input_mp_p2 = INPUT_NONE;
}

void far pascal input_wait_for_change(int frames_to_wait)
{
    int frames_waited = 0;

    // Release phase has no timeout, including when frames_to_wait is negative.
    while(1) {
        input_mode_interface();
        if(input_sp == INPUT_NONE) {
            break;
        }
        frame_delay(1);
    }

    if(!frames_to_wait) {
        frames_to_wait = 9999;
    }

    // Both 0 and 9999 mean an unlimited press phase. Negative values skip it.
    while(frames_waited < frames_to_wait) {
        input_mode_interface();
        if(input_sp != INPUT_NONE) {
            break;
        }
        frames_waited++;
        frame_delay(1);
        if(frames_to_wait == 9999) {
            frames_waited = 0;
        }
    }
}
