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
// The real original DOS launcher frees two separate MRS archives, then
// hands off through a true far-Pascal entrypoint with a four-byte
// segmented null vararg; the native resource cleanup order matters.
enum main_exec_mrs_slot_t {
 MAIN_EXEC_FIRST_MRS = 0,
 MAIN_EXEC_SECOND_MRS = 1,
};

extern "C" int far pascal main_exec(const char far *binary_fn)
{
 graph_pi_free(&pi_headers[0], pi_buffers[0]);
 super_free();
 graph_hide();
 text_clear();
 gaiji_restore();
 // Two original separate far-Pascal cleanup calls; a loop changes
 // original machine instructions (native negative af888b).
 mrs_free(MAIN_EXEC_FIRST_MRS);
 mrs_free(MAIN_EXEC_SECOND_MRS);
 game_exit();
 // Under the original large memory model, the execl vararg
 // terminator is a FOUR-BYTE far pointer. A plain integer `0` changes
 // native CODE and the argument width (af888c). Do not modernize this
 // without a real original-compiler and ABI check.
 return execl((char *)binary_fn, (char *)binary_fn, (void far *)0);
}
