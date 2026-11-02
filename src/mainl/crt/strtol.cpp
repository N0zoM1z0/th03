// Original DOS large-model signed long parser,including two near adapters.
// Preserve the original four far scans/callback arguments and overflow clamp.
// BCC must reuse ES from the whitespace scan for the following '-' comparison;
// a typed volatile ES:offset access avoids a redundant LES and spill.
#include <dos.h>
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
extern "C" long near __cdecl _scantol(
    int (near *reader)(Cursor),void (near *unreader)(int,Cursor),
    Cursor p,int radix,int width,int far *count,int far *status);
extern "C" long far __cdecl strtol(
    char far *text,char far * far *ending,int radix)
{
    int count = 0;
    int status;
    int negative;
    long result;
    errno = 0;
    while(_ctype[(int)(signed char)*text+1] & 1) {
        ++text;
        ++count;
    }
    negative = (*(volatile signed char far *)MK_FP(_ES,FP_OFF(text)) == '-');
    result = _scantol(readChar,unreadChar,&text,radix,0x7fff,&count,&status);
    if(status <= 0)
        text -= count;
    else if(status == 2)
        errno = 34;
    else if(status == 1) {
        if((result >= 0L) == negative) {
            errno = 34;
            result = negative ? 0x80000000L : 0x7FFFFFFFL;
        }
    }
    if(ending)
        *ending = text;
    return result;
}
