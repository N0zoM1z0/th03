; Original Japanese Borland CRT getcurdi: native 16-bit DOS system call.
; Keep real register/flag semantics and near/far error ABI.
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
public _getcurdir
_getcurdir proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,47h
    mov dl,[bp+6]
    lds si,dword ptr [bp+8]
    int 21h
    pop ds
    jc short dir_error
    xor ax,ax
    jmp short dir_done
dir_error:
    push ax
    call __IOERROR
dir_done:
    pop di
    pop si
    pop bp
    retf
_getcurdir endp
_TEXT ends
end
