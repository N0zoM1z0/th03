; Borland DOS file removal through AH=41h, with near runtime IOERROR.
.8086
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _remove
_remove proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,41h
    lds dx,dword ptr [bp+6]
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
_remove endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
