; Original Borland far unsigned-char rotate-right helper.
; Far caller retains argument cleanup; AH is cleared on return.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __crotr
__crotr:
    mov bx,sp
    mov al,byte ptr ss:[bx+4]
    xor ah,ah
    mov cx,word ptr ss:[bx+6]
    ror al,cl
    retf
_TEXT ends
end
