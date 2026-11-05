; Original complete Japanese Borland multibyte string routine FMBSRCHR.
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
public __fmbsrchr

; Actual original Borland imported-byte-table reference region.
org 28
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsrchr_006e
    mov bx,[bp+6]
    cmp byte ptr es:[bx+1],0
    jnz mbstring_fmbsrchr_0044
    inc word ptr [bp+6]
    cmp word ptr [bp+10],0
    jnz mbstring_fmbsrchr_0096
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short mbstring_fmbsrchr_0096

mbstring_fmbsrchr_0044:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov cl,8
    shl ax,cl
    mov dl,es:[bx+1]
    mov dh,0
    or ax,dx
    cmp ax,[bp+10]
    jnz mbstring_fmbsrchr_0069
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax

mbstring_fmbsrchr_0069:
    inc word ptr [bp+6]
    jmp short mbstring_fmbsrchr_0087

mbstring_fmbsrchr_006e:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    cmp ax,[bp+10]
    jnz mbstring_fmbsrchr_0087
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax

mbstring_fmbsrchr_0087:
    les bx,[bp+6]
    inc word ptr [bp+6]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsrchr_0096
    jmp near ptr mbstring_fmbsrchr_0012

mbstring_fmbsrchr_0096:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland imported-byte-table reference region.
org 0

__fmbsrchr:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov word ptr [bp-2],0
    mov word ptr [bp-4],0

mbstring_fmbsrchr_0012:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
