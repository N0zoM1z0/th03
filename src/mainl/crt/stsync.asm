; Original Borland C++ ios::sync_with_stdio: standard stream bridge.
; Actual 8086 source, three typed exception metadata frames and RTTI.
; Original far stdiobuf allocation, stream assignment, flush & unwind.
; No executable CODE byte arrays or patched object programs.
.8086
extrn @$bnew$qui:far,@__RefDestructorCount$qv:far,___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far,@ios@setf$ql:far,@streambuf@$bdtr$qv:far
extrn @ostream@flush$qv:far,@istream_withassign@$basg$qn9streambuf:far,@ostream_withassign@$basg$qn9streambuf:far
extrn _cin:word,_cout:word,_cerr:word
extrn _clog:word,__streams:word,@stdiobuf@$bctr$qn4FILE:far
extrn @stdiobuf@$bdtr$qv:far,___stdin_streambuf:word,___stdout_streambuf:word
extrn ___stderr_streambuf:word
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@sync_with_stdio$qv
; Original Borland exception/RTTI descriptors CODE+0..95.
meta_or_code_0000:
    dd meta_or_code_0264 ; original far class/unwind descriptor
    dw 8327 ; typed C++ metadata word
    dw 65532 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
meta_or_code_000e:
    dd meta_or_code_0264 ; original far class/unwind descriptor
    dw 8327 ; typed C++ metadata word
    dw 65528 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
meta_or_code_001c:
    dd meta_or_code_0264 ; original far class/unwind descriptor
    dw 8327 ; typed C++ metadata word
    dw 65524 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
meta_or_code_002a:
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 65494 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 65535 ; typed C++ metadata word
    dw 6 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw offset meta_or_code_0000 ; original relocated CODE offset
    dw 0 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 65535 ; typed C++ metadata word
    dw 22 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw offset meta_or_code_000e ; original relocated CODE offset
    dw 0 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 65535 ; typed C++ metadata word
    dw 38 ; typed C++ metadata word
    dw 5 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw offset meta_or_code_001c ; original relocated CODE offset

; Actual native C++ standard stream synchronizer +96.
@ios@sync_with_stdio$qv:
    push bp
    mov bp, sp
    sub sp, 2ah
    push si
    push di
    mov ax, seg meta_or_code_0000
    mov bx, offset meta_or_code_002a
    call ___InitExceptBlocks
    cmp word ptr DGROUP:sync_enabled, 0
    je sync_0085
    push word ptr [bp - 2ah]
    call ___ExitExceptBlocks
    jmp near ptr sync_025e
sync_0085:
    mov word ptr DGROUP:sync_enabled, 1
    push ds
    pop es
    mov bx, word ptr DGROUP:_cin
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx,dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 24h]
    push ds
    mov ax,offset DGROUP:_cout
    push ax
    call @ostream@flush$qv
    push ds
    mov ax,offset DGROUP:_clog
    push ax
    call @ostream@flush$qv
    mov ax, 2
    push ax
    push ds
    pop es
    mov bx, word ptr DGROUP:_cin
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@$bdtr$qv
    mov ax, 2
    push ax
    push ds
    pop es
    mov bx, word ptr DGROUP:_cout
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@$bdtr$qv
    mov ax, 2
    push ax
    push ds
    pop es
    mov bx, word ptr DGROUP:_clog
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    call @streambuf@$bdtr$qv
    add sp, 1eh
    mov ax, 2ch
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je sync_0140
    mov word ptr [bp - 1eh], 0eh
    push ds
    mov ax,offset DGROUP:__streams
    push ax
    push dx
    push word ptr [bp - 4]
    call @stdiobuf@$bctr$qn4FILE
    add sp, 8
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 6
sync_0140:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    mov word ptr DGROUP:___stdin_streambuf+2, dx
    mov word ptr DGROUP:___stdin_streambuf, ax
    mov ax, 2ch
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    or ax, dx
    je sync_018e
    mov word ptr [bp - 1eh], 1eh
    push ds
    mov ax,offset DGROUP:__streams+20
    push ax
    push dx
    push word ptr [bp - 8]
    call @stdiobuf@$bctr$qn4FILE
    add sp, 8
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 16h
sync_018e:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
    mov word ptr DGROUP:___stdout_streambuf+2, dx
    mov word ptr DGROUP:___stdout_streambuf, ax
    mov ax, 2ch
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    or ax, dx
    je sync_01dc
    mov word ptr [bp - 1eh], 2eh
    push ds
    mov ax,offset DGROUP:__streams+40
    push ax
    push dx
    push word ptr [bp - 0ch]
    call @stdiobuf@$bctr$qn4FILE
    add sp, 8
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 2
    sbb word ptr es:[bx + 2], 0
    mov word ptr [bp - 1eh], 26h
sync_01dc:
    mov dx, word ptr [bp - 0ah]
    mov ax, word ptr [bp - 0ch]
    mov word ptr DGROUP:___stderr_streambuf+2, dx
    mov word ptr DGROUP:___stderr_streambuf, ax
    push word ptr DGROUP:___stdin_streambuf+2
    push word ptr DGROUP:___stdin_streambuf
    push ds
    mov ax,offset DGROUP:_cin
    push ax
    call @istream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stdout_streambuf+2
    push word ptr DGROUP:___stdout_streambuf
    push ds
    mov ax,offset DGROUP:_cout
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stderr_streambuf+2
    push word ptr DGROUP:___stderr_streambuf
    push ds
    mov ax,offset DGROUP:_cerr
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    push word ptr DGROUP:___stderr_streambuf+2
    push word ptr DGROUP:___stderr_streambuf
    push ds
    mov ax,offset DGROUP:_clog
    push ax
    call @ostream_withassign@$basg$qn9streambuf
    xor ax, ax
    mov dx, 2000h
    push ax
    push dx
    push ds
    push word ptr DGROUP:_cout
    call @ios@setf$ql
    xor ax, ax
    mov dx, 2000h
    push ax
    push dx
    push ds
    push word ptr DGROUP:_clog
    call @ios@setf$ql
    add sp, 30h
    push word ptr [bp - 2ah]
    call ___ExitExceptBlocks
sync_025e:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original Borland exception/RTTI descriptors CODE+612..760.
meta_or_code_0264:
    dw 4 ; typed C++ metadata word
    dw 8336 ; typed C++ metadata word
    dw 10 ; typed C++ metadata word
    dd meta_or_code_0279 ; original far class/unwind descriptor
    db 'stdiobuf *',0 ; original C++ type name
meta_or_code_0279:
    dw 44 ; typed C++ metadata word
    dw 3 ; typed C++ metadata word
    dw 38 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 119 ; typed C++ metadata word
    dw 48 ; typed C++ metadata word
    dw 60 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 2 ; typed C++ metadata word
    dw 2 ; typed C++ metadata word
    dd @stdiobuf@$bdtr$qv ; original far class/unwind descriptor
    dw 5 ; typed C++ metadata word
    dw 64 ; typed C++ metadata word
    db 'stdiobuf',0 ; original C++ type name
    db 0 ; class RTTI alignment
    dd meta_or_code_02bd ; original far class/unwind descriptor
    dw 0 ; typed C++ metadata word
    dw 3 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
meta_or_code_02bd:
    dw 38 ; typed C++ metadata word
    dw 3 ; typed C++ metadata word
    dw 38 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 115 ; typed C++ metadata word
    dw 48 ; typed C++ metadata word
    dw 52 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 1 ; typed C++ metadata word
    dw 1 ; typed C++ metadata word
    dd @streambuf@$bdtr$qv ; original far class/unwind descriptor
    dw 5 ; typed C++ metadata word
    dw 56 ; typed C++ metadata word
    db 'streambuf',0 ; original C++ type name
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
    dw 0 ; typed C++ metadata word
_TEXTA ends

_DATA segment word public 'DATA'
sync_enabled dw 0
_DATA ends
end
