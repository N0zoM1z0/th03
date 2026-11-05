; Original Japanese Borland CRT ioctl: native 16-bit DOS system call.
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
public _ioctl
_ioctl proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds dx,dword ptr [bp+10]
    mov ah,44h
    mov al,[bp+8]
    mov bx,[bp+6]
    mov cx,[bp+14]
    int 21h
    pop ds
    jc short ioctl_error
    cmp word ptr [bp+8],0
    jnz short ioctl_no_dx
    mov ax,dx
    jmp short ioctl_done
ioctl_no_dx:
    jmp short ioctl_done
ioctl_error:
    push ax
    call __IOERROR
ioctl_done:
    pop di
    pop si
    pop bp
    retf
_ioctl endp
_TEXT ends
end
