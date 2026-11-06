; Original Japanese Borland setbuf: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn _setvbuf:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setbuf
; Complete disjoint instruction chunks preserve original native field order.

org 37
    call _setvbuf
    add sp, 0ch
    pop di
    pop si
    pop bp
    retf

org 0
_setbuf label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, 0200h
    push ax
    mov ax, word ptr [bp+0ah]
    or ax, word ptr [bp+0ch]
    je short select_unbuffered
    xor ax, ax
    jmp short pass_buffer_mode
select_unbuffered:
    mov ax, 2
pass_buffer_mode:
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
