; Original complete Japanese Borland multibyte string routine FMBSICMP.
; Native real 8086 CODE with original far/near MBCS buffer convention,
; original __ctype/__mbctype+1 and signed/unsigned return flags.
.8086
extrn __ctype:byte
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
public __fmbsicmp

; Actual original Borland imported-byte-table reference region.
org 151
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_fmbsicmp_00a1
    sub dx,32

mbstring_fmbsicmp_00a1:
    cmp [bp-2],dx
    jz mbstring_fmbsicmp_00b5
    cmp [bp-2],dx
    jnc mbstring_fmbsicmp_00b0
    mov ax,65535
    jmp short mbstring_fmbsicmp_00b3

mbstring_fmbsicmp_00b0:
    mov ax,1

mbstring_fmbsicmp_00b3:
    jmp short mbstring_fmbsicmp_00c0

mbstring_fmbsicmp_00b5:
    cmp word ptr [bp-2],0
    jz mbstring_fmbsicmp_00be
    jmp near ptr mbstring_fmbsicmp_0008

mbstring_fmbsicmp_00be:
    xor ax,ax

mbstring_fmbsicmp_00c0:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 110
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsicmp_0095
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsicmp_0082
    xor dx,dx
    jmp short mbstring_fmbsicmp_00a1

mbstring_fmbsicmp_0082:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]
    jmp short mbstring_fmbsicmp_00a1

mbstring_fmbsicmp_0095:
    mov bx,dx

; Actual original Borland imported-byte-table reference region.
org 80
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_fmbsicmp_005b
    sub word ptr [bp-2],32

mbstring_fmbsicmp_005b:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov dx,ax
    inc word ptr [bp+10]
    mov al,dl
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 29
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsicmp_004d
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsicmp_0034
    mov word ptr [bp-2],0
    jmp short mbstring_fmbsicmp_005b

mbstring_fmbsicmp_0034:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    jmp short mbstring_fmbsicmp_005b

mbstring_fmbsicmp_004d:
    mov bx,[bp-2]

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsicmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

mbstring_fmbsicmp_0008:
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
