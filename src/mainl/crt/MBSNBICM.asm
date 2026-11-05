; Original complete Japanese Borland multibyte string routine MBSNBICM.
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
public __mbsnbicmp

; Actual original Borland imported-byte-table reference region.
org 175
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_mbsnbicm_00b9
    sub dx,32

mbstring_mbsnbicm_00b9:
    cmp [bp-2],dx
    jz mbstring_mbsnbicm_00cd
    cmp [bp-2],dx
    jnc mbstring_mbsnbicm_00c8
    mov ax,65535
    jmp short mbstring_mbsnbicm_00cb

mbstring_mbsnbicm_00c8:
    mov ax,1

mbstring_mbsnbicm_00cb:
    jmp short mbstring_mbsnbicm_00de

mbstring_mbsnbicm_00cd:
    cmp word ptr [bp-2],0
    jz mbstring_mbsnbicm_00dc

mbstring_mbsnbicm_00d3:
    cmp word ptr [bp+14],0
    jna mbstring_mbsnbicm_00dc
    jmp near ptr mbstring_mbsnbicm_000b

mbstring_mbsnbicm_00dc:
    xor ax,ax

mbstring_mbsnbicm_00de:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 125
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnbicm_00ad
    cmp word ptr [bp+14],0
    jna mbstring_mbsnbicm_00dc
    dec word ptr [bp+14]
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnbicm_009a
    xor dx,dx
    jmp short mbstring_mbsnbicm_00b9

mbstring_mbsnbicm_009a:
    mov cl,8
    shl dx,cl
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    or dx,ax
    inc word ptr [bp+10]
    jmp short mbstring_mbsnbicm_00b9

mbstring_mbsnbicm_00ad:
    mov bx,dx

; Actual original Borland imported-byte-table reference region.
org 95
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_mbsnbicm_006a
    sub word ptr [bp-2],32

mbstring_mbsnbicm_006a:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov dx,ax
    inc word ptr [bp+10]
    mov al,dl
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 35
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnbicm_005c
    cmp word ptr [bp+14],0
    ja mbstring_mbsnbicm_0033
    jmp near ptr mbstring_mbsnbicm_00dc

mbstring_mbsnbicm_0033:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnbicm_0043
    mov word ptr [bp-2],0
    jmp short mbstring_mbsnbicm_006a

mbstring_mbsnbicm_0043:
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    les bx,[bp+6]
    mov dl,es:[bx]
    mov dh,0
    or ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    jmp short mbstring_mbsnbicm_006a

mbstring_mbsnbicm_005c:
    mov bx,[bp-2]

; Actual original Borland imported-byte-table reference region.
org 0

__mbsnbicmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_mbsnbicm_00d3

mbstring_mbsnbicm_000b:
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
