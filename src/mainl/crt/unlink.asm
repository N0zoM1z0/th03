; Original far DOS unlink, not a modern libc remove() alias object.
; Keep its distinct CRT member/public, actual AH=41h and near error ABI.
.8086
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _unlink
_unlink proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,41h
    lds dx,dword ptr [bp+6]
    int 21h
    pop ds
    jb short dos_error
    xor ax,ax
    jmp short unlink_return
dos_error:
    push ax
    call __IOERROR
unlink_return:
    pop di
    pop si
    pop bp
    retf
_unlink endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
