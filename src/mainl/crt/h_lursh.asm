; Unsigned DX:AX right shift by CL; preserve the near-to-far return shim.
; Original Japanese Borland h_lursh: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public LXURSH@
public F_LXURSH@
public N_LXURSH@
N_LXURSH@ label near
    pop bx
    push cs
    push bx
F_LXURSH@ label far
LXURSH@ label far
    cmp cl, 010h
    jae short shift_high_word
    mov bx, dx
    shr ax, cl
    shr dx, cl
    neg cl
    add cl, 010h
    shl bx, cl
    or ax, bx
    retf
shift_high_word:
    sub cl, 010h
    xchg dx, ax
    xor dx, dx
    shr ax, cl
    retf
_TEXT ends
end
