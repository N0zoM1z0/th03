// Bounded type-compatibility/descriptor bank of the original DOS xx.cpp TU.
// Include after sameTypeID and before the member-call/catch/dispatch banks.
#include "xx_abi.h"
#include <stdlib.h>

static int near findBaseType(xx_type_ptr source,xx_type_ptr destination,
    xx_type_ptr far *friends,int public_path)
{
    XXBase far *list;
    int accessible;
    xx_type_ptr base;

    list = (XXBase far *)((char far *)source + source->data.object.virtual_bases_offset);
    for(;;list++) {
        base = list->type;
        if(!base)
            break;
        if(list->flags & 8)
            continue;
        accessible = public_path && ((list->flags & 3) == 3);
        if(sameTypeID(destination,base) && accessible)
            return 1;
        if((base->data.object.flags & 4) &&
            findBaseType(base,destination,friends,accessible))
            return 1;
    }
    list = (XXBase far *)((char far *)source + source->data.object.bases_offset);
    for(;;list++) {
        base = list->type;
        if(!base)
            break;
        accessible = public_path && ((list->flags & 3) == 3);
        if(sameTypeID(destination,base) && accessible)
            return 1;
        if((base->data.object.flags & 4) &&
            findBaseType(base,destination,friends,accessible))
            return 1;
    }
    return 0;
}

static int near compatibleType(xx_type_ptr source,xx_type_ptr destination,
    int exact,xx_type_ptr far *friends)
{
    unsigned source_mask;
    unsigned destination_mask;

    for(;;) {
        if(source == destination)
            return 1;
        source_mask = source->mask;
        destination_mask = destination->mask;
        if((source_mask & destination_mask) & 0x10) {
            source_mask &= 0x3300;
            destination_mask &= 0x3300;
            if(source_mask == destination_mask)
                goto indirect;
            if(exact)
                return 0;
            if((source_mask & 0x300) != (destination_mask & 0x300)) {
                if((source_mask & ~destination_mask) & 0x300)
                    return 0;
                source_mask |= 0x300;
                destination_mask |= 0x300;
                if(source_mask == destination_mask)
                    goto indirect;
            }
            if((source_mask | 0x3000) != (destination_mask | 0x3000))
                return 0;
            // This older near-to-far case returns without inspecting pointees.
            return (source_mask & 0x1000) != 0;
        }
        if((source_mask & destination_mask) & 0x400) {
            if(source->data.array.count != destination->data.array.count) {
                if(exact)
                    return 0;
                if(source->data.array.count || destination->data.array.count)
                    return 0;
            }
indirect:
            exact = 1;
            source = source->data.pointer.base;
            destination = destination->data.pointer.base;
            continue;
        }
        if(sameTypeID(source,destination))
            return 1;
        if(!(source_mask & 2) || !(destination_mask & 1) ||
            !(source->data.object.flags & 4))
            return 0;
        return findBaseType(source,destination,friends,1);
    }
}

// Only the observed far slot at runtime+20h is described. The intervening
// runtime storage is not represented by invented fields or padding.
#define XX_EMERGENCY_BUFFER (*(void far * far *)((char far *)XX_RUNTIME + 0x20))

static xx_exception_ptr far allocExceptMem(unsigned size)
{
    void far *memory = malloc(size);
    if(!memory) {
        if(size > 128 || (XX_RUNTIME->flags & 1))
            abort();
        XX_RUNTIME->flags |= 1;
        return (xx_exception_ptr)XX_EMERGENCY_BUFFER;
    }
    return (xx_exception_ptr)memory;
}

static void far freeExceptMem(xx_exception_ptr exception)
{
    if(exception == (xx_exception_ptr)XX_EMERGENCY_BUFFER)
        XX_RUNTIME->flags &= ~1;
    else
        free(exception);
}

#undef XX_EMERGENCY_BUFFER

static int near typeIDcaught(xx_type_ptr source,xx_type_ptr far *friends,
    xx_type_ptr destination,unsigned flags,int fspec)
{
    unsigned source_mask;
    unsigned destination_mask;

    if(compatibleType(source,destination,0,friends))
        return 1;
    source_mask = source->mask;
    destination_mask = destination->mask;
    if(destination_mask & 0x20) {
        if(compatibleType(source,destination->data.pointer.base,1,friends))
            return 1;
        destination = destination->data.pointer.base;
        destination_mask = destination->mask;
        if(!(destination_mask & 0x10))
            return 0;
        if(compatibleType(source,destination,0,friends))
            return 1;
        if((source_mask & 0x3000) != (destination_mask & 0x3000))
            return 0;
    }
    if(destination_mask & 0x10) {
        if(flags & 1)
            return 1;
        if(!(source_mask & 0x10))
            return 0;
        if((source_mask & 0x2000) && !(destination_mask & 0x2000))
            return 0;
        if(destination_mask & 0x40)
            // The DOS void-pointer fallback requires equal CV bits.
            return (source_mask & 0x300) == (destination_mask & 0x300);
    }
    return 0;
}
