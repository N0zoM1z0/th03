; Original Borland 16-bit BCD<->x87 conversion and pow10/log10 helpers.
; EMUL emits the authentic FIDRQQ/FIERQQ/FIWRQQ relocations on x87 code.
; Typed x87 extended constants retain the original 80-bit rounding.
.8086
.8087
EMUL
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Private near helper: push 10^exponent onto the x87 stack.
bcd_binary_power10 proc near
    push bp
    mov bp,sp
    push si
    push di
    mov si,[bp+4]
    or si,si
    mov dx,si
    jz short adjust_power
    jns short abs_exponent_ready
    neg si
abs_exponent_ready:
    cmp si,1387h
    jbe short exponent_bounded
    mov si,1387h
exponent_bounded:
    mov bx,7
    and bx,si
    shl bx,1
    shl bx,1
    add bx,offset _DATA:integer_power10
    fild dword ptr [bx]
    mov cl,3
    shr si,cl
    mov di,offset _DATA:extended_power10
power_bit_loop:
    or si,si
    jz short adjust_power
    shr si,1
    jnc short next_power_bit
    fld tbyte ptr [di]
    fmulp st(1),st(0)
next_power_bit:
    add di,10
    jmp short power_bit_loop
adjust_power:
    or dx,dx
    jz short pow_return
    jns short multiply_power
    fdivp st(1),st(0)
    jmp short pow_return
multiply_power:
    fmulp st(1),st(0)
pow_return:
    pop di
    pop si
    pop bp
    ret 2
bcd_binary_power10 endp

public __BCD_TOBINARY
__BCD_TOBINARY proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    fild qword ptr es:[bx]
    mov ax,word ptr es:[bx+8]
    cmp al,2
    jbe short special_class
    sub ax,93h
    push ax
    call bcd_binary_power10
    jmp short bcd_to_binary_done
special_class:
    jz short quiet_nan
    or al,al
    jz short bcd_to_binary_done
    fmul dword ptr DGROUP:bcd_positive_infinity
    jmp short bcd_to_binary_done
quiet_nan:
    fstp st(0)
    fld dword ptr DGROUP:bcd_quiet_nan
bcd_to_binary_done:
    pop di
    pop si
    pop bp
    retf 4
__BCD_TOBINARY endp

public __BCD_TODECIMAL
__BCD_TODECIMAL proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+14h]
    mov dx,[bp+12h]
    mov cx,7fffh
    les si,dword ptr [bp+6]
    and ax,cx
    jz short write_zero
    cmp ax,cx
    jz short special_float
    sub ax,403bh
    neg ax
    mov dx,4d10h
    imul dx
    xchg dx,ax
    mov dx,[bp+0ah]
    cmp ax,dx
    jl short choose_exponent
    xchg dx,ax
choose_exponent:
    cmp ax,90h
    jg short write_zero
    cmp ax,0ff94h
    jl short load_one
    fld tbyte ptr [bp+0ch]
    push ax
    call bcd_binary_power10
    neg ax
    add ax,93h
    jmp short store_bcd
special_float:
    or dx,dx
    jz short load_zero
load_one:
    fld1
    mov al,1
    test byte ptr [bp+15h],80h
    jz short store_bcd
    fchs
    jmp short store_bcd
load_zero:
    fldz
    mov al,2
    jmp short store_bcd
write_zero:
    fldz
    mov al,0
store_bcd:
    fistp qword ptr es:[si]
    mov ah,0
    mov word ptr es:[si+8],ax
    fwait
    pop di
    pop si
    pop bp
    retf 10h
__BCD_TODECIMAL endp

public __BCD_LOG10
__BCD_LOG10 proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    fild qword ptr es:[bx]
    int 3eh
    clc
    nop
    sub word ptr es:[bx+8],93h
    fiadd word ptr es:[bx+8]
    add word ptr es:[bx+8],93h
    fwait
    pop di
    pop si
    pop bp
    retf 4
__BCD_LOG10 endp

public __BCD_POW10
__BCD_POW10 proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],0
    mov word ptr es:[bx],1
    mov word ptr es:[bx+6],0
    mov word ptr es:[bx+4],0
    mov ax,[bp+0ah]
    add ax,93h
    cmp ax,0ffh
    jg short excessive_power
    cmp ax,3
    jl short underflow_power
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+8],ax
    jmp short pow10_done
underflow_power:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],0
    mov word ptr es:[bx],0
    mov word ptr es:[bx+8],0
    jmp short pow10_done
excessive_power:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+8],1
pow10_done:
    pop di
    pop si
    pop bp
    retf 6
__BCD_POW10 endp
_TEXT ends

_DATA segment word public 'DATA'
; 10^0..10^7 (eight exact 32-bit integer powers).
integer_power10 dd 1,10,100,1000,10000,100000,1000000,10000000

; 10^(8*2^i), i=0..9. Each 80-bit value is its genuine x87
; 64-bit significand followed by the exponent/sign word.
; The original Borland constants deliberately retain their native
; extended precision; TASM's decimal DT rounding differs by ULPs.
extended_power10 label tbyte
    dq 0BEBC200000000000h ; 10^8 mantissa
    dw 04019h ; biased x87 exponent
    dq 08E1BC9BF04000000h ; 10^16 mantissa
    dw 04034h ; biased x87 exponent
    dq 09DC5ADA82B70B59Eh ; 10^32 mantissa
    dw 04069h ; biased x87 exponent
    dq 0C2781F49FFCFA6D5h ; 10^64 mantissa
    dw 040D3h ; biased x87 exponent
    dq 093BA47C980E98CE0h ; 10^128 mantissa
    dw 041A8h ; biased x87 exponent
    dq 0AA7EEBFB9DF9DE8Eh ; 10^256 mantissa
    dw 04351h ; biased x87 exponent
    dq 0E319A0AEA60E91C7h ; 10^512 mantissa
    dw 046A3h ; biased x87 exponent
    dq 0C976758681750C17h ; 10^1024 mantissa
    dw 04D48h ; biased x87 exponent
    dq 09E8B3B5DC53D5DE5h ; 10^2048 mantissa
    dw 05A92h ; biased x87 exponent
    dq 0C46052028A20979Bh ; 10^4096 mantissa
    dw 07525h ; biased x87 exponent

; IEEE 32-bit special classes for BCD conversion.
bcd_positive_infinity dd 07F800000h
bcd_quiet_nan dd 07FC00000h
_DATA ends
end
