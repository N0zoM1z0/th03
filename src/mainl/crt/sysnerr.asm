; Original Japanese Borland sysnerr: complete CRT source owner.
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
public __sys_nerr
__sys_nerr dw 030h
_DATA ends
end
