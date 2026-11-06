; Original Japanese Borland brk: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __brk:near
extrn __sbrk:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _brk
public _sbrk
; Complete disjoint instruction chunks preserve original native field order.

org 11
    call __brk
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_sbrk label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    cwd
    push dx
    push ax

org 31
    call __sbrk
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

org 0
_brk label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
