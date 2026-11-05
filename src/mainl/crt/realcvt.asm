; Original Japanese Borland large-model CRT member: realcvt.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn __cvtfak:word,__RealCvtVector:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _CVTSEG,_DATA
_CVTSEG segment word public 'DATA'
_CVTSEG ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __REALCVT
__REALCVT:
    jmp word ptr __RealCvtVector
_TEXT ends
end
