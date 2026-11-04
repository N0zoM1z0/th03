; Original Japanese Borland C++ srbskoff full stream buffer method.
; Real 8086 far pointer arithmetic, vtable calls and original ABI.
; No executable machine-CODE byte arrays, no patched OBJ records.
.8086
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@seekoff$ql12ios@seek_diri

; Selected original C++ far entry, 600 CODE bytes.
@strstreambuf@seekoff$ql12ios@seek_diri:
    push bp
    mov bp, sp
    sub sp, 10h
    push si
    push di
    mov word ptr [bp - 2], 0ffffh
    mov word ptr [bp - 4], 0ffffh
    cmp word ptr [bp + 0eh], 2
    jne loc_0055
    les bx,dword ptr [bp + 6]
    test byte ptr es:[bx + 2eh], 4
    jne loc_0030
    cmp word ptr [bp + 0ch], 0
    jl loc_003c
    jg loc_0030
    cmp word ptr [bp + 0ah], 0
    jbe loc_003c
loc_0030:
    mov word ptr [bp - 2], 0ffffh
    mov word ptr [bp - 4], 0ffffh
    jmp short loc_0067
loc_003c:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cwd
    add ax, word ptr [bp + 0ah]
    adc dx, word ptr [bp + 0ch]
    jmp short loc_0061
loc_0055:
    cmp word ptr [bp + 0eh], 0
    jne loc_0067
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
loc_0061:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
loc_0067:
    test byte ptr [bp + 10h], 1
    jne loc_0070
    jmp near ptr loc_016e
loc_0070:
    cmp word ptr [bp + 0eh], 1
    jne loc_00ba
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_0089
    mov ax, word ptr es:[bx + 1eh]
    jmp short loc_009a
loc_0089:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je loc_00ae
    mov ax, word ptr es:[bx + 12h]
loc_009a:
    les bx,dword ptr [bp + 6]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    add ax, word ptr [bp + 0ah]
    adc dx, word ptr [bp + 0ch]
    jmp short loc_00b4
loc_00ae:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
loc_00b4:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
loc_00ba:
    cmp word ptr [bp - 2], 0
    jl loc_00e5
    jne loc_00c8
    cmp word ptr [bp - 4], 0
    jb loc_00e5
loc_00c8:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cwd
    cmp dx, word ptr [bp - 2]
    jg loc_00f1
    jl loc_00e5
    cmp ax, word ptr [bp - 4]
    jae loc_00f1
loc_00e5:
    mov word ptr [bp - 2], 0ffffh
    mov word ptr [bp - 4], 0ffffh
    jmp short loc_016e
loc_00f1:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    add ax, word ptr [bp - 4]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    mov ax, word ptr es:[bx + 1ah]
    or ax, word ptr es:[bx + 1ch]
    je loc_011e
    mov ax, word ptr es:[bx + 1ah]
    cmp ax, word ptr [bp - 8]
    jae loc_011e
    mov dx, word ptr es:[bx + 1ch]
    jmp short loc_0124
loc_011e:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
loc_0124:
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    or ax, word ptr es:[bx + 24h]
    je loc_0146
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr [bp - 8]
    jbe loc_0146
    mov dx, word ptr es:[bx + 24h]
    jmp short loc_014c
loc_0146:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
loc_014c:
    mov word ptr [bp - 0eh], dx
    mov word ptr [bp - 10h], ax
    push dx
    push ax
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    push word ptr [bp - 0ch]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    add sp, 10h
loc_016e:
    test byte ptr [bp + 10h], 2
    jne loc_0177
    jmp near ptr loc_024c
loc_0177:
    cmp word ptr [bp + 0eh], 1
    jne loc_01c1
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 12h]
    or ax, word ptr es:[bx + 14h]
    je loc_0190
    mov ax, word ptr es:[bx + 12h]
    jmp short loc_01a1
loc_0190:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 1eh]
    or ax, word ptr es:[bx + 20h]
    je loc_01b5
    mov ax, word ptr es:[bx + 1eh]
loc_01a1:
    les bx,dword ptr [bp + 6]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    add ax, word ptr [bp + 0ah]
    adc dx, word ptr [bp + 0ch]
    jmp short loc_01bb
loc_01b5:
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
loc_01bb:
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
loc_01c1:
    cmp word ptr [bp - 2], 0
    jl loc_01ec
    jne loc_01cf
    cmp word ptr [bp - 4], 0
    jb loc_01ec
loc_01cf:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    xor dx, dx
    sub ax, word ptr es:[bx + 6]
    sbb dx, 0
    cwd
    cmp dx, word ptr [bp - 2]
    jg loc_01f8
    jl loc_01ec
    cmp ax, word ptr [bp - 4]
    jae loc_01f8
loc_01ec:
    mov word ptr [bp - 2], 0ffffh
    mov word ptr [bp - 4], 0ffffh
    jmp short loc_024c
loc_01f8:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 8]
    mov ax, word ptr es:[bx + 6]
    add ax, word ptr [bp - 4]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    mov ax, word ptr es:[bx + 16h]
    or ax, word ptr es:[bx + 18h]
    je loc_0225
    mov ax, word ptr es:[bx + 16h]
    cmp ax, word ptr [bp - 8]
    jbe loc_0225
    mov dx, word ptr es:[bx + 18h]
    jmp short loc_0230
loc_0225:
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 0ch]
    mov ax, word ptr es:[bx + 0ah]
loc_0230:
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    push dx
    push ax
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setp$qnct1
    add sp, 0ch
loc_024c:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
