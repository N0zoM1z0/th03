#ifndef TH03_MAINL_XX_DISPATCH_ABI_H
#define TH03_MAINL_XX_DISPATCH_ABI_H

#include <dos.h>
#include <stddef.h>

// The recovered DOS runtime uses SS-relative registration pointers, DWORD
// destructor counts, and far descriptors. These are prefixes used by this bank;
// they do not describe the later Win32 runtime or claim ownership of its storage.
#pragma option -a-

struct XXType;
struct XXDtorTable;
struct XXRegistration;
struct XXException;
struct XXHandler;
typedef XXRegistration __ss *xx_registration_ptr;
typedef XXException far *xx_exception_ptr;
typedef XXType far *xx_type_ptr;
typedef void (far __cdecl *xx_code_ptr)();
typedef void (far __cdecl *xx_free_ptr)(xx_exception_ptr);

struct XXContextTable {
    xx_type_ptr far *throw_list;
    unsigned bp_offset;
};

struct XXRegistration {
    xx_registration_ptr next;
    xx_code_ptr catcher;
    XXContextTable far *table;
    unsigned saved_sp;
    unsigned context;
    unsigned saved_ds;
    unsigned saved_si;
    unsigned unwinding;
    unsigned long exception_code;
    void __ss *exception_info;
    unsigned long initial_dtor_count;
    unsigned char flags;
};

struct XXHandler {
    xx_code_ptr body;
    xx_type_ptr type;
    unsigned flags;
    void far *copy_constructor;
    unsigned copy_mask;
};

struct XXHandlerTable {
    unsigned argument_offset;
    unsigned argument_size;
    XXHandler entries[1];
};

struct XXException {
    xx_exception_ptr previous;
    xx_type_ptr type;
    xx_type_ptr far *friends;
    unsigned flags;
    unsigned size;
    xx_type_ptr base;
    unsigned mask;
    unsigned class_flags;
    unsigned free_ds;
    xx_free_ptr free;
    void far *copy_constructor;
    unsigned copy_mask;
    xx_registration_ptr registration;
    XXHandler far *handler;
    unsigned context;
    unsigned throw_line;
    unsigned char far *throw_file;
    xx_type_ptr argument_type;
    void __ss *argument_address;
    unsigned char argument_buffer;
    unsigned char argument_copy;
};

struct XXRuntimePrefix {
    xx_exception_ptr exceptions;
    unsigned flags;
    unsigned saved_ds;
    unsigned saved_si;
};

struct XXExceptionRecord {
    unsigned long code;
    unsigned long flags;
    void __ss *nested;
    xx_code_ptr address;
    unsigned count;
    unsigned long information[15];
};

struct XXExceptionPointers {
    XXExceptionRecord __ss *exception;
    void far *context;
};

#pragma option -a.

// Native __InitExceptBlocks and the dispatcher agree on these exact offsets.
typedef char xx_registration_prefix_bytes[(sizeof(XXRegistration)==31) ? 1 : -1];
typedef char xx_registration_table[(offsetof(XXRegistration,table)==6) ? 1 : -1];
typedef char xx_registration_saved_ds[(offsetof(XXRegistration,saved_ds)==14) ? 1 : -1];
typedef char xx_registration_dtc[(offsetof(XXRegistration,initial_dtor_count)==26) ? 1 : -1];
typedef char xx_descriptor_registration[(offsetof(XXException,registration)==36) ? 1 : -1];
typedef char xx_descriptor_payload[(sizeof(XXException)==58) ? 1 : -1];
typedef char xx_handler_size[(sizeof(XXHandler)==16) ? 1 : -1];
typedef char xx_exception_arguments[(offsetof(XXExceptionRecord,information)==16) ? 1 : -1];

enum { XX_FREE_DS = offsetof(XXException,free_ds) };

#define XX_CHAIN (*(xx_registration_ptr __ss *)0x14)
#define XX_RUNTIME (*(XXRuntimePrefix far * __ss *)0x16)

// Private interfaces belong to the surrounding xx TU. Their bodies remain
// outside this recovered bank; declaring them does not provide replacements.
int near typeIDcaught(xx_type_ptr,xx_type_ptr far *,xx_type_ptr,unsigned,int);
int near dtorCleanup(XXDtorTable far *,long,xx_registration_ptr,unsigned);
void near exceptionHandled(xx_exception_ptr);
void near initCatchArg(XXHandler far *,xx_registration_ptr,xx_exception_ptr,
    XXHandlerTable far *,unsigned);
extern "C" void far __cdecl __call_unexpected();
extern "C" void far __cdecl _Global_unwind(xx_registration_ptr,XXExceptionRecord __ss *);
extern "C" void far __cdecl __JumpToCatch__();

#endif
