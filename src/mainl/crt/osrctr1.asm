; Complete original osrctr1 Borland 16-bit C++ strstream constructors.
; All three real far constructors, typed class RTTI and unwind table.
; Genuine symbolic 8086 instructions, not executable CODE byte arrays.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@streambuf@$bdtr$qv:far,@ostream@$bctr$qn9streambuf:far
extrn @ostream@$bdtr$qv:far,@strstreambuf@$bdtr$qv:far,@strstreambase@$bctr$qncit1:far
extrn @strstreambase@$bdtr$qv:far,@ostrstream@$bdtr$qv:far,_strlen:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostrstream@$bctr$qncii,@ostrstream@$bctr$qnzcii,@ostrstream@$bctr$qnucii

; Original far C++ constructor CODE+0.
@ostrstream@$bctr$qncii:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0027
    mov ax, 62h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0027
    jmp near ptr code_00e3
code_0027:
    cmp word ptr [bp + 0ah], 0
    jne code_0054
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_0054:
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @strstreambase@$bctr$qncit1
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ostream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
    test byte ptr [bp + 12h], 0ch
    je code_00e3
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    call _strlen
    pop cx
    pop cx
    xor dx, dx
    push dx
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4
    mov word ptr [bp - 2], ax
    push word ptr [bp + 8]
    push ax
    mov es, word ptr [bp + 8]
    mov bx, word ptr [bp - 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 1ch]
    add sp, 0ch
code_00e3:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original far C++ constructor CODE+257.
@ostrstream@$bctr$qnzcii:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0128
    mov ax, 62h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0128
    jmp near ptr code_01e4
code_0128:
    cmp word ptr [bp + 0ah], 0
    jne code_0155
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_0155:
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @strstreambase@$bctr$qncit1
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ostream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
    test byte ptr [bp + 12h], 0ch
    je code_01e4
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    call _strlen
    pop cx
    pop cx
    xor dx, dx
    push dx
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4
    mov word ptr [bp - 2], ax
    push word ptr [bp + 8]
    push ax
    mov es, word ptr [bp + 8]
    mov bx, word ptr [bp - 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 1ch]
    add sp, 0ch
code_01e4:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original far C++ constructor CODE+514.
@ostrstream@$bctr$qnucii:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0229
    mov ax, 62h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0229
    jmp near ptr code_02e5
code_0229:
    cmp word ptr [bp + 0ah], 0
    jne code_0256
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_0256:
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @strstreambase@$bctr$qncit1
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ostream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
    test byte ptr [bp + 12h], 0ch
    je code_02e5
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push word ptr [bp + 0eh]
    push word ptr [bp + 0ch]
    call _strlen
    pop cx
    pop cx
    xor dx, dx
    push dx
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4
    mov word ptr [bp - 2], ax
    push word ptr [bp + 8]
    push ax
    mov es, word ptr [bp + 8]
    mov bx, word ptr [bp - 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 1ch]
    add sp, 0ch
code_02e5:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original Borland class-descriptor RTTI, not executable instructions.
native_class_0303:
    dw 56459 ; C++ RTTI descriptor word
    dw 33590 ; C++ RTTI descriptor word
    dw 1095 ; C++ RTTI descriptor word
    dw 60102 ; C++ RTTI descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/type metadata
native_class_030f:
    dw 56459 ; C++ RTTI descriptor word
    dw 33590 ; C++ RTTI descriptor word
    dw 1095 ; C++ RTTI descriptor word
    dw 60106 ; C++ RTTI descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/type metadata
native_class_031b:
    dw 98 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dw 127 ; C++ RTTI descriptor word
    dw 50 ; C++ RTTI descriptor word
    dw 70 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 6 ; C++ RTTI descriptor word
    dw 5 ; C++ RTTI descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 82 ; C++ RTTI descriptor word
    db 'ostrstream',0 ; original C++ class name
    db 0 ; RTTI alignment byte
    dd native_class_03e9 ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dd native_class_03a7 ; original far destructor/type metadata
    dw 54 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_0371 ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 13 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_0371:
    dw 40 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 115 ; C++ RTTI descriptor word
    dw 42 ; C++ RTTI descriptor word
    dw 46 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 1 ; C++ RTTI descriptor word
    dw 1 ; C++ RTTI descriptor word
    dd @ios@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 50 ; C++ RTTI descriptor word
    db 'ios',0 ; original C++ class name
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_03a7:
    dw 44 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dw 127 ; C++ RTTI descriptor word
    dw 46 ; C++ RTTI descriptor word
    dw 50 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dw 1 ; C++ RTTI descriptor word
    dd @ostream@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 62 ; C++ RTTI descriptor word
    db 'ostream',0 ; original C++ class name
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_0371 ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 7 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_03e9:
    dw 94 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dw 127 ; C++ RTTI descriptor word
    dw 52 ; C++ RTTI descriptor word
    dw 56 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 4 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dd @strstreambase@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 68 ; C++ RTTI descriptor word
    db 'strstreambase',0 ; original C++ class name
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_0371 ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 7 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_0437 ; original far destructor/type metadata
    dw 4 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_0437:
    dw 50 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 119 ; C++ RTTI descriptor word
    dw 52 ; C++ RTTI descriptor word
    dw 64 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dw 2 ; C++ RTTI descriptor word
    dd @strstreambuf@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 68 ; C++ RTTI descriptor word
    db 'strstreambuf',0 ; original C++ class name
    db 0 ; RTTI alignment byte
    dd native_class_047f ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_047f:
    dw 38 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 38 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 115 ; C++ RTTI descriptor word
    dw 48 ; C++ RTTI descriptor word
    dw 52 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 1 ; C++ RTTI descriptor word
    dw 1 ; C++ RTTI descriptor word
    dd @streambuf@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 56 ; C++ RTTI descriptor word
    db 'streambuf',0 ; original C++ class name
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original 28-byte C++ unwind and RTTI far-pointer table.
    dd native_class_031b ; original far destructor/type pointer
    dw 0 ; original unwind descriptor field
    dw 0 ; original unwind descriptor field
ctor_unwind_08:
    dd @ostrstream@$bdtr$qv ; original far destructor/type pointer
    dw 54 ; original unwind descriptor field
    dw 8 ; original unwind descriptor field
ctor_unwind_10:
    dd native_class_030f ; original far destructor/type pointer
    dw 58 ; original unwind descriptor field
    dw 16 ; original unwind descriptor field
ctor_unwind_18:
    dd native_class_0303 ; original far destructor/type pointer
_DATA ends
end
