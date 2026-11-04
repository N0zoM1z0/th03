; Original Japanese Borland large-model CRT strnicmp, source-level
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
public _strnicmp

_strnicmp:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    cld
    lds si,dword ptr [bp + 6]
    les di,dword ptr [bp + 0ah]
    mov cx, word ptr [bp + 0eh]
    xor ax, ax
    mov bx, ax
    mov dx, 617ah
loc_0017:
    jcxz loc_003d
    lodsb
    mov bl, byte ptr es:[di]
    or al, al
    je loc_003d
    scasb
    loope loc_0017
    cmp al, dh
    jb loc_002e
    cmp al, dl
    ja loc_002e
    sub al, 20h
loc_002e:
    cmp bl, dh
    jb loc_0039
    cmp bl, dl
    ja loc_0039
    sub bl, 20h
loc_0039:
    cmp al, bl
    je loc_0017
loc_003d:
    sub ax, bx
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
