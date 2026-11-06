; Original Japanese Borland errormsg: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
include stdio_layout.inc
extrn __rtl_write:far
extrn __streams:byte
extrn _strlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___ErrorMessage
; Original statement chunks preserve native relocation chronology.

org 30
    call __rtl_write
    add sp, 8
    pop di
    pop si
    pop bp
    retf

org 25
    mov al, byte ptr DGROUP:__streams[2*FILE_BYTES+FILE_FD]
    cbw
    push ax

org 11
    call _strlen
    pop cx
    pop cx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
___ErrorMessage label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
