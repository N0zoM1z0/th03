; Original 16-bit DOS DUP/DUP2 FAR APIs. Keep native dos AH=45/46,
; __openfd entries and exact mutable __exitopen FAR close callback.
.8086
extrn __IOERROR:near
extrn __openfd:byte
extrn __exitopen:dword
extrn __xclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _dup2,_dup

_dup2 proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,46h
    mov bx,[bp+6]
    mov cx,[bp+8]
    int 21h
    jb short dup2_error
    mov bx,[bp+6]
    add bx,bx
    mov ax,word ptr DGROUP:__openfd[bx]
    mov bx,[bp+8]
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],ax
    mov word ptr DGROUP:__exitopen+2,seg __xclose
    mov word ptr DGROUP:__exitopen,offset __xclose
    xor ax,ax
    jmp short dup2_done
dup2_error:
    push ax
    call __IOERROR
dup2_done:
    pop di
    pop si
    pop bp
    retf
_dup2 endp

_dup proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,45h
    mov bx,[bp+6]
    int 21h
    jb short dup_error
    mov dx,ax
    mov bx,[bp+6]
    add bx,bx
    mov ax,word ptr DGROUP:__openfd[bx]
    mov bx,dx
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],ax
    mov word ptr DGROUP:__exitopen+2,seg __xclose
    mov word ptr DGROUP:__exitopen,offset __xclose
    mov ax,dx
    jmp short dup_done
dup_error:
    push ax
    call __IOERROR
dup_done:
    pop di
    pop si
    pop bp
    retf
_dup endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
