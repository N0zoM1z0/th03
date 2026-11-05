; Original complete Japanese Borland multibyte string routine FMBSNICM.
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
public __fmbsnicmp

; Actual original Borland imported-byte-table reference region.
org 154
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_fmbsnicm_00a4
    sub dx,32

mbstring_fmbsnicm_00a4:
    cmp [bp-2],dx
    jz mbstring_fmbsnicm_00b8
    cmp [bp-2],dx
    jnc mbstring_fmbsnicm_00b3
    mov ax,65535
    jmp short mbstring_fmbsnicm_00b6

mbstring_fmbsnicm_00b3:
    mov ax,1

mbstring_fmbsnicm_00b6:
    jmp short mbstring_fmbsnicm_00cc

mbstring_fmbsnicm_00b8:
    cmp word ptr [bp-2],0
    jz mbstring_fmbsnicm_00ca
    dec word ptr [bp+14]

mbstring_fmbsnicm_00c1:
    cmp word ptr [bp+14],0
    jna mbstring_fmbsnicm_00ca
    jmp near ptr mbstring_fmbsnicm_000b

mbstring_fmbsnicm_00ca:
    xor ax,ax

mbstring_fmbsnicm_00cc:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 113
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsnicm_0098
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsnicm_0085
    xor dx,dx
    jmp short mbstring_fmbsnicm_00a4

mbstring_fmbsnicm_0085:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]
    jmp short mbstring_fmbsnicm_00a4

mbstring_fmbsnicm_0098:
    mov bx,dx

; Actual original Borland imported-byte-table reference region.
org 83
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_fmbsnicm_005e
    sub word ptr [bp-2],32

mbstring_fmbsnicm_005e:
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
    jz mbstring_fmbsnicm_0050
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsnicm_0037
    mov word ptr [bp-2],0
    jmp short mbstring_fmbsnicm_005e

mbstring_fmbsnicm_0037:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    jmp short mbstring_fmbsnicm_005e

mbstring_fmbsnicm_0050:
    mov bx,[bp-2]

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsnicmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_fmbsnicm_00c1

mbstring_fmbsnicm_000b:
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
