// Entry and private descriptor-name helper at the front of DOS xx.cpp.
#include "xx_abi.h"

extern "C" void far __cdecl __JumpToCatch__()
{
    // BX/CX supply the destination stack/frame,DX:AX the far catch address.
    // The compiler's unreachable SI/DI restoration remains part of this body.
    asm {
        mov sp,bx
        mov bp,cx
        push dx
        push ax
        retf
    }
}

static const char far * far typeIDname(xx_type_ptr type)
{
    if(!type)
        return "<notype>";
    return (const char far *)type+type->name_offset;
}
