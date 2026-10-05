#ifndef TH03_MAIN_CORE_INITMAIN_HPP
#define TH03_MAIN_CORE_INITMAIN_HPP

extern "C" {
int far pascal mem_assign_dos(unsigned parasize);
void far pascal vsync_start(void);
void far pascal egc_start(void);
void far pascal graph_400line(void);
int far pascal js_start(void);
void far pascal pfstart(const unsigned char far *parfile);
}

void far vram_planes_set(void);
int far pascal game_init_main(const unsigned char far *pf_fn);

#endif
