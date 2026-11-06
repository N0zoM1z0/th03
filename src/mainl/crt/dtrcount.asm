; Original Japanese Borland dtrcount: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
public __DestructorCount
__DestructorCount dd ?
_BSS ends
end
