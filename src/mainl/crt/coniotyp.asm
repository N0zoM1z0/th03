; Original Japanese Borland coniotyp: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
extrn ___conio_type_init:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public ___conio_type
___conio_type dw 00h
_DATA ends
end
