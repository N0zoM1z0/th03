; Original Japanese Borland CRT MBCLEN; natural 16-bit source.
.8086
extrn __mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __mbclen
__mbclen proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov al,byte ptr es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz short one_byte
    mov ax,2
    jmp short end_length
one_byte:
    mov ax,1
end_length:
    pop di
    pop si
    pop bp
    retf
__mbclen endp
_TEXT ends
end
