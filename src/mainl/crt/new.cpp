// Original allocation policy: zero requests become one; failure calls the
// installed handler and retries. A null handler permits a null return.
// Borland -O1 emits the owned startup/exit and exception records.
#include <cstring.h>
#include <except.h>
#include <new.h>
#include <stdlib.h>

xalloc __xalloc("Out of memory", 0);

void xnew_handler()
{
    throw __xalloc;
}

new_handler _new_handler = xnew_handler;

new_handler set_new_handler(new_handler handler)
{
    new_handler previous = _new_handler;
    _new_handler = handler;
    return previous;
}

void *operator new(size_t size)
{
    void *block = 0;
    size = size ? size : 1;
    while ((block = malloc(size)) == 0 && _new_handler) {
        _new_handler();
    }
    return block;
}
