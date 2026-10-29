; Return DOS IOCTL device bit80h verbatim; the original does not check carry.
.8086
include stdio_layout.inc
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _isatty
_isatty proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,4400h
    mov bx,[bp+6]
    int 21h
    xchg dx,ax
    and ax,80h
    pop di
    pop si
    pop bp
    retf
_isatty endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
