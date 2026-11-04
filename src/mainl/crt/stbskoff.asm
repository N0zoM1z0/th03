; Reconstructed Borland 16-bit large-model stbskoff.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@seekoff$ql12ios@seek_diri

@streambuf@seekoff$ql12ios@seek_diri:
    push si
    push di
    mov dx, 0ffffh
    mov ax, 0ffffh
    pop di
    pop si
    retf
_TEXTA ends
end
