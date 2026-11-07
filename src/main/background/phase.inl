/* Current native TC4 4.02 C++ hypothesis, NOT portable defined C++.
 * Include text inside BOTH complete original periodic renderers, after
 * their local declarations. `frame` is a signed 16-bit int, whereas
 * `round_or_result_frame` is already an unsigned 16-bit global clock;
 * `changed` is a byte and is intentionally NOT initialized on 416
 * phase paths. The original later indeterminate read is real target
 * behavior, not a reason to invent default initialization.
 *
 * Natural C++ `frame = global % 4096`, plus the unsigned 8-/4-frame
 * `if(!remainder)` guards, compiles original-exact in BOTH physical
 * background objects (`af880a/c/d`). However, dropping the explicit
 * unsigned conversion from signed local `frame` before `%8` changes
 * CODE (`af880b`); switching the wave `&127` test to `%128`
 * (`af880e`) OR using `!(frame&64)` (`af880g`) also changes CODE.
 * Keep the original mask and all register/branch/byte semantics.
 */
// Each include expands inside its original periodic controller. This enum
// introduces no object DATA/BSS and preserves the real 16-bit signed
// local frame and the externally maintained unsigned-word global clock.
enum {
    BG_PHASE_FULL_PERIOD = 4096,
    BG_PHASE_REST_1_END = 1024,
    BG_PHASE_INCREMENT_1_END = 1280,
    BG_PHASE_REST_2_END = 2048,
    BG_PHASE_DECREMENT_1_END = 2304,
    BG_PHASE_REST_3_END = 3072,
    BG_PHASE_WAVE_END = 4064,
    BG_PHASE_INCREMENT_TICK = 8,
    BG_PHASE_DECREMENT_TICK = 4,
    BG_PHASE_WAVE_MASK = 127,
    BG_PHASE_WAVE_UP_TIME = 64
};
frame = (round_or_result_frame % BG_PHASE_FULL_PERIOD);
if(frame < BG_PHASE_REST_1_END) {
    changed = 0;
} else if(frame < BG_PHASE_INCREMENT_1_END) {
    if(!(static_cast<unsigned int>(frame) % BG_PHASE_INCREMENT_TICK)) {
        goto background_phase_increment;
    }
} else if(frame < BG_PHASE_REST_2_END) {
    changed = 0;
} else if(frame < BG_PHASE_DECREMENT_1_END) {
    if(!(static_cast<unsigned int>(frame) % BG_PHASE_DECREMENT_TICK)) {
        goto background_phase_decrement;
    }
} else if(frame < BG_PHASE_REST_3_END) {
    changed = 0;
} else if(frame < BG_PHASE_WAVE_END) {
    // The 128-tick direction wave is signed-local but uses the original
    // mask/compare sequence. Even a bit-64 test emits different TC4 CODE.
    if((frame & BG_PHASE_WAVE_MASK) < BG_PHASE_WAVE_UP_TIME) {
background_phase_increment:
        background_angle++;
    } else {
background_phase_decrement:
        background_angle--;
    }
    changed = 1;
} else {
    changed = 0;
}
