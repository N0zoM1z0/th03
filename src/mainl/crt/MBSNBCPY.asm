; Original Japanese Borland multibyte algorithm MBSNBCPY.
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
public __mbsnbcpy

__mbsnbcpy:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov cx, word ptr [bp + 0eh]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short mbs_005f

mbs_0019:
    les bx,dword ptr [bp + 0ah]
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    je mbs_004c
    cmp cx, 2
    jb mbs_0079
    mov bx, word ptr [bp + 0ah]
    cmp byte ptr es:[bx + 1], 0
    je mbs_0079
    les bx,dword ptr [bp + 0ah]
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    inc word ptr [bp + 0ah]
    inc word ptr [bp - 4]
    dec cx

mbs_004c:
    les bx,dword ptr [bp + 0ah]
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], al
    inc word ptr [bp + 0ah]
    inc word ptr [bp - 4]
    dec cx

mbs_005f:
    or cx, cx
    jbe mbs_0079
    les bx,dword ptr [bp + 0ah]
    cmp byte ptr es:[bx], 0
    jne mbs_0019
    jmp short mbs_0079

mbs_006e:
    les bx,dword ptr [bp - 4]
    mov byte ptr es:[bx], 0
    inc word ptr [bp - 4]
    dec cx

mbs_0079:
    or cx, cx
    ja mbs_006e
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
