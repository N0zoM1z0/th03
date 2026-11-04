; Original Borland ostream signed and unsigned long formatting.
; Hex, octal, sign and prefix conversion with real far output ABI.
; Symbolic 8086 instructions; DATA holds printable digit tables.
.8086
extrn @ostream@outstr$qnxct1:far,F_LUMOD@:far,F_LUDIV@:far,F_LXURSH@:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$blsh$ql,@ostream@$blsh$qul
long_to_ascii:
    push bp
    mov bp, sp
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], 0
loc_000c:
    dec word ptr [bp + 6]
    xor ax, ax
    mov dx, 0ah
    push ax
    push dx
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call F_LUMOD@
    add al, 30h
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], al
    xor ax, ax
    mov dx, 0ah
    push ax
    push dx
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call F_LUDIV@
    mov word ptr [bp + 0ch], dx
    mov word ptr [bp + 0ah], ax
    or ax, word ptr [bp + 0ch]
    jne loc_000c
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
hex_conversion:
    push bp
    mov bp, sp
    push si
    push di
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], 0
loc_005c:
    dec word ptr [bp + 6]
    mov al, byte ptr [bp + 0ah]
    and al, 7
    add al, 30h
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], al
    mov cx, 3
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    call F_LXURSH@
    mov word ptr [bp + 0ch], dx
    mov word ptr [bp + 0ah], ax
    or ax, word ptr [bp + 0ch]
    jne loc_005c
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf
write_integer_digits:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    cmp word ptr [bp + 0eh], 0
    je loc_00a4
    mov dx, ds
    mov ax,offset DGROUP:digit_upper
    jmp short loc_00a9
loc_00a4:
    mov dx, ds
    mov ax,offset DGROUP:digit_lower
loc_00a9:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], 0
loc_00b6:
    dec word ptr [bp + 6]
    mov ax, word ptr [bp + 0ah]
    and ax, 0fh
    les bx,dword ptr [bp - 4]
    add bx, ax
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], al
    mov cx, 4
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    call F_LXURSH@
    mov word ptr [bp + 0ch], dx
    mov word ptr [bp + 0ah], ax
    or ax, word ptr [bp + 0ch]
    jne loc_00b6
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Public original far ostream long output entry.
@ostream@$blsh$ql:
    push bp
    mov bp, sp
    sub sp, 20h
    push si
    push di
    mov word ptr [bp - 2], 0
    mov word ptr [bp - 4], 0
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 40h
    je loc_0116
    mov ax, 10h
    jmp short loc_012b
loc_0116:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 20h
    je loc_0128
    mov ax, 8
    jmp short loc_012b
loc_0128:
    mov ax, 0ah
loc_012b:
    mov bx, ax
    cmp bx, 0ah
    jne loc_0145
    cmp word ptr [bp + 0ch], 0
    jg loc_0145
    jl loc_0140
    cmp word ptr [bp + 0ah], 0
    jae loc_0145
loc_0140:
    mov ax, 1
    jmp short loc_0147
loc_0145:
    xor ax, ax
loc_0147:
    mov word ptr [bp - 0ah], ax
    cmp word ptr [bp - 0ah], 0
    je loc_015f
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    neg dx
    neg ax
    sbb dx, 0
    jmp short loc_0165
loc_015f:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
loc_0165:
    mov word ptr [bp - 0ch], dx
    mov word ptr [bp - 0eh], ax
    cmp bx, 0ah
    jne loc_01bb
    push dx
    push ax
    push ss
    lea ax, [bp - 11h]
    push ax
    push cs
    call long_to_ascii
    add sp, 8
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    mov ax, word ptr [bp - 0eh]
    or ax, word ptr [bp - 0ch]
    jne loc_018f
    jmp near ptr loc_0244
loc_018f:
    cmp word ptr [bp - 0ah], 0
    je loc_01a0
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:sign_minus
    jmp near ptr loc_0244
loc_01a0:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 11h], 4
    jne loc_01b0
    jmp near ptr loc_0244
loc_01b0:
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:sign_plus
    jmp near ptr loc_0244
loc_01bb:
    cmp bx, 10h
    jne loc_0217
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 11h], 2
    je loc_01d2
    mov ax, 1
    jmp short loc_01d4
loc_01d2:
    xor ax, ax
loc_01d4:
    mov word ptr [bp - 10h], ax
    push ax
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    push ss
    lea ax, [bp - 11h]
    push ax
    push cs
    call write_integer_digits
    add sp, 0ah
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 80h
    je loc_0244
    cmp word ptr [bp - 10h], 0
    je loc_020a
    mov dx, ds
    mov ax,offset DGROUP:prefix_hex_upper
    jmp short loc_020f
loc_020a:
    mov dx, ds
    mov ax,offset DGROUP:prefix_hex_lower
loc_020f:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short loc_0244
loc_0217:
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    push ss
    lea ax, [bp - 11h]
    push ax
    push cs
    call hex_conversion
    add sp, 8
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 80h
    je loc_0244
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:prefix_zero
loc_0244:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@outstr$qnxct1
    add sp, 0ch
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Public original far ostream long output entry.
@ostream@$blsh$qul:
    push bp
    mov bp, sp
    sub sp, 1ah
    push si
    push di
    mov word ptr [bp - 2], 0
    mov word ptr [bp - 4], 0
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 40h
    je loc_02dd
    test byte ptr es:[bx + 11h], 2
    je loc_0295
    mov ax, 1
    jmp short loc_0297
loc_0295:
    xor ax, ax
loc_0297:
    mov word ptr [bp - 0ah], ax
    push ax
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push ss
    lea ax, [bp - 0bh]
    push ax
    push cs
    call write_integer_digits
    add sp, 0ah
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 80h
    jne loc_02c3
    jmp near ptr loc_034e
loc_02c3:
    cmp word ptr [bp - 0ah], 0
    je loc_02d0
    mov dx, ds
    mov ax,offset DGROUP:prefix_hex_upper_unsigned
    jmp short loc_02d5
loc_02d0:
    mov dx, ds
    mov ax,offset DGROUP:prefix_hex_lower_unsigned
loc_02d5:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short loc_034e
loc_02dd:
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 20h
    je loc_0319
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push ss
    lea ax, [bp - 0bh]
    push ax
    push cs
    call hex_conversion
    add sp, 8
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 10h], 80h
    je loc_034e
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:prefix_zero_unsigned
    jmp short loc_034e
loc_0319:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push ss
    lea ax, [bp - 0bh]
    push ax
    push cs
    call long_to_ascii
    add sp, 8
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je loc_034e
    les bx,dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx + 11h], 4
    je loc_034e
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4],offset DGROUP:sign_plus_unsigned
loc_034e:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@outstr$qnxct1
    add sp, 0ch
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends

_DATA segment word public 'DATA'
digit_lower db '0123456789abcdef'
digit_upper db '0123456789ABCDEF'
sign_minus db '-',0
sign_plus db '+',0
prefix_hex_upper db '0X',0
prefix_hex_lower db '0x',0
prefix_zero db '0',0
prefix_hex_upper_unsigned db '0X',0
prefix_hex_lower_unsigned db '0x',0
prefix_zero_unsigned db '0',0
sign_plus_unsigned db '+',0
_DATA ends
end
