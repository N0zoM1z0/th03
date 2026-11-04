; Original Japanese Borland large-model CRT atol, source-level
; 8086 instruction semantics and far/near ABI; no target CODE array.
.8086
extrn __ctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _atol,_atoi

_atol:
    push bp
    mov bp, sp
    push si
    push di
    push es
    push bp
    les si,dword ptr [bp + 6]
    cld
    sub ax, ax
    cwd
    mov cx, 0ah
    mov bh, 0
    mov di,offset __ctype+1
loc_0016:
    mov bl, byte ptr es:[si]
    inc si
    test byte ptr [bx + di], 1
    jne loc_0016
    mov bp, 0
    cmp bl, 2bh
    je loc_002d
    cmp bl, 2dh
    jne loc_0031
    inc bp
loc_002d:
    mov bl, byte ptr es:[si]
    inc si
loc_0031:
    cmp bl, 39h
    ja loc_0065
    sub bl, 30h
    jb loc_0065
    mul cx
    add ax, bx
    adc dl, dh
    je loc_002d
    jmp short loc_0057
loc_0045:
    mov di, dx
    mov cx, 0ah
    mul cx
    xchg di, ax
    xchg dx, cx
    mul dx
    xchg dx, ax
    xchg di, ax
    add ax, bx
    adc dx, cx
loc_0057:
    mov bl, byte ptr es:[si]
    inc si
    cmp bl, 39h
    ja loc_0065
    sub bl, 30h
    jae loc_0045
loc_0065:
    dec bp
    jl loc_006f
    neg dx
    neg ax
    sbb dx, 0
loc_006f:
    pop bp
    pop es
    pop di
    pop si
    pop bp
    retf

_atoi:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call _atol
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
