; Proved original stream wrapper family; each TU retains its own native owner.
STREAM_WORD_MANIP macro api_name,ios_member_offset
; Native source chunks retain original logical FIXUPP chronology.

org 109
    mov word ptr es:[bx],offset _TEXTA:manipulator_apply
    mov ax, word ptr [bp-2]
    mov word ptr es:[bx+4], ax
manip_constructed:
    mov dx, word ptr [bp-4]
    mov ax, word ptr [bp-6]
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 103
    mov word ptr es:[bx+2],seg manipulator_apply

org 84
    call @$bnew$qui
    pop cx
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
manip_storage_ready:
    or ax, dx
    je short manip_constructed
    les bx, dword ptr [bp-6]

org 0
manipulator_apply label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-2], ax
    les bx, dword ptr [bp+6]
    add bx, ios_member_offset
    mov word ptr [bp-6], bx
    mov ax, word ptr es:[bx]
    mov ax, word ptr [bp-2]
    mov word ptr es:[bx], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
api_name label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-2], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, word ptr [bp-4]
    je short manip_allocate
    mov ax, word ptr [bp-6]
    jmp short manip_storage_ready
manip_allocate:
    mov ax, 6
    push ax
endm
