; Original Japanese Borland CRT fnsplit; natural 16-bit source.
.8086
extrn ___fnsplit:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fnsplit
_fnsplit proc far
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
    call ___fnsplit
    add sp,20
    pop di
    pop si
    pop bp
    retf
_fnsplit endp
_TEXT ends
end
