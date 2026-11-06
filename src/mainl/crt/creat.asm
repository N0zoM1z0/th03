; Original Borland DOS creat with private near AH=3Ch bridge, umask,
; installable __exitopen FAR close callback and original FILE descriptor.
.8086
extrn _ioctl:far
extrn __IOERROR:near
extrn __openfd:byte
extrn __fmode:word
extrn __exitopen:dword
extrn __xclose:far
extrn __notUmask:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

creat_dos_private proc near
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds dx,dword ptr [bp+6]
    mov ah,3ch
    mov cx,[bp+4]
    int 21h
    pop ds
    jb short create_error
    jmp short create_return
create_error:
    push ax
    call __IOERROR
create_return:
    pop di
    pop si
    pop bp
    ret 6
creat_dos_private endp

public _creat
_creat proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,word ptr DGROUP:__notUmask
    and word ptr [bp+0ah],ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    test byte ptr [bp+0ah],80h
    je short creat_not_binary
    xor ax,ax
    jmp short creat_have_mode
creat_not_binary:
    mov ax,1
creat_have_mode:
    push ax
    call near ptr creat_dos_private
    mov [bp-2],ax
    cmp word ptr [bp-2],0
    jl short creat_return
    mov word ptr DGROUP:__exitopen+2,seg __xclose
    mov word ptr DGROUP:__exitopen,offset __xclose
    xor ax,ax
    push ax
    push word ptr [bp-2]
    call _ioctl
    pop cx
    pop cx
    test al,80h
    je short creat_flags_not_binary
    mov ax,2000h
    jmp short creat_have_file_flags
creat_flags_not_binary:
    xor ax,ax
creat_have_file_flags:
    or ax,word ptr DGROUP:__fmode
    push ax
    test byte ptr [bp+0ah],80h
    je short creat_flags_normal
    mov ax,100h
    jmp short creat_have_text_flags
creat_flags_normal:
    xor ax,ax
creat_have_text_flags:
    pop dx
    or dx,ax
    or dx,1004h
    mov bx,[bp-2]
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],dx
creat_return:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_creat endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
