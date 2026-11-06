; Borland large-model istream::operator>>(long double&), original slot 765.
; Complete mantissa/exponent parser with real streambuf refill and x87 scaling.
; BP-0Ch: character; BP-0Eh: mantissa sign; BP-10h: exponent/scale sign;
; BP-14h/-12h: decimal exponent; BP-16h: digit-present / stream success;
; BP-1Ah/-18h: explicit exponent; BP-20h: factor; BP-2Ah: current power.
; EMUL keeps the original FPU runtime references. Borland's x87 frame method 4
; is represented by TASM frame method 5; raw OMF record identity is not claimed.
.8086
.8087
EMUL
extrn @ios@setstate$qi:far
extrn @streambuf@do_snextc$qv:far
extrn @istream@ipfx$qi:far
extrn __ctype:byte
extrn __huge_dble:qword
extrn __huge_ldble:tbyte
extrn _errno:word
extrn F_LXMUL@:far
extrn FIDRQQ:far
extrn FIERQQ:far
extrn FIWRQQ:far
extrn __turboFloat:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qmg
@istream@$brsh$qmg proc far
    push bp
    mov bp,sp
    sub sp,2ah
    push si
    push di
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jne short parser_begin
    jmp near ptr parser_return
parser_begin:
    mov word ptr [bp-16h],0
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-4],es
    mov [bp-6],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp-6]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short first_buffered_char
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-8],es
    mov [bp-0ah],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,dword ptr es:[bx+2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+0ch]
    pop cx
    pop cx
    jmp short first_have_char
first_buffered_char:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
first_have_char:
    mov [bp-0ch],ax
    cmp word ptr [bp-0ch],2dh
    jne short first_not_minus
    mov ax,1
    jmp short first_sign_ready
first_not_minus:
    xor ax,ax
first_sign_ready:
    mov [bp-0eh],ax
    cmp word ptr [bp-0ch],2bh
    je short consume_sign
    cmp word ptr [bp-0eh],0
    je short signed_char_ready
consume_sign:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short sign_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short sign_from_buffer
sign_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short sign_char_ready
sign_from_buffer:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
sign_char_ready:
    mov [bp-0ch],ax
    jmp short parse_init
signed_char_ready:
    cmp word ptr [bp-0ch],-1
    jne short parse_init
    mov ax,4
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
parse_init:
    les bx,dword ptr [bp+0ah]
    fldz
    fstp tbyte ptr es:[bx]
    fwait
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    jne short first_digit
    jmp near ptr fractional_start
first_digit:
    mov word ptr [bp-16h],1
digit_loop:
    sub word ptr [bp-0ch],30h
    les bx,dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fmul dword ptr DGROUP:digit_ten
    mov ax,[bp-0ch]
    mov [bp-2],ax
    fild word ptr [bp-2]
    faddp st(1),st(0)
    les bx,dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short digit_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short digit_from_buffer
digit_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short digit_char_ready
digit_from_buffer:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
digit_char_ready:
    mov [bp-0ch],ax
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    je short fractional_start
    jmp near ptr digit_loop
fractional_start label near
    mov word ptr [bp-12h],0
    mov word ptr [bp-14h],0
    cmp word ptr [bp-0ch],2eh
    je short consume_decimal_point
    jmp near ptr exponent_start
consume_decimal_point:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short fraction_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short fraction_buffered
fraction_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short fraction_got_char
fraction_buffered:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
fraction_got_char:
    mov [bp-0ch],ax
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    jne short fraction_digit_prepared
    jmp near ptr exponent_start
fraction_digit_prepared:
    mov word ptr [bp-16h],1
fraction_digit_loop:
    sub word ptr [bp-0ch],30h
    les bx,dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fmul dword ptr DGROUP:digit_ten
    mov ax,[bp-0ch]
    mov [bp-2],ax
    fild word ptr [bp-2]
    faddp st(1),st(0)
    les bx,dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    sub word ptr [bp-14h],1
    sbb word ptr [bp-12h],0
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short fraction_next_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short fraction_next_buffered
fraction_next_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short fraction_next_got_char
fraction_next_buffered:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
fraction_next_got_char:
    mov [bp-0ch],ax
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    je short exponent_start
    jmp near ptr fraction_digit_loop

; Parse an optional signed decimal exponent only after mantissa digits.
exponent_start:
    cmp word ptr [bp-016h], 0
    jne short exponent_marker_check
    jmp near ptr scale_begin
exponent_marker_check:
    cmp word ptr [bp-0ch], 065h
    je short consume_exponent_marker
    cmp word ptr [bp-0ch], 045h
    je short consume_exponent_marker
    jmp near ptr scale_begin
consume_exponent_marker:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    mov ax, word ptr es:[bx+01eh]
    or ax, word ptr es:[bx+020h]
    je short exponent_marker_refill
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    inc word ptr es:[bx+01eh]
    mov ax, word ptr es:[bx+01eh]
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    cmp ax, word ptr es:[bx+022h]
    jb short exponent_marker_buffered
exponent_marker_refill:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short exponent_marker_got_char
exponent_marker_buffered:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    les bx, dword ptr es:[bx+01eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
exponent_marker_got_char:
    mov word ptr [bp-0ch], ax
    mov bx, word ptr [bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1], 2
    jne short exponent_present
    cmp word ptr [bp-0ch], 02bh
    je short exponent_present
    cmp word ptr [bp-0ch], 02dh
    jne short exponent_absent
exponent_present:
    mov ax, 1
    jmp short exponent_presence_ready
exponent_absent:
    xor ax, ax
exponent_presence_ready:
    mov word ptr [bp-016h], ax
    mov word ptr [bp-018h], 0
    mov word ptr [bp-01ah], 0
    cmp word ptr [bp-016h], 0
    jne short exponent_sign
    jmp near ptr invalid_exponent
exponent_sign:
    cmp word ptr [bp-0ch], 02dh
    jne short exponent_not_negative
    mov ax, 1
    jmp short exponent_sign_ready
exponent_not_negative:
    xor ax, ax
exponent_sign_ready:
    mov word ptr [bp-010h], ax
    cmp word ptr [bp-0ch], 02bh
    je short consume_exponent_sign
    cmp word ptr [bp-010h], 0
    je short exponent_digit_check
consume_exponent_sign:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    mov ax, word ptr es:[bx+01eh]
    or ax, word ptr es:[bx+020h]
    je short exponent_sign_refill
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    inc word ptr es:[bx+01eh]
    mov ax, word ptr es:[bx+01eh]
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    cmp ax, word ptr es:[bx+022h]
    jb short exponent_sign_buffered
exponent_sign_refill:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short exponent_sign_got_char
exponent_sign_buffered:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    les bx, dword ptr es:[bx+01eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
exponent_sign_got_char:
    mov word ptr [bp-0ch], ax
exponent_digit_check:
    mov bx, word ptr [bp-0ch]
    mov al, byte ptr DGROUP:__ctype[bx+1]
    mov ah, 0
    and ax, 2
    mov word ptr [bp-016h], ax
    cmp word ptr [bp-016h], 0
    jne short exponent_digit_loop
invalid_exponent:
    les bx, dword ptr [bp+0ah]
    fldz
    fstp tbyte ptr es:[bx]
    fwait
    jmp near ptr apply_exponent_sign

; Accumulate the exponent as a signed 32-bit value, capped at 49320.
exponent_digit_loop:
    cmp word ptr [bp-018h], 0
    jg short next_exponent_digit
    jl short accumulate_exponent_digit
    cmp word ptr [bp-01ah], 0c0a8h
    jae short next_exponent_digit
accumulate_exponent_digit:
    sub word ptr [bp-0ch], 030h
    mov cx, word ptr [bp-018h]
    mov bx, word ptr [bp-01ah]
    xor dx, dx
    mov ax, 0ah
    call F_LXMUL@
    push ax
    mov ax, word ptr [bp-0ch]
    push dx
    cwd
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    mov word ptr [bp-018h], bx
    mov word ptr [bp-01ah], cx
next_exponent_digit:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    mov ax, word ptr es:[bx+01eh]
    or ax, word ptr es:[bx+020h]
    je short exponent_digit_refill
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    inc word ptr es:[bx+01eh]
    mov ax, word ptr es:[bx+01eh]
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    cmp ax, word ptr es:[bx+022h]
    jb short exponent_digit_buffered
exponent_digit_refill:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short exponent_digit_got_char
exponent_digit_buffered:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx+2]
    les bx, dword ptr es:[bx+01eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
exponent_digit_got_char:
    mov word ptr [bp-0ch], ax
    mov bx, word ptr [bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1], 2
    je short apply_exponent_sign
    jmp near ptr exponent_digit_loop

; Combine explicit and fractional exponents, clamping to +/- 493200.
apply_exponent_sign:
    cmp word ptr [bp-010h], 0
    je short positive_exponent
    mov dx, word ptr [bp-018h]
    mov ax, word ptr [bp-01ah]
    add ax, 07970h
    adc dx, -8
    cmp dx, word ptr [bp-012h]
    jg short clamp_negative_exponent
    jl short subtract_exponent
    cmp ax, word ptr [bp-014h]
    jae short clamp_negative_exponent
subtract_exponent:
    mov dx, word ptr [bp-018h]
    mov ax, word ptr [bp-01ah]
    sub word ptr [bp-014h], ax
    sbb word ptr [bp-012h], dx
    jmp short scale_begin
clamp_negative_exponent:
    mov word ptr [bp-012h], 0fff8h
    mov word ptr [bp-014h], 07970h
    jmp short scale_begin
positive_exponent:
    mov ax, 7
    mov dx, 08690h
    sub dx, word ptr [bp-01ah]
    sbb ax, word ptr [bp-018h]
    cmp ax, word ptr [bp-012h]
    jl short clamp_positive_exponent
    jg short add_exponent
    cmp dx, word ptr [bp-014h]
    jbe short clamp_positive_exponent
add_exponent:
    mov dx, word ptr [bp-018h]
    mov ax, word ptr [bp-01ah]
    add word ptr [bp-014h], ax
    adc word ptr [bp-012h], dx
    jmp short scale_begin
clamp_positive_exponent:
    mov word ptr [bp-012h], 7
    mov word ptr [bp-014h], 08690h

; Predivide extremely small mantissas by 10^2466 before scaling.
scale_begin:
    cmp word ptr [bp-012h], -1
    jg short check_underflow
    jne short prescale_tiny
    cmp word ptr [bp-014h], 0ecbdh
    ja short check_underflow
prescale_tiny:
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fld tbyte ptr DGROUP:tiny_scale
    fdivp st(1),st(0)
    les bx, dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    add word ptr [bp-014h], 09a2h
    adc word ptr [bp-012h], 0

; The original range tests use -4931 and +4932, with unchecked input.
check_underflow:
    cmp word ptr [bp-012h], -1
    jg short check_overflow
    jge short check_underflow_low_word
    jmp near ptr underflow
check_underflow_low_word:
    cmp word ptr [bp-014h], 0ecbdh
    jae short check_overflow
    jmp near ptr underflow
check_overflow:
    cmp word ptr [bp-012h], 0
    jl short check_digits
    jle short check_overflow_low_word
    jmp near ptr overflow
check_overflow_low_word:
    cmp word ptr [bp-014h], 01344h
    jbe short check_digits
    jmp near ptr overflow
check_digits:
    cmp word ptr [bp-016h], 0
    jne short scale_init
    jmp near ptr finish

; Exponentiation by squaring: factor at BP-20h, base at BP-2Ah.
scale_init:
    xor cx, cx
    fld1
    fstp tbyte ptr [bp-020h]
    fld dword ptr DGROUP:digit_ten
    fstp tbyte ptr [bp-02ah]
    fwait
    cmp word ptr [bp-012h], 0
    jg short scale_nonnegative
    jl short scale_negative
    cmp word ptr [bp-014h], 0
    jae short scale_nonnegative
scale_negative:
    mov ax, 1
    jmp short scale_sign_ready
scale_nonnegative:
    xor ax, ax
scale_sign_ready:
    mov word ptr [bp-010h], ax
    cmp word ptr [bp-010h], 0
    jne short negate_exponent
    jmp near ptr power_loop_test
negate_exponent:
    mov dx, word ptr [bp-012h]
    mov ax, word ptr [bp-014h]
    neg dx
    neg ax
    sbb dx, 0
    mov word ptr [bp-012h], dx
    mov word ptr [bp-014h], ax
    jmp near ptr power_loop_test

; Check the factor multiplication against the original huge long double.
power_bit:
    test byte ptr [bp-014h], 1
    je short shift_exponent
    fld tbyte ptr DGROUP:__huge_ldble
    fld tbyte ptr [bp-020h]
    fdivp st(1),st(0)
    fld tbyte ptr [bp-02ah]
    fcompp
    fstsw word ptr [bp-2]
    fwait
    mov ax, word ptr [bp-2]
    sahf
    ja short factor_overflow
    fld tbyte ptr [bp-02ah]
    fld tbyte ptr [bp-020h]
    fmulp st(1),st(0)
    fstp tbyte ptr [bp-020h]
    fwait
    jmp short shift_exponent
factor_overflow:
    mov cx, 1
shift_exponent:
    mov dx, word ptr [bp-012h]
    mov ax, word ptr [bp-014h]
    sar dx, 1
    rcr ax, 1
    mov word ptr [bp-012h], dx
    mov word ptr [bp-014h], ax
    cmp word ptr [bp-012h], 0
    jl short power_loop_test
    jg short square_base
    cmp word ptr [bp-014h], 0
    jbe short power_loop_test

; Check the base square before multiplying.
square_base:
    fld tbyte ptr DGROUP:__huge_ldble
    fld tbyte ptr [bp-02ah]
    fdivp st(1),st(0)
    fld tbyte ptr [bp-02ah]
    fcompp
    fstsw word ptr [bp-2]
    fwait
    mov ax, word ptr [bp-2]
    sahf
    ja short square_overflow
    fld tbyte ptr [bp-02ah]
    fld tbyte ptr [bp-02ah]
    fmulp st(1),st(0)
    fstp tbyte ptr [bp-02ah]
    fwait
    jmp short power_loop_test
square_overflow:
    mov cx, 1
power_loop_test:
    cmp word ptr [bp-012h], 0
    jle short power_loop_low_word
    jmp near ptr power_bit
power_loop_low_word:
    jne short scale_ready
    cmp word ptr [bp-014h], 0
    jbe short scale_ready
    jmp near ptr power_bit
scale_ready:
    or cx, cx
    je short factor_unit_check
    jmp near ptr scaling_status

; Apply the computed factor unless it remains one or overflowed.
factor_unit_check:
    fld tbyte ptr [bp-020h]
    fld1
    fcompp
    fstsw word ptr [bp-2]
    fwait
    mov ax, word ptr [bp-2]
    sahf
    je short scaling_status
    cmp word ptr [bp-010h], 0
    je short scale_up_check
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fld tbyte ptr [bp-020h]
    fdivp st(1),st(0)
    jmp short store_scaled
scale_up_check:
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fld1
    fcompp
    fstsw word ptr [bp-2]
    fwait
    mov ax, word ptr [bp-2]
    sahf
    jae short multiply_factor
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fld tbyte ptr DGROUP:__huge_ldble
    fdivrp st(1),st(0)
    fld tbyte ptr [bp-020h]
    fcompp
    fstsw word ptr [bp-2]
    fwait
    mov ax, word ptr [bp-2]
    sahf
    ja short scale_overflow
multiply_factor:
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fld tbyte ptr [bp-020h]
    fmulp st(1),st(0)
store_scaled:
    les bx, dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    jmp short scaling_status
scale_overflow:
    mov cx, 1
scaling_status:
    or cx, cx
    je short finish
    cmp word ptr [bp-010h], 0
    je short overflow

; Original saturation and ERANGE behavior; retain the qword huge value.
underflow:
    les bx, dword ptr [bp+0ah]
    fldz
    jmp short store_saturation
overflow:
    fld qword ptr DGROUP:__huge_dble
    les bx, dword ptr [bp+0ah]
store_saturation:
    fstp tbyte ptr es:[bx]
    fwait
    mov word ptr DGROUP:_errno, 022h

; Apply the mantissa sign or set failbit, and eofbit for EOF.
finish:
    cmp word ptr [bp-016h], 0
    je short fail
    cmp word ptr [bp-0eh], 0
    je short parser_return
    les bx, dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fchs
    les bx, dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    jmp short parser_return
fail:
    cmp word ptr [bp-0ch], -1
    jne short fail_non_eof
    mov ax, 3
    jmp short set_failed_state
fail_non_eof:
    mov ax, 2
set_failed_state:
    push ax
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp, 6

; Return the original far istream reference, restoring saved registers.
parser_return:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
@istream@$brsh$qmg endp
_TEXTA ends
_DATA segment word public 'DATA'
digit_ten dd 10.0
; Borland's 10^2466 extended-precision scalar. A typed hex real literal
; preserves its value: TASM decimal conversion of 1e2466 is 11 ULP lower.
tiny_scale dt 5FFEEAB388127BCCB000r
_DATA ends
end
