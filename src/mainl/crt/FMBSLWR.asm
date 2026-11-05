; Original complete Japanese Borland multibyte string routine FMBSLWR.
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
public __fmbslwr

; Actual original Borland original imported call or byte-table reference region.
org 64
    test byte ptr DGROUP:__ctype[bx+1],4
    jz mbstring_fmbslwr_0052
    mov bx,[bp-4]
    mov al,es:[bx]
    add al,32
    mov es:[bx],al

mbstring_fmbslwr_0052:
    inc word ptr [bp-4]

mbstring_fmbslwr_0055:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbslwr_0016
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Actual original Borland original imported call or byte-table reference region.
org 32
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbstring_fmbslwr_0036
    mov bx,[bp-4]
    cmp byte ptr es:[bx+1],0
    jz mbstring_fmbslwr_0036
    inc word ptr [bp-4]
    jmp short mbstring_fmbslwr_0052

mbstring_fmbslwr_0036:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland original imported call or byte-table reference region.
org 0

__fmbslwr:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short mbstring_fmbslwr_0055

mbstring_fmbslwr_0016:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
