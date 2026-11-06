; Original Japanese Borland assert: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
include stdio_layout.inc
extrn __streams:byte
extrn _fprintf:far
extrn _abort:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___assertfail
; Original statement chunks preserve native relocation chronology.

org 39
    call _abort
    pop di
    pop si
    pop bp
    retf

org 31
    call _fprintf
    add sp, 012h

org 27
    mov ax,offset DGROUP:__streams+2*FILE_BYTES
    push ax

org 0
___assertfail label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ds
_TEXT ends
end
