; Original complete Japanese Borland multibyte string routine MBSNSET.
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
public __mbsnset

; Actual original Borland imported-byte-table reference region.
org 100
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnset_0070
    mov ax,1
    jmp short mbstring_mbsnset_0072

mbstring_mbsnset_0070:
    xor ax,ax

mbstring_mbsnset_0072:
    mov dl,al
    les bx,[bp-4]
    mov al,[bp+10]
    mov es:[bx],al
    inc word ptr [bp-4]
    dec word ptr [bp+12]

mbstring_mbsnset_0083:
    cmp word ptr [bp+12],0
    jna mbstring_mbsnset_0092
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jnz mbstring_mbsnset_0021

mbstring_mbsnset_0092:
    or dl,dl
    jz mbstring_mbsnset_00a6
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jz mbstring_mbsnset_00a6

mbstring_mbsnset_009f:
    les bx,[bp-4]
    mov byte ptr es:[bx],32

mbstring_mbsnset_00a6:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 51
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_mbsnset_003f
    mov ax,1
    jmp short mbstring_mbsnset_0041

mbstring_mbsnset_003f:
    xor ax,ax

mbstring_mbsnset_0041:
    mov dl,al
    les bx,[bp-4]
    cmp byte ptr es:[bx+1],0
    jz mbstring_mbsnset_009f
    les bx,[bp-4]
    mov es:[bx],cl
    inc word ptr [bp-4]

mbstring_mbsnset_0056:
    or dl,dl
    jnz mbstring_mbsnset_0070
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 0

__mbsnset:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    mov dl,0
    mov ax,[bp+10]
    mov cl,8
    shr ax,cl
    mov cl,al
    jmp short mbstring_mbsnset_0083

mbstring_mbsnset_0021:
    or cl,cl
    jz mbstring_mbsnset_0056
    or dl,dl
    jnz mbstring_mbsnset_003f
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
