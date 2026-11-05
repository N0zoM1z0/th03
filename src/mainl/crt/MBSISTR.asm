; Original complete Japanese Borland multibyte string routine MBSISTR.
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
public __ismbstrail

__ismbstrail:
    push bp
    mov bp,sp
    push si
    push di
    jmp short mbstring_mbsistr_003c

mbstring_mbsistr_0007:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsistr_0039
    inc word ptr [bp+6]
    mov dx,[bp+8]
    mov ax,[bp+6]
    cmp dx,[bp+12]
    jnz mbstring_mbsistr_0030
    cmp ax,[bp+10]
    jnz mbstring_mbsistr_0030
    mov ax,1
    jmp short mbstring_mbsistr_004f

mbstring_mbsistr_0030:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_mbsistr_004d

mbstring_mbsistr_0039:
    inc word ptr [bp+6]

mbstring_mbsistr_003c:
    mov ax,[bp+6]
    cmp ax,[bp+10]
    ja mbstring_mbsistr_004d
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsistr_0007

mbstring_mbsistr_004d:
    xor ax,ax

mbstring_mbsistr_004f:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
