; Original Japanese Borland C++ ioststd standard iostream lifecycle.
; Typed exception tracking and RTTI records in CODE, three streams
; and streambuf handles in BSS, two init and two exit registrations.
; Real 8086 instructions; no machine-code byte arrays/object patches.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,@__GetPolymorphicDTC$qnvui:far
extrn ___InitExceptBlocks:far,___ExitExceptBlocks:far,_isatty:far
extrn @ios@$bdtr$qv:far,@ios@setf$ql:far,@ios@tie$qn7ostream:far
extrn @streambuf@$bdtr$qv:far,@istream@$bdtr$qv:far,@ostream@$bdtr$qv:far
extrn @istream_withassign@$bctr$qv:far,@istream_withassign@$bdtr$qv:far,@istream_withassign@$basg$qn9streambuf:far
extrn @ostream_withassign@$bctr$qv:far,@ostream_withassign@$bdtr$qv:far,@ostream_withassign@$basg$qn9streambuf:far
extrn @filebuf@$bctr$qi:far,@filebuf@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
_EXIT_ segment word public 'EXITDATA'
_EXIT_ ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @Iostream_delete$qv

; Original Borland C++ typed metadata CODE+0000..00d7
code_0000:
    dd code_06dc ; Borland far pointer / lifetime descriptor
    dw 8327 ; original C++ descriptor word
    dw 65532 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_000e:
    dd code_06dc ; Borland far pointer / lifetime descriptor
    dw 8327 ; original C++ descriptor word
    dw 65528 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_001c:
    dd code_06dc ; Borland far pointer / lifetime descriptor
    dw 8327 ; original C++ descriptor word
    dw 65524 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_002a:
    dd code_06bd ; Borland far pointer / lifetime descriptor
    dw 8325 ; original C++ descriptor word
    dw 65520 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0038:
    dd code_069e ; Borland far pointer / lifetime descriptor
    dw 8325 ; original C++ descriptor word
    dw 65516 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0046:
    dd code_069e ; Borland far pointer / lifetime descriptor
    dw 8325 ; original C++ descriptor word
    dw 65512 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0054:
    dd code_069e ; Borland far pointer / lifetime descriptor
    dw 8325 ; original C++ descriptor word
    dw 65508 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0062:
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65478 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 6 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0000 ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 22 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_000e ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_001c ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 54 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_002a ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 70 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0038 ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 86 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0046 ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 102 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0054 ; original relocatable CODE offset

; Original real 8086 C++ startup/destruction instructions +00d8.
initialize_standard_streams:
    push bp
    mov bp, sp
    sub sp, 3ah
    push si
    push di
    mov ax, seg code_0000
    mov bx, offset code_0062
    call ___InitExceptBlocks
    mov ax, 36h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je code_012a
    mov word ptr [bp - 2eh], 0eh
    xor ax, ax
    push ax
    push dx
    push word ptr [bp - 4]
    call @filebuf@$bctr$qi
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 6
code_012a:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    mov word ptr DGROUP:___stdin_streambuf+2, dx
    mov word ptr DGROUP:___stdin_streambuf, ax
    mov ax, 36h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    or ax, dx
    je code_0177
    mov word ptr [bp - 2eh], 1eh
    mov ax, 1
    push ax
    push dx
    push word ptr [bp - 8]
    call @filebuf@$bctr$qi
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 16h
code_0177:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
    mov word ptr DGROUP:___stdout_streambuf+2, dx
    mov word ptr DGROUP:___stdout_streambuf, ax
    mov ax, 36h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    or ax, dx
    je code_01c4
    mov word ptr [bp - 2eh], 2eh
    mov ax, 2
    push ax
    push dx
    push word ptr [bp - 0ch]
    call @filebuf@$bctr$qi
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 26h
code_01c4:
    mov dx, word ptr [bp - 0ah]
    mov ax, word ptr [bp - 0ch]
    mov word ptr DGROUP:___stderr_streambuf+2, dx
    mov word ptr DGROUP:___stderr_streambuf, ax
    mov ax, ds
    mov dx, offset DGROUP:_cin
    mov word ptr [bp - 0eh], ax
    mov word ptr [bp - 10h], dx
    or dx, ax
    je code_020f
    mov word ptr [bp - 2eh], 3eh
    xor ax, ax
    push ax
    push word ptr [bp - 0eh]
    push word ptr [bp - 10h]
    call @istream_withassign@$bctr$qv
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 3
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 36h
    jmp short code_020f
code_020f:
    mov ax, ds
    mov dx, offset DGROUP:_cout
    mov word ptr [bp - 12h], ax
    mov word ptr [bp - 14h], dx
    or dx, ax
    je code_024d
    mov word ptr [bp - 2eh], 4eh
    xor ax, ax
    push ax
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    call @ostream_withassign@$bctr$qv
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 3
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 46h
    jmp short code_024d
code_024d:
    mov ax, ds
    mov dx, offset DGROUP:_cerr
    mov word ptr [bp - 16h], ax
    mov word ptr [bp - 18h], dx
    or dx, ax
    je code_028b
    mov word ptr [bp - 2eh], 5eh
    xor ax, ax
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    call @ostream_withassign@$bctr$qv
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 3
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 56h
    jmp short code_028b
code_028b:
    mov ax, ds
    mov dx, offset DGROUP:_clog
    mov word ptr [bp - 1ah], ax
    mov word ptr [bp - 1ch], dx
    or dx, ax
    je code_02c9
    mov word ptr [bp - 2eh], 6eh
    xor ax, ax
    push ax
    push word ptr [bp - 1ah]
    push word ptr [bp - 1ch]
    call @ostream_withassign@$bctr$qv
    add sp, 6
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 3
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 2eh], 66h
    jmp short code_02c9
code_02c9:
    push word ptr DGROUP:___stdin_streambuf+2
    push word ptr DGROUP:___stdin_streambuf
    push ds
    mov ax, offset DGROUP:_cin
    push ax
    call @istream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stdout_streambuf+2
    push word ptr DGROUP:___stdout_streambuf
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stderr_streambuf+2
    push word ptr DGROUP:___stderr_streambuf
    push ds
    mov ax, offset DGROUP:_clog
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stderr_streambuf+2
    push word ptr DGROUP:___stderr_streambuf
    push ds
    mov ax, offset DGROUP:_cerr
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    push ds
    push word ptr DGROUP:_cin
    call @ios@tie$qn7ostream
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    push ds
    push word ptr DGROUP:_clog
    call @ios@tie$qn7ostream
    add sp, 30h
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    push ds
    push word ptr DGROUP:_cerr
    call @ios@tie$qn7ostream
    xor ax, ax
    mov dx, 2000h
    push ax
    push dx
    push ds
    push word ptr DGROUP:_cerr
    call @ios@setf$ql
    add sp, 10h
    mov ax, 1
    push ax
    call _isatty
    pop cx
    or ax, ax
    je code_0377
    xor ax, ax
    mov dx, 2000h
    push ax
    push dx
    push ds
    push word ptr DGROUP:_cout
    call @ios@setf$ql
    add sp, 8
code_0377:
    push word ptr [bp - 3ah]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original Borland C++ typed metadata CODE+0385..03e4
code_0385:
    dd code_0688 ; Borland far pointer / lifetime descriptor
    dw 16527 ; original C++ descriptor word
    dw 65532 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0393:
    dd code_0688 ; Borland far pointer / lifetime descriptor
    dw 16527 ; original C++ descriptor word
    dw 65528 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_03a1:
    dd code_0688 ; Borland far pointer / lifetime descriptor
    dw 16527 ; original C++ descriptor word
    dw 65524 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_03af:
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65494 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 6 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0385 ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 22 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0393 ; original relocatable CODE offset
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65535 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_03a1 ; original relocatable CODE offset

; Original real 8086 C++ startup/destruction instructions +03e5.
@Iostream_delete$qv:
    push bp
    mov bp, sp
    sub sp, 2ah
    push si
    push di
    mov ax, seg code_0000
    mov bx, offset code_03af
    call ___InitExceptBlocks
    mov dx, word ptr DGROUP:___stdin_streambuf+2
    mov ax, word ptr DGROUP:___stdin_streambuf
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, word ptr [bp - 2]
    je code_044d
    xor ax, ax
    push ax
    push dx
    push word ptr [bp - 4]
    call @__GetPolymorphicDTC$qnvui
    add sp, 6
    push ax
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    pop ax
    add word ptr es:[bx], ax
    adc word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 0eh
    mov ax, 3
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    call dword ptr [bx]
    add sp, 6
    mov word ptr [bp - 1eh], 6
    jmp short code_044d
code_044d:
    mov dx, word ptr DGROUP:___stdout_streambuf+2
    mov ax, word ptr DGROUP:___stdout_streambuf
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    or ax, word ptr [bp - 6]
    je code_04a2
    xor ax, ax
    push ax
    push dx
    push word ptr [bp - 8]
    call @__GetPolymorphicDTC$qnvui
    add sp, 6
    push ax
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    pop ax
    add word ptr es:[bx], ax
    adc word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 1eh
    mov ax, 3
    push ax
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    les bx, dword ptr [bp - 8]
    mov bx, word ptr es:[bx]
    call dword ptr [bx]
    add sp, 6
    mov word ptr [bp - 1eh], 16h
    jmp short code_04a2
code_04a2:
    mov dx, word ptr DGROUP:___stderr_streambuf+2
    mov ax, word ptr DGROUP:___stderr_streambuf
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    or ax, word ptr [bp - 0ah]
    je code_04f7
    xor ax, ax
    push ax
    push dx
    push word ptr [bp - 0ch]
    call @__GetPolymorphicDTC$qnvui
    add sp, 6
    push ax
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    pop ax
    add word ptr es:[bx], ax
    adc word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 2eh
    mov ax, 3
    push ax
    push word ptr [bp - 0ah]
    push word ptr [bp - 0ch]
    les bx, dword ptr [bp - 0ch]
    mov bx, word ptr es:[bx]
    call dword ptr [bx]
    add sp, 6
    mov word ptr [bp - 1eh], 26h
    jmp short code_04f7
code_04f7:
    push word ptr [bp - 2ah]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original Borland C++ typed metadata CODE+0505..053e
code_0505:
    dd code_0632 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dd DGROUP:_cin ; Borland far object pointer (original GROUP frame)
    dd code_05dc ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dd DGROUP:_cout ; Borland far object pointer (original GROUP frame)
    dd code_05dc ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dd DGROUP:_cerr ; Borland far object pointer (original GROUP frame)
    dd code_05dc ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dd DGROUP:_clog ; Borland far object pointer (original GROUP frame)
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0531:
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 65506 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 5 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw code_0505 ; original relocatable CODE offset

; Original real 8086 C++ startup/destruction instructions +053f.
initialize_streams_fallback:
    push bp
    mov bp, sp
    sub sp, 1eh
    push si
    push di
    mov ax, seg code_0000
    mov bx, offset code_0531
    call ___InitExceptBlocks
    mov word ptr [bp - 12h], 6
    xor ax, ax
    push ax
    push ds
    mov ax, offset DGROUP:_cin
    push ax
    call @istream_withassign@$bctr$qv
    xor ax, ax
    push ax
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    call @ostream_withassign@$bctr$qv
    xor ax, ax
    push ax
    push ds
    mov ax, offset DGROUP:_cerr
    push ax
    call @ostream_withassign@$bctr$qv
    xor ax, ax
    push ax
    push ds
    mov ax, offset DGROUP:_clog
    push ax
    call @ostream_withassign@$bctr$qv
    add sp, 18h
    push word ptr [bp - 1eh]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
destroy_streams_fallback:
    push si
    push di
    mov ax, 2
    push ax
    push ds
    mov ax, offset DGROUP:_clog
    push ax
    call @ostream_withassign@$bdtr$qv
    mov ax, 2
    push ax
    push ds
    mov ax, offset DGROUP:_cerr
    push ax
    call @ostream_withassign@$bdtr$qv
    mov ax, 2
    push ax
    push ds
    mov ax, offset DGROUP:_cout
    push ax
    call @ostream_withassign@$bdtr$qv
    mov ax, 2
    push ax
    push ds
    mov ax, offset DGROUP:_cin
    push ax
    call @istream_withassign@$bdtr$qv
    add sp, 18h
    pop di
    pop si
    retf

; Original Borland C++ typed metadata CODE+05dc..0827
code_05dc:
    dw 44 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 127 ; original C++ descriptor word
    dw 58 ; original C++ descriptor word
    dw 70 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dd @ostream_withassign@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 82 ; original C++ descriptor word
    db 'ostream_withassign',0 ; original RTTI class name
    db 0 ; typed RTTI padding byte
    dd code_07e6 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dd code_07b0 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 13 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0632:
    dw 46 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 127 ; original C++ descriptor word
    dw 58 ; original C++ descriptor word
    dw 70 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dd @istream_withassign@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 82 ; original C++ descriptor word
    db 'istream_withassign',0 ; original RTTI class name
    db 0 ; typed RTTI padding byte
    dd code_076e ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dd code_07b0 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 13 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0688:
    dw 4 ; original C++ descriptor word
    dw 8208 ; original C++ descriptor word
    dw 10 ; original C++ descriptor word
    dd code_0732 ; Borland far pointer / lifetime descriptor
    db 'streambuf *',0 ; original RTTI class name
code_069e:
    dw 4 ; original C++ descriptor word
    dw 8336 ; original C++ descriptor word
    dw 10 ; original C++ descriptor word
    dd code_05dc ; Borland far pointer / lifetime descriptor
    db 'ostream_withassign *',0 ; original RTTI class name
code_06bd:
    dw 4 ; original C++ descriptor word
    dw 8336 ; original C++ descriptor word
    dw 10 ; original C++ descriptor word
    dd code_0632 ; Borland far pointer / lifetime descriptor
    db 'istream_withassign *',0 ; original RTTI class name
code_06dc:
    dw 4 ; original C++ descriptor word
    dw 8336 ; original C++ descriptor word
    dw 10 ; original C++ descriptor word
    dd code_06f0 ; Borland far pointer / lifetime descriptor
    db 'filebuf *',0 ; original RTTI class name
code_06f0:
    dw 54 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 119 ; original C++ descriptor word
    dw 46 ; original C++ descriptor word
    dw 58 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dd @filebuf@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 62 ; original C++ descriptor word
    db 'filebuf',0 ; original RTTI class name
    dd code_0732 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_0732:
    dw 38 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 115 ; original C++ descriptor word
    dw 48 ; original C++ descriptor word
    dw 52 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dd @streambuf@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 56 ; original C++ descriptor word
    db 'streambuf',0 ; original RTTI class name
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_076e:
    dw 46 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 127 ; original C++ descriptor word
    dw 46 ; original C++ descriptor word
    dw 50 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dd @istream@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 62 ; original C++ descriptor word
    db 'istream',0 ; original RTTI class name
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dd code_07b0 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 7 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_07b0:
    dw 40 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 115 ; original C++ descriptor word
    dw 42 ; original C++ descriptor word
    dw 46 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dd @ios@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 50 ; original C++ descriptor word
    db 'ios',0 ; original RTTI class name
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
code_07e6:
    dw 44 ; original C++ descriptor word
    dw 3 ; original C++ descriptor word
    dw 38 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 127 ; original C++ descriptor word
    dw 46 ; original C++ descriptor word
    dw 50 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 2 ; original C++ descriptor word
    dw 1 ; original C++ descriptor word
    dd @ostream@$bdtr$qv ; Borland far pointer / lifetime descriptor
    dw 5 ; original C++ descriptor word
    dw 62 ; original C++ descriptor word
    db 'ostream',0 ; original RTTI class name
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dd code_07b0 ; Borland far pointer / lifetime descriptor
    dw 0 ; original C++ descriptor word
    dw 7 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
    dw 0 ; original C++ descriptor word
_TEXTA ends

_BSS segment word public 'BSS'
assume cs:nothing
public _cin,_cout,_cerr,_clog,___stdin_streambuf,___stdout_streambuf,___stderr_streambuf
_cin:
    db 46 dup (?) ; selected original uninitialized _cin
_cout:
    db 44 dup (?) ; selected original uninitialized _cout
_cerr:
    db 44 dup (?) ; selected original uninitialized _cerr
_clog:
    db 44 dup (?) ; selected original uninitialized _clog
___stdin_streambuf:
    db 4 dup (?) ; selected original uninitialized ___stdin_streambuf
___stdout_streambuf:
    db 4 dup (?) ; selected original uninitialized ___stdout_streambuf
___stderr_streambuf:
    db 4 dup (?) ; selected original uninitialized ___stderr_streambuf
_BSS ends

_INIT_ segment word public 'INITDATA'
    db 1,10h
    dd initialize_standard_streams
    db 1,20h
    dd initialize_streams_fallback
_INIT_ ends
_EXIT_ segment word public 'EXITDATA'
    db 1,10h
    dd @Iostream_delete$qv
    db 1,20h
    dd destroy_streams_fallback
_EXIT_ ends
end
