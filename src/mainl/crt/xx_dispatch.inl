// Bounded local unwind and exception-dispatch include from the DOS xx.cpp TU.
// Native integration is pending recovery of the surrounding private helpers.
#include "xx_abi.h"

#pragma option -xd-

enum XXBlockKind {
    XB_FINALLY, XB_EXCEXP, XB_EXCCNS, XB_TRYCPP, XB_CATCH, XB_DEST
};

static void near local_unwind(xx_registration_ptr err, unsigned target)
{
    XXContextTable far *table;
    unsigned context;
    unsigned outer;
    unsigned new_bp;
    unsigned new_ds;
    int dtor_adjustment = 0;

    new_ds = XX_RUNTIME->saved_ds = err->saved_ds;
    XX_RUNTIME->saved_si = err->saved_si;
    table = err->table;
    new_bp = (unsigned)err - table->bp_offset;

    for(context = err->context; context && context != target; context = outer) {
        XXBlockKind kind;
        unsigned at = context;
        xx_exception_ptr exception;
        xx_exception_ptr far *link;
        static xx_code_ptr finally_body;
        int minimum;
        XXDtorTable far *destructors;

        outer = *(unsigned far *)((char far *)table + at);
        at += sizeof(unsigned);
        kind = (XXBlockKind)*(unsigned far *)((char far *)table + at);
        at += sizeof(unsigned);
        err->context = outer;

        switch(kind) {
        case XB_TRYCPP:
        case XB_EXCEXP:
        case XB_EXCCNS:
            break;
        case XB_FINALLY:
            finally_body = *(xx_code_ptr far *)((char far *)table + at + sizeof(xx_code_ptr));
            err->unwinding = 1;
            // ES retains our DGROUP while the callback executes in its saved
            // DS and BP. Locals still use SS after DS changes.
            asm {
                push ds
                pop es
                push ds
                mov ds, new_ds
                push bp
                mov bp, new_bp
                call dword ptr es:[offset DGROUP:finally_body]
                pop bp
                pop ds
            }
            err->unwinding = 0;
            break;
        case XB_CATCH:
            at += sizeof(void far *);
            for(link = &XX_RUNTIME->exceptions; (exception = *link) != 0;
                link = &exception->previous) {
                if(exception->registration == err && exception->context == context)
                    break;
            }
            // The original assumes the matching descriptor exists.
            *link = exception->previous;
            exceptionHandled(exception);
            asm {
                push ds
                les bx, exception
                mov ds, es:[bx+XX_FREE_DS]
            }
            exception->free(exception);
            asm pop ds;
            break;
        case XB_DEST:
            minimum = *(unsigned far *)((char far *)table + at);
            at += sizeof(unsigned);
            destructors = *(XXDtorTable near * far *)((char far *)table + at);
            destructors = (XXDtorTable far *)MK_FP(FP_SEG(table),FP_OFF(destructors));
            dtor_adjustment = dtorCleanup(destructors,minimum+dtor_adjustment,err,new_bp);
            break;
        default:
            break;
        }
    }
}

extern "C" void far __cdecl _Local_unwind(unsigned target)
{
    xx_registration_ptr err = XX_CHAIN;
    local_unwind(err,target);
}

extern "C" void far __cdecl _Return_unwind()
{
    xx_registration_ptr err = XX_CHAIN;
    local_unwind(err,0);
    XX_CHAIN = err->next;
}

static XXHandler far *near findMatchingHandler(XXHandlerTable far *table,
    xx_exception_ptr exception)
{
    XXHandler far *handler;
    xx_type_ptr type;

    for(handler = table->entries; handler->body; ++handler) {
        type = handler->type;
        if(!type || typeIDcaught(exception->type,exception->friends,type,exception->flags,0))
            return handler;
    }
    return 0;
}

// This semantic ABI tag precedes the entry so the unwinder can recognize the
// compiler's handler. It is data, not an instruction encoding or alignment fill.
#pragma codestring "**BCCxh1"
extern "C" int far __cdecl _ExceptionHandler(void far *exception_pointer,
    void __ss *registration_pointer,void far *context_pointer,void far *)
{
    XXExceptionRecord __ss *record = (XXExceptionRecord __ss *)exception_pointer;
    xx_registration_ptr err = (xx_registration_ptr)registration_pointer;
    void far *saved_context = context_pointer;
    xx_exception_ptr exception = (xx_exception_ptr)record->information[2];
    XXContextTable far *table;
    unsigned context;
    unsigned outer;
    unsigned new_bp;
    unsigned new_sp;
    unsigned new_ds;
    unsigned new_si;

    table = err->table;
    new_bp = (unsigned)err - table->bp_offset;
    new_sp = err->saved_sp;
    new_ds = XX_RUNTIME->saved_ds = err->saved_ds;
    new_si = XX_RUNTIME->saved_si = err->saved_si;

    if(record->flags & 6) {
        local_unwind(err,0);
        if(record->code == 0x0EEFFACEUL) {
            xx_type_ptr far *allowed = table->throw_list;
            if(allowed) {
                while(*allowed) {
                    if(typeIDcaught(exception->type,exception->friends,*allowed,
                        exception->flags,1))
                        goto throw_allowed;
                    ++allowed;
                }
                xx_registration_ptr saved_chain = XX_CHAIN;
                XX_CHAIN = err->next;
                __call_unexpected();
                XX_CHAIN = saved_chain;
            }
        }
throw_allowed:
        return 1;
    }

    for(context = err->context; context; context = outer) {
        XXBlockKind kind;
        unsigned at = context;
        XXHandler far *handler;
        XXHandlerTable far *handlers;
        xx_code_ptr body;
        unsigned new_context;
        unsigned unwind_target;
        XXExceptionPointers pointers;
        static xx_code_ptr filter_expression;
        int filter;

        outer = *(unsigned far *)((char far *)table + at);
        at += sizeof(unsigned);
        kind = (XXBlockKind)*(unsigned far *)((char far *)table + at);
        at += sizeof(unsigned);

        switch(kind) {
        case XB_TRYCPP:
            if(record->code != 0x0EEFFACEUL)
                break;
            handlers = *(XXHandlerTable far * far *)((char far *)table + at);
            at += sizeof(XXHandlerTable far *);
            handler = findMatchingHandler(handlers,exception);
            if(!handler)
                break;
            exception->registration = err;
            exception->handler = handler;
            exception->context = at;
            unwind_target = context;
            new_context = at;
            body = handler->body;

jump_to_handler:
            _Global_unwind(err,record);
            local_unwind(err,unwind_target);
            err->context = new_context;
            if(kind == XB_TRYCPP)
                initCatchArg(handler,err,exception,handlers,new_bp);
            _DX = FP_SEG(body);
            _AX = FP_OFF(body);
            _SI = new_si;
            _DS = new_ds;
            _BX = new_sp;
            _CX = new_bp;
            __JumpToCatch__();
            break;

        case XB_EXCEXP:
            if(record->code == 0x0EEFFACEUL)
                break;
            pointers.exception = record;
            pointers.context = saved_context;
            err->exception_code = record->code;
            err->exception_info = &pointers;
            filter_expression = *(xx_code_ptr far *)((char far *)table + at);
            asm {
                mov ax, ds
                mov es, ax
                push si
                mov si, new_si
                push ds
                mov ds, new_ds
                push bp
                mov bp, new_bp
                call dword ptr es:[offset DGROUP:filter_expression]
                pop bp
                pop ds
                pop si
            }
            filter = _AX;
            goto got_filter;

        case XB_EXCCNS:
            if(record->code == 0x0EEFFACEUL)
                break;
            err->exception_code = record->code;
            filter = *(int far *)((char far *)table + at);
got_filter:
            if(filter < 0) {
                if(record->flags & 1)
                    err->context = outer;
                return 0;
            }
            if(filter == 0)
                break;
            err->exception_info = 0;
            at += sizeof(xx_code_ptr);
            unwind_target = new_context = outer;
            body = *(xx_code_ptr far *)((char far *)table + at);
            goto jump_to_handler;

        case XB_FINALLY:
        case XB_CATCH:
        case XB_DEST:
            break;
        default:
            break;
        }
    }
    return 1;
}
