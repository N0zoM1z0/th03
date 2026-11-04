; Original Japanese Borland large-model CRT strncmp, source-level
; 8086 instruction semantics and far/near ABI; no target CODE array.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _strncmp

_strncmp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    cld
    les di,dword ptr [bp + 0ah]
    mov si, di
    mov ax, word ptr [bp + 0eh]
    mov cx, ax
    jcxz loc_0032
    mov bx, ax
    xor al, al
    repne scasb
    sub bx, cx
    mov cx, bx
    mov di, si
    lds si,dword ptr [bp + 6]
    repe cmpsb
    mov al, byte ptr [si - 1]
    mov bl, byte ptr es:[di - 1]
    xor ah, ah
    mov bh, ah
    sub ax, bx
loc_0032:
    mov ds, dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
