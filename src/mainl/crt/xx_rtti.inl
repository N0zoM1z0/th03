// Tail of the original DOS xx.cpp TU. Compiler-produced throw descriptors,
// the typeinfo vtable and class descriptor follow these function definitions.
#include "xx_abi.h"
#include <typeinfo.h>
#include <string.h>
#include <mem.h>

// The two empty exception objects occupy adjacent single BSS bytes,+8/+9.
// Recover their shared storage as a packed pair of actual exception values.
#pragma option -a-
static struct XXRttiExceptions {
    Bad_typeid typeid_value;
    Bad_cast cast_value;
} rtti_exceptions;
#pragma option -a.

extern "C" int far __cdecl _CurrExcContext(void __ss *registration)
{
    xx_registration_ptr err = (xx_registration_ptr)registration;
    char far *handler;
    if(err == (xx_registration_ptr)0xFFFF)
        return -1;
    handler = (char far *)err->catcher-8;
    // This DOS version has no imported-jump-table indirection fallback.
    if(memcmp(handler,"**BCCxh1",8))
        return -1;
    return err->context;
}

unsigned char far * far __cdecl __ThrowFileName()
{
    return *(unsigned char far * far *)((char far *)XX_RUNTIME+0x16);
}

unsigned far __cdecl __ThrowLineNumber()
{
    return *(unsigned far *)((char far *)XX_RUNTIME+0x1A);
}

char far * far __cdecl __ThrowExceptionName()
{
    return *(char far * far *)((char far *)XX_RUNTIME+0x1C);
}

typeinfo::typeinfo(const typeinfo far &)
{
    // The original unsupported copy operation throws a null typeinfo pointer.
    throw (typeinfo far *)0;
}

typeinfo &typeinfo::operator=(const typeinfo far &)
{
    return *this;
}

typeinfo::~typeinfo() {}

int typeinfo::operator==(const typeinfo far &other) const
{
    return sameTypeID((xx_type_ptr)tpp,(xx_type_ptr)other.tpp);
}

int typeinfo::operator!=(const typeinfo far &other) const
{
    return !(*this == other);
}

int typeinfo::before(const typeinfo far &other) const
{
    if(!tpp)
        return 0;
    if(!other.tpp)
        return 1;
    return strcmp((const char far *)tpp+((xx_type_ptr)tpp)->name_offset,
        (const char far *)other.tpp+((xx_type_ptr)other.tpp)->name_offset) < 0;
}

const char far *typeinfo::name() const
{
    return typeIDname((xx_type_ptr)tpp);
}

void far * far __cdecl __GetTypeInfo(void far *object,void far *vtable,
    void far *,void far *result_address)
{
    xx_type_ptr type;
    typeinfo far *result;
    result = (typeinfo far *)result_address;
    if(!object)
        throw rtti_exceptions.typeid_value;
    vtable = (char far *)vtable-*(unsigned far *)((char far *)vtable-2);
    type = *(xx_type_ptr far *)((char far *)vtable-8);
    result->tpp = (tpid far *)type;
    return result;
}

static void far * near searchBaseClass(void far *address,xx_type_ptr type,
    void far *target_address,xx_type_ptr destination,
    void far *source_address,xx_type_ptr source,int __ss *public_result,
    int public_path,xx_type_ptr virtual_type)
{
    XXBase far *bases;
    int ordinary;
    int matched_public = 0;
    void far *matched_address = 0;
    int matches = 0;

    if((source && sameTypeID(source,type)) || !(type->data.object.flags & 4))
        return 0;
    ordinary = 0;
    bases = (XXBase far *)((char far *)type+type->data.object.virtual_bases_offset);
    for(;;) {
        for(;;bases++) {
            int accessible;
            void far *base_address;
            xx_type_ptr next_virtual;
            xx_type_ptr base;
            void far *found;
            base = bases->type;
            if(!base)
                break;
            if(bases->flags & 8)
                continue;
            accessible = public_path && ((bases->flags & 3) == 3);
            base_address = (char far *)address+bases->offset;
            next_virtual = virtual_type;
            if(bases->flags & 4) {
                base_address = MK_FP(FP_SEG(base_address),
                    *(unsigned far *)base_address);
                next_virtual = base;
            }
            if(!sameTypeID(destination,base)) {
                if(!(base->data.object.flags & 4))
                    continue;
                found = searchBaseClass(base_address,base,target_address,
                    destination,source_address,source,public_result,accessible,
                    next_virtual);
                if(!found)
                    continue;
                base_address = found;
                accessible = *public_result;
            }
            else {
                if(target_address) {
                    if(base_address == target_address)
                        return base_address;
                    continue;
                }
                if(source_address && !searchBaseClass(base_address,base,
                    source_address,source,0,0,public_result,0,0))
                    continue;
            }
            if(matches && base_address == matched_address)
                matched_public |= accessible;
            else {
                ++matches;
                matched_address = base_address;
                matched_public = accessible;
            }
        }
        if(ordinary)
            break;
        ++ordinary;
        bases = (XXBase far *)((char far *)type+type->data.object.bases_offset);
    }
    *public_result = matched_public;
    if(matches != 1)
        matched_address = 0;
    return matched_address;
}

void far * far __cdecl __DynamicCast(void far *object,void far *vtable,
    void far *source_id,void far *destination_id,int is_reference)
{
    xx_type_ptr source = (xx_type_ptr)source_id;
    xx_type_ptr destination = (xx_type_ptr)destination_id;
    xx_type_ptr complete_type;
    void far *complete_address;
    void far *result;
    int accessible;

    if(object) {
        complete_address = (char far *)object-
            *(unsigned far *)((char far *)vtable-4);
        vtable = (char far *)vtable-*(unsigned far *)((char far *)vtable-2);
        complete_type = *(xx_type_ptr far *)((char far *)vtable-8);
        if(!destination || sameTypeID(destination,complete_type))
            return complete_address;
        if(!sameTypeID(source,complete_type)) {
            result = searchBaseClass(complete_address,complete_type,0,
                destination,object,source,&accessible,1,0);
            if(result)
                return result;
        }
        result = searchBaseClass(complete_address,complete_type,0,destination,
            0,0,&accessible,1,0);
        if(result && accessible)
            return result;
    }
    if(is_reference)
        throw rtti_exceptions.cast_value;
    return 0;
}
