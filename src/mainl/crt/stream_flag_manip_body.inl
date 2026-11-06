; Proved original stream wrapper family; each TU retains its own native owner.
STREAM_FLAG_MANIP macro api_name,flag_method
; Native source chunks retain original logical FIXUPP chronology.

org 106
    mov word ptr es:[bx],offset _TEXTA:manipulator_apply
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr es:[bx+6], dx
    mov word ptr es:[bx+4], ax
manip_constructed:
    mov dx, word ptr [bp-6]
    mov ax, word ptr [bp-8]
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 100
    mov word ptr es:[bx+2],seg manipulator_apply

org 81
    call @$bnew$qui
    pop cx
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
manip_storage_ready:
    or ax, dx
    je short manip_constructed
    les bx, dword ptr [bp-8]

org 17
    call flag_method
    add sp, 8
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf
api_name label far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp+0ch]
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    or ax, word ptr [bp-6]
    je short manip_allocate
    mov ax, word ptr [bp-8]
    jmp short manip_storage_ready
manip_allocate:
    mov ax, 8
    push ax

org 0
manipulator_apply label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
endm
