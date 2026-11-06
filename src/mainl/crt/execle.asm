; Original Japanese Borland execle: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
extrn __exec:near
extrn __LoadProg:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _execle
; Original statement chunks preserve native relocation chronology.

org 61
    call __LoadProg
    add sp, 010h
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 57
    mov ax,offset __exec
    push ax

org 0
_execle label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    lea ax, [bp+0ah]
    mov word ptr [bp-2], ss
    mov word ptr [bp-4], ax
scan_argument_end:
    les bx, dword ptr [bp-4]
    add word ptr [bp-4], 4
    mov ax, word ptr es:[bx]
    or ax, word ptr es:[bx+2]
    jne short scan_argument_end
    xor ax, ax
    push ax
    les bx, dword ptr [bp-4]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push ss
    lea ax, [bp+0ah]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
