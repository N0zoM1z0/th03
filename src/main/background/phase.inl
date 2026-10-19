/* TC4 C++ SOURCE HYPOTHESIS; NOT PORTABLE DEFINED C++.
 * Include text inside EACH complete periodic renderer, after its ordinary
 * local declarations. `frame` is signed16, `changed` is unsigned char,
 * `background_angle` is the existing unsigned-byte direction variable.
 * There is deliberately no default assignment to changed.
 * Its indeterminate read later is not portable defined C++ behavior.
 */
frame = (round_or_result_frame & 4095);
if(frame < 1024) {
    changed = 0;
} else if(frame < 1280) {
    if((frame & 7) == 0) {
        background_angle++;
        changed = 1;
    }
} else if(frame < 2048) {
    changed = 0;
} else if(frame < 2304) {
    if((frame & 3) == 0) {
        background_angle--;
        changed = 1;
    }
} else if(frame < 3072) {
    changed = 0;
} else if(frame < 4064) {
    if((frame & 127) < 64) {
        background_angle++;
    } else {
        background_angle--;
    }
    changed = 1;
} else {
    changed = 0;
}
