; Entire original Japanese Borland CRT h_ldiv member.
; Four complete signed/unsigned 32-bit div/mod operations, with near-to-far caller stubs and common bitwise long division core.
; Natural 8086 source, complete near/far aliases and original branch behavior.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_LDIV@,F_LDIV@,LDIV@,N_LUDIV@,F_LUDIV@,LUDIV@,N_LMOD@,F_LMOD@,LMOD@,N_LUMOD@,F_LUMOD@,LUMOD@

; Original aliases share an exact instruction address.
N_LDIV@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_LDIV@:
LDIV@:
    xor cx,cx
    jmp short h_ldiv_001d

; Original aliases share an exact instruction address.
N_LUDIV@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_LUDIV@:
LUDIV@:
    mov cx,1
    jmp short h_ldiv_001d

; Original aliases share an exact instruction address.
N_LMOD@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_LMOD@:
LMOD@:
    mov cx,2
    jmp short h_ldiv_001d

; Original aliases share an exact instruction address.
N_LUMOD@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_LUMOD@:
LUMOD@:
    mov cx,3

h_ldiv_001d:
    push bp
    push si
    push di
    mov bp,sp
    mov di,cx
    mov ax,[bp+10]
    mov dx,[bp+12]
    mov bx,[bp+14]
    mov cx,[bp+16]
    or cx,cx
    jnz h_ldiv_003c
    or dx,dx
    jz h_ldiv_00a1
    or bx,bx
    jz h_ldiv_00a1

h_ldiv_003c:
    test di,1
    jnz h_ldiv_005e
    or dx,dx
    jns h_ldiv_0050
    neg dx
    neg ax
    sbb dx,0
    or di,12

h_ldiv_0050:
    or cx,cx
    jns h_ldiv_005e
    neg cx
    neg bx
    sbb cx,0
    xor di,4

h_ldiv_005e:
    mov bp,cx
    mov cx,32
    push di
    xor di,di
    xor si,si

h_ldiv_0068:
    shl ax,1
    rcl dx,1
    rcl si,1
    rcl di,1
    cmp di,bp
    jc h_ldiv_007f
    ja h_ldiv_007a
    cmp si,bx
    jc h_ldiv_007f

h_ldiv_007a:
    sub si,bx
    sbb di,bp
    inc ax

h_ldiv_007f:
    loop h_ldiv_0068
    pop bx
    test bx,2
    jz h_ldiv_008e
    mov ax,si
    mov dx,di
    shr bx,1

h_ldiv_008e:
    test bx,4
    jz h_ldiv_009b
    neg dx
    neg ax
    sbb dx,0

h_ldiv_009b:
    pop di
    pop si
    pop bp
    retf 8

h_ldiv_00a1:
    div bx
    test di,2
    jz h_ldiv_00aa
    xchg ax,dx

h_ldiv_00aa:
    xor dx,dx
    jmp short h_ldiv_009b
_TEXT ends
end
