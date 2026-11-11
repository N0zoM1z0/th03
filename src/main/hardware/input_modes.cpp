#pragma option -zCSHARED

#include "src/main/hardware/input.hpp"

// Keep the joystick read and merge in each physical caller. Extracting
// a C++ helper changes TC4 register allocation. The two joystick-vs-key
// entrypoints can return immediately if no joystick exists.

void far pascal input_mode_interface(void)
{
    input_reset_sense_key_held();
    if(js_bexist) {
        js_sense();
        input_sp |= js_stat[0];
    }
    input_sp |= input_mp_p1;
}

void far pascal input_mode_key_vs_key(void)
{
    input_reset_sense_key_held();
}

void far pascal input_mode_joy_vs_key(void)
{
    input_reset_sense_key_held();
    if(!js_bexist) {
        return;
    }
    js_sense();
    input_mp_p1 = js_stat[0];
    input_mp_p2 = input_sp;
}

void far pascal input_mode_key_vs_joy(void)
{
    input_reset_sense_key_held();
    if(!js_bexist) {
        return;
    }
    js_sense();
    input_mp_p2 = js_stat[0];
    input_mp_p1 = input_sp;
}

void far pascal input_mode_1p_vs_cpu(void)
{
    input_reset_sense_key_held();
    input_mp_p1 |= input_sp;
    if(js_bexist) {
        js_sense();
        input_mp_p1 |= js_stat[0];
    }
    input_mp_p2 = INPUT_NONE;
}

void far pascal input_mode_cpu_vs_1p(void)
{
    input_reset_sense_key_held();
    input_mp_p2 = input_sp | input_mp_p1;
    if(js_bexist) {
        js_sense();
        input_mp_p2 |= js_stat[0];
    }
    input_mp_p1 = INPUT_NONE;
}

void far pascal input_mode_cpu_vs_cpu(void)
{
    input_reset_sense_key_held();
    // Keep the separate original short-circuit flag tests. A single
    // combined mask generates seven fewer bytes under TC4 (af839b).
    // Keep original two independent short-circuit bit tests. Combining
    // their masks produced 360 instead of 367 native CODE bytes in
    // freshly compiled original af907d, not just historical af839b.
    if((input_sp & INPUT_CANCEL) || (input_sp & INPUT_OK)) {
        input_sp = INPUT_CANCEL;
    }
    input_mp_p1 = INPUT_NONE;
    input_mp_p2 = INPUT_NONE;
}

void far pascal input_mode_attract(void)
{
    input_reset_sense_key_held();
    if(js_bexist) {
        js_sense();
        input_sp |= js_stat[0];
    }
    input_sp |= input_mp_p1;
    input_mp_p1 = INPUT_NONE;
    input_mp_p2 = INPUT_NONE;
}

// Historical wait sentinel: zero means unlimited press polling, while a
// negative caller-supplied frame bound skips the press phase entirely.
enum { INPUT_WAIT_UNLIMITED_FRAMES = 9999 };

void far pascal input_wait_for_change(int frames_to_wait)
{
    int frames_waited = 0;

    // Release phase has no timeout, even for negative limits. This
    // source point has no defined `true` (`while(true)` failed in
    // af907a). The do-loop samples at least once, retains the original
    // scan/delay order, and ends only after the input word is released.
    do {
        input_mode_interface();
        // The release phase must sample at least once and has no
        // timeout, irrespective of the caller's press-phase limit.
        if(!input_sp) {
            break;
        }
        frame_delay(1);
    } while(1);

    if(!frames_to_wait) {
        frames_to_wait = INPUT_WAIT_UNLIMITED_FRAMES;
    }

    // Zero selects the original 9999-frame unlimited sentinel; negative
    // values skip only this second press phase, never the release wait.
    // The bounded while-loop retains the original signed 16-bit limit;
    // the counter reset stays after the real input read and frame delay.
    while(frames_waited < frames_to_wait) {
        input_mode_interface();
        if(input_sp) {
            break;
        }
        ++frames_waited;
        frame_delay(1);
        if(frames_to_wait == INPUT_WAIT_UNLIMITED_FRAMES) {
            frames_waited = 0;
        }
    }
}
