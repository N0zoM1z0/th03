; Original DOS far-cdecl chdir with native AH=3Bh and DS:DX far path.
; Restore caller DS and report carry failures through the near __IOERROR.
.8086
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _chdir
_chdir proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,3Bh
    lds dx,dword ptr [bp+6]
    int 21h
    pop ds
    jb short dos_error
    xor ax,ax
    jmp short chdir_return
dos_error:
    push ax
    call __IOERROR
chdir_return:
    pop di
    pop si
    pop bp
    retf
_chdir endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
