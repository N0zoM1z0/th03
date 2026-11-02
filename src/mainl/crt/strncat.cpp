// Original Borland DOS large-model bounded string append.
// The two far strlen calls and far movmem retain their original cdecl order.
// Store the second strlen result *inside* the comparison to use its live
// AX return instead of adding a non-original stack reload.
extern "C" unsigned far __cdecl strlen(const char far *);
extern "C" void far __cdecl movmem(const void far *,void far *,unsigned);
extern "C" char far * far __cdecl strncat(char far *destination,
    const char far *source,unsigned limit)
{
    unsigned length;
    unsigned end = strlen(destination);
    if((length = strlen(source)) > limit)
        length=limit;
    movmem(source,destination+end,length);
    destination[end+length] = 0;
    return destination;
}
