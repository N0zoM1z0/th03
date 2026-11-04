; Original Japanese Borland 16-bit ostrstream osrctr2 full member.
; Real C++ method, two executable adjustor thunks and class RTTI.
; 16-bit symbolic instructions and genuine unwind far pointers.
; No original executable CODE byte arrays, padding or OBJ patches.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@streambuf@$bdtr$qv:far,@ostream@$bctr$qn9streambuf:far
extrn @ostream@$bdtr$qv:far,@strstreambuf@$bdtr$qv:far,@strstreambase@$bctr$qv:far
extrn @strstreambase@$bdtr$qv:far,@ostrstream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostrstream@$bctr$qv
@ostrstream@$bctr$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne local_0021
    mov ax, 62h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    je local_0094
local_0021:
    cmp word ptr [bp + 0ah], 0
    jne local_004e
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
local_004e:
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @strstreambase@$bctr$qv
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
    add sp, 10h
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:unwind_18
local_0094:
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

; Original Borland multiple-inheritance virtual destructor adjustors.
original_00b0:
    mov bx,sp
    add word ptr ss:[bx+4],-58
    jmp far ptr @ostrstream@$bdtr$qv
original_00bc:
    mov bx,sp
    add word ptr ss:[bx+4],-54
    jmp far ptr @ostrstream@$bdtr$qv

; Real Borland class RTTI and unwind descriptor words.
original_00c8:
    dw 98 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 50 ; original class RTTI word
    dw 70 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 6 ; original class RTTI word
    dw 5 ; original class RTTI word
    dd @ostrstream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 82 ; original class RTTI word
    db 'ostrstream',0 ; original C++ class name
    db 0 ; original RTTI tail byte
    dd original_0196 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd original_0154 ; relocated far virtual destructor/type pointer
    dw 54 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_011e ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 13 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_011e:
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
original_0154:
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
    dd original_011e ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0196:
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
    dd original_011e ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_01e4 ; relocated far virtual destructor/type pointer
    dw 4 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_01e4:
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
    dd original_022c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_022c:
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
; Original 28-byte exception frame: four far destructor/type pointers.
    dd original_00c8 ; actual original far unwind pointer
    dw 0 ; unwind descriptor
    dw 0 ; unwind descriptor
unwind_08:
    dd @ostrstream@$bdtr$qv ; actual original far unwind pointer
    dw 54 ; unwind descriptor
    dw 8 ; unwind descriptor
unwind_10:
    dd original_00bc ; actual original far unwind pointer
    dw 58 ; unwind descriptor
    dw 16 ; unwind descriptor
unwind_18:
    dd original_00b0 ; actual original far unwind pointer
_DATA ends
end
