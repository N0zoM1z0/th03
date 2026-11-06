; Original DOS file descriptor mode switch, preserving Borland's
; __nfile bounds, __openfd text/binary bits and near __IOERROR ABI.
.8086
extrn __nfile:word
extrn __IOERROR:near
extrn __openfd:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setmode
_setmode proc far
    push bp
    mov bp,sp
    push si
    push di
    mov cx,[bp+8]
    mov ax,[bp+6]
    cmp ax,word ptr DGROUP:__nfile
    jb short mode_check
    mov ax,6
    jmp short mode_error
mode_check:
    mov dx,cx
    and dx,0c000h
    mov ax,dx
    cmp ax,cx
    jne short mode_invalid
    cmp dx,0c000h
    je short mode_invalid
    mov bx,[bp+6]
    add bx,bx
    mov cx,word ptr DGROUP:__openfd[bx]
    mov bx,[bp+6]
    add bx,bx
    mov ax,cx
    and ax,3fffh
    or ax,dx
    mov word ptr DGROUP:__openfd[bx],ax
    mov ax,cx
    and ax,0c000h
    jmp short mode_done
mode_invalid:
    mov ax,1
mode_error:
    push ax
    call __IOERROR
mode_done:
    pop di
    pop si
    pop bp
    retf
_setmode endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
