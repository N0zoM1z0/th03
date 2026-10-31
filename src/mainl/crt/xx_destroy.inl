// Bounded destruction bank of the original monolithic DOS xx.cpp TU.
// Include after xx_dispatch.inl; its caller sees the TU's static forward
// declaration of dtorCleanup. No later NEWXX/Delphi counter model is used here.
#include "xx_abi.h"

enum {
    XT_CLASS = 0x0002, XT_POINTER = 0x0010, XT_ARRAY = 0x0400,
    XC_DTOR = 0x0002, XC_VTABLE = 0x0010, XC_VIRTUAL_DTOR = 0x0020,
    XC_RTTI = 0x0040, XC_FAR_VPTR = 0x1000,
    XD_PTRVAL = 0x0001, XD_DELPTR = 0x0002, XD_STACKVAR = 0x0004,
    XD_DELETE = 0x0008, XD_RETVAL = 0x0010, XD_RETCTX = 0x0020,
    XD_VECCNT = 0x0040, XD_FARPTR = 0x0080, XD_DTCADJ = 0x0100
};

// These are interfaces to the preceding xx bodies and the original runtime.
void near callDestructor(void far *,xx_code_ptr,unsigned,int);
void near callMemberFunc(void far *,xx_code_ptr,unsigned);
extern "C" void far __cdecl __call_terminate();

static void far destroyOneObject(void far *address,xx_type_ptr type,int virtual_bases)
{
    // Both catch-all scopes are present in the DOS target's 78-byte EH data.
    try {
        try {
            callDestructor(address,type->data.object.dtor_address,
                type->data.object.dtor_mask,virtual_bases);
        }
        catch(...) { __call_terminate(); }
    }
    catch(...) { __call_terminate(); }
}

static void far destroyVariable(void far *,xx_type_ptr,unsigned long,int,unsigned);
static void far destroyArray(void far *,xx_type_ptr,unsigned long,unsigned);

static void far destroyBases(void far *address,XXBase far *last,
    XXBase far *first,unsigned count,int is_virtual,unsigned new_bp)
{
    while(--last >= first) {
        void far *base_address = (char far *)address + last->offset;
        xx_type_ptr base_type;

        if(is_virtual)
            // A near virtual-base offset retains the object's segment.
            base_address = MK_FP(FP_SEG(base_address),*(unsigned far *)base_address);
        base_type = last->type;
        if(!(base_type->data.object.flags & XC_DTOR))
            continue;
        destroyVariable(base_address,base_type,count,0,new_bp);
        count = 0;
    }
}

static void far destroyVariable(void far *address,xx_type_ptr type,
    unsigned long dtor_count,int virtual_bases,unsigned new_bp)
{
    XXBase far *normal_first,far *normal_last;
    XXBase far *virtual_first,far *virtual_last;
    XXMember far *member_first,far *member_last;
    unsigned long remaining;
    unsigned count;

    remaining = virtual_bases ? type->data.object.dtor_count :
        type->data.object.nonvirtual_dtor_count;
    if(dtor_count == 0 || dtor_count >= remaining) {
        destroyOneObject(address,type,virtual_bases);
        return;
    }

    remaining = dtor_count;
    virtual_first = virtual_last = (XXBase far *)((char far *)type +
        type->data.object.virtual_bases_offset);
    if(virtual_bases) {
        for(;;virtual_last++) {
            xx_type_ptr base_type = virtual_last->type;
            if(!base_type)
                break;
            if(!(base_type->data.object.flags & XC_DTOR))
                continue;
            count = base_type->data.object.nonvirtual_dtor_count;
            if(count >= remaining) {
                destroyBases(address,virtual_last+1,virtual_first,
                    (unsigned)remaining,1,new_bp);
                return;
            }
            remaining -= count;
        }
    }

    normal_first = normal_last = (XXBase far *)((char far *)type +
        type->data.object.bases_offset);
    for(;;normal_last++) {
        xx_type_ptr base_type = normal_last->type;
        if(!base_type)
            break;
        if(!(base_type->data.object.flags & XC_DTOR))
            continue;
        count = base_type->data.object.nonvirtual_dtor_count;
        if(count >= remaining) {
            destroyBases(address,normal_last+1,normal_first,
                (unsigned)remaining,0,new_bp);
            if(virtual_bases)
                destroyBases(address,virtual_last,virtual_first,0,1,new_bp);
            return;
        }
        remaining -= count;
    }

    member_first = member_last = (XXMember far *)((char far *)type +
        type->data.object.members_offset);
    for(;;member_last++) {
        unsigned elements;
        xx_type_ptr member_type = member_last->type;
        elements = 1;
        if(member_type->mask & XT_ARRAY) {
            elements = (unsigned)member_type->data.array.count;
            member_type = member_type->data.array.element;
        }
        count = elements * member_type->data.object.dtor_count;
        if(count < remaining) {
            remaining -= count;
            continue;
        }
        do {
            void far *member_address = (char far *)address + member_last->offset;
            xx_type_ptr member_type = member_last->type;

            // The DOS body reuses this search's element count while walking
            // backward. Later RTL sources recompute it; preserve the target.
            if(elements > 1)
                destroyArray(member_address,member_last->type,remaining,new_bp);
            else
                destroyVariable(member_address,member_type,remaining,1,new_bp);
            remaining = 0;
        } while(--member_last >= member_first);
        destroyBases(address,normal_last,normal_first,0,0,new_bp);
        if(virtual_bases)
            destroyBases(address,virtual_last,virtual_first,0,1,new_bp);
        return;
    }
}

static void far destroyArray(void far *address,xx_type_ptr type,
    unsigned long dtor_count,unsigned new_bp)
{
    xx_type_ptr element_type = type;
    unsigned elements = (unsigned)element_type->data.array.count;
    unsigned long element_dtors;
    unsigned long completed;

    element_type = element_type->data.array.element;
    element_dtors = element_type->data.object.dtor_count;
    if(!dtor_count)
        dtor_count = element_dtors * elements;
    completed = dtor_count / element_dtors;
    dtor_count -= completed * element_dtors;
    address = (char far *)address + completed * element_type->size;
    if(dtor_count)
        destroyVariable(address,element_type,dtor_count,1,new_bp);
    while(completed--) {
        address = (char far *)address - element_type->size;
        destroyVariable(address,element_type,element_dtors,1,new_bp);
    }
}

static void far * far findTrueTypeAndAddr(void far *address,xx_type_ptr __ss *type_ptr)
{
    xx_type_ptr type = *type_ptr;
    if((type->data.object.flags & (XC_VTABLE|XC_RTTI)) == (XC_VTABLE|XC_RTTI)
        && type->data.object.vptr_offset != 0xFFFF) {
        void far *vtable = (char far *)address + type->data.object.vptr_offset;
        if(type->data.object.flags & XC_FAR_VPTR)
            vtable = *(void far * far *)vtable;
        else
            vtable = *(void near * far *)vtable;
        address = (char far *)address - ((unsigned far *)vtable)[-2];
        vtable = (char far *)vtable - ((unsigned far *)vtable)[-1];
        *type_ptr = *(xx_type_ptr far *)((char far *)vtable-8);
    }
    return address;
}

// The native search uses current directly,with no extra WORD induction pointer
// to current->flags. Keep its 32-byte frame and restore the outer profile below.
#pragma option -O-v
static int near dtorCleanup(XXDtorTable far *table,long minimum,
    xx_registration_ptr err,unsigned new_bp)
{
    unsigned long initial;
    unsigned long dtor_count;
    XXDtorTable far *current;
    int free_pointer = 0;

    // Only the low offset is tested: FFFF is an encoded empty region.
    if((unsigned)table == 0xFFFF)
        return 0;
    initial = err->initial_dtor_count;
    dtor_count = *__RefDestructorCount() - initial;
    dtor_count -= minimum;
    if(table->flags & XD_RETCTX)
        dtor_count = table->type->data.pointer.base->data.object.dtor_count;
    if(table->flags & XD_DTCADJ)
        return table->type->data.object.nonvirtual_dtor_count;
    if((long)dtor_count <= 0) {
        if((table->flags & (XD_PTRVAL|XD_DELPTR)) == (XD_PTRVAL|XD_DELPTR)) {
            current = table;
            free_pointer++;
            goto destroy;
        }
        return 0;
    }

    for(current = table;;current++) {
        xx_type_ptr type,element_type;
        unsigned count;
        if(!current->type) {
            current--;
            break;
        }
        type = element_type = current->type;
        count = 1;
        if(type->mask & XT_POINTER) {
            type = element_type = type->data.pointer.base;
            if((type->mask & XT_CLASS) &&
                (type->data.object.flags & XC_VIRTUAL_DTOR) &&
                (current->flags & XD_DELETE)) {
                void far *address;
                void far *pointer_address;
                if(current->flags & XD_STACKVAR)
                    address = (char __ss *)new_bp + current->location.frame_offset;
                else
                    address = current->location.address;
                pointer_address = address;
                if(current->flags & XD_FARPTR)
                    address = *(void far * far *)pointer_address;
                else
                    address = *(void near * far *)pointer_address;
                if(current->flags & XD_VECCNT)
                    *(unsigned *)&address += 4;
                address = findTrueTypeAndAddr(address,&type);
                element_type = type;
            }
        }
        if(type->mask & XT_ARRAY) {
            count = (unsigned)element_type->data.array.count;
            element_type = element_type->data.array.element;
        }
        count *= element_type->data.object.dtor_count;
        if(count >= dtor_count)
            break;
        dtor_count -= count;
    }

destroy:
    do {
        xx_type_ptr type = current->type;
        unsigned flags = current->flags;
        void far *address;
        void far *pointer_address;
        void far *block_address;

        if(flags & XD_STACKVAR)
            address = (char __ss *)new_bp + current->location.frame_offset;
        else
            address = current->location.address;
        if(flags & (XD_PTRVAL|XD_RETVAL)) {
            type = type->data.pointer.base;
            pointer_address = address;
            if(flags & XD_FARPTR)
                address = *(void far * far *)pointer_address;
            else
                address = *(void near * far *)pointer_address;
            block_address = address;
            if((flags & (XD_DELETE|XD_VECCNT)) == XD_VECCNT)
                *(unsigned *)&address += 4;
            if((type->mask & XT_CLASS) &&
                (type->data.object.flags & XC_VIRTUAL_DTOR) &&
                (flags & XD_DELETE))
                // The DOS body keeps the pre-adjustment allocation pointer.
                address = findTrueTypeAndAddr(address,&type);
        }
        if(!free_pointer) {
            if(type->mask & XT_ARRAY)
                destroyArray(address,type,dtor_count,new_bp);
            else
                destroyVariable(address,type,dtor_count,1,new_bp);
        }
        if((flags & (XD_PTRVAL|XD_DELPTR)) == (XD_PTRVAL|XD_DELPTR)) {
            if((flags & (XD_DELETE|XD_VECCNT)) == (XD_DELETE|XD_VECCNT))
                *(unsigned *)&block_address -= 4;
            if(type->mask & XT_ARRAY) {
                type = type->data.array.element;
                if(type->data.object.delete_array_address)
                    callMemberFunc(block_address,type->data.object.delete_array_address,
                        type->data.object.delete_array_mask);
                else if(flags & XD_FARPTR)
                    delete[] (char far *)block_address;
            }
            else {
                if(type->data.object.delete_address)
                    callMemberFunc(block_address,type->data.object.delete_address,
                        type->data.object.delete_mask);
                else if(flags & XD_FARPTR)
                    delete (char far *)block_address;
            }
        }
        dtor_count = 0;
    } while(current-- > table);
    return 0;
}
#pragma option -Ov
