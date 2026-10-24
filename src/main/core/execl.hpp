#ifndef TH03_MAIN_CORE_EXECL_HPP
#define TH03_MAIN_CORE_EXECL_HPP

// FAR Pascal argument: a four-byte filename pointer. Success replaces MAIN;
// failure returns execl()'s signed AX status after releasing local resources.
extern "C" int far pascal main_exec(const char far *binary_fn);

#endif
