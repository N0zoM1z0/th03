; Original Japanese Borland bcd2: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
.8087
EMUL
extrn @istream@$brsh$qmg:far
extrn @ostream@$blsh$qg:far
extrn __BCD_TOBINARY:far
extrn __BCD_TODECIMAL:far
extrn FIDRQQ:far
extrn FIWRQQ:far
extrn N_SCOPY@:near
extrn __turboFloat:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @$BLSH$QM7OSTREAMM3BCD
public @$BRSH$QM7ISTREAMM3BCD
; Native source chunks retain original logical FIXUPP chronology.

org 134
    call N_SCOPY@
    mov dx, word ptr [bp+0ch]
    mov ax, word ptr [bp+0ah]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf 8

org 121
    call __BCD_TODECIMAL
    lea ax, [bp-01eh]
    push ss
    push ax
    mov cx, 0ah

org 115
    fwait
    lea ax, [bp-01eh]
    push ax

org 106
    fstp tbyte ptr [bp-030h]
    mov ax, 01388h
    push ax
    push ss

org 99
    fld tbyte ptr [bp-014h]
    sub sp, 0ah

org 95
    fstp tbyte ptr [bp-014h]

org 91
    fld tbyte ptr [bp-0ah]

org 77
    call @istream@$brsh$qmg
    add sp, 8
    push word ptr [bp+8]
    push word ptr [bp+6]

org 42
    call @ostream@$blsh$qg
    add sp, 0eh
    pop di
    pop si
    mov sp, bp
    pop bp
    retf 8
@$BRSH$QM7ISTREAMM3BCD label far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
    push ss
    lea ax, [bp-0ah]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 34
    fwait
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 30
    fstp tbyte ptr [bp-012h]

org 22
    call __BCD_TOBINARY
    sub sp, 0ah

org 0
@$BLSH$QM7OSTREAMM3BCD label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    push dx
    push ax
_TEXT ends
end
