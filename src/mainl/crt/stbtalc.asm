; Original signed high-word guard and preincremented 32-bit bit number.
; Original Japanese Borland stbtalc: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @ios@nextbit:dword
extrn F_LXLSH@:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@bitalloc$qv
; Complete disjoint instruction chunks preserve original native field order.

org 43
    call F_LXLSH@
bitalloc_return:
    pop di
    pop si
    retf

org 33
    adc word ptr DGROUP:@ios@nextbit+2, 0
    xor dx, dx
    mov ax, 1

org 29
    mov cx, word ptr DGROUP:@ios@nextbit

org 24
allocate_next_bit:
    add word ptr DGROUP:@ios@nextbit, 1

org 11
    cmp word ptr DGROUP:@ios@nextbit, 01fh
    jb short allocate_next_bit
no_bits_available:
    xor dx, dx
    xor ax, ax
    jmp short bitalloc_return

org 2
    cmp word ptr DGROUP:@ios@nextbit+2, 0
    jl short allocate_next_bit
    jne short no_bits_available

org 0
@ios@bitalloc$qv label far
    push si
    push di
_TEXTA ends
end
