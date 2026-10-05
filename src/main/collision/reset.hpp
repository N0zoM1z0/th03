#ifndef TH03_MAIN_COLLISION_RESET_HPP
#define TH03_MAIN_COLLISION_RESET_HPP

// Near call in MAIN_01; preserves DI, clobbers ES, and assumes forward DF.
extern "C" void near collmap_reset(void);

#endif
