; Borland DOS file rename, two far paths via DS:DX and ES:DI.
.8086
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _rename
_rename proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,56h
    lds dx,dword ptr [bp+6]
    les di,dword ptr [bp+0Ah]
    int 21h
    pop ds
    jb short failed
    xor ax,ax
    jmp short done
failed:
    push ax
    call __IOERROR
done:
    pop di
    pop si
    pop bp
    retf
_rename endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
