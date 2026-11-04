; Original DOS date/time writes use AH=2Bh/2Dh and far caller structure.
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
public _setdate,_settime
_setdate proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2Bh
    les si,dword ptr [bp+6]
    mov cx,word ptr es:[si]
    mov dx,word ptr es:[si+2]
    int 21h
    pop di
    pop si
    pop bp
    retf
_setdate endp
_settime proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2Dh
    les si,dword ptr [bp+6]
    mov cx,word ptr es:[si]
    mov dx,word ptr es:[si+2]
    int 21h
    pop di
    pop si
    pop bp
    retf
_settime endp
_TEXT ends
end
