; Original Japanese Borland execve: complete native runtime/process member.
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
public _execve
; Original statement chunks preserve native relocation chronology.

org 30
    call __LoadProg
    add sp, 010h
    pop di
    pop si
    pop bp
    retf

org 26
    mov ax,offset __exec
    push ax

org 0
_execve label far
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
