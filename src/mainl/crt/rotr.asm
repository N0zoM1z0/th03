; Reconstructed Borland 16-bit large-model rotr.
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
public __rotr

__rotr:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    mov cx, word ptr [bp + 8]
    ror ax, cl
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
