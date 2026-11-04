; Reconstructed Borland 16-bit large-model JISSPACE.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _jisspace

_jisspace:
    push bp
    mov bp, sp
    push si
    push di
    cmp word ptr [bp + 6], 8140h
    jne label_0011
    mov ax, 1
    jmp short label_0013

label_0011:
    xor ax, ax

label_0013:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
