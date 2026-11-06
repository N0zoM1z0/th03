; Original Japanese Borland _fsopen: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
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
public __fsopen
; Complete disjoint instruction chunks preserve original native field order.

org 48
    call __OPENFP
fsopen_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 8
    call __GETFP
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short open_allocated_stream
    xor dx, dx
    xor ax, ax
    jmp short fsopen_return
open_allocated_stream:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+0eh]

org 0
__fsopen label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
_TEXT ends
end
