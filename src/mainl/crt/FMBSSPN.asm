; Original complete Japanese Borland multibyte string routine FMBSSPN.
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
public __fmbsspn

; Actual original Borland imported-byte-table reference region.
org 143
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsspn_00a2
    inc word ptr [bp-4]
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsspn_00b1

mbstring_fmbsspn_00a2:
    inc word ptr [bp-4]

mbstring_fmbsspn_00a5:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsspn_00b1
    jmp near ptr mbstring_fmbsspn_0017

mbstring_fmbsspn_00b1:
    mov ax,[bp-4]
    xor dx,dx
    sub ax,[bp+6]
    sbb dx,0
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 47
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsspn_0062
    les bx,[bp-4]
    mov al,es:[bx]
    les bx,[bp-8]
    cmp al,es:[bx]
    jnz mbstring_fmbsspn_0054
    les bx,[bp-4]
    mov al,es:[bx+1]
    les bx,[bp-8]
    cmp al,es:[bx+1]
    jz mbstring_fmbsspn_007c

mbstring_fmbsspn_0054:
    inc word ptr [bp-8]
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsspn_0070
    jmp short mbstring_fmbsspn_007c

mbstring_fmbsspn_0062:
    les bx,[bp-4]
    mov al,es:[bx]
    les bx,[bp-8]
    cmp al,es:[bx]
    jz mbstring_fmbsspn_007c

mbstring_fmbsspn_0070:
    inc word ptr [bp-8]

mbstring_fmbsspn_0073:
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsspn_0025

mbstring_fmbsspn_007c:
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsspn_00b1
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsspn:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp near ptr mbstring_fmbsspn_00a5

mbstring_fmbsspn_0017:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short mbstring_fmbsspn_0073

mbstring_fmbsspn_0025:
    les bx,[bp-8]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
