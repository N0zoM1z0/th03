#pragma codeseg HITCIRC_TEXT main_01
#include "src/main/core/execl.hpp"
#include <process.h>
#include "src/main/formats/pi_load.hpp"
#include "src/main/formats/mrs.hpp"
#include "src/main/core/exit.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
extern "C" {
void far pascal super_free(void);
void far pascal graph_hide(void);
int far pascal gaiji_restore(void);
}
extern "C" int far pascal main_exec(const char far *binary_fn)
{
 graph_pi_free(&pi_headers[0], pi_buffers[0]);
 super_free();
 graph_hide();
 text_clear();
 gaiji_restore();
 mrs_free(0);
 mrs_free(1);
 game_exit();
 // Large-model execl reads a four-byte null pointer from varargs.
 return execl((char *)binary_fn, (char *)binary_fn, (void far *)0);
}
