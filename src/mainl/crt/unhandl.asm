; Original Japanese Borland unhandl: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
extrn ___ErrorMessage:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
unhandled_filter dd 0
unhandled_message db 'Unhandled exception encountered',0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public SETUNHANDLEDEXCEPTIONFILTER
public UNHANDLEDEXCEPTIONFILTER
; Original statement chunks preserve native relocation chronology.

org 102
    call ___ErrorMessage
    pop cx
    pop cx
    xor dx, dx
    mov ax, 1
unhandled_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf 2

org 91
    mov word ptr [bp-4],offset DGROUP:unhandled_message
    push word ptr [bp-2]
    push word ptr [bp-4]

org 68
    call dword ptr DGROUP:unhandled_filter
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, word ptr [bp-2]
    je short unhandled_default
    mov ax, word ptr [bp-4]
    jmp short unhandled_return
unhandled_default:
    mov word ptr [bp-2], ds

org 59
    or ax, word ptr DGROUP:unhandled_filter+2
    je short unhandled_default
    push word ptr [bp+6]

org 56
    mov ax, word ptr DGROUP:unhandled_filter

org 31
    mov word ptr DGROUP:unhandled_filter, ax
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf 4
UNHANDLEDEXCEPTIONFILTER label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di

org 27
    mov word ptr DGROUP:unhandled_filter+2, dx

org 12
    mov ax, word ptr DGROUP:unhandled_filter
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]

org 8
    mov dx, word ptr DGROUP:unhandled_filter+2

org 0
SETUNHANDLEDEXCEPTIONFILTER label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
_TEXT ends
end
