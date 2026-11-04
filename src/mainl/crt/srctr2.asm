; Original Japanese Borland C++ srctr2 complete constructor.
; Real 8086 far constructor, genuine destructor adjustor and RTTI.
; No executable CODE byte initializer, no padding or OBJ patch.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far,@ios@init$qn9streambuf:far,@streambuf@$bdtr$qv:far
extrn @strstreambuf@$bctr$qv:far,@strstreambuf@$bdtr$qv:far,@strstreambase@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambase@$bctr$qv

@strstreambase@$bctr$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne native_branch_0021
    mov ax, 5eh
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    je native_branch_007d

native_branch_0021:
    cmp word ptr [bp + 0ah], 0
    jne native_branch_0044
    mov ax, word ptr [bp + 6]
    add ax, 36h
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx

native_branch_0044:
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2], offset DGROUP:native_unwind_08
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx], offset DGROUP:native_unwind_10
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    call @strstreambuf@$bctr$qv
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@init$qn9streambuf
    add sp, 0ch

native_branch_007d:
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

; Actual 8086 far C++ destructor-adjustment thunk.
dtor_adjustor:
    mov bx,sp
    add word ptr ss:[bx+4],-54
    jmp far ptr @strstreambase@$bdtr$qv

; Non-executable original Borland C++ typed RTTI and class records.
native_rtti_00a5:
    dw 94 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dw 38 ; native C++ descriptor
    dw 2 ; native C++ descriptor
    dw 127 ; native C++ descriptor
    dw 52 ; native C++ descriptor
    dw 56 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 4 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dd @strstreambase@$bdtr$qv ; original far destructor/type pointer
    dw 5 ; native C++ descriptor
    dw 68 ; native C++ descriptor
    db 'strstreambase',0 ; authentic original RTTI class name
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dd native_rtti_013b ; original far destructor/type pointer
    dw 0 ; native C++ descriptor
    dw 7 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dd native_rtti_00f3 ; original far destructor/type pointer
    dw 4 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
native_rtti_00f3:
    dw 50 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dw 38 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 119 ; native C++ descriptor
    dw 52 ; native C++ descriptor
    dw 64 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 2 ; native C++ descriptor
    dw 2 ; native C++ descriptor
    dd @strstreambuf@$bdtr$qv ; original far destructor/type pointer
    dw 5 ; native C++ descriptor
    dw 68 ; native C++ descriptor
    db 'strstreambuf',0 ; authentic original RTTI class name
    db 0 ; native RTTI alignment
    dd native_rtti_0171 ; original far destructor/type pointer
    dw 0 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
native_rtti_013b:
    dw 40 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dw 38 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 115 ; native C++ descriptor
    dw 42 ; native C++ descriptor
    dw 46 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 1 ; native C++ descriptor
    dw 1 ; native C++ descriptor
    dd @ios@$bdtr$qv ; original far destructor/type pointer
    dw 5 ; native C++ descriptor
    dw 50 ; native C++ descriptor
    db 'ios',0 ; authentic original RTTI class name
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
native_rtti_0171:
    dw 38 ; native C++ descriptor
    dw 3 ; native C++ descriptor
    dw 38 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 115 ; native C++ descriptor
    dw 48 ; native C++ descriptor
    dw 52 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 1 ; native C++ descriptor
    dw 1 ; native C++ descriptor
    dd @streambuf@$bdtr$qv ; original far destructor/type pointer
    dw 5 ; native C++ descriptor
    dw 56 ; native C++ descriptor
    db 'streambuf',0 ; authentic original RTTI class name
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
    dw 0 ; native C++ descriptor
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original native 20-byte C++ constructor unwind frame.
    dd native_rtti_00a5 ; real relocated native far pointer
    dw 0 ; original unwind word
    dw 0 ; original unwind word
native_unwind_08:
    dd @strstreambase@$bdtr$qv ; real relocated native far pointer
    dw 54 ; original unwind word
    dw 8 ; original unwind word
native_unwind_10:
    dd dtor_adjustor ; real relocated native far pointer
_DATA ends
end
