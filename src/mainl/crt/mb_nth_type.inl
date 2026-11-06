; Scan through the requested signed index, preserving lead/trail state and CBW result.
; Bounded original member body; wrapper owns its public and native segments.
MB_NTH_TYPE macro api_name
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 55
    test byte ptr DGROUP:__mbctype[bx+1], 8
    je short invalid_trail_byte
    mov al, 2
    jmp short store_byte_type
invalid_trail_byte:
    mov al, 0ffh
store_byte_type:
    mov cl, al
    cmp dx, word ptr [bp+0ah]
    jl short advance_byte
    cbw
    jmp short nth_type_return
advance_byte:
    inc dx
test_requested_index:
    cmp dx, word ptr [bp+0ah]
    jle short scan_current_byte
no_character:
    mov ax, 0ffffh
nth_type_return:
    pop di
    pop si
    pop bp
    retf

org 34
    test byte ptr DGROUP:__mbctype[bx+1], 4
    je short single_byte
    mov al, 1
    jmp short store_byte_type
single_byte:
    mov al, 0
    jmp short store_byte_type
classify_trail_byte:
    mov al, bl
    mov ah, 0
    mov bx, ax

org 0
api_name label far
    push bp
    mov bp, sp
    push si
    push di
    mov cl, 0ffh
    xor dx, dx
    jmp short test_requested_index
scan_current_byte:
    les bx, dword ptr [bp+6]
    add bx, dx
    mov bl, byte ptr es:[bx]
    or bl, bl
    je short no_character
    cmp cl, 1
    je short classify_trail_byte
    mov al, bl
    mov ah, 0
    mov bx, ax
endm
