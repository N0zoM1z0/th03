; Original complete Japanese Borland multibyte string routine MBSLEN.
; Native real 8086 CODE with original far/near MBCS buffer convention,
; original __ctype/__mbctype+1 and signed/unsigned return flags.
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
public __mbslen

__mbslen:
    push bp
    mov bp,sp
    push si
    push di
    xor dx,dx
    jmp short mbstring_mbslen_002a

mbstring_mbslen_0009:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbslen_0026
    inc word ptr [bp+6]
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_mbslen_0033

mbstring_mbslen_0026:
    inc word ptr [bp+6]
    inc dx

mbstring_mbslen_002a:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbslen_0009

mbstring_mbslen_0033:
    mov ax,dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
