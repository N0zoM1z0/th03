; Original complete Japanese Borland multibyte string routine FMBSCMP.
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
public __fmbscmp

; Actual original Borland imported-byte-table reference region.
org 94
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbscmp_0083
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbscmp_0072
    xor dx,dx
    jmp short mbstring_fmbscmp_0083

mbstring_fmbscmp_0072:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]

mbstring_fmbscmp_0083:
    cmp [bp-2],dx
    jz mbstring_fmbscmp_0097
    cmp [bp-2],dx
    jnc mbstring_fmbscmp_0092
    mov ax,65535
    jmp short mbstring_fmbscmp_0095

mbstring_fmbscmp_0092:
    mov ax,1

mbstring_fmbscmp_0095:
    jmp short mbstring_fmbscmp_00a2

mbstring_fmbscmp_0097:
    cmp word ptr [bp-2],0
    jz mbstring_fmbscmp_00a0
    jmp near ptr mbstring_fmbscmp_0008

mbstring_fmbscmp_00a0:
    xor ax,ax

mbstring_fmbscmp_00a2:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 29
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbscmp_004b
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbscmp_0034
    mov word ptr [bp-2],0
    jmp short mbstring_fmbscmp_004b

mbstring_fmbscmp_0034:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]

mbstring_fmbscmp_004b:
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

__fmbscmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

mbstring_fmbscmp_0008:
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
