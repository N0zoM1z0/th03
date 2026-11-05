; Original ostream::write: full 16-bit far binary sputn and ios state flow.
.8086
extrn @ios@setstate$qi:far
extrn @streambuf@sputn$qnxci:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@write$qnxci
@ostream@write$qnxci proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+0ah],086h
    jnz short return_stream
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@sputn$qnxci
    add sp,10
    cmp ax,[bp+14]
    jz short return_stream
    mov ax,4
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
return_stream:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@ostream@write$qnxci endp
_TEXTA ends
end
