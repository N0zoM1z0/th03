; Both entries consume the linker-provided absolute __AHSHIFT value.
; Original Japanese Borland h_psbh: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
extrn __AHSHIFT:abs
_TEXT segment byte public 'CODE'
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public F_PSBH@
public N_PSBH@
N_PSBH@ label near
    push si
    mov si, cx
    mov cx,offset __AHSHIFT
    shr dx, cl
    shr si, cl
    sub ax, bx
    sbb dx, si
    pop si
    ret
F_PSBH@ label far
    push si
    mov si, cx
    mov cx,offset __AHSHIFT
    shr dx, cl
    shr si, cl
    sub ax, bx
    sbb dx, si
    pop si
    retf
_TEXT ends
end
