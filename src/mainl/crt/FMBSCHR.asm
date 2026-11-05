; Complete Borland Japanese multibyte-character string search FMBSCHR.
; Original far return, DBCS lead-byte classification and DX:AX pointer ABI.
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
public __fmbschr

__fmbschr:
    push bp
    mov bp,sp
    push si
    push di

fmbschr_branch_0005:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz fmbschr_branch_0049
    mov bx,[bp+6]
    cmp byte ptr es:[bx+1],0
    jnz fmbschr_branch_002b
    cmp word ptr [bp+10],0
    jnz fmbschr_branch_006c
    inc word ptr [bp+6]
    jmp short fmbschr_branch_0056

fmbschr_branch_002b:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov cl,8
    shl ax,cl
    mov dl,es:[bx+1]
    mov dh,0
    or ax,dx
    cmp ax,[bp+10]
    jz fmbschr_branch_0056
    inc word ptr [bp+6]
    jmp short fmbschr_branch_0067

fmbschr_branch_0049:
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    cmp ax,[bp+10]
    jnz fmbschr_branch_005e

fmbschr_branch_0056:
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short fmbschr_branch_0070

fmbschr_branch_005e:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz fmbschr_branch_006c

fmbschr_branch_0067:
    inc word ptr [bp+6]
    jmp short fmbschr_branch_0005

fmbschr_branch_006c:
    xor dx,dx
    xor ax,ax

fmbschr_branch_0070:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
