; Original Japanese Borland 16-bit fstream iofsctr1 full member.
; Real C++ method, three executable adjustor thunks and class RTTI.
; 16-bit symbolic instructions and genuine unwind far pointers.
; No original executable CODE byte arrays, padding or OBJ patches.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@streambuf@$bdtr$qv:far,@istream@$bdtr$qv:far
extrn @ostream@$bdtr$qv:far,@iostream@$bdtr$qv:far,@iostream@$bctr$qv:far
extrn @filebuf@$bdtr$qv:far,@fstreambase@$bctr$qv:far,@fstreambase@$bdtr$qv:far
extrn @fstream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @fstream@$bctr$qv
@fstream@$bctr$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne local_0021
    mov ax, 6ch
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    je local_009a
local_0021:
    cmp word ptr [bp + 0ah], 0
    jne local_0058
    mov ax, word ptr [bp + 6]
    add ax, 44h
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 44h
    mov word ptr es:[bx + 3ah], ax
    mov ax, word ptr [bp + 6]
    add ax, 44h
    mov word ptr es:[bx + 40h], ax
    mov ax, word ptr [bp + 6]
    add ax, 44h
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
local_0058:
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @fstreambase@$bctr$qv
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    push word ptr [bp + 8]
    push ax
    call @iostream@$bctr$qv
    add sp, 0ch
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:unwind_08
    mov word ptr es:[bx + 3ch],offset DGROUP:unwind_10
    mov word ptr es:[bx + 42h],offset DGROUP:unwind_18
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:unwind_20
local_009a:
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
original_00b6:
    mov bx,sp
    add word ptr ss:[bx+4],-68
    jmp far ptr @fstream@$bdtr$qv
original_00c2:
    mov bx,sp
    add word ptr ss:[bx+4],-64
    jmp far ptr @fstream@$bdtr$qv
original_00ce:
    mov bx,sp
    add word ptr ss:[bx+4],-58
    jmp far ptr @fstream@$bdtr$qv

; Real Borland class RTTI and unwind descriptor words.
original_00da:
    dw 108 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 46 ; original class RTTI word
    dw 66 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 8 ; original class RTTI word
    dw 7 ; original class RTTI word
    dd @fstream@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 78 ; original class RTTI word
    db 'fstream',0 ; original C++ class name
    dd original_01b6 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd original_0162 ; relocated far virtual destructor/type pointer
    dw 58 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_012c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 13 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_012c:
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
original_0162:
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
    dd original_0286 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd original_0244 ; relocated far virtual destructor/type pointer
    dw 6 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_012c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 13 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_01b6:
    dw 98 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 127 ; original class RTTI word
    dw 50 ; original class RTTI word
    dw 54 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 4 ; original class RTTI word
    dw 3 ; original class RTTI word
    dd @fstreambase@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 66 ; original class RTTI word
    db 'fstreambase',0 ; original C++ class name
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_012c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dd original_0202 ; relocated far virtual destructor/type pointer
    dw 4 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0202:
    dw 54 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 38 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 119 ; original class RTTI word
    dw 46 ; original class RTTI word
    dw 58 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 2 ; original class RTTI word
    dw 2 ; original class RTTI word
    dd @filebuf@$bdtr$qv ; relocated far virtual destructor/type pointer
    dw 5 ; original class RTTI word
    dw 62 ; original class RTTI word
    db 'filebuf',0 ; original C++ class name
    dd original_02c8 ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 3 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0244:
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
    dd original_012c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_0286:
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
    dd original_012c ; relocated far virtual destructor/type pointer
    dw 0 ; original class RTTI word
    dw 7 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
    dw 0 ; original class RTTI word
original_02c8:
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
    dd original_00da ; actual original far unwind pointer
    dw 0 ; unwind descriptor
    dw 0 ; unwind descriptor
unwind_08:
    dd @fstream@$bdtr$qv ; actual original far unwind pointer
    dw 58 ; unwind descriptor
    dw 8 ; unwind descriptor
unwind_10:
    dd original_00ce ; actual original far unwind pointer
    dw 64 ; unwind descriptor
    dw 16 ; unwind descriptor
unwind_18:
    dd original_00c2 ; actual original far unwind pointer
    dw 68 ; unwind descriptor
    dw 24 ; unwind descriptor
unwind_20:
    dd original_00b6 ; actual original far unwind pointer
_DATA ends
end
