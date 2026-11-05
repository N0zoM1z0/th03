; Reconstructed Japanese original Borland CRT cibmwhxy.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
extrn __IBM_VIDEOINT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_WHEREXY
__IBM_WHEREXY proc near
    push si
    push di
    mov ah,3
    mov bh,0
    call __IBM_VIDEOINT
    mov ax,dx
    pop di
    pop si
    ret
__IBM_WHEREXY endp
_TEXT ends
end
