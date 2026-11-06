; Preserve the original descriptor-state clear before the low-level close result.
; Original Japanese Borland close: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include crt_errno.inc
extrn __nfile:word
extrn __rtl_close:far
extrn __IOERROR:near
extrn __openfd:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _close
; Complete disjoint instruction chunks preserve original native field order.

org 34
    call __rtl_close
    pop cx
close_return:
    pop di
    pop si
    pop bp
    retf

org 27
    mov word ptr DGROUP:__openfd[bx], 0
    push dx

org 18
    call __IOERROR
    jmp short close_return
clear_descriptor_state:
    mov bx, dx
    add bx, bx

org 8
    cmp dx, word ptr DGROUP:__nfile
    jb short clear_descriptor_state
    mov ax, EBADF
    push ax

org 0
_close label far
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp+6]
_TEXT ends
end
