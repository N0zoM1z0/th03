; Original Borland DOS create/new-create with native near 21h core,
; full FAR pathname/result pointers and exact DOSERROR propagation.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
doscreat_core proc near
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,byte ptr [bp+4]
    mov cx,[bp+0ah]
    lds dx,dword ptr [bp+0ch]
    int 21h
    pop ds
    jb short doscreat_error
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],ax
    xor ax,ax
    jmp short doscreat_done
doscreat_error:
    push ax
    call __DOSERROR
doscreat_done:
    pop di
    pop si
    pop bp
    ret 0ch
doscreat_core endp

public __dos_creat,__dos_creatnew
__dos_creat proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    mov al,3ch
    push ax
    call doscreat_core
    pop di
    pop si
    pop bp
    retf
__dos_creat endp
__dos_creatnew proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    mov al,5bh
    push ax
    call doscreat_core
    pop di
    pop si
    pop bp
    retf
__dos_creatnew endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
