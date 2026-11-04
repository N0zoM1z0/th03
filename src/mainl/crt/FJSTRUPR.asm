; Original Japanese Borland multibyte algorithm FJSTRUPR.
; Genuine native 8086 with original __mbctype GROUP-relative state.
; Exact Borland large-model near/far pointer and DBCS behavior.
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
public __fjstrupr

__fjstrupr:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short mbs_006f

mbs_0016:
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx], 7ah
    ja mbs_002c
    cmp byte ptr es:[bx], 61h
    jb mbs_002c
    mov al, byte ptr es:[bx]
    add al, 0e0h
    jmp short mbs_005b

mbs_002c:
    les bx,dword ptr [bp - 4]
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    je mbs_006c
    inc word ptr [bp - 4]
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx - 1], 82h
    jne mbs_0063
    cmp byte ptr es:[bx], 81h
    jb mbs_0063
    cmp byte ptr es:[bx], 9ah
    ja mbs_0063
    mov al, byte ptr es:[bx]
    add al, 0dfh

mbs_005b:
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    jmp short mbs_006c

mbs_0063:
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    je mbs_0078

mbs_006c:
    inc word ptr [bp - 4]

mbs_006f:
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne mbs_0016

mbs_0078:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
