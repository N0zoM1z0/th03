// Bounded call adapters from the original DOS xx.cpp TU, before the unwind and
// destruction banks. Keep each near/far and caller/callee-cleaned signature:
// the compact call kind is derived from the compiler's original member mask.
// The 16-bit fastcall signatures put this last. A virtual-base copy places its
// zero flag first, then source, then destination (AX, BX, DX for near pointers).
#include "xx_abi.h"

#define XX_INVOKE(distance,convention,signature,arguments) \
    ((void (distance convention *) signature)function) arguments

static void near callCopyCtor(void far *destination,void far *source,
    xx_code_ptr function,unsigned mask)
{
    unsigned saved_ds;
    unsigned kind;

    saved_ds = XX_RUNTIME->saved_ds;
    asm push ds;
    asm mov ds, saved_ds;
    kind = mask & 1;
    if(mask & 4) kind |= 2;
    if(mask & 2) {
        kind |= 4;
        if(!(mask & 0x100)) kind |= 0x20;
    }
    if(mask & 0x20) kind |= 8;
    if(mask & 0x80) kind |= 0x10;

    if(mask & 0x1000) {
        // A copy constructor for a class with virtual bases gets a zero flag.
        switch(kind) {
        case 0: XX_INVOKE(near,__cdecl,(void near *,int,void near *),((void near *)destination,0,(void near *)source)); break;
        case 1: XX_INVOKE(far,__cdecl,(void near *,int,void near *),((void near *)destination,0,(void near *)source)); break;
        case 2: XX_INVOKE(near,__cdecl,(void far *,int,void far *),(destination,0,source)); break;
        case 3: XX_INVOKE(far,__cdecl,(void far *,int,void far *),(destination,0,source)); break;
        case 4: XX_INVOKE(near,__pascal,(int,void near *,void near *),(0,(void near *)source,(void near *)destination)); break;
        case 5: XX_INVOKE(far,__pascal,(int,void near *,void near *),(0,(void near *)source,(void near *)destination)); break;
        case 6: XX_INVOKE(near,__pascal,(int,void far *,void far *),(0,source,destination)); break;
        case 7: XX_INVOKE(far,__pascal,(int,void far *,void far *),(0,source,destination)); break;
        case 8: XX_INVOKE(near,__fastcall,(int,void near *,void near *),(0,(void near *)source,(void near *)destination)); break;
        case 9: XX_INVOKE(far,__fastcall,(int,void near *,void near *),(0,(void near *)source,(void near *)destination)); break;
        case 10: XX_INVOKE(near,__fastcall,(int,void far *,void far *),(0,source,destination)); break;
        case 11: XX_INVOKE(far,__fastcall,(int,void far *,void far *),(0,source,destination)); break;
        case 16:
            asm mov si, word ptr destination;
            XX_INVOKE(near,__cdecl,(int,void near *),(0,(void near *)source)); break;
        case 17:
            asm mov si, word ptr destination;
            XX_INVOKE(far,__cdecl,(int,void near *),(0,(void near *)source)); break;
        case 18:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(near,__cdecl,(int,void far *),(0,source));
            asm pop ds;
            break;
        case 19:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(far,__cdecl,(int,void far *),(0,source));
            asm pop ds;
            break;
        case 20:
            asm mov si, word ptr destination;
            XX_INVOKE(near,__pascal,(int,void near *),(0,(void near *)source)); break;
        case 21:
            asm mov si, word ptr destination;
            XX_INVOKE(far,__pascal,(int,void near *),(0,(void near *)source)); break;
        case 22:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(near,__pascal,(int,void far *),(0,source));
            asm pop ds;
            break;
        case 23:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(far,__pascal,(int,void far *),(0,source));
            asm pop ds;
            break;
        default: break;
        }
    }
    else {
        switch(kind) {
        case 0: XX_INVOKE(near,__cdecl,(void near *,void near *),((void near *)destination,(void near *)source)); break;
        case 1: XX_INVOKE(far,__cdecl,(void near *,void near *),((void near *)destination,(void near *)source)); break;
        case 2: XX_INVOKE(near,__cdecl,(void far *,void far *),(destination,source)); break;
        case 3: XX_INVOKE(far,__cdecl,(void far *,void far *),(destination,source)); break;
        case 4: XX_INVOKE(near,__pascal,(void near *,void near *),((void near *)source,(void near *)destination)); break;
        case 5: XX_INVOKE(far,__pascal,(void near *,void near *),((void near *)source,(void near *)destination)); break;
        case 6: XX_INVOKE(near,__pascal,(void far *,void far *),(source,destination)); break;
        case 7: XX_INVOKE(far,__pascal,(void far *,void far *),(source,destination)); break;
        case 8: XX_INVOKE(near,__fastcall,(void near *,void near *),((void near *)source,(void near *)destination)); break;
        case 9: XX_INVOKE(far,__fastcall,(void near *,void near *),((void near *)source,(void near *)destination)); break;
        case 10: XX_INVOKE(near,__fastcall,(void far *,void far *),(source,destination)); break;
        case 11: XX_INVOKE(far,__fastcall,(void far *,void far *),(source,destination)); break;
        case 16:
            asm mov si, word ptr destination;
            XX_INVOKE(near,__cdecl,(void near *),((void near *)source)); break;
        case 17:
            asm mov si, word ptr destination;
            XX_INVOKE(far,__cdecl,(void near *),((void near *)source)); break;
        case 18:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(near,__cdecl,(void far *),(source));
            asm pop ds;
            break;
        case 19:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(far,__cdecl,(void far *),(source));
            asm pop ds;
            break;
        case 20:
            asm mov si, word ptr destination;
            XX_INVOKE(near,__pascal,(void near *),((void near *)source)); break;
        case 21:
            asm mov si, word ptr destination;
            XX_INVOKE(far,__pascal,(void near *),((void near *)source)); break;
        case 22:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(near,__pascal,(void far *),(source));
            asm pop ds;
            break;
        case 23:
            asm push ds;
            asm lds si, destination;
            XX_INVOKE(far,__pascal,(void far *),(source));
            asm pop ds;
            break;
        default: break;
        }
    }
    asm pop ds;
}

static void near callDestructor(void far *destination,xx_code_ptr function,
    unsigned mask,int virtual_bases)
{
    unsigned flags = virtual_bases ? 2 : 0;
    unsigned saved_ds;
    unsigned kind;

    saved_ds = XX_RUNTIME->saved_ds;
    asm push ds;
    asm mov ds, saved_ds;
    kind = mask & 1;
    if(mask & 4) kind |= 2;
    if(mask & 2) {
        kind |= 4;
        if(!(mask & 0x100)) kind |= 0x20;
    }
    if(mask & 0x20) kind |= 8;
    if(mask & 0x80) kind |= 0x10;

    switch(kind) {
    case 0: XX_INVOKE(near,__cdecl,(void near *,int),((void near *)destination,flags)); break;
    case 1: XX_INVOKE(far,__cdecl,(void near *,int),((void near *)destination,flags)); break;
    case 2: XX_INVOKE(near,__cdecl,(void far *,int),(destination,flags)); break;
    case 3: XX_INVOKE(far,__cdecl,(void far *,int),(destination,flags)); break;
    case 4: XX_INVOKE(near,__pascal,(int,void near *),(flags,(void near *)destination)); break;
    case 5: XX_INVOKE(far,__pascal,(int,void near *),(flags,(void near *)destination)); break;
    case 6: XX_INVOKE(near,__pascal,(int,void far *),(flags,destination)); break;
    case 7: XX_INVOKE(far,__pascal,(int,void far *),(flags,destination)); break;
    case 8: XX_INVOKE(near,__fastcall,(int,void near *),(flags,(void near *)destination)); break;
    case 9: XX_INVOKE(far,__fastcall,(int,void near *),(flags,(void near *)destination)); break;
    case 10: XX_INVOKE(near,__fastcall,(int,void far *),(flags,destination)); break;
    case 11: XX_INVOKE(far,__fastcall,(int,void far *),(flags,destination)); break;
    case 16:
        asm mov si, word ptr destination;
        XX_INVOKE(near,__cdecl,(int),(flags)); break;
    case 17:
        asm mov si, word ptr destination;
        XX_INVOKE(far,__cdecl,(int),(flags)); break;
    case 18:
        asm push ds;
        asm lds si, destination;
        XX_INVOKE(near,__cdecl,(int),(flags));
        asm pop ds;
        break;
    case 19:
        asm push ds;
        asm lds si, destination;
        XX_INVOKE(far,__cdecl,(int),(flags));
        asm pop ds;
        break;
    case 20:
        asm mov si, word ptr destination;
        XX_INVOKE(near,__pascal,(int),(flags)); break;
    case 21:
        asm mov si, word ptr destination;
        XX_INVOKE(far,__pascal,(int),(flags)); break;
    case 22:
        asm push ds;
        asm lds si, destination;
        XX_INVOKE(near,__pascal,(int),(flags));
        asm pop ds;
        break;
    case 23:
        asm push ds;
        asm lds si, destination;
        XX_INVOKE(far,__pascal,(int),(flags));
        asm pop ds;
        break;
    default: break;
    }
    asm pop ds;
}

static void near callMemberFunc(void far *destination,xx_code_ptr function,unsigned mask)
{
    unsigned saved_ds;
    unsigned kind;

    saved_ds = XX_RUNTIME->saved_ds;
    asm push ds;
    asm mov ds, saved_ds;
    kind = mask & 1;
    if(mask & 4) kind |= 2;
    if(mask & 2) kind |= 4;
    if(mask & 0x20) kind |= 8;

    switch(kind) {
    case 0: XX_INVOKE(near,__cdecl,(void near *),((void near *)destination)); break;
    case 1: XX_INVOKE(far,__cdecl,(void near *),((void near *)destination)); break;
    case 2: XX_INVOKE(near,__cdecl,(void far *),(destination)); break;
    case 3: XX_INVOKE(far,__cdecl,(void far *),(destination)); break;
    case 4: XX_INVOKE(near,__pascal,(void near *),((void near *)destination)); break;
    case 5: XX_INVOKE(far,__pascal,(void near *),((void near *)destination)); break;
    case 6: XX_INVOKE(near,__pascal,(void far *),(destination)); break;
    case 7: XX_INVOKE(far,__pascal,(void far *),(destination)); break;
    case 8: XX_INVOKE(near,__fastcall,(void near *),((void near *)destination)); break;
    case 9: XX_INVOKE(far,__fastcall,(void near *),((void near *)destination)); break;
    case 10: XX_INVOKE(near,__fastcall,(void far *),(destination)); break;
    case 11: XX_INVOKE(far,__fastcall,(void far *),(destination)); break;
    default: break;
    }
    asm pop ds;
}

#undef XX_INVOKE
