#ifndef TH03_MAIN_CORE_EXIT_HPP
#define TH03_MAIN_CORE_EXIT_HPP

extern "C" {
void far pascal pfend(void);
void far pascal graph_clear(void);
void far pascal vsync_end(void);
int far pascal mem_unassign(void);
void far pascal text_clear(void);
void far pascal js_end(void);
void far pascal egc_start(void);
}

void far __cdecl game_exit(void);

#endif
