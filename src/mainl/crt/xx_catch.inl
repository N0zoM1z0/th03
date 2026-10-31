// Bounded catch cleanup/argument initialization bank in the DOS xx.cpp TU.
// Include after the private type comparator and member-call adapters, before
// dispatch/destruction. Original compiler EH data precede destThrownValue.
#include "xx_abi.h"
#include <mem.h>

#pragma option -xd-

extern "C" void far __cdecl __call_terminate();

static void near destThrownValue(void far *address,xx_code_ptr destructor,unsigned mask)
{
    try {
        callDestructor(address,destructor,mask,1);
    }
    catch(...) { __call_terminate(); }
}

static void near exceptionHandled(xx_exception_ptr exception)
{
    xx_type_ptr type;

    if(exception->argument_buffer) {
        if(exception->class_flags & 2) {
            unsigned long saved_count;
            saved_count = *__RefDestructorCount();
            // The DOS target takes this descriptor from type,+4; it does not
            // substitute the later RTL's cached base descriptor,+16.
            type = exception->type;
            destThrownValue((char far *)exception + sizeof(XXException),
                type->data.object.dtor_address,type->data.object.dtor_mask);
            *__RefDestructorCount() = saved_count;
        }
        exception->argument_buffer = 0;
    }
    if(exception->argument_copy) {
        xx_type_ptr type = exception->argument_type;
        if((type->mask & 2) && (type->data.object.flags & 2))
            destThrownValue(exception->argument_address,
                type->data.object.dtor_address,type->data.object.dtor_mask);
        exception->argument_copy = 0;
    }
}

void far __cdecl _CatchCleanup()
{
    xx_exception_ptr exception = XX_RUNTIME->exceptions;
    xx_registration_ptr err;

    XX_RUNTIME->exceptions = exception->previous;
    err = exception->registration;
    err->context = *(unsigned far *)((char far *)err->table + err->context);
    exceptionHandled(exception);
    asm {
        push ds
        les bx, exception
        mov ds, es:[bx+XX_FREE_DS]
    }
    exception->free(exception);
    asm pop ds;
}

static int near findBaseAddress(XXBase far *list,int is_virtual,
    xx_type_ptr destination,void far * __ss *address_ptr)
{
    for(;;list++) {
        xx_type_ptr type = list->type;
        void far *address;
        XXBase far *bases;

        if(!type)
            return 0;
        address = (char far *)*address_ptr + list->offset;
        if(is_virtual)
            address = MK_FP(FP_SEG(address),*(unsigned far *)address);
        if(!sameTypeID(type,destination)) {
            if(!(type->mask & 2))
                continue;
            bases = (XXBase far *)((char far *)type + type->data.object.bases_offset);
            // The target tests the computed far pointer,not the relative WORD.
            if(!bases || !findBaseAddress(bases,0,destination,&address))
                continue;
        }
        *address_ptr = address;
        return 1;
    }
}

static void far * far adjustClassAddress(void far *address,
    xx_type_ptr source,xx_type_ptr destination)
{
    XXBase far *list;
    if(!address)
        return address;
    list = (XXBase far *)((char far *)source + source->data.object.bases_offset);
    if(findBaseAddress(list,0,destination,&address))
        return address;
    list = (XXBase far *)((char far *)source + source->data.object.virtual_bases_offset);
    if(findBaseAddress(list,1,destination,&address))
        return address;
    return 0;
}

static void near initCatchArg(XXHandler far *handler,xx_registration_ptr err,
    xx_exception_ptr exception,XXHandlerTable far *table,unsigned new_bp)
{
    xx_type_ptr handler_type;
    xx_type_ptr type;
    unsigned size;
    unsigned mask;
    unsigned base;
    void far *value;
    void far *pointer;
    int keep_original;

    exception->argument_type = handler_type = handler->type;
    if(!handler_type)
        return;
    if(handler->flags & 0x80)
        return;
    keep_original = !(handler->flags & 1);
    value = (char far *)exception + sizeof(XXException);
    exception->argument_copy = 1;
    exception->argument_address = (void __ss *)(new_bp + table->argument_offset);
    type = handler_type;
    size = type->size;
    mask = type->mask;
    base = mask;
    if(mask & 0x30) {
        type = type->data.pointer.base;
        base = type->mask;
    }
    if((mask & 0x10) && (exception->flags & 1)) {
        memset(exception->argument_address,0,size);
        keep_original = 1;
        goto done;
    }
    if((base & 1) && (mask & 0x30)) {
        if(mask & 0x20)
            keep_original = 1;
        else {
            value = *(void far * far *)value;
            if(exception->mask & 0x1000) {
                value = (void near *)FP_OFF(value);
                keep_original = 1;
            }
        }
        if(!sameTypeID(exception->base,type)) {
            void far *old_value = value;
            value = adjustClassAddress(value,exception->base,type);
            if(value != old_value)
                keep_original = 1;
        }
        memcpy(exception->argument_address,&value,size);
        goto done;
    }
    if(exception->mask & 1) {
        if(!sameTypeID(exception->base,type)) {
            value = adjustClassAddress(value,exception->base,type);
            keep_original = 1;
        }
        if(type->data.object.flags & 1) {
            callCopyCtor(exception->argument_address,value,
                (xx_code_ptr)handler->copy_constructor,handler->copy_mask);
            keep_original = 1;
        }
        else
            memcpy(exception->argument_address,value,size);
        goto done;
    }
    if(mask & 0x20) {
        memcpy(exception->argument_address,&value,size);
        keep_original = 1;
        goto done;
    }
    if((mask & 0x10) && exception->size != size) {
        pointer = *(void near * far *)value;
        memcpy(exception->argument_address,&pointer,sizeof(pointer));
    }
    else
        memcpy(exception->argument_address,value,size);

done:
    if(!keep_original) {
        if(type->data.object.flags & 2)
            destThrownValue(value,type->data.object.dtor_address,type->data.object.dtor_mask);
        exception->argument_buffer = 0;
    }
}
