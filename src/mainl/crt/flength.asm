; Original DOS filelength preserves and restores the file seek position.
.8086
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _filelength
_filelength proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,4201h
    mov bx,[bp+6]
    xor cx,cx
    xor dx,dx
    int 21h
    jc short seek_error
    push dx
    push ax
    mov ax,4202h
    xor cx,cx
    xor dx,dx
    int 21h
    mov [bp-4],ax
    mov [bp-2],dx
    pop dx
    pop cx
    jc short seek_error
    mov ax,4200h
    int 21h
    jc short seek_error
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short return_length
seek_error:
    push ax
    call __IOERROR
    cwd
return_length:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_filelength endp
_TEXT ends
end
