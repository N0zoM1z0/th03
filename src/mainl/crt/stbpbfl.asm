; Reconstructed Japanese original Borland CRT stbpbfl.
; Original 16-bit ABI, real instructions and symbolic references.
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
public @streambuf@pbackfail$qi
@streambuf@pbackfail$qi proc far
    push si
    push di
    mov ax,0ffffh
    pop di
    pop si
    retf
@streambuf@pbackfail$qi endp
_TEXTA ends
end
