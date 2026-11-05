; Original far-call sibling of N_SCOPY@: identical byte-count handling,
; but return address occupies four stack bytes; two original public aliases.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public F_SCOPY@,SCOPY@
F_SCOPY@:
SCOPY@:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+0ah]
    cld
    shr cx,1
    rep movsw
    adc cx,cx
    rep movsb
    pop ds
    pop di
    pop si
    pop bp
    retf 8
_TEXT ends
end
