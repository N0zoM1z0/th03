; Original Japanese Borland files2: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
include stdio_tmp.inc
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __nfile,__openfd
__nfile dw 20
__openfd label word
; Original initial WORD states for stdin/out/err/aux/printer, then unused descriptors.
dw 6001h,6002h,6002h,0a004h,0a002h
dw 15 dup (0)
_DATA ends
end
