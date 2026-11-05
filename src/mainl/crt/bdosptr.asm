; Original Japanese Borland CRT bdosptr: native 16-bit DOS system call.
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
public _bdosptr
_bdosptr proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,[bp+6]
    mov al,[bp+12]
    lds dx,dword ptr [bp+8]
    clc
    int 21h
    pop ds
    jc short dos_error
    jmp short dos_done
dos_error:
    push ax
    call __IOERROR
dos_done:
    pop di
    pop si
    pop bp
    retf
_bdosptr endp
_TEXT ends
end
