; Original Borland FAR ldiv(long,long) 32-bit signed quotient/remainder
; using native 16-bit restoring division and near N_SCOPY@ result transfer.
.8086
extrn N_SCOPY@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _ldiv
_ldiv proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    push bp
    xor cx,cx
    mov ax,[bp+0ah]
    mov dx,[bp+0ch]
    mov bx,[bp+0eh]
    mov bp,[bp+10h]
    xor si,si
    or dx,dx
    jns short positive_dividend
    neg dx
    neg ax
    sbb dx,si
    inc cl
positive_dividend:
    or bp,bp
    jns short positive_divisor
    neg bp
    neg bx
    sbb bp,si
    xor cl,1
positive_divisor:
    push cx
    mov di,bp
    or di,dx
    jne short long_quotient
    div bx
    xchg si,dx
    jmp short divmod_ready
long_quotient:
    mov cx,20h
    mov di,si
divmod_loop:
    shl ax,1
    rcl dx,1
    rcl si,1
    rcl di,1
    cmp di,bp
    jb short divmod_next
    ja short divmod_subtract
    cmp si,bx
    jb short divmod_next
divmod_subtract:
    sub si,bx
    sbb di,bp
    inc ax
divmod_next:
    loop divmod_loop
divmod_ready:
    pop cx
    jcxz short divmod_sign_done
    neg di
    neg si
    sbb di,0
    neg dx
    neg ax
    sbb dx,0
divmod_sign_done:
    pop bp
    mov [bp-8],ax
    mov [bp-6],dx
    mov [bp-4],si
    mov [bp-2],di
    push word ptr [bp+8]
    push word ptr [bp+6]
    lea ax,[bp-8]
    push ss
    push ax
    mov cx,8
    call N_SCOPY@
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_ldiv endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
