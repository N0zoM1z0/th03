; Original complete Japanese Borland multibyte string routine FMBSNCAT.
; Native real 8086 CODE with original far/near MBCS buffer convention,
; original __ctype/__mbctype+1 and signed/unsigned return flags.
.8086
extrn __mbctype:byte
extrn __fmbsbtype:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fmbsncat

; Actual original Borland original imported call or byte-table reference region.
org 95
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbsncat_0084
    mov bx,[bp+10]
    cmp byte ptr es:[bx+1],0
    jz mbstring_fmbsncat_00a8
    les bx,[bp+10]
    mov al,es:[bx]
    les bx,[bp-4]
    mov es:[bx],al
    inc word ptr [bp+10]
    inc word ptr [bp-4]
    jmp short mbstring_fmbsncat_008d

mbstring_fmbsncat_0084:
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz mbstring_fmbsncat_00a8

mbstring_fmbsncat_008d:
    les bx,[bp+10]
    mov al,es:[bx]
    les bx,[bp-4]
    mov es:[bx],al
    inc word ptr [bp+10]
    inc word ptr [bp-4]
    dec word ptr [bp+14]

mbstring_fmbsncat_00a2:
    cmp word ptr [bp+14],0
    ja mbstring_fmbsncat_0055

mbstring_fmbsncat_00a8:
    les bx,[bp-4]
    mov byte ptr es:[bx],0

mbstring_fmbsncat_00af:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland original imported call or byte-table reference region.
org 67
    call __fmbsbtype
    add sp,6
    cmp ax,1
    jnz mbstring_fmbsncat_00a2
    dec word ptr [bp-4]
    jmp short mbstring_fmbsncat_00a2

mbstring_fmbsncat_0055:
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland original imported call or byte-table reference region.
org 0

__fmbsncat:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    cmp word ptr [bp+14],0
    ja mbstring_fmbsncat_0011
    jmp near ptr mbstring_fmbsncat_00af

mbstring_fmbsncat_0011:
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short mbstring_fmbsncat_0022

mbstring_fmbsncat_001f:
    inc word ptr [bp-4]

mbstring_fmbsncat_0022:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsncat_001f
    mov ax,[bp-4]
    cmp ax,[bp+6]
    jna mbstring_fmbsncat_00a2
    xor dx,dx
    sub ax,[bp+6]
    sbb dx,0
    dec ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
