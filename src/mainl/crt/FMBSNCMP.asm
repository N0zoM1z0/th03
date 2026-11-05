; Original complete Japanese Borland multibyte string routine FMBSNCMP.
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
public __fmbsncmp

; Actual original Borland imported-byte-table reference region.
org 97
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsncmp_0086
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsncmp_0075
    xor dx,dx
    jmp short mbstring_fmbsncmp_0086

mbstring_fmbsncmp_0075:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]

mbstring_fmbsncmp_0086:
    cmp [bp-2],dx
    jz mbstring_fmbsncmp_009a
    cmp [bp-2],dx
    jnc mbstring_fmbsncmp_0095
    mov ax,65535
    jmp short mbstring_fmbsncmp_0098

mbstring_fmbsncmp_0095:
    mov ax,1

mbstring_fmbsncmp_0098:
    jmp short mbstring_fmbsncmp_00ae

mbstring_fmbsncmp_009a:
    cmp word ptr [bp-2],0
    jz mbstring_fmbsncmp_00ac
    dec word ptr [bp+14]

mbstring_fmbsncmp_00a3:
    cmp word ptr [bp+14],0
    jna mbstring_fmbsncmp_00ac
    jmp near ptr mbstring_fmbsncmp_000b

mbstring_fmbsncmp_00ac:
    xor ax,ax

mbstring_fmbsncmp_00ae:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 32
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsncmp_004e
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsncmp_0037
    mov word ptr [bp-2],0
    jmp short mbstring_fmbsncmp_004e

mbstring_fmbsncmp_0037:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]

mbstring_fmbsncmp_004e:
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

__fmbsncmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_fmbsncmp_00a3

mbstring_fmbsncmp_000b:
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
