; Proved original stream wrapper family; each TU retains its own native owner.
STREAM_SEEK_OFFSET macro api_name,seek_mode
; Native source chunks retain original logical FIXUPP chronology.

org 88
    call @ios@setstate$qi
    add sp, 6
seek_return:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 0
api_name label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+0ah], 084h
    jne short seek_failed
    mov ax, seek_mode
    push ax
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp-2], es
    mov word ptr [bp-4], bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx, dword ptr es:[bx+2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx+01ch]
    add sp, 0ch
    cmp dx, -1
    jne short seek_return
    cmp ax, 0ffffh
    jne short seek_return
seek_failed:
    mov ax, 2
    push ax
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]
endm
