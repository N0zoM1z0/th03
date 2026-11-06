; Original Borland 16-bit long division/modulus helper family.
; Twelve near/far/alternate public names share one real 32-bit
; restoring-division core with signed and unsigned behaviors.
; PUBLIC order follows the original twelve OMF export entries. JWasm
; preserves this declaration chronology, including same-address aliases;
; TASM 5 hash enumeration does not. No code or MAP patch is involved.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public LUMOD@,LDIV@,F_LUMOD@,N_LUMOD@
public N_LMOD@,F_LMOD@,LMOD@
public N_LUDIV@,F_LUDIV@,LUDIV@
public N_LDIV@,F_LDIV@
N_LDIV@ label near
    pop cx
    push cs
    push cx
F_LDIV@ label far
LDIV@ label far
    xor cx,cx
    jmp short division_core
N_LUDIV@ label near
    pop cx
    push cs
    push cx
F_LUDIV@ label far
LUDIV@ label far
    mov cx,1
    jmp short division_core
N_LMOD@ label near
    pop cx
    push cs
    push cx
F_LMOD@ label far
LMOD@ label far
    mov cx,2
    jmp short division_core
N_LUMOD@ label near
    pop cx
    push cs
    push cx
F_LUMOD@ label far
LUMOD@ label far
    mov cx,3
division_core:
    push bp
    push si
    push di
    mov bp,sp
    mov di,cx
    mov ax,[bp+0ah]
    mov dx,[bp+0ch]
    mov bx,[bp+0eh]
    mov cx,[bp+10h]
    or cx,cx
    jne short full_division
    or dx,dx
    je short reduced_division
    or bx,bx
    je short reduced_division
full_division:
    test di,1
    jne short unsigned_division
    or dx,dx
    jns short maybe_negative_divisor
    neg dx
    neg ax
    sbb dx,0
    or di,0ch
maybe_negative_divisor:
    or cx,cx
    jns short unsigned_division
    neg cx
    neg bx
    sbb cx,0
    xor di,4
unsigned_division:
    mov bp,cx
    mov cx,20h
    push di
    xor di,di
    xor si,si
long_division_loop:
    shl ax,1
    rcl dx,1
    rcl si,1
    rcl di,1
    cmp di,bp
    jb short next_division_bit
    ja short subtract_divisor
    cmp si,bx
    jb short next_division_bit
subtract_divisor:
    sub si,bx
    sbb di,bp
    inc ax
next_division_bit:
    loop long_division_loop
    pop bx
    test bx,2
    je short adjust_signed_result
    mov ax,si
    mov dx,di
    shr bx,1
adjust_signed_result:
    test bx,4
    je short division_done
    neg dx
    neg ax
    sbb dx,0
division_done:
    pop di
    pop si
    pop bp
    retf 8
reduced_division:
    div bx
    test di,2
    je short reduced_quotient
    xchg dx,ax
reduced_quotient:
    xor dx,dx
    jmp short division_done
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
