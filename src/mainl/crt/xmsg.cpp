// Own the exception's message through a distinct string object. Retain the
// original delete-then-new assignment order and compiler-generated EH records.
#include <cstring.h>
#include <except.h>

xmsg::xmsg(const string far &message)
    : str(new string(message))
{
}

xmsg::xmsg(const xmsg far &message)
    : str(new string(*message.str))
{
}

xmsg::~xmsg()
{
    delete str;
}

void xmsg::raise() throw(xmsg)
{
    throw *this;
}

xmsg &xmsg::operator=(const xmsg far &source)
{
    if (this != &source) {
        delete str;
        str = new string(*source.str);
    }
    return *this;
}
