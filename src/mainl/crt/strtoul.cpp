// Original Borland DOS large-model unsigned long text conversion.
// Two private near scanner adapters preserve the historical __scantol ABI.
// BCC retains the character value in AX after sign extension; using
// register int and _AX avoids a non-original DX test without byte patches.
extern "C" int errno;
extern "C" unsigned char _ctype[];
typedef char far * far *Cursor;
static int near readChar(Cursor p)
{
    register int c = *(*p)++;
    if(!_AX) return -1;
    return c;
}
static void near unreadChar(int ch,Cursor p)
{
    --*p;
}
extern "C" unsigned long near __cdecl _scantol(
    int (near *reader)(Cursor),void (near *unreader)(int,Cursor),
    Cursor p,int radix,int width,int far *count,int far *status);
extern "C" unsigned long far __cdecl strtoul(
    char far *text,char far * far *ending,int radix)
{
    int count = 0;
    int status = 0;
    unsigned long result = 0;
    while(_ctype[(int)(signed char)*text+1] & 1) {
        ++text;
        ++count;
    }
    errno = 0;
    result = _scantol(readChar,unreadChar,&text,radix,0x7fff,&count,&status);
    if(status <= 0)
        text -= count;
    else if(status == 2) {
        result = 0xffffffffL;
        errno = 34;
    }
    if(ending)
        *ending = text;
    return result;
}
