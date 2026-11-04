; Original Japanese Borland large-model CRT stricmp, source-level
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
public _stricmp

_stricmp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    cld
    lds si,dword ptr [bp + 6]
    les di,dword ptr [bp + 0ah]
    xor ax, ax
    mov bx, ax
    mov cx, 617ah
loc_0015:
    lodsb
    mov bl, byte ptr es:[di]
    or al, al
    je loc_0039
    scasb
    je loc_0015
    cmp al, ch
    jb loc_002a
    cmp al, cl
    ja loc_002a
    sub al, 20h
loc_002a:
    cmp bl, ch
    jb loc_0035
    cmp bl, cl
    ja loc_0035
    sub bl, 20h
loc_0035:
    cmp al, bl
    je loc_0015
loc_0039:
    sub ax, bx
    mov ds, dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
