; Original Japanese Borland C++ osrdtr complete destructor.
; Genuine far 8086 method, typed class RTTI and unwind pointers.
; No original executable machine CODE bytes or patched object records.
.8086
extrn @$bdele$qnv:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @streambuf@$bdtr$qv:far,@ostream@$bdtr$qv:far,@strstreambuf@$bdtr$qv:far
extrn @strstreambase@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostrstream@$bdtr$qv
@ostrstream@$bdtr$qv:
    push bp
    mov bp, sp
    push si
    push di
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 1
    sbb word ptr es:[bx + 2], 0
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je local_0087
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:dtor_unwind_08
    mov word ptr es:[bx + 38h],offset DGROUP:dtor_unwind_10
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:dtor_unwind_18
    xor ax, ax
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ostream@$bdtr$qv
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @strstreambase@$bdtr$qv
    add sp, 0ch
    test byte ptr [bp + 0ah], 2
    je local_0074
    xor ax, ax
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 3ah
    push word ptr [bp + 8]
    push ax
    call @ios@$bdtr$qv
    add sp, 6
local_0074:
    test byte ptr [bp + 0ah], 1
    je local_0087
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @$bdele$qnv
    pop cx
    pop cx
local_0087:
    pop di
    pop si
    pop bp
    retf

; Original typed Borland C++ RTTI / virtual destructor descriptors.
dtor_meta_008b:
    dw 56459 ; class descriptor word
    dw 33590 ; class descriptor word
    dw 1095 ; class descriptor word
    dw 60102 ; class descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/class pointer
dtor_meta_0097:
    dw 56459 ; class descriptor word
    dw 33590 ; class descriptor word
    dw 1095 ; class descriptor word
    dw 60106 ; class descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/class pointer
dtor_meta_00a3:
    dw 98 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 2 ; class descriptor word
    dw 127 ; class descriptor word
    dw 50 ; class descriptor word
    dw 70 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 6 ; class descriptor word
    dw 5 ; class descriptor word
    dd @ostrstream@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 82 ; class descriptor word
    db 'ostrstream',0 ; actual original class name
    db 0 ; class descriptor trailing byte
    dd dtor_meta_0171 ; original far destructor/class pointer
    dw 0 ; class descriptor word
    dw 3 ; class descriptor word
    dd dtor_meta_012f ; original far destructor/class pointer
    dw 54 ; class descriptor word
    dw 3 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dd dtor_meta_00f9 ; original far destructor/class pointer
    dw 0 ; class descriptor word
    dw 13 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
dtor_meta_00f9:
    dw 40 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 0 ; class descriptor word
    dw 115 ; class descriptor word
    dw 42 ; class descriptor word
    dw 46 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 1 ; class descriptor word
    dw 1 ; class descriptor word
    dd @ios@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 50 ; class descriptor word
    db 'ios',0 ; actual original class name
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
dtor_meta_012f:
    dw 44 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 2 ; class descriptor word
    dw 127 ; class descriptor word
    dw 46 ; class descriptor word
    dw 50 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 2 ; class descriptor word
    dw 1 ; class descriptor word
    dd @ostream@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 62 ; class descriptor word
    db 'ostream',0 ; actual original class name
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dd dtor_meta_00f9 ; original far destructor/class pointer
    dw 0 ; class descriptor word
    dw 7 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
dtor_meta_0171:
    dw 94 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 2 ; class descriptor word
    dw 127 ; class descriptor word
    dw 52 ; class descriptor word
    dw 56 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 4 ; class descriptor word
    dw 3 ; class descriptor word
    dd @strstreambase@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 68 ; class descriptor word
    db 'strstreambase',0 ; actual original class name
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dd dtor_meta_00f9 ; original far destructor/class pointer
    dw 0 ; class descriptor word
    dw 7 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dd dtor_meta_01bf ; original far destructor/class pointer
    dw 4 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
dtor_meta_01bf:
    dw 50 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 0 ; class descriptor word
    dw 119 ; class descriptor word
    dw 52 ; class descriptor word
    dw 64 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 2 ; class descriptor word
    dw 2 ; class descriptor word
    dd @strstreambuf@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 68 ; class descriptor word
    db 'strstreambuf',0 ; actual original class name
    db 0 ; class descriptor trailing byte
    dd dtor_meta_0207 ; original far destructor/class pointer
    dw 0 ; class descriptor word
    dw 3 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
dtor_meta_0207:
    dw 38 ; class descriptor word
    dw 3 ; class descriptor word
    dw 38 ; class descriptor word
    dw 0 ; class descriptor word
    dw 115 ; class descriptor word
    dw 48 ; class descriptor word
    dw 52 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 1 ; class descriptor word
    dw 1 ; class descriptor word
    dd @streambuf@$bdtr$qv ; original far destructor/class pointer
    dw 5 ; class descriptor word
    dw 56 ; class descriptor word
    db 'streambuf',0 ; actual original class name
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
    dw 0 ; class descriptor word
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Actual original 28-byte exception frame / far-pointer table.
    dd dtor_meta_00a3 ; real relocated far pointer
    dw 0 ; unwind descriptor field
    dw 0 ; unwind descriptor field
dtor_unwind_08:
    dd @ostrstream@$bdtr$qv ; real relocated far pointer
    dw 54 ; unwind descriptor field
    dw 8 ; unwind descriptor field
dtor_unwind_10:
    dd dtor_meta_0097 ; real relocated far pointer
    dw 58 ; unwind descriptor field
    dw 16 ; unwind descriptor field
dtor_unwind_18:
    dd dtor_meta_008b ; real relocated far pointer
_DATA ends
end
