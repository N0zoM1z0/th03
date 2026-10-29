; Raw DOS write plus the public un-translated wrapper. IOERROR consumes its WORD.
.8086
include stdio_layout.inc
extrn __IOERROR:near,__openfd:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __rtl_write,__write
__rtl_write proc far
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx],1
    je dos_write
    mov ax,5
    push ax
    jmp short translate_error
 dos_write:
    push ds
    mov ah,40h
    mov bx,[bp+6]
    mov cx,[bp+12]
    lds dx,[bp+8]
    int 21h
    pop ds
    jc dos_error
    push ax
    mov bx,[bp+6]
    add bx,bx
    or word ptr DGROUP:__openfd[bx],O_CHANGED
    pop ax
    jmp short raw_write_done
 dos_error:
    push ax
 translate_error:
    call __IOERROR
 raw_write_done:
    pop di
    pop si
    pop bp
    retf
__rtl_write endp
__write proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr __rtl_write
    add sp,8
    pop di
    pop si
    pop bp
    retf
__write endp
_TEXT ends
end
