; Original complete Japanese Borland multibyte string routine MBCCPY.
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
public __mbccpy

__mbccpy:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+10]
    mov al,es:[bx]
    les bx,[bp+6]
    mov es:[bx],al
    les bx,[bp+10]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbccpy_002d
    mov bx,[bp+10]
    mov al,es:[bx+1]
    les bx,[bp+6]
    mov es:[bx+1],al

mbstring_mbccpy_002d:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
