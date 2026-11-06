; Reserve the caller value on SS, copy WORDs plus an odd byte, and retain return kind.
; Original Japanese Borland h_spush: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_SPUSH@
public F_SPUSH@
public SPUSH@
N_SPUSH@ label near
    pop bx
    sub sp, cx
    push cs
    jmp short copy_stack_argument
F_SPUSH@ label far
SPUSH@ label far
    pop bx
    pop es
    sub sp, cx
    push es
copy_stack_argument:
    push bx
    push di
    push ds
    mov di, sp
    add di, 8
    mov bx, ss
    mov es, bx
    mov ds, dx
    xchg si, ax
    cld
    shr cx, 1
    rep movsw
    adc cx, cx
    rep movsb
    xchg si, ax
    pop ds
    pop di
    retf
_TEXT ends
end
