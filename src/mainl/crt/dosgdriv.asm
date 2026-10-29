; One-based drive APIs around DOS zero-based drive services.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_getdrive,__dos_setdrive
__dos_getdrive proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,19h
    int 21h
    mov ah,0
    inc ax
    les bx,[bp+6]
    mov es:[bx],ax
    pop di
    pop si
    pop bp
    retf
__dos_getdrive endp
__dos_setdrive proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dl,[bp+6]
    dec dl
    mov ah,0eh
    int 21h
    mov ah,0
    les bx,[bp+8]
    mov es:[bx],ax
    pop di
    pop si
    pop bp
    retf
__dos_setdrive endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
