; Original Japanese Borland large-model CRT member: scantod.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn __cvtfak:word,__ScanTodVector:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _SCNSEG,_DATA
_SCNSEG segment word public 'DATA'
_SCNSEG ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __scantod,__scanrslt,__scanpop
__scantod:
    jmp word ptr __ScanTodVector
__scanrslt:
    jmp word ptr __ScanTodVector+2
__scanpop:
    jmp word ptr __ScanTodVector+4
_TEXT ends
end
