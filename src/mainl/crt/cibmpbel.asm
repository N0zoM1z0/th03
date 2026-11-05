; Reconstructed Japanese original Borland CRT cibmpbel.
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
public ___ibm_cputbell
___ibm_cputbell proc near
    push si
    push di
    mov ah,0eh
    mov al,7
    call __IBM_VIDEOINT
    pop di
    pop si
    retf
___ibm_cputbell endp
_TEXT ends
end
