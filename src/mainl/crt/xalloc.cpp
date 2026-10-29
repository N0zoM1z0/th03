// Complete xalloc TU, including compiler-generated copy/destructor and
// exception metadata under the scoped Borland -O1 profile.
#include <except.h>

xalloc::xalloc(const string far &message, size_t size)
    : xmsg(message), siz(size)
{
}

void xalloc::raise() throw(xalloc)
{
    throw *this;
}
