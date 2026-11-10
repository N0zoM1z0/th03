; TH03 OP's original master.lib IRAND, retained as a symbolic source include.
; The seed belongs to the original rand[data].asm DATA owner, not here.
; Uses its original 8086 32-bit LCG: seed = seed * 0x015A4E35 + 1.
; Returns the top fifteen bits in AX; preserves the original CX/DX/FLAGS effects.

HI_MUL equ 015ah
LO_MUL equ 04e35h

func IRAND
    mov ax, LO_MUL
    mul word ptr random_seed+2
    mov cx, ax
    mov ax, HI_MUL
    mul word ptr random_seed
    add cx, ax
    mov ax, LO_MUL
    mul word ptr random_seed
    add ax, 1
    adc dx, cx
    mov word ptr random_seed, ax
    mov ax, dx
    mov word ptr random_seed+2, ax
    and ah, 7fh
    ret
endfunc
