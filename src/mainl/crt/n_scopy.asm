; Original near-call callee-pop8 far-pointer block copy; CX is byte length.
; Shift/ADC preserves the odd trailing byte after REP MOVSW.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_SCOPY@
N_SCOPY@:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds si,dword ptr [bp+4]
    les di,dword ptr [bp+8]
    cld
    shr cx,1
    rep movsw
    adc cx,cx
    rep movsb
    pop ds
    pop di
    pop si
    pop bp
    ret 8
_TEXT ends
end
