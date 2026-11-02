// Reconstructed natural Borland DOS large-model far-cdecl fscanf.
// The near scanner gets its authentic near input/unget callbacks, its
// two far stream/format pointers and a far pointer to the first vararg.
// The expression &format+1 is a real far stack address: unlike a
// temporary va_list it emits the original PUSH SS / LEA AX sequence.
extern "C" int near __cdecl _Nfgetc(void far *);
extern "C" int near __cdecl _Nungetc(int,void far *);
typedef int (near *Fget)(void far *);
typedef int (near *Funget)(int,void far *);
extern "C" int near __cdecl _scanner(Fget,Funget,void far *,char far *,void far *);

extern "C" int far __cdecl fscanf(void far *stream,char far *format,...)
{
    return _scanner(_Nfgetc,_Nungetc,stream,format,(void far*)(&format+1));
}
