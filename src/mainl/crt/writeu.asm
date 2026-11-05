; Reconstructed Japanese original Borland CRT writeu.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
extrn ___write:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _write
_write:
    jmp ___write
_TEXT ends
end
