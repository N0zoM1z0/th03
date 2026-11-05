; Original complete Japanese Borland multibyte string routine MBCCMP.
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
public __mbccmp

; Actual original Borland imported-byte-table reference region.
org 87
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbccmp_007b
    mov bx,[bp+10]
    cmp byte ptr es:[bx+1],0
    jnz mbstring_mbccmp_006c
    xor dx,dx
    jmp short mbstring_mbccmp_007b

mbstring_mbccmp_006c:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx+1]
    mov ah,0
    or dx,ax

mbstring_mbccmp_007b:
    cmp [bp-2],dx
    jz mbstring_mbccmp_008f
    cmp [bp-2],dx
    jnc mbstring_mbccmp_008a
    mov ax,65535
    jmp short mbstring_mbccmp_008d

mbstring_mbccmp_008a:
    mov ax,1

mbstring_mbccmp_008d:
    jmp short mbstring_mbccmp_0091

mbstring_mbccmp_008f:
    xor ax,ax

mbstring_mbccmp_0091:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 26
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbccmp_0047
    mov bx,[bp+6]
    cmp byte ptr es:[bx+1],0
    jnz mbstring_mbccmp_0032
    mov word ptr [bp-2],0
    jmp short mbstring_mbccmp_0047

mbstring_mbccmp_0032:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx+1]
    mov dh,0
    or ax,dx
    mov [bp-2],ax

mbstring_mbccmp_0047:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov dx,ax
    mov al,dl
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 0

__mbccmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov [bp-2],ax
    mov al,[bp-2]
    mov ah,0
    mov bx,ax
_TEXT ends
end
