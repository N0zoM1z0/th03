; Original DOS get/set file attributes through INT 21h AH=43h.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_getfileattr,__dos_setfileattr
__dos_getfileattr proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,43h
    xor al,al
    lds dx,dword ptr [bp+6]
    int 21h
    pop ds
    jc short get_attr_error
    les bx,dword ptr [bp+10]
    mov word ptr es:[bx],cx
    xor ax,ax
    jmp short get_attr_done
get_attr_error:
    push ax
    call __DOSERROR
get_attr_done:
    pop di
    pop si
    pop bp
    retf
__dos_getfileattr endp
__dos_setfileattr proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,43h
    mov al,1
    lds dx,dword ptr [bp+6]
    mov cx,[bp+10]
    int 21h
    pop ds
    jc short set_attr_error
    xor ax,ax
    jmp short set_attr_done
set_attr_error:
    push ax
    call __DOSERROR
set_attr_done:
    pop di
    pop si
    pop bp
    retf
__dos_setfileattr endp
_TEXT ends
end
