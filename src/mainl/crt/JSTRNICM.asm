; Original complete Japanese Borland multibyte string routine JSTRNICM.
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
public _jstrnicmp

; Actual original Borland imported-byte-table reference region.
org 139
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_jstrnicm_00c0
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz mbstring_jstrnicm_00bc
    mov cl,8
    shl dx,cl
    mov al,es:[bx]
    mov ah,0
    add dx,ax
    inc word ptr [bp+10]
    cmp dx,33409
    jc mbstring_jstrnicm_00d1
    cmp dx,33434
    ja mbstring_jstrnicm_00d1
    mov ax,dx
    sub ax,33
    jmp short mbstring_jstrnicm_00d3

mbstring_jstrnicm_00bc:
    xor dx,dx
    jmp short mbstring_jstrnicm_00d5

mbstring_jstrnicm_00c0:
    cmp dx,97
    jc mbstring_jstrnicm_00d1
    cmp dx,122
    ja mbstring_jstrnicm_00d1
    mov ax,dx
    sub ax,32
    jmp short mbstring_jstrnicm_00d3

mbstring_jstrnicm_00d1:
    mov ax,dx

mbstring_jstrnicm_00d3:
    mov dx,ax

mbstring_jstrnicm_00d5:
    cmp [bp-2],dx
    jz mbstring_jstrnicm_00e9
    cmp [bp-2],dx
    jnc mbstring_jstrnicm_00e4
    mov ax,65535
    jmp short mbstring_jstrnicm_00e7

mbstring_jstrnicm_00e4:
    mov ax,1

mbstring_jstrnicm_00e7:
    jmp short mbstring_jstrnicm_00fd

mbstring_jstrnicm_00e9:
    cmp word ptr [bp-2],0
    jz mbstring_jstrnicm_00fb
    dec word ptr [bp+14]

mbstring_jstrnicm_00f2:
    cmp word ptr [bp+14],0
    jna mbstring_jstrnicm_00fb
    jmp near ptr mbstring_jstrnicm_000b

mbstring_jstrnicm_00fb:
    xor ax,ax

mbstring_jstrnicm_00fd:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 32
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_jstrnicm_005e
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_jstrnicm_0057
    mov ax,[bp-2]
    mov cl,8
    shl ax,cl
    mov dl,es:[bx]
    mov dh,0
    add ax,dx
    mov [bp-2],ax
    inc word ptr [bp+6]
    cmp word ptr [bp-2],33409
    jc mbstring_jstrnicm_0072
    cmp word ptr [bp-2],33434
    ja mbstring_jstrnicm_0072
    sub ax,33
    jmp short mbstring_jstrnicm_0075

mbstring_jstrnicm_0057:
    mov word ptr [bp-2],0
    jmp short mbstring_jstrnicm_0078

mbstring_jstrnicm_005e:
    cmp word ptr [bp-2],97
    jc mbstring_jstrnicm_0072
    cmp word ptr [bp-2],122
    ja mbstring_jstrnicm_0072
    mov ax,[bp-2]
    sub ax,32
    jmp short mbstring_jstrnicm_0075

mbstring_jstrnicm_0072:
    mov ax,[bp-2]

mbstring_jstrnicm_0075:
    mov [bp-2],ax

mbstring_jstrnicm_0078:
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

_jstrnicmp:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    jmp near ptr mbstring_jstrnicm_00f2

mbstring_jstrnicm_000b:
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
