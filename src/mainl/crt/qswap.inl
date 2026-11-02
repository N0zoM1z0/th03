; Recovered first near helper of the original 756-byte DOS qsort TU.
; Called with two far addresses and callee-cleanup RET 8, with a WORD
; element width in the original 6-byte qsort-owned BSS at offset 4.
qsort_swap proc near
    push bp
    mov bp,sp
    push si
    push di
    push ds
    cld
    mov cx,qsort_width
    les di,dword ptr [bp+4]
    lds si,dword ptr [bp+8]
    shr cx,1
    jae short word_swaps
    mov al,es:[di]
    movsb
    mov [si-1],al
    je short swap_done
word_swaps:
    mov ax,es:[di]
    movsw
    mov [si-2],ax
    loop word_swaps
swap_done:
    pop ds
    pop di
    pop si
    pop bp
    ret 8
qsort_swap endp
