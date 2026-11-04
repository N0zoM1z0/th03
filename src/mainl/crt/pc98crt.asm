; Reconstructed Borland 16-bit large-model pc98crt.
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
public _pc98crt

_pc98crt:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov cx, word ptr [bp + 0ah]
    mov bx, word ptr [bp + 0ch]
    mov ah, byte ptr [bp + 6]
    mov al, dl
    int 18h
    xor ah, ah
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
