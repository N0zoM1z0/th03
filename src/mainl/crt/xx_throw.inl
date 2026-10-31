// DOS xx.cpp throw/global-unwind bank, after the member-call adapters.
// The runtime name/diagnostic fields are borrowed slots, not owned storage.
#include "xx_abi.h"
#include <mem.h>

#pragma option -xd-

extern "C" void far __cdecl __call_terminate();
extern "C" unsigned char _8086;
extern "C" void far __cdecl __saveregs RaiseException(unsigned long,
    unsigned long,unsigned long,const unsigned long far *);

#define XX_THROW_FILE (*(unsigned char far * far *)((char far *)XX_RUNTIME+0x16))
#define XX_THROW_LINE (*(unsigned far *)((char far *)XX_RUNTIME+0x1A))
#define XX_THROW_NAME (*(char far * far *)((char far *)XX_RUNTIME+0x1C))

static void far __cdecl tossAnException(void far *type_id,void far *address,
    xx_type_ptr far *friends,xx_code_ptr copy_constructor,unsigned copy_mask,
    unsigned flags,unsigned line,unsigned char far *file,unsigned long pc,
    int rethrow)
{
    // The DOS entry caches the opaque compiler argument as a typed descriptor.
    xx_type_ptr type = (xx_type_ptr)type_id;
    xx_type_ptr base;
    unsigned size,mask,class_flags;
    xx_exception_ptr exception;
    char far *source;
    char far *destination;
    unsigned long saved_count;
    unsigned long arguments[3];

    XX_RUNTIME->saved_ds = _DS;
    XX_THROW_NAME = (char far *)XX_RUNTIME+0x28;
    source = (char far *)type+type->name_offset;
    destination = XX_THROW_NAME;
    for(;*source;source++) {
        if(FP_OFF(destination) < FP_OFF(XX_THROW_NAME)+0x7F)
            *destination++ = *source;
    }
    *destination = 0;
    XX_THROW_LINE = line;
    XX_THROW_FILE = file;
    base = type;
    size = type->size;
    mask = type->mask;
    class_flags = (mask & 2) ? type->data.object.flags : 0;
    if(mask & 0x30)
        base = base->data.pointer.base;
    exception = (xx_exception_ptr)allocExceptMem(size+sizeof(XXException));
    exception->previous = XX_RUNTIME->exceptions;
    XX_RUNTIME->exceptions = exception;
    exception->type = type;
    exception->flags = flags;
    exception->size = size;
    exception->mask = mask;
    exception->class_flags = class_flags;
    exception->base = base;
    exception->friends = friends;
    exception->registration = 0;
    exception->handler = 0;
    exception->free_ds = _DS;
    exception->free = freeExceptMem;
    exception->throw_line = line;
    exception->throw_file = file;
    exception->copy_constructor = copy_constructor;
    exception->copy_mask = copy_mask;
    exception->argument_copy = 0;
    exception->argument_buffer = 1;
    memcpy((char far *)exception+sizeof(XXException),address,size);
    if(class_flags & 1) {
        saved_count = *__RefDestructorCount();
        try {
            callCopyCtor((char far *)exception+sizeof(XXException),address,
                copy_constructor,copy_mask);
        }
        catch(...) { __call_terminate(); }
        *__RefDestructorCount() = saved_count;
    }
    if(!rethrow && (class_flags & 2)) {
        try {
            callDestructor(address,type->data.object.dtor_address,
                type->data.object.dtor_mask,1);
        }
        catch(...) { __call_terminate(); }
    }
    arguments[0] = (unsigned long)XX_THROW_NAME;
    arguments[1] = pc;
    arguments[2] = (unsigned long)exception;
    RaiseException(0x0EEFFACEUL,1,3,arguments);
}

// These public C++ spellings are consumed by compiler-generated throw sites.
void far __cdecl _ThrowException(void far *type,void far *address,
    void far *friends,void far *copy_constructor,unsigned copy_mask,
    unsigned flags,unsigned line,unsigned char far *file)
{
    unsigned frame;
    unsigned long pc;
    asm mov frame,bp;
    pc = *(unsigned long __ss *)(frame+2);
    tossAnException((xx_type_ptr)type,address,(xx_type_ptr far *)friends,
        (xx_code_ptr)copy_constructor,copy_mask,flags,line,file,
        pc,0);
}

void far __cdecl _ReThrowException(unsigned line,unsigned char far *file)
{
    unsigned frame;
    unsigned long pc;
    xx_exception_ptr exception;
    asm mov frame,bp;
    pc = *(unsigned long __ss *)(frame+2);
    exception = XX_RUNTIME->exceptions;
    if(!exception)
        __call_terminate();
    tossAnException(exception->type,exception->argument_buffer ?
        (char far *)exception+sizeof(XXException) : exception->argument_address,
        exception->friends,(xx_code_ptr)exception->copy_constructor,
        exception->copy_mask,exception->flags,line,file,
        pc,1);
}

static void far exceptionChainHook() {}

typedef int (far __cdecl *xx_chain_handler)(XXExceptionRecord far *,
    xx_registration_ptr,void far *,unsigned long);

static int far dispatchException(XXExceptionRecord __ss *record,
    void far *context,xx_registration_ptr target)
{
    xx_registration_ptr current;
    int unwinding = 0;
    if(record->flags & 6)
        ++unwinding;
    current = XX_CHAIN;
    exceptionChainHook();
    for(;current != (xx_registration_ptr)0xFFFF && current != target;
        current = current->next) {
        xx_registration_ptr handler_record = current;
        int disposition = ((xx_chain_handler)handler_record->catcher)(record,current,context,0);
        if(disposition == 0)
            return disposition;
        if(unwinding)
            XX_CHAIN = current;
    }
    if(unwinding)
        XX_CHAIN = current;
    return 1;
}

extern "C" void far __cdecl _Global_unwind(xx_registration_ptr target,
    XXExceptionRecord __ss *record)
{
    XXExceptionRecord local;
    if(!record) {
        local.code = 0x26;
        local.flags = 2;
        local.count = 0;
        record = &local;
    }
    record->flags |= 2;
    dispatchException(record,0,target);
}

// Used DOS context prefix: flags,six debug DWORDs and the112-byte x87 save
// area precede segment/general registers. Only the fields written below are
// initialized. The original's remaining stack-frame ownership is still open.
#pragma option -a-
struct XXRaiseContext {
    unsigned long context_flags;
    unsigned long dr0,dr1,dr2,dr3,dr6,dr7;
    struct {
        unsigned long control,status,tag,error_offset,error_selector;
        unsigned long data_offset,data_selector;
        unsigned char registers[80];
        unsigned long cr0;
    } floating;
    unsigned long seg_gs,seg_fs,es,ds;
    unsigned long edi,esi,ebx,edx,ecx,eax,ebp;
    unsigned long eip,cs,eflags,stack_pointer,stack_segment;
};
struct XXRaiseSaved16 {
    unsigned es,ds,di,si,bp,sp,bx,dx,cx,ax;
};
struct XXRaiseReturn32 {
    unsigned gs,fs,es,ds;
    unsigned long edi,esi,ebp,esp,ebx,edx,ecx,eax,flags;
    unsigned ip,cs;
};
struct XXRaiseReturn16 {
    unsigned es,ds,di,si,bp,sp,bx,dx,cx,ax,flags,ip,cs;
};
#pragma option -a.
typedef char xx_raise_context_prefix_bytes[(sizeof(XXRaiseContext)==204) ? 1 : -1];
typedef char xx_raise_context_gs[(offsetof(XXRaiseContext,seg_gs)==140) ? 1 : -1];
typedef char xx_raise_return32_bytes[(sizeof(XXRaiseReturn32)==48) ? 1 : -1];
typedef char xx_raise_return16_bytes[(sizeof(XXRaiseReturn16)==26) ? 1 : -1];

// The 16-bit native assembler lacks these 386 mnemonics. Instruction intrinsics
// retain the CPU operations; the two BP displacements remain compiler symbols.
// Its local-symbol arithmetic subtracts member offsets,unlike the -S emitter.
#ifdef TH03_XX_NATIVE_OBJECT
enum {
    XX_BP_eflags = offsetof(XXRaiseContext,eflags),
    XX_BP_seg_fs = offsetof(XXRaiseContext,seg_fs),
    XX_BP_seg_gs = offsetof(XXRaiseContext,seg_gs),
    XX_BP_stack_segment = offsetof(XXRaiseContext,stack_segment)
};
#define XX_CPU386()
#define XX_CPU186()
#define XX_CPU8086()
#define XX_PUSHAD() __emit__(0x66,0x60)
#define XX_POPAD() __emit__(0x66,0x61)
#define XX_POPA() __emit__(0x61)
#define XX_PUSHFD() __emit__(0x66,0x9C)
#define XX_POPFD() __emit__(0x66,0x9D)
#define XX_POP_EAX() __emit__(0x66,0x58)
#define XX_SHR_EAX_16() __emit__(0x66,0xC1,0xE8,16)
#define XX_POP_GS() __emit__(0x0F,0xA9)
#define XX_POP_FS() __emit__(0x0F,0xA1)
#define XX_CONTEXT_WORD(field,extra) [context-XX_BP_##field+extra]
#define XX_SAVE_FS() __emit__(0x8C,0xA6); asm dw offset context-XX_BP_seg_fs
#define XX_SAVE_GS() __emit__(0x8C,0xAE); asm dw offset context-XX_BP_seg_gs
#else
#define XX_CPU386() asm .386
#define XX_CPU186() asm .186
#define XX_CPU8086() asm .8086
#define XX_PUSHAD() asm pushad
#define XX_POPAD() asm popad
#define XX_POPA() asm popa
#define XX_PUSHFD() asm pushfd
#define XX_POPFD() asm popfd
#define XX_POP_EAX() asm pop eax
#define XX_SHR_EAX_16() asm shr eax,16
#define XX_POP_GS() asm pop gs
#define XX_POP_FS() asm pop fs
#define XX_CONTEXT_WORD(field,extra) context.field+extra
#define XX_SAVE_FS() asm mov word ptr context.seg_fs,fs
#define XX_SAVE_GS() asm mov word ptr context.seg_gs,gs
#endif

static void far exceptionContextHook(void __ss *) {}

// The native argument loop indexes each DWORD directly; it has no induction
// pointer temporaries. Keep that option local to this register-save routine.
#pragma option -O-v
extern "C" void far __cdecl __saveregs RaiseException(unsigned long code,
    unsigned long flags,unsigned long count,const unsigned long far *arguments)
{
    unsigned i;
    xx_code_ptr pc;
    unsigned saved_flags;
    unsigned frame;
    XXExceptionRecord exception;
    XXRaiseContext context;
    XXRaiseSaved16 saved;
    unsigned long registers[8];
    // The resume frame overlaps the top of this function's stack frame.
    // Keep its address in ES:BX throughout the writes, as in the DOS runtime;
    // a compiler-spilled far pointer would overwrite itself during the copy.
#define return32 ((XXRaiseReturn32 far *)MK_FP(_ES,_BX))
#define return16 ((XXRaiseReturn16 far *)MK_FP(_ES,_BX))

    exceptionContextHook((char __ss *)&context+sizeof(context));
    // AX also supplies the low half captured by the following PUSHAD.
    asm pushf;
    asm pop ax;
    saved_flags = _AX;
    if(_8086 >= 3) {
        XX_CPU386();
        XX_PUSHAD();
        asm mov frame,sp;
        memcpy(registers,(void __ss *)frame,sizeof(registers));
        XX_POPAD();
        context.edi = registers[0];
        context.esi = registers[1];
        context.ebx = registers[4];
        context.edx = registers[5];
        context.ecx = registers[6];
        context.eax = registers[7];
        context.ebp = registers[2];
        XX_PUSHFD();
        XX_POP_EAX();
        XX_SHR_EAX_16();
        asm mov word ptr XX_CONTEXT_WORD(eflags,2),ax;
        asm mov ax,saved_flags;
        asm mov word ptr XX_CONTEXT_WORD(eflags,0),ax;
        asm mov word ptr XX_CONTEXT_WORD(seg_fs,2),0;
        XX_SAVE_FS();
        asm mov word ptr XX_CONTEXT_WORD(seg_gs,2),0;
        XX_SAVE_GS();
        XX_CPU8086();
    }
    else {
        context.edi = context.esi = context.ebx = context.edx =
            context.ecx = context.eax = context.ebp = 0;
        context.eflags = saved_flags;
    }
    context.stack_pointer = context.ebp+24;
    if(code == 0x0EEFFACEUL)
        pc = (xx_code_ptr)arguments[1];
    else {
        asm mov frame,bp;
        pc = *(xx_code_ptr __ss *)(frame+sizeof(XXRaiseSaved16));
    }
    context.eip = FP_OFF(pc);
    context.cs = FP_SEG(pc);
    asm mov frame,bp;
    memcpy(&saved,(void __ss *)frame,sizeof(saved));
    context.ds = saved.ds;
    context.es = saved.es;
    context.stack_segment = _SS;
    *(unsigned __ss *)&context.eax = saved.ax;
    *(unsigned __ss *)&context.ebx = saved.bx;
    *(unsigned __ss *)&context.ecx = saved.cx;
    *(unsigned __ss *)&context.edx = saved.dx;
    *(unsigned __ss *)&context.esi = saved.si;
    *(unsigned __ss *)&context.edi = saved.di;
    *(unsigned __ss *)&context.ebp = saved.bp;
    exception.code = code & ~0x10000000UL;
    exception.flags = flags;
    exception.address = pc;
    exception.nested = 0;
    if(!arguments)
        count = 0;
    if(count > 15)
        count = 15;
    exception.count = (unsigned)count;
    for(i=0;i<count;i++)
        exception.information[i] = arguments[i];
    for(;;) {
        if(!dispatchException(&exception,&context,(xx_registration_ptr)0xFFFF)) {
            if(!(flags & 1))
                break;
            exception.code = 0xC0000025UL;
            exception.flags = flags;
            exception.address = 0;
            exception.nested = 0;
            exception.count = 0;
        }
        else {
            exception.flags |= 2;
            if(dispatchException(&exception,&context,(xx_registration_ptr)0xFFFF))
                goto unhandled;
            break;
        }
    }
    if(_8086 >= 3) {
        _CX = (unsigned)context.stack_pointer-48;
        _ES = (unsigned)context.stack_segment;
        _BX = _CX;
        return32->gs = (unsigned)context.seg_gs;
        return32->fs = (unsigned)context.seg_fs;
        return32->es = (unsigned)context.es;
        return32->ds = (unsigned)context.ds;
        return32->edi = context.edi;
        return32->esi = context.esi;
        return32->ebp = context.ebp;
        return32->esp = context.stack_pointer;
        return32->ebx = context.ebx;
        return32->edx = context.edx;
        return32->ecx = context.ecx;
        return32->eax = context.eax;
        return32->flags = context.eflags;
        return32->ip = (unsigned)context.eip;
        return32->cs = (unsigned)context.cs;
        XX_CPU386();
        asm mov ss,word ptr XX_CONTEXT_WORD(stack_segment,0);
        asm mov sp,bx;
        XX_POP_GS();
        XX_POP_FS();
        asm pop es;
        asm pop ds;
        XX_POPAD();
        XX_POPFD();
        asm retf;
        XX_CPU8086();
        return;
    }
    else {
        _CX = (unsigned)context.stack_pointer-26;
        _ES = (unsigned)context.stack_segment;
        _BX = _CX;
        return16->es = (unsigned)context.es;
        return16->ds = (unsigned)context.ds;
        return16->di = (unsigned)context.edi;
        return16->si = (unsigned)context.esi;
        return16->bp = (unsigned)context.ebp;
        return16->sp = (unsigned)context.stack_pointer;
        return16->bx = (unsigned)context.ebx;
        return16->dx = (unsigned)context.edx;
        return16->cx = (unsigned)context.ecx;
        return16->ax = (unsigned)context.eax;
        return16->flags = (unsigned)context.eflags;
        return16->ip = (unsigned)context.eip;
        return16->cs = (unsigned)context.cs;
        asm mov ss,word ptr XX_CONTEXT_WORD(stack_segment,0);
        asm mov sp,bx;
        XX_CPU186();
        asm pop es;
        asm pop ds;
        XX_POPA();
        asm popf;
        asm retf;
        XX_CPU8086();
        return;
    }
unhandled:
    __call_terminate();
}

#pragma option -Ov
#undef XX_CPU386
#undef XX_CPU186
#undef XX_CPU8086
#undef XX_PUSHAD
#undef XX_POPAD
#undef XX_POPA
#undef XX_PUSHFD
#undef XX_POPFD
#undef XX_POP_EAX
#undef XX_SHR_EAX_16
#undef XX_POP_GS
#undef XX_POP_FS
#undef XX_CONTEXT_WORD
#undef XX_SAVE_FS
#undef XX_SAVE_GS
#undef return32
#undef return16
#undef XX_THROW_FILE
#undef XX_THROW_LINE
#undef XX_THROW_NAME
