; Original Japanese Borland multibyte algorithm MBSREV.
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
public __mbsrev

__mbsrev:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short mbs_0047

mbs_0016:
    les bx,dword ptr [bp - 4]
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    je mbs_0044
    inc word ptr [bp - 4]
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    je mbs_0050
    les bx,dword ptr [bp - 4]
    mov dl, byte ptr es:[bx]
    mov al, byte ptr es:[bx - 1]
    mov byte ptr es:[bx], al
    mov byte ptr es:[bx - 1], dl

mbs_0044:
    inc word ptr [bp - 4]

mbs_0047:
    les bx,dword ptr [bp - 4]
    cmp byte ptr es:[bx], 0
    jne mbs_0016

mbs_0050:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    jmp short mbs_0079

mbs_005e:
    les bx,dword ptr [bp - 8]
    mov dl, byte ptr es:[bx]
    les bx,dword ptr [bp - 4]
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp - 8]
    mov byte ptr es:[bx], al
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], dl
    inc word ptr [bp - 8]

mbs_0079:
    dec word ptr [bp - 4]
    mov ax, word ptr [bp - 8]
    cmp ax, word ptr [bp - 4]
    jb mbs_005e
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
