; Reconstructed Japanese original Borland CRT cnecpbel.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
extrn __NEC_VIDEOINTDC:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___nec_cputbell
___nec_cputbell proc near
    push si
    push di
    mov cl,10h
    mov ah,0
    mov dl,7
    call __NEC_VIDEOINTDC
    pop di
    pop si
    retf
___nec_cputbell endp
_TEXT ends
end
