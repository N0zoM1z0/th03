; Original complete Japanese Borland multibyte string routine MBSNCCNT.
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
public __mbsnccnt

__mbsnccnt:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+10]
    xor cx,cx
    jmp short mbstring_mbsnccnt_0033

mbstring_mbsnccnt_000c:
    dec dx
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnccnt_002f
    inc word ptr [bp+6]
    or dx,dx
    jna mbstring_mbsnccnt_0040
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_mbsnccnt_0040
    dec dx

mbstring_mbsnccnt_002f:
    inc cx
    inc word ptr [bp+6]

mbstring_mbsnccnt_0033:
    or dx,dx
    jna mbstring_mbsnccnt_0040
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnccnt_000c

mbstring_mbsnccnt_0040:
    mov ax,cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
