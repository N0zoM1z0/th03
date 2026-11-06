; Signed DX:AX right shift by CL, including the original high-word path.
; Original Japanese Borland h_lrsh: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public LXRSH@
public N_LXRSH@
public F_LXRSH@
N_LXRSH@ label near
    pop bx
    push cs
    push bx
F_LXRSH@ label far
LXRSH@ label far
    cmp cl, 010h
    jae short shift_high_word
    mov bx, dx
    shr ax, cl
    sar dx, cl
    neg cl
    add cl, 010h
    shl bx, cl
    or ax, bx
    retf
shift_high_word:
    sub cl, 010h
    xchg dx, ax
    cwd
    sar ax, cl
    retf
_TEXT ends
end
