; Original Borland PC-98 large-model collation/transform functions.
; Symbolic structure/branches match the selected native member.
; Buffer/pointer ownership follows original far/near ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
COLLATE_TEXT segment word public 'CODE'
COLLATE_TEXT ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _GetNextKeyWeight,_GetSubstituteString,_GetCompressLevelWeight,_GetExpansionString,_GetNextAuxChar,_GetNextExpansionWeight
collate_stack_frame_stub:
    push bp
    mov bp, sp
    sub sp, 24h
    mov sp, bp
    pop bp
    retf

; Original exported collation interface.
_GetNextKeyWeight:
    push es
    push di
loc_000c:
    test dl, dl
    jne loc_0070
loc_0010:
    mov al, byte ptr [si]
    inc si
    inc word ptr ss:[bx]
    test al, al
    je loc_006b
loc_001a:
    mov di, word ptr [bp - 18h]
    mov es, word ptr [bp - 16h]
    xor ah, ah
    add di, ax
    mov ah, byte ptr es:[di]
    test ah, 0feh
    jne loc_0039
loc_002c:
    add di, word ptr [bp - 1ch]
    mov al, byte ptr es:[di]
loc_0032:
    cmp al, 0
    je loc_000c
loc_0036:
    pop di
    pop es
    ret
loc_0039:
    test ah, 2
    je loc_004d
    test ch, 4
    je loc_004d
    test dl, 2
    jne loc_004d
    call _GetSubstituteString
    jae loc_0075
loc_004d:
    test ah, 4
    je loc_005c
    test dl, 4
    jne loc_005c
    call _GetExpansionString
    jae loc_0082
loc_005c:
    test ah, 8
    je loc_002c
    call _GetCompressLevelWeight
    jae loc_0032
    xor ah, 8
    jmp short loc_002c
loc_006b:
    or dl, 80h
    jmp short loc_0036
loc_0070:
    test dl, 2
    je loc_007d
loc_0075:
    call _GetNextAuxChar
    jae loc_001a
    xor dl, 2
loc_007d:
    test dl, 4
    je loc_0010
loc_0082:
    call _GetNextExpansionWeight
    jae loc_0032
    xor dl, 4
    jmp short loc_0010

; Original exported collation interface.
_GetSubstituteString:
    push es
    push di
    push cx
    push bx
    les bx, dword ptr [bp - 24h]
    les di, dword ptr es:[bx + 19ch]
    xor bx, bx
    xor cx, cx
    dec si
loc_009d:
    mov cl, byte ptr es:[bx + di]
    cmp byte ptr es:[bx + di], 0
    je loc_00db
loc_00a6:
    cmp byte ptr es:[bx + di + 1], al
    jne loc_00b4
    inc bx
    dec cx
    mov al, byte ptr [bx + si]
    jcxz loc_00bd
    jmp short loc_00a6
loc_00b4:
    add di, 16h
    xor cx, cx
    xor bx, bx
    jmp short loc_009d
loc_00bd:
    xor ch, ch
    mov cl, byte ptr es:[di]
    add si, cx
    add di, 0ch
    pop bx
    pop cx
    mov word ptr ss:[bx + 2], di
    mov word ptr ss:[bx + 4], es
    dec word ptr ss:[bx]
    or dl, 2
    clc
    pop di
    pop es
    ret
loc_00db:
    pop bx
    pop cx
    inc si
    mov al, byte ptr [si]
    stc
    pop di
    pop es
    ret

; Original exported collation interface.
_GetCompressLevelWeight:
    push es
    push di
    push bx
    push cx
    les bx, dword ptr [bp - 24h]
    les di, dword ptr es:[bx + 198h]
    xor bx, bx
    xor cx, cx
    dec si
loc_00f5:
    mov cl, byte ptr es:[di]
    cmp byte ptr es:[bx + di], 0
    je loc_0129
loc_00fe:
    cmp byte ptr es:[bx + di + 1], al
    jne loc_010c
    inc bx
    dec cx
    mov al, byte ptr [bx + si]
    jcxz loc_0115
    jmp short loc_00fe
loc_010c:
    add di, 13h
    xor cx, cx
    xor bx, bx
    jmp short loc_00f5
loc_0115:
    mov bx, word ptr [bp - 1ah]
    mov al, byte ptr es:[bx + di + 0bh]
    xor ch, ch
    mov cl, byte ptr es:[di]
    add si, cx
    clc
loc_0124:
    pop cx
    pop bx
    pop di
    pop es
    ret
loc_0129:
    mov al, byte ptr [si]
    inc si
    stc
    jmp short loc_0124

; Original exported collation interface.
_GetExpansionString:
    les di, dword ptr [bp - 24h]
    les di, dword ptr es:[di + 194h]
    sub di, 52h
loc_013a:
    add di, 52h
    cmp byte ptr es:[di], 0
    je loc_0171
    cmp byte ptr es:[di], al
    jne loc_013a
    mov al, byte ptr es:[di + 1]
    xor ah, ah
    mov word ptr ss:[bx + 6], ax
    inc di
    inc di
    push cx
    mov cx, word ptr [bp - 1ah]
    jcxz loc_0160
loc_015a:
    add di, 0ah
    dec cx
    jne loc_015a
loc_0160:
    pop cx
    mov word ptr ss:[bx + 2], di
    mov word ptr ss:[bx + 4], es
    dec word ptr ss:[bx]
    or dl, 4
    clc
    ret
loc_0171:
    stc
    ret

; Original exported collation interface.
_GetNextAuxChar:
    mov di, word ptr ss:[bx + 2]
    mov es, word ptr ss:[bx + 4]
    mov al, byte ptr es:[di]
    test al, al
    je loc_018c
    inc di
    mov word ptr ss:[bx + 2], di
    inc word ptr ss:[bx]
    clc
    ret
loc_018c:
    stc
    ret

; Original exported collation interface.
_GetNextExpansionWeight:
    mov es, word ptr ss:[bx + 4]
loc_0192:
    mov di, word ptr ss:[bx + 2]
    cmp word ptr ss:[bx + 6], 0
    je loc_01b1
    mov al, byte ptr es:[di]
    inc word ptr ss:[bx + 2]
    dec word ptr ss:[bx + 6]
    inc word ptr ss:[bx]
    test al, al
    je loc_0192
    clc
    ret
loc_01b1:
    stc
    ret
_TEXT ends
end
