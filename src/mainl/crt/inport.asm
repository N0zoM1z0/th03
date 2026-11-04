; Reconstructed Borland 16-bit large-model inport.
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
public _inport,_inportb,_inpw,_inp

_inport:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    in ax, dx
    pop di
    pop si
    pop bp
    retf

_inportb:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    in al, dx
    xor ah, ah
    pop di
    pop si
    pop bp
    retf

_inpw:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    in ax, dx
    pop di
    pop si
    pop bp
    retf

_inp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    in al, dx
    xor ah, ah
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
