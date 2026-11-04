; Complete original isrctr2 Borland 16-bit C++ strstream constructors.
; All three real far constructors, typed class RTTI and unwind table.
; Genuine symbolic 8086 instructions, not executable CODE byte arrays.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@streambuf@$bdtr$qv:far,@istream@$bctr$qn9streambuf:far
extrn @istream@$bdtr$qv:far,@strstreambuf@$bdtr$qv:far,@strstreambase@$bctr$qncit1:far
extrn @strstreambase@$bdtr$qv:far,@istrstream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istrstream@$bctr$qnci,@istrstream@$bctr$qnzci,@istrstream@$bctr$qnuci

; Original far C++ constructor CODE+0.
@istrstream@$bctr$qnci:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0024
    mov ax, 64h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0024
    jmp near ptr code_00a4
code_0024:
    cmp word ptr [bp + 0ah], 0
    jne code_0051
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_0051:
    xor ax, ax
    push ax
    push ax
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
    call @istream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
code_00a4:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf

; Original far C++ constructor CODE+192.
@istrstream@$bctr$qnzci:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_00e4
    mov ax, 64h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_00e4
    jmp near ptr code_0164
code_00e4:
    cmp word ptr [bp + 0ah], 0
    jne code_0111
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_0111:
    xor ax, ax
    push ax
    push ax
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
    call @istream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
code_0164:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf

; Original far C++ constructor CODE+384.
@istrstream@$bctr$qnuci:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_01a4
    mov ax, 64h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_01a4
    jmp near ptr code_0224
code_01a4:
    cmp word ptr [bp + 0ah], 0
    jne code_01d1
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 3ch
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_01d1:
    xor ax, ax
    push ax
    push ax
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
    call @istream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:ctor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:ctor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ctor_unwind_18
code_0224:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    pop bp
    retf

; Original Borland class-descriptor RTTI, not executable instructions.
native_class_0240:
    dw 56459 ; C++ RTTI descriptor word
    dw 33590 ; C++ RTTI descriptor word
    dw 1095 ; C++ RTTI descriptor word
    dw 60100 ; C++ RTTI descriptor word
    dd @istrstream@$bdtr$qv ; original far destructor/type metadata
native_class_024c:
    dw 56459 ; C++ RTTI descriptor word
    dw 33590 ; C++ RTTI descriptor word
    dw 1095 ; C++ RTTI descriptor word
    dw 60106 ; C++ RTTI descriptor word
    dd @istrstream@$bdtr$qv ; original far destructor/type metadata
native_class_0258:
    dw 100 ; C++ RTTI descriptor word
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
    dd @istrstream@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 82 ; C++ RTTI descriptor word
    db 'istrstream',0 ; original C++ class name
    db 0 ; RTTI alignment byte
    dd native_class_0326 ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dd native_class_02e4 ; original far destructor/type metadata
    dw 54 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_02ae ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 13 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_02ae:
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
native_class_02e4:
    dw 46 ; C++ RTTI descriptor word
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
    dd @istream@$bdtr$qv ; original far destructor/type metadata
    dw 5 ; C++ RTTI descriptor word
    dw 62 ; C++ RTTI descriptor word
    db 'istream',0 ; original C++ class name
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_02ae ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 7 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_0326:
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
    dd native_class_02ae ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 7 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dd native_class_0374 ; original far destructor/type metadata
    dw 4 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_0374:
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
    dd native_class_03bc ; original far destructor/type metadata
    dw 0 ; C++ RTTI descriptor word
    dw 3 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
    dw 0 ; C++ RTTI descriptor word
native_class_03bc:
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
    dd native_class_0258 ; original far destructor/type pointer
    dw 0 ; original unwind descriptor field
    dw 0 ; original unwind descriptor field
ctor_unwind_08:
    dd @istrstream@$bdtr$qv ; original far destructor/type pointer
    dw 54 ; original unwind descriptor field
    dw 8 ; original unwind descriptor field
ctor_unwind_10:
    dd native_class_024c ; original far destructor/type pointer
    dw 60 ; original unwind descriptor field
    dw 16 ; original unwind descriptor field
ctor_unwind_18:
    dd native_class_0240 ; original far destructor/type pointer
_DATA ends
end
