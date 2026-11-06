; Register one of 32 FAR termination callbacks, preserving original word count.
; Code first, initialized count next, uninitialized callback table last.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _atexit
_atexit label far
org 39
    inc word ptr DGROUP:__atexitcnt
    xor ax,ax
done:
    pop di
    pop si
    pop bp
    retf
org 35
    mov word ptr DGROUP:__atexittbl[bx],ax
org 31
    mov word ptr DGROUP:__atexittbl[bx+2],dx
org 17
register_handler:
    mov bx,word ptr DGROUP:__atexitcnt
    mov cl,2
    shl bx,cl
    mov dx,[bp+8]
    mov ax,[bp+6]
org 0
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr DGROUP:__atexitcnt,32
    jne register_handler
    mov ax,1
    jmp short done
_TEXT ends
_DATA segment word public 'DATA'
public __atexitcnt
__atexitcnt dw 0
_DATA ends
_BSS segment word public 'BSS'
public __atexittbl
__atexittbl dd 32 dup (?)
_BSS ends
end
