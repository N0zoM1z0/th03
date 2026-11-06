; Original Japanese Borland ccomputn: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __NEC_RESET_VRAM_ACCESS:near
extrn __NEC_START_VRAM_ACCESS:near
extrn __NEC_END_VRAM_ACCESS:near
extrn __NEC_OUTPUT_CHAR:near
extrn __IBM_RESET_VRAM_ACCESS:near
extrn __IBM_START_VRAM_ACCESS:near
extrn __IBM_END_VRAM_ACCESS:near
extrn __IBM_OUTPUT_CHAR:near
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __RESET_VRAM_ACCESS
public __START_VRAM_ACCESS
public __END_VRAM_ACCESS
public __OUTPUT_CHAR
; Complete disjoint instruction chunks follow original OMF field chronology.

org 110
    call __IBM_OUTPUT_CHAR
output_return:
    pop di
    pop si
    pop bp
    ret 2

org 102
output_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short output_return
    push ax

org 97
    call __NEC_OUTPUT_CHAR
    jmp short output_return

org 89
    cmp word ptr DGROUP:___conio_type, 2
    jne short output_ibm
    push ax

org 75
    call __IBM_END_VRAM_ACCESS
end_return:
    pop di
    pop si
    ret
__OUTPUT_CHAR label near
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+4]

org 68
end_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short end_return

org 63
    call __NEC_END_VRAM_ACCESS
    jmp short end_return

org 56
    cmp word ptr DGROUP:___conio_type, 2
    jne short end_ibm

org 48
    call __IBM_START_VRAM_ACCESS
start_return:
    pop di
    pop si
    ret
__END_VRAM_ACCESS label near
    push si
    push di

org 41
start_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short start_return

org 36
    call __NEC_START_VRAM_ACCESS
    jmp short start_return

org 29
    cmp word ptr DGROUP:___conio_type, 2
    jne short start_ibm

org 21
    call __IBM_RESET_VRAM_ACCESS
reset_return:
    pop di
    pop si
    ret
__START_VRAM_ACCESS label near
    push si
    push di

org 14
reset_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short reset_return

org 9
    call __NEC_RESET_VRAM_ACCESS
    jmp short reset_return

org 2
    cmp word ptr DGROUP:___conio_type, 2
    jne short reset_ibm

org 0
__RESET_VRAM_ACCESS label near
    push si
    push di
_TEXT ends
end
