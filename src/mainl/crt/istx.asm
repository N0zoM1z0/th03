; Native Borland istx C++ istream/ostream constructor recovery.
; Original far virtual stream buffer/file buffer ownership and cleanup.
; Real symbolic 8086 procedures plus typed RTTI/exception metadata.
; Never embedded original executable machine CODE byte arrays.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far,@ios@$bdtr$qv:far,@ios@tie$qn7ostream:far
extrn @ios@skip$qi:far,@ios@$bctr$qv:far,@ios@init$qn9streambuf:far
extrn @streambuf@$bdtr$qv:far,@istream@$bdtr$qv:far,@strstreambuf@$bctr$qncit1:far
extrn @strstreambuf@$bdtr$qv:far,@filebuf@$bctr$qi:far,@filebuf@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$bctr$qinci,@istream@$bctr$qiin7ostream

; Typed original exception/RTTI CODE descriptors from +0 to +35.
code_0000:
    dd code_0268 ; original far exception/type descriptor
    dw 8327 ; original typed C++ descriptor word
    dw 65532 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_000e:
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 65502 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 5 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 65535 ; original typed C++ descriptor word
    dw 6 ; original typed C++ descriptor word
    dw 5 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw offset code_0000 ; original CODE label offset field

; Original real 8086 constructor body CODE+36..292.
@istream@$bctr$qinci:
    push bp
    mov bp, sp
    sub sp, 22h
    push si
    push di
    mov ax, seg code_0000
    mov bx, offset code_000e
    call ___InitExceptBlocks
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0056
    mov ax, 2eh
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0056
    jmp near ptr code_00ff
code_0056:
    cmp word ptr [bp + 0ah], 0
    jne code_0081
    mov ax, word ptr [bp + 6]
    add ax, 6
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 6
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
    add word ptr [bp - 8], 1
    adc word ptr [bp - 6], 0
code_0081:
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2], offset DGROUP:ctor_data_08
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx], offset DGROUP:ctor_data_10
    mov ax, 32h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je code_00d9
    mov word ptr [bp - 16h], 0eh
    xor ax, ax
    push ax
    push ax
    push ax
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push dx
    push word ptr [bp - 4]
    call @strstreambuf@$bctr$qncit1
    add sp, 0eh
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 16h], 6
code_00d9:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    push dx
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@init$qn9streambuf
    push word ptr [bp + 12h]
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@skip$qi
    add sp, 0eh
code_00ff:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    push word ptr [bp - 22h]
    call ___ExitExceptBlocks
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Typed original exception/RTTI CODE descriptors from +293 to +328.
code_0125:
    dd code_0254 ; original far exception/type descriptor
    dw 8327 ; original typed C++ descriptor word
    dw 65532 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_0133:
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 65502 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 5 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 65535 ; original typed C++ descriptor word
    dw 6 ; original typed C++ descriptor word
    dw 5 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw offset code_0125 ; original CODE label offset field

; Original real 8086 constructor body CODE+329..595.
@istream@$bctr$qiin7ostream:
    push bp
    mov bp, sp
    sub sp, 22h
    push si
    push di
    mov ax, seg code_0000
    mov bx, offset code_0133
    call ___InitExceptBlocks
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_017b
    mov ax, 2eh
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_017b
    jmp near ptr code_022e
code_017b:
    cmp word ptr [bp + 0ah], 0
    jne code_01a6
    mov ax, word ptr [bp + 6]
    add ax, 6
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 6
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
    add word ptr [bp - 8], 1
    adc word ptr [bp - 6], 0
code_01a6:
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2], offset DGROUP:ctor_data_08
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx], offset DGROUP:ctor_data_10
    mov ax, 36h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je code_01f6
    mov word ptr [bp - 16h], 0eh
    push word ptr [bp + 0ch]
    push dx
    push word ptr [bp - 4]
    call @filebuf@$bctr$qi
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 16h], 6
code_01f6:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    push dx
    push ax
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@init$qn9streambuf
    push word ptr [bp + 0eh]
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@skip$qi
    push word ptr [bp + 12h]
    push word ptr [bp + 10h]
    les bx,dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@tie$qn7ostream
    add sp, 16h
code_022e:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    push word ptr [bp - 22h]
    call ___ExitExceptBlocks
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Typed original exception/RTTI CODE descriptors from +596 to +970.
code_0254:
    dw 4 ; original typed C++ descriptor word
    dw 8336 ; original typed C++ descriptor word
    dw 10 ; original typed C++ descriptor word
    dd code_0317 ; original far exception/type descriptor
    db 'filebuf *',0 ; original Borland C++ RTTI string
code_0268:
    dw 4 ; original typed C++ descriptor word
    dw 8336 ; original typed C++ descriptor word
    dw 10 ; original typed C++ descriptor word
    dd code_02cf ; original far exception/type descriptor
    db 'strstreambuf *',0 ; original Borland C++ RTTI string
code_0281:
    dw 56459 ; original typed C++ descriptor word
    dw 33590 ; original typed C++ descriptor word
    dw 1095 ; original typed C++ descriptor word
    dw 60154 ; original typed C++ descriptor word
    dd @istream@$bdtr$qv ; original far exception/type descriptor
code_028d:
    dw 46 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 38 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dw 127 ; original typed C++ descriptor word
    dw 46 ; original typed C++ descriptor word
    dw 50 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dw 1 ; original typed C++ descriptor word
    dd @istream@$bdtr$qv ; original far exception/type descriptor
    dw 5 ; original typed C++ descriptor word
    dw 62 ; original typed C++ descriptor word
    db 'istream',0 ; original Borland C++ RTTI string
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dd code_0395 ; original far exception/type descriptor
    dw 0 ; original typed C++ descriptor word
    dw 7 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_02cf:
    dw 50 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 38 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 119 ; original typed C++ descriptor word
    dw 52 ; original typed C++ descriptor word
    dw 64 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dd @strstreambuf@$bdtr$qv ; original far exception/type descriptor
    dw 5 ; original typed C++ descriptor word
    dw 68 ; original typed C++ descriptor word
    db 'strstreambuf',0 ; original Borland C++ RTTI string
    db 0 ; original RTTI alignment byte
    dd code_0359 ; original far exception/type descriptor
    dw 0 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_0317:
    dw 54 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 38 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 119 ; original typed C++ descriptor word
    dw 46 ; original typed C++ descriptor word
    dw 58 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dw 2 ; original typed C++ descriptor word
    dd @filebuf@$bdtr$qv ; original far exception/type descriptor
    dw 5 ; original typed C++ descriptor word
    dw 62 ; original typed C++ descriptor word
    db 'filebuf',0 ; original Borland C++ RTTI string
    dd code_0359 ; original far exception/type descriptor
    dw 0 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_0359:
    dw 38 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 38 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 115 ; original typed C++ descriptor word
    dw 48 ; original typed C++ descriptor word
    dw 52 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 1 ; original typed C++ descriptor word
    dw 1 ; original typed C++ descriptor word
    dd @streambuf@$bdtr$qv ; original far exception/type descriptor
    dw 5 ; original typed C++ descriptor word
    dw 56 ; original typed C++ descriptor word
    db 'streambuf',0 ; original Borland C++ RTTI string
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
code_0395:
    dw 40 ; original typed C++ descriptor word
    dw 3 ; original typed C++ descriptor word
    dw 38 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 115 ; original typed C++ descriptor word
    dw 42 ; original typed C++ descriptor word
    dw 46 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 1 ; original typed C++ descriptor word
    dw 1 ; original typed C++ descriptor word
    dd @ios@$bdtr$qv ; original far exception/type descriptor
    dw 5 ; original typed C++ descriptor word
    dw 50 ; original typed C++ descriptor word
    db 'ios',0 ; original Borland C++ RTTI string
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
    dw 0 ; original typed C++ descriptor word
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original C++ exception unwinding DATA frame.
    dd code_028d ; original far destructor/RTTI pointer
    dw 0 ; original exception descriptor field
    dw 0 ; original exception descriptor field
ctor_data_08:
    dd @istream@$bdtr$qv ; original far destructor/RTTI pointer
    dw 6 ; original exception descriptor field
    dw 8 ; original exception descriptor field
ctor_data_10:
    dd code_0281 ; original far destructor/RTTI pointer
_DATA ends
end
