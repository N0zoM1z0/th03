// Original DOS Borland large-model counted string fill.
// Preserve its two real far CRT calls: strlen and setmem, and do not
// replace this by a different libc implementation or add guards.
extern "C" unsigned far __cdecl strlen(const char far *);
extern "C" void far __cdecl setmem(void far *,unsigned,int);
extern "C" char far * far __cdecl strnset(char far *destination,
    int c,unsigned n)
{
    unsigned length = strlen(destination);
    if(length<n)
        n=length;
    setmem(destination,n,c);
    return destination;
}
