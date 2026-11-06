; Original Japanese Borland pureerr: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
extrn _exit:far
extrn ___ErrorMessage:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
pure_near_message db 'Pure virtual function called',0
pure_far_message db 'Pure virtual function called',0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __npure_error_
public __fpure_error_
; Original statement chunks preserve native relocation chronology.

org 56
    call _exit
    add sp, 6
    pop ds
    pop di
    pop si
    retf

org 47
    call ___ErrorMessage
    mov ax, 1
    push ax

org 43
    mov ax,offset DGROUP:pure_far_message
    push ax

org 37
    mov ax,seg DGROUP:pure_near_message
    mov ds, ax
    push ds

org 22
    call _exit
    add sp, 6
    pop ds
    pop di
    pop si
    ret
__fpure_error_ label far
    push si
    push di
    push ds

org 13
    call ___ErrorMessage
    mov ax, 1
    push ax

org 9
    mov ax,offset DGROUP:pure_near_message
    push ax

org 3
    mov ax,seg DGROUP:pure_near_message
    mov ds, ax
    push ds

org 0
__npure_error_ label near
    push si
    push di
    push ds
_TEXT ends
end
