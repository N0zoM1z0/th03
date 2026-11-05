; Original complete Japanese Borland multibyte string routine FMBSNEXT.
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
public __fmbsnextc

__fmbsnextc:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsnext_002c
    mov bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov cl,8
    shl ax,cl
    mov dl,es:[bx+1]
    mov dh,0
    or ax,dx
    jmp short mbstring_fmbsnext_0034

mbstring_fmbsnext_002c:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0

mbstring_fmbsnext_0034:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
