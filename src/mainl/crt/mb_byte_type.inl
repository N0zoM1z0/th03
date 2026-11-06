; States: 0 single, 1 lead, 2 trail, -1 illegal; preserve unsigned table indexing.
; Bounded original member body; wrapper owns its public and native segments.
MB_BYTE_TYPE macro api_name
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 85
    test byte ptr DGROUP:__mbctype[bx+1], 3
    je short illegal_byte
single_byte:
    xor ax, ax
    jmp short byte_type_return
illegal_byte:
    mov ax, 0ffffh
byte_type_return:
    pop di
    pop si
    pop bp
    retf

org 72
    test byte ptr DGROUP:__ctype[bx+1], 0deh
    jne short single_byte
    mov al, dl
    mov ah, 0
    mov bx, ax

org 54
    test byte ptr DGROUP:__mbctype[bx+1], 4
    je short classify_single_byte
    mov ax, 1
    jmp short byte_type_return
classify_single_byte:
    mov al, dl
    mov ah, 0
    mov bx, ax

org 22
    test byte ptr DGROUP:__mbctype[bx+1], 8
    je short illegal_byte
    mov ax, 2
    jmp short byte_type_return
classify_nontrail_state:
    or ax, ax
    je short classify_lead_or_single
    cmp ax, 2
    je short classify_lead_or_single
    cmp ax, 0ffffh
    jne short illegal_byte
classify_lead_or_single:
    mov al, dl
    mov ah, 0
    mov bx, ax

org 0
api_name label far
    push bp
    mov bp, sp
    push si
    push di
    mov dl, byte ptr [bp+6]
    mov ax, word ptr [bp+8]
    cmp ax, 1
    jne short classify_nontrail_state
    mov al, dl
    mov ah, 0
    mov bx, ax
endm
