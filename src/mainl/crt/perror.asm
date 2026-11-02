; Original DOS far-cdecl perror: print prefix and libc error message.
; Uses original _errno and __sys_nerr, far __sys_errlist pointer table,
; and genuine stdout/stderr __streams+40 far FILE for _fputs.
; Original initialized DATA strings are real user-visible messages.
; Original OMF fields are restored by original disjoint mnemonic blocks.
.8086
extrn __streams:word
extrn _fputs:far
extrn __sys_errlist:word
extrn __sys_nerr:word
extrn _errno:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
perror_unknown db 'Unknown error',0
perror_colon db ': ',0
perror_newline db 0Ah,0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _perror
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 083h
    call _fputs
    add sp, 010h
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 07Fh
    mov ax,offset DGROUP:perror_newline
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 07Ah
    mov ax,offset DGROUP:__streams+40
    push ax
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 074h
    call _fputs
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 06Ah
    mov ax,offset DGROUP:__streams+40
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 061h
    call _fputs
    add sp, 010h
perror_print_message:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 05Dh
    mov ax,offset DGROUP:perror_colon
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 058h
    mov ax,offset DGROUP:__streams+40
    push ax
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 052h
    call _fputs
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04Ah
    mov ax,offset DGROUP:__streams+40
    push ax
    push word ptr [bp+8]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 033h
    mov word ptr [bp-4],offset DGROUP:perror_unknown
perror_print_prefix:
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    je short perror_print_message
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx], 0
    je short perror_print_message
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 024h
    mov ax,word ptr DGROUP:[bx+__sys_errlist]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short perror_print_prefix
perror_unknown_error:
    mov word ptr [bp-2], ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 020h
    mov dx,word ptr DGROUP:[bx+__sys_errlist+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 018h
    mov bx,word ptr DGROUP:_errno
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 011h
    cmp word ptr DGROUP:_errno,0
    jl short perror_unknown_error
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0Bh
    cmp ax,word ptr DGROUP:__sys_nerr
    jge short perror_unknown_error
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 08h
    mov ax,word ptr DGROUP:_errno
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_perror label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
_TEXT ends
end
