; Reconstructed Japanese original Borland CRT readu.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
extrn ___read:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _read
_read:
    jmp ___read
_TEXT ends
end
