; Original Japanese Borland fmode: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __fmode
__fmode dw 04000h
public __notUmask
__notUmask dw 0ffffh
_DATA ends
end
