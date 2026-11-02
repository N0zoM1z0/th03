; Original Borland DOS __scantol: counted input scanner, radix conversion,
; overflow saturation, optional sign and output count/status side effects.
; Private digit_for_radix uses BL=input, CL=radix, returns BX digit value
; with Carry clear when valid and set when invalid. The inc SP/inc SP
; path intentionally discards the saved BX word on success.
; Public __scantol uses near cdecl with input/unget near callbacks;
; the output count and scan status live through original far pointers.
; Do not add null guards, data-table opcodes or non-original padding.
.8086
extrn __ctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
digit_for_radix proc near
    push si
    push di
    push bx
    sub bl, 030h
    jb short not_a_digit
    cmp bl, 9
    jbe short test_radix
    cmp bl, 02ah
    ja short normalize_high_letter
    sub bl, 7
    jmp short check_letter_digit
normalize_high_letter:
    sub bl, 027h
check_letter_digit:
    cmp bl, 9
    jbe short not_a_digit
test_radix:
    cmp bl, cl
    jae short not_a_digit
    inc sp
    inc sp
    clc
    mov bh, 0
    jmp short digit_done
not_a_digit:
    pop bx
    stc
digit_done:
    pop di
    pop si
    ret
digit_for_radix endp
public __scantol
__scantol proc near
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov byte ptr [bp-1], 0
    mov word ptr [bp-4], 0
    mov word ptr [bp-6], 1
scan_next_leading_space:
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    or ax, ax
    jl short handle_eof
    cbw
    xchg bx, ax
    test bl, 080h
    jne short scan_optional_sign
    mov di, offset __ctype+1
    test byte ptr [bx+di], 1
    jne short scan_next_leading_space
scan_optional_sign:
    xchg bx, ax
    dec word ptr [bp+0eh]
    jl short reject_invalid_radix
    cmp al, 02bh
    je short scan_after_sign
    cmp al, 02dh
    jne short setup_accumulator
    inc byte ptr [bp-1]
scan_after_sign:
    dec word ptr [bp+0eh]
    jl short reject_invalid_radix
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    or ax, ax
    jl short handle_eof
setup_accumulator:
    sub si, si
    mov di, si
    mov cx, word ptr [bp+0ch]
    jcxz short infer_radix
    cmp cx, 024h
    ja short reject_invalid_radix
    cmp cl, 2
    jb short reject_invalid_radix
    cmp al, 030h
    jne short convert_first_digit
    cmp cl, 010h
    jne short scan_digits
    dec word ptr [bp+0eh]
    jl short scan_width_exhausted
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    cmp al, 078h
    je short scan_digits
    cmp al, 058h
    je short scan_digits
    jmp near ptr convert_current_digit
handle_eof:
    mov word ptr [bp-6], 0ffffh
    jmp short scan_cleanup
reject_invalid_radix:
    mov word ptr [bp-6], 0
scan_cleanup:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-4]
    sub ax, ax
    cwd
    jmp near ptr write_scan_outputs
scan_width_exhausted:
    jmp near ptr finalize_accumulator
infer_radix:
    cmp al, 030h
    mov word ptr [bp+0ch], 0ah
    jne short convert_first_digit
    dec word ptr [bp+0eh]
    jl short scan_width_exhausted
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    mov word ptr [bp+0ch], 8
    cmp al, 078h
    je short scan_116
    cmp al, 058h
    jne short convert_current_digit
scan_116:
    mov word ptr [bp+0ch], 010h
scan_digits:
    jmp short fetch_next_digit
convert_first_digit:
    mov cx, word ptr [bp+0ch]
    xchg bx, ax
    call digit_for_radix
    xchg bx, ax
    jb short reject_invalid_radix
    xchg si, ax
    jmp short fetch_next_digit
accumulate_digit:
    xchg si, ax
    mul word ptr [bp+0ch]
    add si, ax
    adc di, dx
    jne short read_next_digit
fetch_next_digit:
    dec word ptr [bp+0eh]
    jl short finalize_accumulator
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
convert_current_digit:
    mov cx, word ptr [bp+0ch]
    xchg bx, ax
    call digit_for_radix
    xchg bx, ax
    jae short accumulate_digit
    jmp short unget_final_character
accumulate_long:
    xchg si, ax
    mul cx
    xchg di, ax
    xchg cx, dx
    mul dx
    add si, di
    adc ax, cx
    xchg di, ax
    adc dl, dh
    jne short overflow_saturate
read_next_digit:
    dec word ptr [bp+0eh]
    jl short finalize_accumulator
    inc word ptr [bp-4]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call word ptr [bp+4]
    pop cx
    pop cx
    mov cx, word ptr [bp+0ch]
    xchg bx, ax
    call digit_for_radix
    xchg bx, ax
    jae short accumulate_long
unget_final_character:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push ax
    call word ptr [bp+6]
    add sp, 6
    dec word ptr [bp-4]
finalize_accumulator:
    mov dx, di
    xchg si, ax
    cmp byte ptr [bp-1], 0
    je short write_scan_outputs
    neg dx
    neg ax
    sbb dx, 0
write_scan_outputs:
    les di, dword ptr [bp+010h]
    mov bx, word ptr [bp-4]
    add word ptr es:[di], bx
    les di, dword ptr [bp+014h]
    mov bx, word ptr [bp-6]
    mov word ptr es:[di], bx
    jmp short return_scantol
overflow_saturate:
    mov ax, 0ffffh
    mov dx, 07fffh
    add al, byte ptr [bp-1]
    adc ah, 0
    adc dx, 0
    mov word ptr [bp-6], 2
    jmp short write_scan_outputs
return_scantol:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
__scantol endp
_TEXT ends
end
