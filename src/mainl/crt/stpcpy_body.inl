; Copy the original strlen+1 WORD count; return destination offset+strlen unchanged segment.
; Bounded original member body; wrapper owns its public and native segments.
COPY_STRING_END macro api_name
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 38
    call _memcpy
    add sp, 0ah
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, word ptr [bp-2]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 14
    call _strlen
    pop cx
    pop cx
    mov word ptr [bp-2], ax
    inc ax
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
api_name label far
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
endm
