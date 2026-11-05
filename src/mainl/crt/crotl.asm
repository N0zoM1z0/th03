; Original Borland far unsigned-char rotate-left helper.
; AL receives the byte at SS:SP+4 and CL the rotate count; AH is zeroed.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __crotl
__crotl:
    mov bx,sp
    mov al,byte ptr ss:[bx+4]
    xor ah,ah
    mov cx,word ptr ss:[bx+6]
    rol al,cl
    retf
_TEXT ends
end
