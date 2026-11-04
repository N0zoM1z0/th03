; Recovered Japanese Borland large-model srdtr destructor.
; Actual 8086 far C++ destructor plus executable native adjustor.
; Typed class RTTI and real 20-byte initialized unwind DATA.
; Never machine-CODE byte arrays or patched native OBJ records.
.8086
extrn @$bdele$qnv:far,@__RefDestructorCount$qv:far,@ios@$bdtr$qv:far
extrn @streambuf@$bdtr$qv:far,@strstreambuf@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambase@$bdtr$qv

@strstreambase@$bdtr$qv:
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
    je native_0074
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2],offset DGROUP:unwind_ref08
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:unwind_ref16
    mov ax, 2
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    call @strstreambuf@$bdtr$qv
    add sp, 6
    test byte ptr [bp + 0ah], 2
    je native_0061
    xor ax, ax
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 36h
    push word ptr [bp + 8]
    push ax
    call @ios@$bdtr$qv
    add sp, 6

native_0061:
    test byte ptr [bp + 0ah], 1
    je native_0074
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @$bdele$qnv
    pop cx
    pop cx

native_0074:
    pop di
    pop si
    pop bp
    retf

; Original same-member far destructor thunk; prevent near folding.
assume cs:nothing
native_destructor_adjustor:
    mov bx,sp
    add word ptr ss:[bx+4],-54
    jmp far ptr @strstreambase@$bdtr$qv

; Nonexecutable original Borland RTTI/destructor records.
rtti_0084:
    dw 94 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dw 38 ; C++ RTTI descriptor
    dw 2 ; C++ RTTI descriptor
    dw 127 ; C++ RTTI descriptor
    dw 52 ; C++ RTTI descriptor
    dw 56 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 4 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dd @strstreambase@$bdtr$qv ; far destructor/type descriptor
    dw 5 ; C++ RTTI descriptor
    dw 68 ; C++ RTTI descriptor
    db 'strstreambase',0 ; original class name
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dd rtti_011a ; far destructor/type descriptor
    dw 0 ; C++ RTTI descriptor
    dw 7 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dd rtti_00d2 ; far destructor/type descriptor
    dw 4 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
rtti_00d2:
    dw 50 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dw 38 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 119 ; C++ RTTI descriptor
    dw 52 ; C++ RTTI descriptor
    dw 64 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 2 ; C++ RTTI descriptor
    dw 2 ; C++ RTTI descriptor
    dd @strstreambuf@$bdtr$qv ; far destructor/type descriptor
    dw 5 ; C++ RTTI descriptor
    dw 68 ; C++ RTTI descriptor
    db 'strstreambuf',0 ; original class name
    db 0 ; native RTTI alignment
    dd rtti_0150 ; far destructor/type descriptor
    dw 0 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
rtti_011a:
    dw 40 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dw 38 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 115 ; C++ RTTI descriptor
    dw 42 ; C++ RTTI descriptor
    dw 46 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 1 ; C++ RTTI descriptor
    dw 1 ; C++ RTTI descriptor
    dd @ios@$bdtr$qv ; far destructor/type descriptor
    dw 5 ; C++ RTTI descriptor
    dw 50 ; C++ RTTI descriptor
    db 'ios',0 ; original class name
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
rtti_0150:
    dw 38 ; C++ RTTI descriptor
    dw 3 ; C++ RTTI descriptor
    dw 38 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 115 ; C++ RTTI descriptor
    dw 48 ; C++ RTTI descriptor
    dw 52 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 1 ; C++ RTTI descriptor
    dw 1 ; C++ RTTI descriptor
    dd @streambuf@$bdtr$qv ; far destructor/type descriptor
    dw 5 ; C++ RTTI descriptor
    dw 56 ; C++ RTTI descriptor
    db 'streambuf',0 ; original class name
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
    dw 0 ; C++ RTTI descriptor
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original native exception/unwind DATA descriptors.
    dd rtti_0084 ; original far unwind pointer
    dw 0 ; original unwind field
    dw 0 ; original unwind field
unwind_ref08:
    dd @strstreambase@$bdtr$qv ; original far unwind pointer
    dw 54 ; original unwind field
    dw 8 ; original unwind field
unwind_ref16:
    dd native_destructor_adjustor ; original far unwind pointer
_DATA ends
end
