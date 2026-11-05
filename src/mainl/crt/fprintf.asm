; Complete original Borland Japanese CRT fprintf ABI and control flow.
.8086
extrn __FPUTN:near
extrn __VPRINTER:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fprintf
_fprintf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,offset __FPUTN
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    lea ax,[bp+14]
    push ax
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_fprintf endp
_TEXT ends
end
