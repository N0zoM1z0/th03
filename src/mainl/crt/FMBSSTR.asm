; Original complete Japanese Borland multibyte string routine FMBSSTR.
; Native real 8086 CODE with original far/near MBCS buffer convention,
; original __ctype/__mbctype+1 and signed/unsigned return flags.
.8086
extrn __fstrlen:far
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
public __fmbsstr

; Actual original Borland original imported call or byte-table reference region.
org 158
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsstr_00b2
    mov bx,[bp+6]
    cmp byte ptr es:[bx+1],0
    jz mbstring_fmbsstr_00b2
    inc word ptr [bp+6]

mbstring_fmbsstr_00b2:
    inc word ptr [bp+6]

mbstring_fmbsstr_00b5:
    mov ax,[bp+6]
    cmp ax,[bp-6]
    jna mbstring_fmbsstr_004f

mbstring_fmbsstr_00bd:
    xor dx,dx
    xor ax,ax

mbstring_fmbsstr_00c1:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland original imported call or byte-table reference region.
org 36
    call __fstrlen
    pop cx
    pop cx
    mov bx,ax
    or bx,bx
    jnz mbstring_fmbsstr_0034
    jmp near ptr mbstring_fmbsstr_00bd

mbstring_fmbsstr_0034:
    cmp [bp-2],bx
    jna mbstring_fmbsstr_003c
    jmp near ptr mbstring_fmbsstr_00bd

mbstring_fmbsstr_003c:
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,bx
    sub ax,[bp-2]
    mov [bp-4],dx
    mov [bp-6],ax
    jmp short mbstring_fmbsstr_00b5

mbstring_fmbsstr_004f:
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-8],dx
    mov [bp-10],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-12],dx
    mov [bp-14],ax
    jmp short mbstring_fmbsstr_006f

mbstring_fmbsstr_0069:
    inc word ptr [bp-10]
    inc word ptr [bp-14]

mbstring_fmbsstr_006f:
    les bx,[bp-10]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsstr_0083
    mov al,es:[bx]
    les bx,[bp-14]
    cmp al,es:[bx]
    jz mbstring_fmbsstr_0069

mbstring_fmbsstr_0083:
    les bx,[bp-14]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsstr_0094

mbstring_fmbsstr_008c:
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short mbstring_fmbsstr_00c1

mbstring_fmbsstr_0094:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland original imported call or byte-table reference region.
org 14
    call __fstrlen
    pop cx
    pop cx
    mov [bp-2],ax
    cmp word ptr [bp-2],0
    jna mbstring_fmbsstr_008c
    push word ptr [bp+8]
    push word ptr [bp+6]

; Actual original Borland original imported call or byte-table reference region.
org 0

__fmbsstr:
    push bp
    mov bp,sp
    sub sp,14
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
_TEXT ends
end
