; Original Japanese Borland CRT chmoda: native 16-bit DOS system call.
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
public __rtl_chmod
__rtl_chmod proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov cx,[bp+12]
    mov ah,43h
    mov al,[bp+10]
    lds dx,dword ptr [bp+6]
    int 21h
    pop ds
    jc short chmod_error
    xchg ax,cx
    jmp short chmod_done
chmod_error:
    push ax
    call __IOERROR
chmod_done:
    pop di
    pop si
    pop bp
    retf
__rtl_chmod endp
_TEXT ends
end
