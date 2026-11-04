; Original Borland DOS interrupt-vector get/set far APIs.
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
public __dos_getvect,__dos_setvect
__dos_getvect proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,35h
    mov al,byte ptr [bp+6]
    int 21h
    xchg bx,ax
    mov dx,es
    pop di
    pop si
    pop bp
    retf
__dos_getvect endp
__dos_setvect proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,25h
    mov al,byte ptr [bp+6]
    push ds
    lds dx,dword ptr [bp+8]
    int 21h
    pop ds
    pop di
    pop si
    pop bp
    retf
__dos_setvect endp
_TEXT ends
end
