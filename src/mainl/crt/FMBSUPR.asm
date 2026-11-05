; Original complete Japanese Borland multibyte string routine FMBSUPR.
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
public __fmbsupr

; Actual original Borland original imported call or byte-table reference region.
org 64
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbstring_fmbsupr_0052
    mov bx,[bp-4]
    mov al,es:[bx]
    add al,224
    mov es:[bx],al

mbstring_fmbsupr_0052:
    inc word ptr [bp-4]

mbstring_fmbsupr_0055:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jnz mbstring_fmbsupr_0016
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
    jz mbstring_fmbsupr_0036
    mov bx,[bp-4]
    cmp byte ptr es:[bx+1],0
    jz mbstring_fmbsupr_0036
    inc word ptr [bp-4]
    jmp short mbstring_fmbsupr_0052

mbstring_fmbsupr_0036:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax

; Actual original Borland original imported call or byte-table reference region.
org 0

__fmbsupr:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short mbstring_fmbsupr_0055

mbstring_fmbsupr_0016:
    les bx,[bp-4]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
_TEXT ends
end
