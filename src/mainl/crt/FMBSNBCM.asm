; Original complete Japanese Borland multibyte string routine FMBSNBCM.
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
public __fmbsnbcmp

; Actual original Borland imported-byte-table reference region.
org 109
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsnbcm_009b
    cmp word ptr [bp+14],0
    jna mbstring_fmbsnbcm_00be
    dec word ptr [bp+14]
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsnbcm_008a
    xor dx,dx
    jmp short mbstring_fmbsnbcm_009b

mbstring_fmbsnbcm_008a:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]

mbstring_fmbsnbcm_009b:
    cmp [bp-2],dx
    jz mbstring_fmbsnbcm_00af
    cmp [bp-2],dx
    jnc mbstring_fmbsnbcm_00aa
    mov ax,65535
    jmp short mbstring_fmbsnbcm_00ad

mbstring_fmbsnbcm_00aa:
    mov ax,1

mbstring_fmbsnbcm_00ad:
    jmp short mbstring_fmbsnbcm_00c0

mbstring_fmbsnbcm_00af:
    cmp word ptr [bp-2],0
    jz mbstring_fmbsnbcm_00be

mbstring_fmbsnbcm_00b5:
    cmp word ptr [bp+14],0
    jna mbstring_fmbsnbcm_00be
    jmp near ptr mbstring_fmbsnbcm_000b

mbstring_fmbsnbcm_00be:
    xor ax,ax

mbstring_fmbsnbcm_00c0:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 35
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsnbcm_005a
    cmp word ptr [bp+14],0
    ja mbstring_fmbsnbcm_0033
    jmp near ptr mbstring_fmbsnbcm_00be

mbstring_fmbsnbcm_0033:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsnbcm_0043
    mov word ptr [bp-2],0
    jmp short mbstring_fmbsnbcm_005a

mbstring_fmbsnbcm_0043:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]

mbstring_fmbsnbcm_005a:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov dx,ax
    inc word ptr [bp+10]
    mov al,dl
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsnbcmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_fmbsnbcm_00b5

mbstring_fmbsnbcm_000b:
    dec word ptr [bp+14]
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov [bp-2],ax
    inc word ptr [bp+6]
    mov al,[bp-2]
    mov ah,0
    mov bx,ax
_TEXT ends
end
