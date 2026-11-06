; Original Japanese Borland fdopen: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include stdio_layout.inc
extrn __OPENFP:near
extrn __GETFP:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fdopen
; Complete disjoint instruction chunks preserve original native field order.

org 58
    call __OPENFP
fdopen_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 14
    call __GETFP
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short bind_descriptor
fdopen_no_stream:
    xor dx, dx
    xor ax, ax
    jmp short fdopen_return
bind_descriptor:
    les bx, dword ptr [bp-4]
    mov al, byte ptr [bp+6]
    mov byte ptr es:[bx+FILE_FD], al
    push word ptr [bp-2]
    push bx
    xor ax, ax
    push ax
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax

org 0
_fdopen label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    cmp word ptr [bp+6], 0
    jl short fdopen_no_stream
_TEXT ends
end
