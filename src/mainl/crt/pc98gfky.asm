; Reconstructed Borland 16-bit large-model pc98gfky.
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
public _pc98getfkey

_pc98getfkey:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds dx, dword ptr [bp + 8]
    mov cl, 0ch
    mov ax, word ptr [bp + 6]
    int 0dch
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
