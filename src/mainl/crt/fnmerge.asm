; Reconstructed Japanese original Borland CRT fnmerge.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
extrn __makepath:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fnmerge
_fnmerge proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+24]
    push word ptr [bp+22]
    push word ptr [bp+20]
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __makepath
    add sp,20
    pop di
    pop si
    pop bp
    retf
_fnmerge endp
_TEXT ends
end
