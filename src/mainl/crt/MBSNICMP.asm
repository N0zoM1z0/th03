; Original complete Japanese Borland multibyte string routine MBSNICMP.
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
public __mbsnicmp

; Actual original Borland imported-byte-table reference region.
org 154
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_mbsnicmp_00a4
    sub dx,32

mbstring_mbsnicmp_00a4:
    cmp [bp-2],dx
    jz mbstring_mbsnicmp_00b8
    cmp [bp-2],dx
    jnc mbstring_mbsnicmp_00b3
    mov ax,65535
    jmp short mbstring_mbsnicmp_00b6

mbstring_mbsnicmp_00b3:
    mov ax,1

mbstring_mbsnicmp_00b6:
    jmp short mbstring_mbsnicmp_00cc

mbstring_mbsnicmp_00b8:
    cmp word ptr [bp-2],0
    jz mbstring_mbsnicmp_00ca
    dec word ptr [bp+14]

mbstring_mbsnicmp_00c1:
    cmp word ptr [bp+14],0
    jna mbstring_mbsnicmp_00ca
    jmp near ptr mbstring_mbsnicmp_000b

mbstring_mbsnicmp_00ca:
    xor ax,ax

mbstring_mbsnicmp_00cc:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 113
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnicmp_0098
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnicmp_0085
    xor dx,dx
    jmp short mbstring_mbsnicmp_00a4

mbstring_mbsnicmp_0085:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]
    jmp short mbstring_mbsnicmp_00a4

mbstring_mbsnicmp_0098:
    mov bx,dx

; Actual original Borland imported-byte-table reference region.
org 83
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_mbsnicmp_005e
    sub word ptr [bp-2],32

mbstring_mbsnicmp_005e:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov dx,ax
    inc word ptr [bp+10]
    mov al,dl
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 32
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnicmp_0050
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnicmp_0037
    mov word ptr [bp-2],0
    jmp short mbstring_mbsnicmp_005e

mbstring_mbsnicmp_0037:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    jmp short mbstring_mbsnicmp_005e

mbstring_mbsnicmp_0050:
    mov bx,[bp-2]

; Actual original Borland imported-byte-table reference region.
org 0

__mbsnicmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_mbsnicmp_00c1

mbstring_mbsnicmp_000b:
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
