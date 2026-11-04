; Original Japanese Borland 16-bit strstream iosrctr2 full member.
; Real C++ method, three executable adjustor thunks and class RTTI.
; 16-bit symbolic instructions and genuine unwind far pointers.
; No original executable CODE byte arrays, padding or OBJ patches.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@streambuf@$bdtr$qv:far,@istream@$bdtr$qv:far
extrn @ostream@$bdtr$qv:far,@iostream@$bctr$qn9streambuf:far,@iostream@$bdtr$qv:far
extrn @strstreambuf@$bdtr$qv:far,@strstreambase@$bctr$qncit1:far,@strstreambase@$bdtr$qv:far
extrn @strstream@$bdtr$qv:far,_strlen:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstream@$bctr$qncii
@strstream@$bctr$qncii:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne local_0027
    mov ax, 68h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne local_0027
    jmp near ptr local_00f3
local_0027:
    cmp word ptr [bp + 0ah], 0
    jne local_005e
    mov ax, word ptr [bp + 6]
    add ax, 40h
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 40h
    mov word ptr es:[bx + 36h], ax
    mov ax, word ptr [bp + 6]
    add ax, 40h
    mov word ptr es:[bx + 3ch], ax
    mov ax, word ptr [bp + 6]
    add ax, 40h
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
local_005e:
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
    call @iostream@$bctr$qn9streambuf
    add sp, 1ah
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:unwind_10
    mov word ptr es:[bx + 3eh],offset DGROUP:unwind_18
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:unwind_20
    test byte ptr [bp + 12h], 0ch
    je local_00f3
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
local_00f3:
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

; Preserve real far jumps to the destructor even when local.
assume cs:_TEXTA
; Original Borland multiple-inheritance virtual destructor adjustors.
original_0111:
    mov bx,sp
    add word ptr ss:[bx+4],-64
    jmp far ptr @strstream@$bdtr$qv
original_011d:
    mov bx,sp
    add word ptr ss:[bx+4],-60
    jmp far ptr @strstream@$bdtr$qv
original_0129:
    mov bx,sp
    add word ptr ss:[bx+4],-54
    jmp far ptr @strstream@$bdtr$qv

; Real Borland class RTTI and unwind descriptor words.
original_0135:
    dw 104 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 48 ; original class RTTI word
    dw 68 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 8 ; original class RTTI word
    dw 7 ; original class RTTI word
    dd @strstream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 80 ; original class RTTI word
    db 'strstream',0 ; original C++ class name
    dd original_0213 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd original_01bf ; relocated far virtual destructor/type pointer
    dw 54 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0189 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 13 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0189:
    dw 40 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 115 ; original class RTTI word
    dw 42 ; original class RTTI word
    dw 46 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 1 ; original class RTTI word
    dw 1 ; original class RTTI word
    dd @ios@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 50 ; original class RTTI word
    db 'ios',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_01bf:
    dw 50 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 48 ; original class RTTI word
    dw 68 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 4 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd @iostream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 80 ; original class RTTI word
    db 'iostream',0 ; original C++ class name
    db 0 ; original RTTI tail byte
    dd original_02eb ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd original_02a9 ; relocated far virtual destructor/type pointer
    dw 6 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0189 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 13 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0213:
    dw 94 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 52 ; original class RTTI word
    dw 56 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 4 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd @strstreambase@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 68 ; original class RTTI word
    db 'strstreambase',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0189 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0261 ; relocated far virtual destructor/type pointer
    dw 4 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0261:
    dw 50 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 119 ; original class RTTI word
    dw 52 ; original class RTTI word
    dw 64 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 2 ; original class RTTI word
    dd @strstreambuf@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 68 ; original class RTTI word
    db 'strstreambuf',0 ; original C++ class name
    db 0 ; original RTTI tail byte
    dd original_032d ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_02a9:
    dw 44 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 46 ; original class RTTI word
    dw 50 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 1 ; original class RTTI word
    dd @ostream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 62 ; original class RTTI word
    db 'ostream',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0189 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_02eb:
    dw 46 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 46 ; original class RTTI word
    dw 50 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 1 ; original class RTTI word
    dd @istream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 62 ; original class RTTI word
    db 'istream',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0189 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_032d:
    dw 38 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 115 ; original class RTTI word
    dw 48 ; original class RTTI word
    dw 52 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 1 ; original class RTTI word
    dw 1 ; original class RTTI word
    dd @streambuf@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 56 ; original class RTTI word
    db 'streambuf',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original 36-byte exception frame: five far destructor/type pointers.
    dd original_0135 ; actual original far unwind pointer
    dw 0 ; unwind descriptor
    dw 0 ; unwind descriptor
unwind_08:
    dd @strstream@$bdtr$qv ; actual original far unwind pointer
    dw 54 ; unwind descriptor
    dw 8 ; unwind descriptor
unwind_10:
    dd original_0129 ; actual original far unwind pointer
    dw 60 ; unwind descriptor
    dw 16 ; unwind descriptor
unwind_18:
    dd original_011d ; actual original far unwind pointer
    dw 64 ; unwind descriptor
    dw 24 ; unwind descriptor
unwind_20:
    dd original_0111 ; actual original far unwind pointer
_DATA ends
end
