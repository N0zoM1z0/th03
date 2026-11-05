; Original complete Japanese Borland multibyte string routine FMBSDEC.
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
public __fmbsdec

; Actual original Borland imported-byte-table reference region.
org 83
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsdec_0065

mbstring_fmbsdec_005a:
    dec word ptr [bp-4]
    mov ax,[bp-4]
    cmp ax,[bp+6]
    jnc mbstring_fmbsdec_0049

mbstring_fmbsdec_0065:
    mov ax,[bp+10]
    xor dx,dx
    sub ax,[bp-4]
    sbb dx,0
    and ax,1
    mov dx,[bp+12]
    push ax
    mov ax,[bp+10]
    pop bx
    sub ax,bx

mbstring_fmbsdec_007d:
    dec ax

mbstring_fmbsdec_007e:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 61
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsdec_005a
    mov ax,[bp-4]
    jmp short mbstring_fmbsdec_007d

mbstring_fmbsdec_0049:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsdec:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz mbstring_fmbsdec_0020
    mov ax,[bp+10]
    or ax,[bp+12]
    jz mbstring_fmbsdec_0020
    mov ax,[bp+10]
    cmp ax,[bp+6]
    ja mbstring_fmbsdec_0026

mbstring_fmbsdec_0020:
    xor dx,dx
    xor ax,ax
    jmp short mbstring_fmbsdec_007e

mbstring_fmbsdec_0026:
    mov dx,[bp+12]
    mov ax,[bp+10]
    dec ax
    mov [bp-2],dx
    mov [bp-4],ax
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
