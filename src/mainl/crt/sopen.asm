; Original Japanese Borland sopen: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn _open:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _sopen
; Complete disjoint instruction chunks preserve original native field order.

org 51
    call _open
    add sp, 6
shared_open_return:
    pop di
    pop si
    pop bp
    retf

org 30
    call _open
    add sp, 8
    jmp short shared_open_return
open_without_create_mode:
    mov ax, dx
    or ax, bx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
_sopen label far
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp+0ah]
    mov bx, word ptr [bp+0ch]
    test dh, 1
    je short open_without_create_mode
    push word ptr [bp+0eh]
    mov ax, dx
    or ax, bx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
