; DX:AX <<= CL. Near entry synthesizes a far return without changing arguments.
; CL >= 16 transfers the low word; the CPU's shift-count masking is intentional.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public N_LXLSH@, F_LXLSH@, LXLSH@
N_LXLSH@:
    pop bx
    push cs
    push bx
F_LXLSH@ label far
LXLSH@ label far
    cmp cl,16
    jae shift_high_word
    mov bx,ax
    shl ax,cl
    shl dx,cl
    neg cl
    add cl,16
    shr bx,cl
    or dx,bx
    retf
shift_high_word:
    sub cl,16
    xchg dx,ax
    xor ax,ax
    shl dx,cl
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
end
