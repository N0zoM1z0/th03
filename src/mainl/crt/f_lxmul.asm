; Far 32x32 unsigned multiply, retaining the low DX:AX of the product.
; Same algorithm as N_LXMUL@ but original far-return and alias ABI.
.8086
_TEXT segment byte public 'CODE'
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public F_LXMUL@,LXMUL@
F_LXMUL@:
LXMUL@:
    push si
    xchg ax,si
    xchg ax,dx
    test ax,ax
    jz multiply_low_limb
    mul bx
multiply_low_limb:
    jcxz multiply_last
    xchg ax,cx
    mul si
    add ax,cx
multiply_last:
    xchg ax,si
    mul bx
    add dx,si
    pop si
    retf
_TEXT ends
end
