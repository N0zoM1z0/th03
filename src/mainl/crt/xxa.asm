; Original Japanese Borland xxa: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
SS_DESTRUCTOR_COUNT equ 10h
SS_EXCEPTION_LIST equ 14h
; SEG DGROUP supplies saved DS in the registration frame at +0Eh.
extrn __ExceptionHandler:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___InitExceptBlock
; Original statement chunks preserve native relocation chronology.

org 0
___InitExceptBlock label far
    mov es, ax
    mov dx, bx
    mov cx, bp
    mov bx, word ptr es:[bx+4]
    add bx, cx
    mov word ptr ss:[bx+6], dx
    mov word ptr ss:[bx+8], ax
    mov ax, sp
    add ax, 4
    mov word ptr ss:[bx+0ah], ax

org 29
    mov ax,seg DGROUP
    mov word ptr ss:[bx+0eh], ax
    mov word ptr ss:[bx+010h], si

org 40
    mov word ptr ss:[bx+2],offset __ExceptionHandler

org 46
    mov word ptr ss:[bx+4],seg __ExceptionHandler
    mov word ptr ss:[bx+0ch], 0
    mov word ptr ss:[bx+012h], 0
    mov ax, word ptr ss:[SS_DESTRUCTOR_COUNT]
    mov word ptr ss:[bx+01ah], ax
    mov ax, word ptr ss:[SS_DESTRUCTOR_COUNT+2]
    mov word ptr ss:[bx+01ch], ax
    mov ax, word ptr ss:[SS_EXCEPTION_LIST]
    mov word ptr ss:[bx], ax
    mov word ptr ss:[SS_EXCEPTION_LIST], bx
    retf
_TEXT ends
end
