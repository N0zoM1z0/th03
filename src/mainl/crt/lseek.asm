; DOS seek clears the handle EOF bit before invoking DOS, including on failure.
.8086
include stdio_layout.inc
extrn __IOERROR:near,__openfd:word
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _lseek
_lseek proc far
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    add bx,bx
    and word ptr DGROUP:__openfd[bx],not O_EOF
    mov ah,42h
    mov al,[bp+12]
    mov bx,[bp+6]
    mov cx,[bp+10]
    mov dx,[bp+8]
    int 21h
    jc seek_error
    jmp short seek_done
 seek_error:
    push ax
    call __IOERROR
    cwd
 seek_done:
    pop di
    pop si
    pop bp
    retf
_lseek endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
