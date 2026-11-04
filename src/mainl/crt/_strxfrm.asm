; Original Borland PC-98 large-model collation/transform functions.
; Symbolic structure/branches match the selected native member.
; Buffer/pointer ownership follows original far/near ABI.
.8086
extrn _GetNextKeyWeight:near,_GetSubstituteString:near,_GetCompressLevelWeight:near,_GetNextAuxChar:near,_GetExpansionString:near,_GetNextExpansionWeight:near,__pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_STRXFRM_TEXT segment word public 'CODE'
_STRXFRM_TEXT ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __strxfrm,_LevelTransform

; Original exported collation interface.
__strxfrm:
    push bp
    mov bp, sp
    sub sp, 24h
    push ds
    push es
    push di
    push si
    lds bx,__pLocale
    mov word ptr [bp - 24h], bx
    mov word ptr [bp - 22h], ds
    mov ax, word ptr [bx + 184h]
    mov word ptr [bp - 1eh], ax
    lds si, dword ptr [bx + 190h]
    inc si
    mov word ptr [bp - 18h], si
    mov word ptr [bp - 16h], ds
    mov word ptr [bp - 1ah], 0
    mov word ptr [bp - 1ch], 0
    les di, dword ptr [bp + 6]
    lds si, dword ptr [bp + 0ah]
    mov word ptr [bp - 20h], di
    mov ax, word ptr [bp + 0eh]
    add word ptr [bp - 20h], ax
    call _LevelTransform
    pop si
    pop di
    pop es
    pop ds
    mov sp, bp
    pop bp
    retf

; Original exported collation interface.
_LevelTransform:
    mov word ptr [bp - 8], 0
    mov word ptr [bp - 10h], 0
    push ds
    lds bx, dword ptr [bp - 24h]
    mov cx, word ptr [bp - 1ah]
    add bx, cx
    mov al, byte ptr [bx + 186h]
    add word ptr [bp - 1ch], 101h
    mov ch, al
    pop ds
    xor dx, dx
    test al, 10h
    je loc_0074
    mov byte ptr es:[di], 1
    inc di
loc_0074:
    mov word ptr [bp - 0eh], di
loc_0077:
    lea bx, [bp - 8]
    call _GetNextKeyWeight
    test dl, 80h
    jne loc_00a7
    test ch, 10h
    jne loc_0094
loc_0087:
    inc al
    mov byte ptr es:[di], al
    inc di
    cmp word ptr [bp - 20h], di
    jne loc_0077
    jmp short loc_00f9
loc_0094:
    mov bx, word ptr [bp - 8]
    add bx, 101h
    mov word ptr es:[di], bx
    inc di
    inc di
    cmp word ptr [bp - 20h], di
    jne loc_0087
    jmp short loc_00f9
loc_00a7:
    test ch, 10h
    je loc_00ba
    mov bx, word ptr [bp - 0eh]
    cmp di, bx
    jne loc_00d9
    dec di
    mov byte ptr es:[di], 0
    jmp short loc_00d9
loc_00ba:
    push ds
    push cx
    mov cx, di
    sub cx, word ptr [bp - 0eh]
    jcxz loc_00d7
    lds bx, dword ptr [bp - 18h]
    inc bx
    add bx, word ptr [bp - 1ch]
    mov al, byte ptr [bx]
    inc al
loc_00ce:
    cmp byte ptr es:[di - 1], al
    jne loc_00d7
    dec di
    loop loc_00ce
loc_00d7:
    pop cx
    pop ds
loc_00d9:
    test ch, 2
    jne loc_00fd
loc_00de:
    inc word ptr [bp - 1ah]
    mov cx, word ptr [bp - 1eh]
    cmp word ptr [bp - 1ah], cx
    jl loc_00f3
    mov byte ptr es:[di], 0
    sub di, word ptr [bp + 6]
    mov ax, di
    ret
loc_00f3:
    lds si, dword ptr [bp + 0ah]
    jmp near ptr _LevelTransform
loc_00f9:
    mov ax, word ptr [bp + 0eh]
    ret
loc_00fd:
    test ch, 10h
    jne loc_0142
    push di
    push es
    pop ds
    push es
    mov cx, di
    mov si, word ptr [bp - 0eh]
    sub cx, si
    cmp cx, 3
    jg loc_0122
    jcxz loc_013e
    mov al, byte ptr [si]
    mov ah, byte ptr es:[di - 1]
    mov byte ptr [si], ah
    mov byte ptr es:[di - 1], al
    jmp short loc_013e
loc_0122:
    shr cx, 1
    shr cx, 1
    jcxz loc_013e
loc_0128:
    mov ax, word ptr [si]
    mov bx, word ptr es:[di - 2]
    xchg al, ah
    xchg bl, bh
    mov word ptr [si], bx
    mov word ptr es:[di - 2], ax
    inc si
    inc si
    dec di
    dec di
    loop loc_0128
loc_013e:
    pop es
    pop di
    jmp short loc_00de
loc_0142:
    push di
    push es
    pop ds
    push es
    mov cx, di
    mov si, word ptr [bp - 0eh]
    sub cx, si
    shr cx, 1
    shr cx, 1
    cmp cx, 2
    jb loc_0179
    dec cx
loc_0157:
    mov ax, word ptr [si]
    mov dl, byte ptr [si + 2]
    mov bx, word ptr es:[di - 3]
    mov dh, byte ptr es:[di - 1]
    mov word ptr [si], bx
    mov byte ptr [si + 2], dh
    mov word ptr es:[di - 3], ax
    mov byte ptr es:[di - 1], dl
    inc si
    dec di
    inc si
    dec di
    inc si
    dec di
    loop loc_0157
loc_0179:
    pop es
    pop di
    jmp near ptr loc_00de
_TEXT ends
end
