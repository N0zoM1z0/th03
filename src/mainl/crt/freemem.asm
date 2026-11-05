; Original Japanese Borland CRT freemem: native 16-bit DOS system call.
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
public _freemem
_freemem proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,49h
    mov es,[bp+6]
    int 21h
    jc short release_error
    xor ax,ax
    jmp short release_done
release_error:
    push ax
    call __IOERROR
release_done:
    pop di
    pop si
    pop bp
    retf
_freemem endp
_TEXT ends
end
