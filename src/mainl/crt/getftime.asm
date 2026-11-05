; Original Japanese Borland CRT getftime: native 16-bit DOS system call.
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
public _getftime
_getftime proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,5700h
    mov bx,[bp+6]
    int 21h
    jc short time_error
    les di,dword ptr [bp+8]
    mov word ptr es:[di],cx
    mov word ptr es:[di+2],dx
    xor ax,ax
    jmp short time_done
time_error:
    push ax
    call __IOERROR
time_done:
    pop di
    pop si
    pop bp
    retf
_getftime endp
_TEXT ends
end
