; Native near unsigned 32-bit multiply, low 32 bits in DX:AX.
; Input DX:AX times CX:BX; preserve SI, original carry and zero paths.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_LXMUL@
N_LXMUL@:
    push si
    xchg ax,si
    xchg ax,dx
    test ax,ax
    jz low_limb
    mul bx
low_limb:
    jcxz multiply_low
    xchg ax,cx
    mul si
    add ax,cx
multiply_low:
    xchg ax,si
    mul bx
    add dx,si
    pop si
    ret
_TEXT ends
end
