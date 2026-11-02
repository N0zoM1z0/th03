// Original Borland C++ 4.5 large-model DOS fputs translation unit.
// Near Pascal __FPUTN writes the far string with a 16-bit length and
// far FILE pointer. The original compiler uses Pascal callee cleanup.
// Use s+length before selecting the final byte: this preserves original
// far ES:BX offset addition and the [BX-1] byte access codegen.
extern "C" int near __pascal __FPUTN(const char far *,unsigned,void far *);
extern "C" unsigned far __cdecl strlen(const char far *);

extern "C" int far __cdecl fputs(const char far *s,void far *stream)
{
    unsigned length;
    if(!s) return 0;
    if((length=strlen(s))==0) return 0;
    if(__FPUTN(s,length,stream))
        return (unsigned char)*(s+length-1);
    return -1;
}
