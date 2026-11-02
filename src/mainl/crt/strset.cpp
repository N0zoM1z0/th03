// Original DOS large-model far-cdecl full-string character replacement.
// Keep the Borland right-to-left nested argument evaluation: c is pushed
// before the far strlen call, then _setmem receives the actual length.
extern "C" unsigned far __cdecl strlen(const char far *);
extern "C" void far __cdecl setmem(void far *,unsigned,int);

extern "C" char far * far __cdecl strset(char far *destination,int value)
{
    setmem(destination,strlen(destination),value);
    return destination;
}
