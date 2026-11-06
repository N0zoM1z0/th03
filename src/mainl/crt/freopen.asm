; Original Japanese Borland freopen: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include stdio_layout.inc
extrn _fclose:far
extrn __OPENFP:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _freopen
; Complete disjoint instruction chunks preserve original native field order.

org 57
    call __OPENFP
freopen_return:
    pop di
    pop si
    pop bp
    retf

org 29
    call _fclose
    pop cx
    pop cx
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    xor ax, ax
    push ax

org 0
_freopen label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+0eh]
    mov ax, word ptr es:[bx+FILE_TOKEN]
    cmp ax, word ptr [bp+0eh]
    je short reopen_valid_stream
    xor dx, dx
    xor ax, ax
    jmp short freopen_return
reopen_valid_stream:
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
end
