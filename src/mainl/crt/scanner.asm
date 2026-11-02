; Original Borland 8086 near __scanner format/conversion dispatcher.
; Callback-driven input, whitespace, field widths, assignment suppression,
; length modifiers, numeric conversions, scansets, strings and characters.
; Its 128-byte DATA table maps 7-bit ASCII characters to 22 format cases.
; Final 44 CODE bytes are the real 22-word relocatable switch vector.
; The scanner preserves its original 42-byte local frame and all unchecked
; 16-bit callback/parser ABIs; no generated target CODE DB byte arrays.
.8086
extrn __scantod:near
extrn __scantol:near
extrn __scanpop:near
extrn __scanrslt:near
_TEXT segment byte public 'CODE'
_TEXT ends
FC_END equ 0
FC_SPACE equ 1
FC_ORDINARY equ 2
FC_PERCENT equ 3
FC_SUPPRESS equ 4
FC_WIDTH equ 5
FC_LOWER_C equ 6
FC_DECIMAL equ 7
FC_UNSIGNED equ 8
FC_AUTOBASE equ 9
FC_FLOAT_EXP equ 10
FC_LONG_UPPER equ 11
FC_SHORT equ 12
FC_LONG_LOWER equ 13
FC_OCTAL equ 14
FC_STRING equ 15
FC_BRACKET equ 16
FC_COUNT equ 17
FC_HEX equ 18
FC_POINTER equ 19
FC_UPPER_N equ 20
FC_UPPER_F equ 21
_DATA segment word public 'DATA'
scanner_classes label byte
; Semantic ASCII formatting classification; each DB is one native
; initialized DATA byte, rather than an LIDATA DUP record.
    db FC_END ; ASCII 00 .
    db FC_ORDINARY ; ASCII 01 .
    db FC_ORDINARY ; ASCII 02 .
    db FC_ORDINARY ; ASCII 03 .
    db FC_ORDINARY ; ASCII 04 .
    db FC_ORDINARY ; ASCII 05 .
    db FC_ORDINARY ; ASCII 06 .
    db FC_ORDINARY ; ASCII 07 .
    db FC_ORDINARY ; ASCII 08 .
    db FC_SPACE ; ASCII 09 .
    db FC_SPACE ; ASCII 0A .
    db FC_SPACE ; ASCII 0B .
    db FC_SPACE ; ASCII 0C .
    db FC_SPACE ; ASCII 0D .
    db FC_ORDINARY ; ASCII 0E .
    db FC_ORDINARY ; ASCII 0F .
    db FC_ORDINARY ; ASCII 10 .
    db FC_ORDINARY ; ASCII 11 .
    db FC_ORDINARY ; ASCII 12 .
    db FC_ORDINARY ; ASCII 13 .
    db FC_ORDINARY ; ASCII 14 .
    db FC_ORDINARY ; ASCII 15 .
    db FC_ORDINARY ; ASCII 16 .
    db FC_ORDINARY ; ASCII 17 .
    db FC_ORDINARY ; ASCII 18 .
    db FC_ORDINARY ; ASCII 19 .
    db FC_ORDINARY ; ASCII 1A .
    db FC_ORDINARY ; ASCII 1B .
    db FC_ORDINARY ; ASCII 1C .
    db FC_ORDINARY ; ASCII 1D .
    db FC_ORDINARY ; ASCII 1E .
    db FC_ORDINARY ; ASCII 1F .
    db FC_SPACE ; ASCII 20  
    db FC_ORDINARY ; ASCII 21 !
    db FC_ORDINARY ; ASCII 22 "
    db FC_ORDINARY ; ASCII 23 #
    db FC_ORDINARY ; ASCII 24 $
    db FC_PERCENT ; ASCII 25 %
    db FC_ORDINARY ; ASCII 26 &
    db FC_ORDINARY ; ASCII 27 '
    db FC_ORDINARY ; ASCII 28 (
    db FC_ORDINARY ; ASCII 29 )
    db FC_SUPPRESS ; ASCII 2A *
    db FC_ORDINARY ; ASCII 2B +
    db FC_ORDINARY ; ASCII 2C ,
    db FC_ORDINARY ; ASCII 2D -
    db FC_ORDINARY ; ASCII 2E .
    db FC_ORDINARY ; ASCII 2F /
    db FC_WIDTH ; ASCII 30 0
    db FC_WIDTH ; ASCII 31 1
    db FC_WIDTH ; ASCII 32 2
    db FC_WIDTH ; ASCII 33 3
    db FC_WIDTH ; ASCII 34 4
    db FC_WIDTH ; ASCII 35 5
    db FC_WIDTH ; ASCII 36 6
    db FC_WIDTH ; ASCII 37 7
    db FC_WIDTH ; ASCII 38 8
    db FC_WIDTH ; ASCII 39 9
    db FC_ORDINARY ; ASCII 3A :
    db FC_ORDINARY ; ASCII 3B ;
    db FC_ORDINARY ; ASCII 3C <
    db FC_ORDINARY ; ASCII 3D =
    db FC_ORDINARY ; ASCII 3E >
    db FC_ORDINARY ; ASCII 3F ?
    db FC_ORDINARY ; ASCII 40 @
    db FC_ORDINARY ; ASCII 41 A
    db FC_ORDINARY ; ASCII 42 B
    db FC_ORDINARY ; ASCII 43 C
    db FC_DECIMAL ; ASCII 44 D
    db FC_FLOAT_EXP ; ASCII 45 E
    db FC_UPPER_F ; ASCII 46 F
    db FC_FLOAT_EXP ; ASCII 47 G
    db FC_SHORT ; ASCII 48 H
    db FC_AUTOBASE ; ASCII 49 I
    db FC_ORDINARY ; ASCII 4A J
    db FC_ORDINARY ; ASCII 4B K
    db FC_LONG_UPPER ; ASCII 4C L
    db FC_ORDINARY ; ASCII 4D M
    db FC_UPPER_N ; ASCII 4E N
    db FC_OCTAL ; ASCII 4F O
    db FC_ORDINARY ; ASCII 50 P
    db FC_ORDINARY ; ASCII 51 Q
    db FC_ORDINARY ; ASCII 52 R
    db FC_ORDINARY ; ASCII 53 S
    db FC_ORDINARY ; ASCII 54 T
    db FC_UNSIGNED ; ASCII 55 U
    db FC_ORDINARY ; ASCII 56 V
    db FC_ORDINARY ; ASCII 57 W
    db FC_HEX ; ASCII 58 X
    db FC_ORDINARY ; ASCII 59 Y
    db FC_ORDINARY ; ASCII 5A Z
    db FC_BRACKET ; ASCII 5B [
    db FC_ORDINARY ; ASCII 5C \
    db FC_BRACKET ; ASCII 5D ]
    db FC_ORDINARY ; ASCII 5E ^
    db FC_ORDINARY ; ASCII 5F _
    db FC_ORDINARY ; ASCII 60 `
    db FC_ORDINARY ; ASCII 61 a
    db FC_ORDINARY ; ASCII 62 b
    db FC_LOWER_C ; ASCII 63 c
    db FC_DECIMAL ; ASCII 64 d
    db FC_FLOAT_EXP ; ASCII 65 e
    db FC_FLOAT_EXP ; ASCII 66 f
    db FC_FLOAT_EXP ; ASCII 67 g
    db FC_SHORT ; ASCII 68 h
    db FC_AUTOBASE ; ASCII 69 i
    db FC_ORDINARY ; ASCII 6A j
    db FC_ORDINARY ; ASCII 6B k
    db FC_LONG_LOWER ; ASCII 6C l
    db FC_ORDINARY ; ASCII 6D m
    db FC_COUNT ; ASCII 6E n
    db FC_OCTAL ; ASCII 6F o
    db FC_POINTER ; ASCII 70 p
    db FC_ORDINARY ; ASCII 71 q
    db FC_ORDINARY ; ASCII 72 r
    db FC_STRING ; ASCII 73 s
    db FC_ORDINARY ; ASCII 74 t
    db FC_UNSIGNED ; ASCII 75 u
    db FC_ORDINARY ; ASCII 76 v
    db FC_ORDINARY ; ASCII 77 w
    db FC_HEX ; ASCII 78 x
    db FC_ORDINARY ; ASCII 79 y
    db FC_ORDINARY ; ASCII 7A z
    db FC_ORDINARY ; ASCII 7B {
    db FC_ORDINARY ; ASCII 7C |
    db FC_ORDINARY ; ASCII 7D }
    db FC_ORDINARY ; ASCII 7E ~
    db FC_ORDINARY ; ASCII 7F .
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __scanner
__scanner proc near
    push bp
    mov bp, sp
    sub sp, 02ah
    push si
    push di
    mov word ptr [bp-4], 0
    mov word ptr [bp-6], 0
    jmp short scan_next_format
scanner_at_0014:
    les di, dword ptr [bp+010h]
    test byte ptr [bp-1], 020h
    je short scan_restore_context
    les di, dword ptr es:[di]
    add word ptr [bp+010h], 4
    ret
scan_restore_context:
    mov di, word ptr es:[di]
    push ds
    pop es
    add word ptr [bp+010h], 2
    ret
scan_next_format:
    push es
    cld
scanner_at_0031:
    mov si, word ptr [bp+0ch]
read_input_char:
    mov es, word ptr [bp+0eh]
    lods byte ptr es:[si]
    or al, al
    je short handle_format_end
    cmp al, 025h
    je short read_format_specifier
scan_main_loop:
    xor ah, ah
    xchg di, ax
    inc word ptr [bp-6]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    or ax, ax
    jl short reached_input_end
    xor ah, ah
    test di, 080h
    jne short scanner_at_0098
    cmp byte ptr [di+scanner_classes], 1
    jne short scanner_at_0098
scanner_at_0065:
    xchg bx, ax
    or bl, bl
    js short scanner_at_0086
    cmp byte ptr [bx+scanner_classes], 1
    jne short scanner_at_0086
    inc word ptr [bp-6]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    or ax, ax
    jg short scanner_at_0065
reached_input_end:
    jmp near ptr scan_input_unget
scanner_at_0086:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push bx
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-6]
    jmp short read_input_char
scanner_at_0098:
    cmp ax, di
    je short read_input_char
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-6]
    jmp near ptr scan_format_continue
handle_format_end:
    jmp near ptr scan_format_continue
read_format_specifier:
    mov word ptr [bp-0ah], 0ffffh
    mov es, word ptr [bp+0eh]
    mov byte ptr [bp-1], 020h
check_format_character:
    lods byte ptr es:[si]
    xor ah, ah
    mov word ptr [bp+0ch], si
    or al, al
    xchg di, ax
    jl short scanner_at_00e3
    mov bl, byte ptr [di+scanner_classes]
    xor bh, bh
    cmp bx, 015h
    jbe short scanner_at_00d8
    jmp near ptr scan_input_unget
scanner_at_00d8:
    add bx, bx
    ; Zero-byte segment-position boundary: keeps literal BCC FIXUPP order
    ; before the forward CODE dispatch table. Does not emit padding.
    org $
    jmp word ptr cs:[bx+scanner_dispatch_table]
format_default:
    xchg di, ax
    jmp near ptr scan_main_loop
scanner_at_00e3:
    jmp near ptr scan_format_continue
format_whitespace:
    or byte ptr [bp-1], 1
    jmp short check_format_character
format_literal:
    sub di, 030h
    xchg word ptr [bp-0ah], di
    or di, di
    jl short check_format_character
    mov ax, 0ah
    mul di
    add word ptr [bp-0ah], ax
    jmp short check_format_character
scan_long_modifier:
    or byte ptr [bp-1], 8
    jmp short check_format_character
scan_short_modifier:
    or byte ptr [bp-1], 4
    jmp short check_format_character
scan_unsigned_modifier:
    or byte ptr [bp-1], 2
    jmp short check_format_character
scan_assignment_suppressed:
    and byte ptr [bp-1], 0dfh
    jmp short check_format_character
scan_field_width:
    or byte ptr [bp-1], 020h
    jmp short check_format_character
scan_unsigned_int:
    mov ax, word ptr [bp-6]
    sub dx, dx
    test byte ptr [bp-1], 1
    je short scanner_at_017f
    jmp near ptr scanner_at_0031
scan_set_length:
    mov si, 8
    jmp short scanner_at_013d
scan_signed_digit:
    mov si, 0ah
    jmp short scanner_at_013d
scan_string_conversion:
    mov si, 010h
    jmp short scanner_at_013d
scan_conversion:
    xor si, si
scanner_at_013d:
    test di, 020h
    jne short scanner_at_014c
    cmp di, 058h
    je short scanner_at_014c
    or byte ptr [bp-1], 4
scanner_at_014c:
    push ss
    lea ax, [bp-8]
    push ax
    push ss
    lea ax, [bp-6]
    push ax
    mov ax, word ptr [bp-0ah]
    and ax, 07fffh
    push ax
    push si
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __scantol
    add sp, 014h
    cmp word ptr [bp-8], 0
    jle short scanner_at_018e
    test byte ptr [bp-1], 1
    jne short scanner_at_018b
    inc word ptr [bp-4]
scanner_at_017f:
    call scanner_at_0014
    stosw
    test byte ptr [bp-1], 4
    je short scanner_at_018b
    xchg dx, ax
    stosw
scanner_at_018b:
    jmp near ptr scanner_at_0031
scanner_at_018e:
    jl short scanner_at_0193
    jmp near ptr scan_format_continue
scanner_at_0193:
    jmp near ptr scan_input_unget
scan_lvalue:
    call scanner_at_0199
scanner_at_0199:
    jmp near ptr scanner_at_0442
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-6]
    and word ptr [bp-0ah], 07fffh
    call scanner_at_01b4
scanner_at_01b4:
    jmp near ptr scanner_at_046c
    push dx
    cmp al, 03ah
    je short scanner_at_01d5
    or ax, ax
    jle short scanner_at_01d0
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-6]
scanner_at_01d0:
    pop dx
    mov bx, ds
    jmp short scanner_at_01f4
scanner_at_01d5:
    call scanner_at_01d8
scanner_at_01d8:
    jmp near ptr scanner_at_046c
    pop bx
    or ax, ax
    jle short scanner_at_01f4
    push dx
    push bx
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-6]
    pop bx
    pop dx
scanner_at_01f4:
    test byte ptr [bp-1], 1
    jne short scanner_at_020a
    call scanner_at_0014
    inc word ptr [bp-4]
    xchg dx, ax
    stosw
    test byte ptr [bp-1], 020h
    je short scanner_at_020a
    xchg bx, ax
    stosw
scanner_at_020a:
    jmp near ptr scanner_at_0031
scanner_at_020d:
    jmp near ptr scan_input_unget
scan_float_conversion:
    push ss
    lea ax, [bp-8]
    push ax
    push ss
    lea ax, [bp-6]
    push ax
    mov ax, 07fffh
    and ax, word ptr [bp-0ah]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __scantod
    add sp, 012h
    cmp word ptr [bp-8], 0
    jle short scanner_at_027a
    mov al, byte ptr [bp-1]
    cbw
    test al, 1
    jne short scanner_at_0274
    call scanner_at_0014
    inc word ptr [bp-4]
    test byte ptr [bp-1], 4
    je short scanner_at_0252
    mov ax, 4
    jmp short scanner_at_025f
scanner_at_0252:
    test byte ptr [bp-1], 8
    je short scanner_at_025d
    mov ax, 8
    jmp short scanner_at_025f
scanner_at_025d:
    xor ax, ax
scanner_at_025f:
    push ax
    test byte ptr [bp-1], 020h
    je short scanner_at_0269
    push es
    jmp short scanner_at_026a
scanner_at_0269:
    push ds
scanner_at_026a:
    push di
    call __scanrslt
    add sp, 6
    jmp near ptr scanner_at_0031
scanner_at_0274:
    call __scanpop
    jmp near ptr scanner_at_0031
scanner_at_027a:
    call __scanpop
    jl short scanner_at_020d
    jmp near ptr scan_format_continue
scan_integer_conversion:
    call scanner_at_0285
scanner_at_0285:
    jmp near ptr scanner_at_0442
    test byte ptr [bp-1], 1
    jne short scanner_at_0294
    call scanner_at_0014
    inc word ptr [bp-4]
scanner_at_0294:
    and word ptr [bp-0ah], 07fffh
    je short scanner_at_02c8
scanner_at_029b:
    test byte ptr [bp-1], 1
    jne short scanner_at_02a2
    stosb
scanner_at_02a2:
    inc word ptr [bp-6]
    push es
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    pop es
    or ax, ax
    jle short scanner_at_02c8
    or al, al
    js short scanner_at_02c3
    xchg bx, ax
    cmp byte ptr [bx+scanner_classes], 1
    xchg bx, ax
    jle short scanner_at_02c8
scanner_at_02c3:
    dec word ptr [bp-0ah]
    jg short scanner_at_029b
scanner_at_02c8:
    push es
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    pop es
    dec word ptr [bp-6]
    test byte ptr [bp-1], 1
    jne short scanner_at_02e3
    mov al, 0
    stosb
scanner_at_02e3:
    jmp near ptr scanner_at_0031
scan_percent_literal:
    test byte ptr [bp-1], 1
    jne short scanner_at_02ef
    call scanner_at_0014
scanner_at_02ef:
    mov si, word ptr [bp-0ah]
    or si, si
    jge short scanner_at_02f9
    mov si, 1
scanner_at_02f9:
    je short scanner_at_0319
scanner_at_02fb:
    inc word ptr [bp-6]
    push es
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    pop es
    or ax, ax
    jl short scanner_at_0325
    test byte ptr [bp-1], 1
    jne short scanner_at_0316
    stosb
scanner_at_0316:
    dec si
    jg short scanner_at_02fb
scanner_at_0319:
    test byte ptr [bp-1], 1
    jne short scanner_at_0322
    inc word ptr [bp-4]
scanner_at_0322:
    jmp near ptr scanner_at_0031
scanner_at_0325:
    jmp near ptr scan_input_unget
scan_char_conversion:
    push es
    sub ax, ax
    cld
    push ss
    pop es
    lea di, [bp-02ah]
    mov cx, 010h
    rep stosw
    pop es
    lods byte ptr es:[si]
    and byte ptr [bp-1], 0efh
    cmp al, 05eh
    jne short scanner_at_0347
    or byte ptr [bp-1], 010h
    lods byte ptr es:[si]
scanner_at_0347:
    mov ah, 0
scanner_at_0349:
    mov dl, al
    mov di, ax
    mov cl, 3
    shr di, cl
    mov cx, 0107h
    and cl, dl
    shl ch, cl
    or byte ptr [bp+di-02ah], ch
scanner_at_035b:
    lods byte ptr es:[si]
    cmp al, 0
    je short scanner_at_038a
    cmp al, 05dh
    je short scanner_at_038d
    cmp al, 02dh
    jne short scanner_at_0349
    cmp dl, byte ptr es:[si]
    ja short scanner_at_0349
    cmp byte ptr es:[si], 05dh
    je short scanner_at_0349
    lods byte ptr es:[si]
    sub al, dl
    je short scanner_at_035b
    add dl, al
scanner_at_037c:
    rol ch, 1
    adc di, 0
    or byte ptr [bp+di-02ah], ch
    dec al
    jne short scanner_at_037c
    jmp short scanner_at_035b
scanner_at_038a:
    jmp near ptr scan_format_continue
scanner_at_038d:
    mov word ptr [bp+0ch], si
    and word ptr [bp-0ah], 07fffh
    mov si, word ptr [bp-0ah]
    test byte ptr [bp-1], 1
    jne short scanner_at_03a1
    call scanner_at_0014
scanner_at_03a1:
    dec si
    jl short scanner_at_03fc
    inc word ptr [bp-6]
    push es
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    pop es
    or ax, ax
    jl short scanner_at_0411
    xchg si, ax
    mov bx, si
    mov cl, 3
    shr si, cl
    mov cx, 0107h
    and cl, bl
    shl ch, cl
    test byte ptr [bp+si-02ah], ch
    xchg si, ax
    xchg bx, ax
    je short scanner_at_03d5
    test byte ptr [bp-1], 010h
    je short scanner_at_03db
    jmp short scanner_at_03e4
scanner_at_03d5:
    test byte ptr [bp-1], 010h
    je short scanner_at_03e4
scanner_at_03db:
    test byte ptr [bp-1], 1
    jne short scanner_at_03a1
    stosb
    jmp short scanner_at_03a1
scanner_at_03e4:
    push es
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    pop es
    dec word ptr [bp-6]
    inc si
    cmp si, word ptr [bp-0ah]
    jge short scanner_at_0405
scanner_at_03fc:
    test byte ptr [bp-1], 1
    jne short scanner_at_040e
    inc word ptr [bp-4]
scanner_at_0405:
    test byte ptr [bp-1], 1
    jne short scanner_at_040e
    mov al, 0
    stosb
scanner_at_040e:
    jmp near ptr scanner_at_0031
scanner_at_0411:
    inc si
    cmp si, word ptr [bp-0ah]
    jge short scan_input_unget
    test byte ptr [bp-1], 1
    jne short scan_input_unget
    mov al, 0
    stosb
    inc word ptr [bp-4]
scan_input_unget:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    mov ax, 0ffffh
    push ax
    call word ptr [bp+6]
    add sp, 6
    cmp word ptr [bp-4], 1
    sbb word ptr [bp-4], 0
scan_format_continue:
    pop es
    mov ax, word ptr [bp-4]
    jmp near ptr scan_finish
scanner_at_0442:
    inc word ptr [bp-6]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    or ax, ax
    jle short scanner_at_0467
    or al, al
    js short scanner_at_0461
    xchg bx, ax
    cmp byte ptr [bx+scanner_classes], 1
    xchg bx, ax
    je short scanner_at_0442
scanner_at_0461:
    pop cx
    add cx, 3
    jmp cx
scanner_at_0467:
    je short scanner_at_0461
    pop cx
    jmp short scan_input_unget
scanner_at_046c:
    sub dx, dx
    mov cx, 4
scanner_at_0471:
    dec word ptr [bp-0ah]
    jl short scanner_at_04bf
    push dx
    push cx
    inc word ptr [bp-6]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    pop cx
    pop dx
    or ax, ax
    jle short scanner_at_04c1
    dec cl
    jl short scanner_at_04c1
    mov ch, al
    sub ch, 030h
    jb short scanner_at_04c1
    cmp ch, 0ah
    jb short scanner_at_04b3
    sub ch, 011h
    jb short scanner_at_04c1
    cmp ch, 6
    jb short scanner_at_04b0
    sub ch, 020h
    jb short scanner_at_04c1
    cmp ch, 6
    jae short scanner_at_04c1
scanner_at_04b0:
    add ch, 0ah
scanner_at_04b3:
    shl dx, 1
    shl dx, 1
    shl dx, 1
    shl dx, 1
    add dl, ch
    jmp short scanner_at_0471
scanner_at_04bf:
    sub ax, ax
scanner_at_04c1:
    cmp cl, 4
    je short scanner_at_04cc
    pop cx
    add cx, 3
    jmp cx
scanner_at_04cc:
    pop cx
    jmp near ptr scan_input_unget
scan_finish:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
__scanner endp
; Dynamic format-dispatch switch table, one genuine relocatable CODE
; offset for every scanner class, including default/whitespace cases.
scanner_dispatch_table label word
    dw offset scan_format_continue ; format class 0
    dw offset scan_format_continue ; format class 1
    dw offset scan_format_continue ; format class 2
    dw offset format_default ; format class 3
    dw offset format_whitespace ; format class 4
    dw offset format_literal ; format class 5
    dw offset scan_percent_literal ; format class 6
    dw offset scan_signed_digit ; format class 7
    dw offset scan_signed_digit ; format class 8
    dw offset scan_conversion ; format class 9
    dw offset scan_float_conversion ; format class 10
    dw offset scan_long_modifier ; format class 11
    dw offset scan_unsigned_modifier ; format class 12
    dw offset scan_short_modifier ; format class 13
    dw offset scan_set_length ; format class 14
    dw offset scan_integer_conversion ; format class 15
    dw offset scan_char_conversion ; format class 16
    dw offset scan_unsigned_int ; format class 17
    dw offset scan_string_conversion ; format class 18
    dw offset scan_lvalue ; format class 19
    dw offset scan_assignment_suppressed ; format class 20
    dw offset scan_field_width ; format class 21
_TEXT ends
end
