; Original complete Japanese Borland multibyte string routine MBSINC.
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
public __mbsinc

__mbsinc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz mbstring_mbsinc_0013
    xor dx,dx
    xor ax,ax
    jmp short mbstring_mbsinc_002e

mbstring_mbsinc_0013:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsinc_0027
    inc word ptr [bp+6]

mbstring_mbsinc_0027:
    mov dx,[bp+8]
    mov ax,[bp+6]
    inc ax

mbstring_mbsinc_002e:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
