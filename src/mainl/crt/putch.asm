; Original Borland DOS console output, near counted CPUTN callback.
.8086
extrn __CPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _putch
_putch proc far
    push bp
    mov bp,sp
    push si
    push di
    push ss
    lea ax,[bp+6]
    push ax
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    call __CPUTN
    pop di
    pop si
    pop bp
    retf
_putch endp
_TEXT ends
end
