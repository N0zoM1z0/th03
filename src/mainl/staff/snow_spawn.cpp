// Semantic alternative, compiler-owned ABI. Uncompiled diagnostic candidate.
// Complete maintained snow spawn behavior; no manual frame/save/return sequence.
#pragma option -zCMAINL_SPAWN_TEXT
struct mainl_spawn_flake_t {
 unsigned char alive;
 unsigned char alignment;
 int left;
 int top;
 int velocity_x;
 int velocity_y;
 int cel;
 unsigned char reserved[4];
};
typedef char mainl_spawn_flake_size[(sizeof(mainl_spawn_flake_t)==16)?1:-1];
extern mainl_spawn_flake_t flakes[80];
extern int mainl_snow_frame;
extern unsigned char mainl_snow_slot_limit;
extern "C" {
 int far pascal IRand(void);
 void far pascal vector2(int &ret_x, int &ret_y, unsigned char angle, int length);
}
extern "C" void near mainl_snow_spawn(void)
{
 unsigned char angle;
 unsigned char length;
 register mainl_spawn_flake_t near *flake;
 register int i;
 flake = flakes;
 for(i = 0; i < mainl_snow_slot_limit; i++, flake++) {
  if(flake->alive == 0 && (i << 3) <= mainl_snow_frame) {
   flake->alive = 1;
   if(i & 3) {
    flake->left = IRand() % ((640 - 8) * 16);
    flake->top = 0;
   } else {
    flake->left = ((640 - 8) * 16);
    flake->top = IRand() % ((400 - 8) * 16);
   }
   angle = (IRand() % 32) + 80;
   length = (IRand() % (4 * 16)) + (3 * 16);
   flake->cel = IRand() & 3;
   vector2(flake->velocity_x, flake->velocity_y, angle, length);
  }
 }
}
