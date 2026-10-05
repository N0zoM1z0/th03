#ifndef TH03_INPUT_HPP
#define TH03_INPUT_HPP

// TC4J large model: DGROUP globals, far code, 16-bit words.
extern "C" {
extern int js_bexist;
extern unsigned int js_stat[2];
int far pascal js_sense(void);
}

void far pascal frame_delay(int frames);

typedef unsigned int input_t;
static const input_t INPUT_NONE       = 0x0000;
static const input_t INPUT_UP         = 0x0001;
static const input_t INPUT_DOWN       = 0x0002;
static const input_t INPUT_LEFT       = 0x0004;
static const input_t INPUT_RIGHT      = 0x0008;
static const input_t INPUT_BOMB       = 0x0010;
static const input_t INPUT_SHOT       = 0x0020;
static const input_t INPUT_UP_LEFT    = 0x0100;
static const input_t INPUT_DOWN_LEFT  = 0x0200;
static const input_t INPUT_UP_RIGHT   = 0x0400;
static const input_t INPUT_DOWN_RIGHT = 0x0800;
static const input_t INPUT_CANCEL     = 0x1000;
static const input_t INPUT_OK         = 0x2000;
static const input_t INPUT_Q          = 0x4000;

extern input_t input_mp_p1;
extern input_t input_mp_p2;
extern input_t input_sp;

void far __cdecl input_reset_sense_key_held(void);

void far pascal input_mode_interface(void);
void far pascal input_mode_key_vs_key(void);
void far pascal input_mode_joy_vs_key(void);
void far pascal input_mode_key_vs_joy(void);
void far pascal input_mode_1p_vs_cpu(void);
void far pascal input_mode_cpu_vs_1p(void);
void far pascal input_mode_cpu_vs_cpu(void);
void far pascal input_mode_attract(void);
void far pascal input_wait_for_change(int frames_to_wait);

#endif
