#pragma option -WX -zCSHARED -k-

#include "src/main/hardware/input.hpp"

// BIOS key-state bytes at segment 0. Only groups and masks used here are named.
enum {
    KEYGROUP_0 = 0x52A,
    KEYGROUP_2 = 0x52C,
    KEYGROUP_3 = 0x52D,
    KEYGROUP_4 = 0x52E,
    KEYGROUP_5 = 0x52F,
    KEYGROUP_6 = 0x530,
    KEYGROUP_7 = 0x531,
    KEYGROUP_8 = 0x532,
    KEYGROUP_9 = 0x533
};

enum {
    K0_ESC = 0x01,
    K2_Q = 0x01,
    K2_R = 0x08,
    K2_T = 0x10,
    K2_Y = 0x20,
    K3_RETURN = 0x10,
    K4_F = 0x01,
    K4_H = 0x04,
    K5_Z = 0x02,
    K5_X = 0x04,
    K5_V = 0x10,
    K5_B = 0x20,
    K5_N = 0x40,
    K6_SPACE = 0x10,
    K7_ARROW_UP = 0x04,
    K7_ARROW_LEFT = 0x08,
    K7_ARROW_RIGHT = 0x10,
    K7_ARROW_DOWN = 0x20,
    K8_NUM_7 = 0x04,
    K8_NUM_8 = 0x08,
    K8_NUM_9 = 0x10,
    K8_NUM_4 = 0x40,
    K9_NUM_6 = 0x01,
    K9_NUM_1 = 0x04,
    K9_NUM_2 = 0x08,
    K9_NUM_3 = 0x10
};

inline char input_peekb(unsigned int segment, unsigned int offset)
{
    return *((char far *)((void __seg *)(segment) + (void near *)(offset)));
}

#define FLAGS_ZERO (_FLAGS & 0x40)

void far __cdecl input_reset_sense_key_held(void)
{
    js_stat[0] = input_sp = input_mp_p2 = input_mp_p1 = INPUT_NONE;

    // The target contains this zero-distance jump before BL is initialized.
    // Keeping the control-flow edge is semantic source; unlike the old
    // codestring, it does not inject target bytes or claim the trailing NOP.
    _asm { jmp sense; }
sense:
    _BL = 2;
    _ES = 0;

    do {
        _AH = input_peekb(_ES, KEYGROUP_7);
        if(_AH & K7_ARROW_UP) {
            input_sp |= INPUT_UP;
        }
        if(_AH & K7_ARROW_DOWN) {
            input_sp |= INPUT_DOWN;
        }
        if(_AH & K7_ARROW_LEFT) {
            input_mp_p2 |= INPUT_SHOT;
            input_sp |= INPUT_LEFT;
        }
        if(_AH & K7_ARROW_RIGHT) {
            input_mp_p2 |= INPUT_BOMB;
            input_sp |= INPUT_RIGHT;
        }

        _AH = input_peekb(_ES, KEYGROUP_9);
        if(_AH & K9_NUM_6) {
            input_mp_p2 |= INPUT_RIGHT;
            input_sp |= INPUT_RIGHT;
        }
        if(_AH & K9_NUM_1) {
            input_mp_p2 |= INPUT_DOWN_LEFT;
            input_sp |= INPUT_DOWN_LEFT;
        }
        if(_AH & K9_NUM_2) {
            input_mp_p2 |= INPUT_DOWN;
            input_sp |= INPUT_DOWN;
        }
        if(_AH & K9_NUM_3) {
            input_mp_p2 |= INPUT_DOWN_RIGHT;
            input_sp |= INPUT_DOWN_RIGHT;
        }

        _AH = input_peekb(_ES, KEYGROUP_8);
        if(_AH & K8_NUM_4) {
            input_mp_p2 |= INPUT_LEFT;
            input_sp |= INPUT_LEFT;
        }
        if(_AH & K8_NUM_7) {
            input_mp_p2 |= INPUT_UP_LEFT;
            input_sp |= INPUT_UP_LEFT;
        }
        if(_AH & K8_NUM_8) {
            input_mp_p2 |= INPUT_UP;
            input_sp |= INPUT_UP;
        }
        if(_AH & K8_NUM_9) {
            input_mp_p2 |= INPUT_UP_RIGHT;
            input_sp |= INPUT_UP_RIGHT;
        }

        _AH = input_peekb(_ES, KEYGROUP_5);
        if(_AH & K5_Z) {
            input_mp_p1 |= INPUT_SHOT;
            input_sp |= INPUT_SHOT;
        }
        if(_AH & K5_X) {
            input_mp_p1 |= INPUT_BOMB;
            input_sp |= INPUT_BOMB;
        }
        if(_AH & K5_V) {
            input_mp_p1 |= INPUT_DOWN_LEFT;
        }
        if(_AH & K5_B) {
            input_mp_p1 |= INPUT_DOWN;
        }
        if(_AH & K5_N) {
            input_mp_p1 |= INPUT_DOWN_RIGHT;
        }

        _AH = input_peekb(_ES, KEYGROUP_4);
        if(_AH & K4_F) {
            input_mp_p1 |= INPUT_LEFT;
        }
        if(_AH & K4_H) {
            input_mp_p1 |= INPUT_RIGHT;
        }

        _AH = input_peekb(_ES, KEYGROUP_2);
        if(_AH & K2_R) {
            input_mp_p1 |= INPUT_UP_LEFT;
        }
        if(_AH & K2_T) {
            input_mp_p1 |= INPUT_UP;
        }
        if(_AH & K2_Y) {
            input_mp_p1 |= INPUT_UP_RIGHT;
        }
        if(_AH & K2_Q) {
            input_sp |= INPUT_Q;
        }

        _AH = input_peekb(_ES, KEYGROUP_0);
        if(_AH & K0_ESC) {
            input_sp |= INPUT_CANCEL;
        }

        _AH = input_peekb(_ES, KEYGROUP_3);
        if(_AH & K3_RETURN) {
            input_sp |= INPUT_OK;
        }

        _AH = input_peekb(_ES, KEYGROUP_6);
        if(_AH & K6_SPACE) {
            input_sp |= INPUT_SHOT;
        }

        _BL--;
        if(FLAGS_ZERO) {
            break;
        }

        _CX = 1024;
delay_loop:
        asm {
            out 0x5F, al;
            loop delay_loop;
        }
    } while(1);
}
