; Original complete Japanese Borland multibyte string routine FMBSNBCN.
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
public __fmbsnbcnt

__fmbsnbcnt:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov cx,[bp+10]
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short mbstring_fmbsnbcn_003b

mbstring_fmbsnbcn_0019:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsnbcn_0037
    mov bx,[bp-4]
    cmp byte ptr es:[bx+1],0
    jz mbstring_fmbsnbcn_0048
    inc word ptr [bp-4]

mbstring_fmbsnbcn_0037:
    dec cx
    inc word ptr [bp-4]

mbstring_fmbsnbcn_003b:
    or cx,cx
    jna mbstring_fmbsnbcn_0048
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsnbcn_0019

mbstring_fmbsnbcn_0048:
    mov ax,[bp-4]
    xor dx,dx
    sub ax,[bp+6]
    sbb dx,0
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXT ends
end
