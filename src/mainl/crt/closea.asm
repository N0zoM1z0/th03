; The __close wrapper uses push CS plus a near call to the FAR __rtl_close entry.
; Original Japanese Borland closea: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __IOERROR:near
extrn __openfd:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __rtl_close
public __close
; Complete disjoint instruction chunks preserve original native field order.

org 16
    mov word ptr DGROUP:__openfd[bx], 0
    xor ax, ax
    jmp short rtl_close_return
translate_close_error:
    push ax

org 27
    call __IOERROR
rtl_close_return:
    pop di
    pop si
    pop bp
    retf
__close label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+6]
    push cs
    call near ptr __rtl_close
    pop cx
    pop di
    pop si
    pop bp
    retf

org 0
__rtl_close label far
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 03eh
    mov bx, word ptr [bp+6]
    int 021h
    jb short translate_close_error
    add bx, bx
_TEXT ends
end
