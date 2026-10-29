// Semantic recovery of the complete xalloc TU. Native layout/codegen is still
// a candidate: the current compiler does not reproduce every retained byte.
#include <except.h>

xalloc::xalloc(const string far &message, size_t size)
    : xmsg(message), siz(size)
{
}

void xalloc::raise() throw(xalloc)
{
    throw *this;
}
