; Original Japanese Borland CRT fstrset; natural 16-bit source.
.8086
extrn __fsetmem:far,__fstrlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fstrset
__fstrset proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fstrlen
    pop cx
    pop cx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fsetmem
    add sp,8
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
__fstrset endp
_TEXT ends
end
