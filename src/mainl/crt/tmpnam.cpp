// Exact original Borland DOS large-model far-cdecl tmpnam.
// A near Pascal __TMPNAM generates a far filename and receives the
// far address of the original DOS static __tmpnum state. The declaration
// order is intentional: it preserves native EXTDEF indices and the
// TARGET-framed near call at CODE+17.
extern "C" char far * near __pascal __TMPNAM(char far *,unsigned far *);
extern "C" unsigned int _tmpnum;

extern "C" char far * far __cdecl tmpnam(char far *destination)
{
    return __TMPNAM(destination,&_tmpnum);
}
