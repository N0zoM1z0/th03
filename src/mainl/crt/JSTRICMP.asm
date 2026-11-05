; Original complete Japanese Borland multibyte string routine JSTRICMP.
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
public _jstricmp

; Actual original Borland imported-byte-table reference region.
org 136
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_jstricmp_00bd
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz mbstring_jstricmp_00b9
    mov cl,8
    shl dx,cl
    mov al,es:[bx]
    mov ah,0
    add dx,ax
    inc word ptr [bp+10]
    cmp dx,33409
    jc mbstring_jstricmp_00ce
    cmp dx,33434
    ja mbstring_jstricmp_00ce
    mov ax,dx
    sub ax,33
    jmp short mbstring_jstricmp_00d0

mbstring_jstricmp_00b9:
    xor dx,dx
    jmp short mbstring_jstricmp_00d2

mbstring_jstricmp_00bd:
    cmp dx,97
    jc mbstring_jstricmp_00ce
    cmp dx,122
    ja mbstring_jstricmp_00ce
    mov ax,dx
    sub ax,32
    jmp short mbstring_jstricmp_00d0

mbstring_jstricmp_00ce:
    mov ax,dx

mbstring_jstricmp_00d0:
    mov dx,ax

mbstring_jstricmp_00d2:
    cmp [bp-2],dx
    jz mbstring_jstricmp_00e6
    cmp [bp-2],dx
    jnc mbstring_jstricmp_00e1
    mov ax,65535
    jmp short mbstring_jstricmp_00e4

mbstring_jstricmp_00e1:
    mov ax,1

mbstring_jstricmp_00e4:
    jmp short mbstring_jstricmp_00f1

mbstring_jstricmp_00e6:
    cmp word ptr [bp-2],0
    jz mbstring_jstricmp_00ef
    jmp near ptr mbstring_jstricmp_0008

mbstring_jstricmp_00ef:
    xor ax,ax

mbstring_jstricmp_00f1:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 29
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_jstricmp_005b
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_jstricmp_0054
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    mov dl,es:[bx]
    mov dh,0
    add ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    cmp word ptr [bp-2],33409
    jc mbstring_jstricmp_006f
    cmp word ptr [bp-2],33434
    ja mbstring_jstricmp_006f
    sub ax,33
    jmp short mbstring_jstricmp_0072

mbstring_jstricmp_0054:
    mov word ptr [bp-2],0
    jmp short mbstring_jstricmp_0075

mbstring_jstricmp_005b:
    cmp word ptr [bp-2],97
    jc mbstring_jstricmp_006f
    cmp word ptr [bp-2],122
    ja mbstring_jstricmp_006f
    mov ax,[bp-2]
    sub ax,32
    jmp short mbstring_jstricmp_0072

mbstring_jstricmp_006f:
    mov ax,[bp-2]

mbstring_jstricmp_0072:
    mov [bp-2],ax

mbstring_jstricmp_0075:
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

_jstricmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

mbstring_jstricmp_0008:
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
