; Original DOS create/temporary create/new create CRT family.
; Private __rtl_creat uses actual DOS INT 21h AH=3Ch/5Ah/5Bh,
; updates the real __openfd flags and calls near __IOERROR.
.8086
extrn __IOERROR:near
extrn __openfd:byte
extrn __fmode:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

public __rtl_creat,__creat,_creattemp,_creatnew
dos_create_core proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ds
    mov ah,byte ptr [bp+6]
    mov cx,[bp+8]
    lds dx,dword ptr [bp+0ah]
    int 21h
    pop ds
    jb short create_failed
    mov [bp-2],ax
    mov bx,[bp-2]
    add bx,bx
    mov ax,[bp+4]
    mov word ptr DGROUP:__openfd[bx],ax
    mov ax,[bp-2]
    jmp short return_create
create_failed:
    push ax
    call __IOERROR
return_create:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 0ah
dos_create_core endp

__rtl_creat proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    mov al,3ch
    push ax
    mov ax,8004h
    push ax
    call near ptr dos_create_core
    pop di
    pop si
    pop bp
    retf
__rtl_creat endp

__creat proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr __rtl_creat
    add sp,6
    pop di
    pop si
    pop bp
    retf
__creat endp

_creattemp proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    mov al,5ah
    push ax
    mov ax,word ptr DGROUP:__fmode
    or ax,4
    push ax
    call near ptr dos_create_core
    pop di
    pop si
    pop bp
    retf
_creattemp endp

_creatnew proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    mov al,5bh
    push ax
    mov ax,word ptr DGROUP:__fmode
    or ax,4
    push ax
    call near ptr dos_create_core
    pop di
    pop si
    pop bp
    retf
_creatnew endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
