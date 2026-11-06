; Original segment:offset subtraction and signed DX:AX result; preserve DI.
; Original Japanese Borland h_psbp: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public PSBP@
public F_PSBP@
public N_PSBP@
N_PSBP@ label near
    pop es
    push cs
    push es
F_PSBP@ label far
PSBP@ label far
    push di
    mov di, cx
    mov ch, dh
    mov cl, 4
    shl dx, cl
    shr ch, cl
    add dx, ax
    adc ch, 0
    mov ax, di
    shl di, cl
    shr ah, cl
    add bx, di
    adc ah, 0
    sub dx, bx
    sbb ch, ah
    mov al, ch
    cbw
    xchg dx, ax
    pop di
    retf
_TEXT ends
end
