#ifndef TH03_MAIN_PFOPEN_HPP
#define TH03_MAIN_PFOPEN_HPP

// Opaque segment handle; archive and file are large-model far pointers.
extern "C" unsigned int far pascal pfopen(const char far *archive, const char far *file);

#endif
