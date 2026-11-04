; Reconstructed Borland 16-bit large-model lrotl.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __lrotl

__lrotl:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    mov dx, word ptr [bp + 8]
    mov cx, word ptr [bp + 0ah]
    and cx, 1fh
    je label_001c

label_0013:
    rcl ax, 1
    rcl dx, 1
    adc ax, 0
    loop label_0013

label_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
