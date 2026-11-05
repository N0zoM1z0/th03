; Original complete Japanese Borland multibyte string routine MBISL2.
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
public __ismbcl2

__ismbcl2:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,39071
    jc mbstring_mbisl2_0032
    cmp dx,60062
    ja mbstring_mbisl2_0032
    cmp dx,40956
    jna mbstring_mbisl2_0020
    cmp dx,57408
    jc mbstring_mbisl2_0032

mbstring_mbisl2_0020:
    mov al,dl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],8
    jz mbstring_mbisl2_0032
    mov ax,1
    jmp short mbstring_mbisl2_0034

mbstring_mbisl2_0032:
    xor ax,ax

mbstring_mbisl2_0034:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
