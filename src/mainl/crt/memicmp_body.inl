; Uppercase unsigned bytes through the original delegate and subtract WORD results.
; Bounded original member body; wrapper owns its public and native segments.
MEMORY_CASE_COMPARE macro api_name,case_converter
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 32
    call case_converter
    pop cx
    pop dx
    sub dx, ax
    mov ax, dx
    or ax, ax
    je short advance_both_pointers
    jmp short compare_return
advance_both_pointers:
    inc word ptr [bp+6]
    inc word ptr [bp+0ah]
test_remaining_count:
    mov ax, word ptr [bp+0eh]
    dec word ptr [bp+0eh]
    or ax, ax
    ja short compare_next_byte
    xor ax, ax
compare_return:
    pop di
    pop si
    pop bp
    retf

org 16
    call case_converter
    pop cx
    push ax
    les bx, dword ptr [bp+0ah]
    mov al, byte ptr es:[bx]
    mov ah, 0
    push ax

org 0
api_name label far
    push bp
    mov bp, sp
    push si
    push di
    jmp short test_remaining_count
compare_next_byte:
    les bx, dword ptr [bp+6]
    mov al, byte ptr es:[bx]
    mov ah, 0
    push ax
endm
