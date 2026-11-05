; Original Borland stdiobuf::pbackfail routes to DOS ungetc(FILE*).
.8086
extrn _ungetc:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@pbackfail$qi
@stdiobuf@pbackfail$qi proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+28h]
    push word ptr es:[bx+26h]
    push word ptr [bp+10]
    call _ungetc
    add sp,6
    pop di
    pop si
    pop bp
    retf
@stdiobuf@pbackfail$qi endp
_TEXTA ends
end
