; Original Japanese Borland CRT allocmem: native 16-bit DOS system call.
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
public _allocmem
_allocmem proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,48h
    mov bx,[bp+6]
    int 21h
    jc short alloc_error
    les di,dword ptr [bp+8]
    mov word ptr es:[di],ax
    mov ax,0ffffh
    jmp short alloc_done
alloc_error:
    push bx
    push ax
    call __IOERROR
    pop ax
alloc_done:
    pop di
    pop si
    pop bp
    retf
_allocmem endp
_TEXT ends
end
