; Original DOS date/time reads return CX:DX into a far caller structure.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getdate,_gettime
_getdate proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2Ah
    int 21h
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],cx
    mov word ptr es:[bx+2],dx
    pop di
    pop si
    pop bp
    retf
_getdate endp
_gettime proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2Ch
    int 21h
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],cx
    mov word ptr es:[bx+2],dx
    pop di
    pop si
    pop bp
    retf
_gettime endp
_TEXT ends
end
