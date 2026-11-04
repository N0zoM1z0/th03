; Original Japanese Borland C++ console stream extension: conbuf and
; constream full methods, virtual slots, RTTI and destructors.
; Real 8086 instructions and typed metadata, no executable code blobs.
.8086
extrn @$bnew$qui:far,@$bdele$qnv:far,@__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far,@ios@setf$ql:far,@ios@tie$qn7ostream:far
extrn @ios@bitalloc$qv:far,@ios@$bctr$qv:far,@streambuf@$bctr$qv:far
extrn @streambuf@$bdtr$qv:far,@streambuf@setbuf$qnci:far,@streambuf@do_sgetn$qnci:far
extrn @streambuf@underflow$qv:far,@streambuf@pbackfail$qi:far,@streambuf@do_sputn$qnxci:far
extrn @streambuf@seekoff$ql12ios@seek_diri:far,@streambuf@seekpos$qli:far,@streambuf@doallocate$qv:far
extrn @ostream@$bctr$qn9streambuf:far,@ostream@$bdtr$qv:far,_cin:word
extrn _clreol:far,_gotoxy:far,_putch:far
extrn _delline:far,_gettextinfo:far,_highvideo:far
extrn _insline:far,_lowvideo:far,_normvideo:far
extrn _textattr:far,_textbackground:far,_textcolor:far
extrn _window:far,__setcursortype:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @conbuf@$bctr$qv,@conbuf@overflow$qi,@conbuf@makeActive$qv,@conbuf@makeInactive$qv,@conbuf@swap$qv,@constream@$bctr$qv,@clreol$qm7ostream,@highvideo$qm7ostream,@lowvideo$qm7ostream,@normvideo$qm7ostream,@delline$qm7ostream,@insline$qm7ostream,@setcrsrtype$qi,@setattr$qi,@setxy$qii,@setbk$qi,@setclr$qi

; Original public C++ method at CODE+0
@conbuf@$bctr$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0021
    mov ax, 35h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    je code_004f
code_0021:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@$bctr$qv
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx], offset DGROUP:constream_vtable
    mov ax, word ptr [bp + 6]
    add ax, 26h
    push word ptr [bp + 8]
    push ax
    call _gettextinfo
    add sp, 8
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 33h], 2
code_004f:
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

; Original public C++ method at CODE+107
@conbuf@overflow$qi:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr DGROUP:@conbuf@current+2
    mov ax, word ptr DGROUP:@conbuf@current
    cmp dx, word ptr [bp + 8]
    jne code_0081
    cmp ax, word ptr [bp + 6]
    je code_0094
code_0081:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_0094
code_0094:
    cmp word ptr [bp + 0ah], 0ah
    jne code_00a4
    mov ax, 0dh
    push ax
    call _putch
    pop cx
code_00a4:
    push word ptr [bp + 0ah]
    call _putch
    pop cx
    pop di
    pop si
    pop bp
    retf

; Original public C++ method at CODE+177
@conbuf@makeActive$qv:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov al, byte ptr es:[bx + 29h]
    mov ah, 0
    push ax
    mov al, byte ptr es:[bx + 28h]
    mov ah, 0
    push ax
    mov al, byte ptr es:[bx + 27h]
    mov ah, 0
    push ax
    mov al, byte ptr es:[bx + 26h]
    mov ah, 0
    push ax
    call _window
    les bx, dword ptr [bp + 6]
    push word ptr es:[bx + 2ah]
    call _textattr
    les bx, dword ptr [bp + 6]
    mov al, byte ptr es:[bx + 32h]
    mov ah, 0
    push ax
    mov al, byte ptr es:[bx + 31h]
    mov ah, 0
    push ax
    call _gotoxy
    les bx, dword ptr [bp + 6]
    push word ptr es:[bx + 33h]
    call __setcursortype
    add sp, 10h
    pop di
    pop si
    pop bp
    retf

; Original public C++ method at CODE+271
@conbuf@makeInactive$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    add ax, 26h
    push word ptr [bp + 8]
    push ax
    call _gettextinfo
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

; Original public C++ method at CODE+297
@conbuf@swap$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr DGROUP:@conbuf@current
    or ax, word ptr DGROUP:@conbuf@current+2
    je code_014b
    push word ptr DGROUP:@conbuf@current+2
    push word ptr DGROUP:@conbuf@current
    les bx, dword ptr DGROUP:@conbuf@current
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 30h]
    pop cx
    pop cx
code_014b:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 2ch]
    pop cx
    pop cx
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr DGROUP:@conbuf@current+2, dx
    mov word ptr DGROUP:@conbuf@current, ax
    pop di
    pop si
    pop bp
    retf

; Original public C++ method at CODE+365
@constream@$bctr$qv:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0191
    mov ax, 61h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne code_0191
    jmp near ptr code_023e
code_0191:
    cmp word ptr [bp + 0ah], 0
    jne code_01b4
    mov ax, word ptr [bp + 6]
    add ax, 39h
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp + 6]
    add ax, 39h
    push word ptr [bp + 8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
code_01b4:
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    mov ax, 1
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@$bctr$qn9streambuf
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 2], offset DGROUP:constrea_vtable_16
    mov bx, word ptr es:[bx]
    mov word ptr es:[bx], offset DGROUP:constrea_vtable_24
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    push cs
    call @conbuf@$bctr$qv
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push ds
    push word ptr DGROUP:_cin
    call @ios@tie$qn7ostream
    xor ax, ax
    mov dx, 2000h
    push ax
    push dx
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setf$ql
    add sp, 1eh
    mov ax, word ptr DGROUP:@constream@isCon_
    or ax, word ptr DGROUP:@constream@isCon_+2
    jne code_0227
    call @ios@bitalloc$qv
    mov word ptr DGROUP:@constream@isCon_+2, dx
    mov word ptr DGROUP:@constream@isCon_, ax
code_0227:
    push word ptr DGROUP:@constream@isCon_+2
    push word ptr DGROUP:@constream@isCon_
    les bx, dword ptr [bp + 6]
    push es
    push word ptr es:[bx]
    call @ios@setf$ql
    add sp, 8
code_023e:
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

; Original public C++ method at CODE+602
@clreol$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_028d
    mov ax, 1
    jmp short code_028f
code_028d:
    xor ax, ax
code_028f:
    or ax, ax
    je code_02d4
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_02ad
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_02cf
code_02ad:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_02cf
code_02cf:
    call _clreol
code_02d4:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+736
@highvideo$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_0313
    mov ax, 1
    jmp short code_0315
code_0313:
    xor ax, ax
code_0315:
    or ax, ax
    je code_035a
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_0333
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_0355
code_0333:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_0355
code_0355:
    call _highvideo
code_035a:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+870
@lowvideo$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_0399
    mov ax, 1
    jmp short code_039b
code_0399:
    xor ax, ax
code_039b:
    or ax, ax
    je code_03e0
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_03b9
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_03db
code_03b9:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_03db
code_03db:
    call _lowvideo
code_03e0:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+1004
@normvideo$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_041f
    mov ax, 1
    jmp short code_0421
code_041f:
    xor ax, ax
code_0421:
    or ax, ax
    je code_0466
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_043f
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_0461
code_043f:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_0461
code_0461:
    call _normvideo
code_0466:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+1138
@delline$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_04a5
    mov ax, 1
    jmp short code_04a7
code_04a5:
    xor ax, ax
code_04a7:
    or ax, ax
    je code_04ec
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_04c5
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_04e7
code_04c5:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_04e7
code_04e7:
    call _delline
code_04ec:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+1272
@insline$qm7ostream:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_052b
    mov ax, 1
    jmp short code_052d
code_052b:
    xor ax, ax
code_052d:
    or ax, ax
    je code_0572
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_054b
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_056d
code_054b:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_056d
code_056d:
    call _insline
code_0572:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_057e:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_05b1
    mov ax, 1
    jmp short code_05b3
code_05b1:
    xor ax, ax
code_05b3:
    or ax, ax
    je code_0611
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 6], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_05d7
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_05f9
code_05d7:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 8], es
    mov word ptr [bp - 0ah], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_05f9
code_05f9:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    les bx, dword ptr es:[bx + 2]
    mov ax, word ptr [bp - 6]
    mov word ptr es:[bx + 33h], ax
    push ax
    call __setcursortype
    pop cx
code_0611:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+1565
@setcrsrtype$qi:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], ax
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or ax, word ptr [bp - 4]
    je code_0641
    mov ax, word ptr [bp - 6]
    jmp short code_0651
code_0641:
    mov ax, 6
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
code_0651:
    or ax, dx
    je code_066a
    les bx, dword ptr [bp - 6]
    mov word ptr es:[bx + 2], seg @conbuf@$bctr$qv
    mov word ptr es:[bx], offset code_057e
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx + 4], ax
code_066a:
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_067c:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_06af
    mov ax, 1
    jmp short code_06b1
code_06af:
    xor ax, ax
code_06b1:
    or ax, ax
    je code_0700
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 6], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_06d5
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_06f7
code_06d5:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 8], es
    mov word ptr [bp - 0ah], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_06f7
code_06f7:
    push word ptr [bp - 6]
    call _textattr
    pop cx
code_0700:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+1804
@setattr$qi:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], ax
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or ax, word ptr [bp - 4]
    je code_0730
    mov ax, word ptr [bp - 6]
    jmp short code_0740
code_0730:
    mov ax, 6
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
code_0740:
    or ax, dx
    je code_0759
    les bx, dword ptr [bp - 6]
    mov word ptr es:[bx + 2], seg @conbuf@$bctr$qv
    mov word ptr es:[bx], offset code_067c
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx + 4], ax
code_0759:
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_076b:
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_079e
    mov ax, 1
    jmp short code_07a0
code_079e:
    xor ax, ax
code_07a0:
    or ax, ax
    je code_07f9
    mov ax, word ptr [bp + 0ch]
    mov word ptr [bp - 6], ax
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 8], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_07ca
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_07ec
code_07ca:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ah], es
    mov word ptr [bp - 0ch], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_07ec
code_07ec:
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    call _gotoxy
    pop cx
    pop cx
code_07f9:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+2053
@setxy$qii:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov ax, word ptr [bp + 0ch]
    mov word ptr [bp - 2], ax
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 4], ax
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    or ax, word ptr [bp - 6]
    je code_082f
    mov ax, word ptr [bp - 8]
    jmp short code_083f
code_082f:
    mov ax, 8
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
code_083f:
    or ax, dx
    je code_085f
    les bx, dword ptr [bp - 8]
    mov word ptr es:[bx + 2], seg @conbuf@$bctr$qv
    mov word ptr es:[bx], offset code_076b
    mov ax, word ptr [bp - 4]
    mov word ptr es:[bx + 4], ax
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx + 6], ax
code_085f:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_0871:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_08a4
    mov ax, 1
    jmp short code_08a6
code_08a4:
    xor ax, ax
code_08a6:
    or ax, ax
    je code_08f5
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 6], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_08ca
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_08ec
code_08ca:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 8], es
    mov word ptr [bp - 0ah], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_08ec
code_08ec:
    push word ptr [bp - 6]
    call _textbackground
    pop cx
code_08f5:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+2305
@setbk$qi:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], ax
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or ax, word ptr [bp - 4]
    je code_0925
    mov ax, word ptr [bp - 6]
    jmp short code_0935
code_0925:
    mov ax, 6
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
code_0935:
    or ax, dx
    je code_094e
    les bx, dword ptr [bp - 6]
    mov word ptr es:[bx + 2], seg @conbuf@$bctr$qv
    mov word ptr es:[bx], offset code_0871
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx + 4], ax
code_094e:
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_0960:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx, dword ptr [bp - 4]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 12h]
    mov ax, word ptr es:[bx + 10h]
    and ax, word ptr DGROUP:@constream@isCon_
    and dx, word ptr DGROUP:@constream@isCon_+2
    or ax, dx
    je code_0993
    mov ax, 1
    jmp short code_0995
code_0993:
    xor ax, ax
code_0995:
    or ax, ax
    je code_09e4
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 6], ax
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov dx, word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 2]
    cmp dx, word ptr DGROUP:@conbuf@current+2
    jne code_09b9
    cmp ax, word ptr DGROUP:@conbuf@current
    je code_09db
code_09b9:
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 8], es
    mov word ptr [bp - 0ah], bx
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 2]
    les bx, dword ptr es:[bx + 2]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 34h]
    pop cx
    pop cx
    jmp short code_09db
code_09db:
    push word ptr [bp - 6]
    call _textcolor
    pop cx
code_09e4:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public C++ method at CODE+2544
@setclr$qi:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 2], ax
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or ax, word ptr [bp - 4]
    je code_0a14
    mov ax, word ptr [bp - 6]
    jmp short code_0a24
code_0a14:
    mov ax, 6
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
code_0a24:
    or ax, dx
    je code_0a3d
    les bx, dword ptr [bp - 6]
    mov word ptr es:[bx + 2], seg @conbuf@$bctr$qv
    mov word ptr es:[bx], offset code_0960
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx + 4], ax
code_0a3d:
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
code_0a4f:
    mov bx, sp
    add word ptr ss:[bx + 4], -39h
    assume cs:NOTHING
    jmp far ptr code_0aef
    assume cs:_TEXT

; Full original typed class RTTI descriptors at CODE+2651
; Original Borland class RTTI/vtable fields are typed CODE metadata.
code_0a5b:
    dw 53 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 38 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 119 ; Borland RTTI descriptor value
    dw 46 ; Borland RTTI descriptor value
    dw 58 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 2 ; Borland RTTI descriptor value
    dw 2 ; Borland RTTI descriptor value
    dd code_0b95 ; Borland far RTTI function/descriptor pointer
    dw 5 ; Borland RTTI descriptor value
    dw 62 ; Borland RTTI descriptor value
class_name_conbuf db 'conbuf',0,0 ; Borland double-zero RTTI terminator
    dd code_0c6d ; Borland far RTTI function/descriptor pointer
    dw 0 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
code_0a9d:
    dw 97 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 38 ; Borland RTTI descriptor value
    dw 2 ; Borland RTTI descriptor value
    dw 127 ; Borland RTTI descriptor value
    dw 48 ; Borland RTTI descriptor value
    dw 60 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 5 ; Borland RTTI descriptor value
    dw 4 ; Borland RTTI descriptor value
    dd code_0aef ; Borland far RTTI function/descriptor pointer
    dw 5 ; Borland RTTI descriptor value
    dw 72 ; Borland RTTI descriptor value
class_name_constream db 'constream',0
    dd code_0c2b ; Borland far RTTI function/descriptor pointer
    dw 0 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dd code_0bf5 ; Borland far RTTI function/descriptor pointer
    dw 0 ; Borland RTTI descriptor value
    dw 13 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dd code_0a5b ; Borland far RTTI function/descriptor pointer
    dw 4 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
code_0aef:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne code_0aff
    jmp near ptr code_0b8f
code_0aff:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 1
    sbb word ptr es:[bx + 2], 0
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    sub word ptr es:[bx], 1
    sbb word ptr es:[bx + 2], 0
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx + 4], offset DGROUP:constream_vtable
    mov word ptr DGROUP:@conbuf@current+2, 0
    mov word ptr DGROUP:@conbuf@current, 0
    xor ax, ax
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4
    push word ptr [bp + 8]
    push ax
    call @streambuf@$bdtr$qv
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @ostream@$bdtr$qv
    add sp, 0ch
    test byte ptr [bp + 0ah], 2
    je code_0b78
    xor ax, ax
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 39h
    push word ptr [bp + 8]
    push ax
    call @ios@$bdtr$qv
    add sp, 6
    jmp short code_0b78
code_0b78:
    test byte ptr [bp + 0ah], 1
    je code_0b8d
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short code_0b91
code_0b8d:
    jmp short code_0b91
code_0b8f:
    xor ax, ax
code_0b91:
    pop di
    pop si
    pop bp
    retf
code_0b95:
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
    je code_0bea
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx], offset DGROUP:constream_vtable
    mov word ptr DGROUP:@conbuf@current+2, 0
    mov word ptr DGROUP:@conbuf@current, 0
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push bx
    call @streambuf@$bdtr$qv
    add sp, 6
    test byte ptr [bp + 0ah], 1
    je code_0bea
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @$bdele$qnv
    pop cx
    pop cx
code_0bea:
    pop di
    pop si
    pop bp
    retf
code_0bee:
    push si
    push di
    xor ax, ax
    pop di
    pop si
    retf

; Full original typed class RTTI descriptors at CODE+3061
; Original Borland class RTTI/vtable fields are typed CODE metadata.
code_0bf5:
    dw 40 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 38 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 115 ; Borland RTTI descriptor value
    dw 42 ; Borland RTTI descriptor value
    dw 46 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 1 ; Borland RTTI descriptor value
    dw 1 ; Borland RTTI descriptor value
    dd @ios@$bdtr$qv ; Borland far RTTI function/descriptor pointer
    dw 5 ; Borland RTTI descriptor value
    dw 50 ; Borland RTTI descriptor value
class_name_ios db 'ios',0
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
code_0c2b:
    dw 44 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 38 ; Borland RTTI descriptor value
    dw 2 ; Borland RTTI descriptor value
    dw 127 ; Borland RTTI descriptor value
    dw 46 ; Borland RTTI descriptor value
    dw 50 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 2 ; Borland RTTI descriptor value
    dw 1 ; Borland RTTI descriptor value
    dd @ostream@$bdtr$qv ; Borland far RTTI function/descriptor pointer
    dw 5 ; Borland RTTI descriptor value
    dw 62 ; Borland RTTI descriptor value
class_name_ostream db 'ostream',0
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dd code_0bf5 ; Borland far RTTI function/descriptor pointer
    dw 0 ; Borland RTTI descriptor value
    dw 7 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
code_0c6d:
    dw 38 ; Borland RTTI descriptor value
    dw 3 ; Borland RTTI descriptor value
    dw 38 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 115 ; Borland RTTI descriptor value
    dw 48 ; Borland RTTI descriptor value
    dw 52 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 1 ; Borland RTTI descriptor value
    dw 1 ; Borland RTTI descriptor value
    dd @streambuf@$bdtr$qv ; Borland far RTTI function/descriptor pointer
    dw 5 ; Borland RTTI descriptor value
    dw 56 ; Borland RTTI descriptor value
class_name_streambuf db 'streambuf',0
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
    dw 0 ; Borland RTTI descriptor value
_TEXT ends
_DATA segment word public 'DATA'
; Runtime Borland RTTI pointers refer to CS labels from DATA.
assume cs:nothing
public @conbuf@current,@constream@isCon_
@conbuf@current:
    dw 0 ; Original Borland conbuf/constream field
    dw 0 ; Original Borland conbuf/constream field
@constream@isCon_:
    dw 0 ; Original Borland conbuf/constream field
    dw 0 ; Original Borland conbuf/constream field
    dd code_0a9d ; Original far vtable/virtual method pointer
    dw 0 ; Original Borland conbuf/constream field
    dw 0 ; Original Borland conbuf/constream field
constrea_vtable_16:
    dd code_0aef ; Original far vtable/virtual method pointer
    dw 57 ; Original Borland conbuf/constream field
    dw 8 ; Original Borland conbuf/constream field
constrea_vtable_24:
    dd code_0a4f ; Original far vtable/virtual method pointer
    dd code_0a5b ; Original far vtable/virtual method pointer
    dw 0 ; Original Borland conbuf/constream field
    dw 0 ; Original Borland conbuf/constream field
constream_vtable:
    dd code_0b95 ; Original far vtable/virtual method pointer
    dd @streambuf@setbuf$qnci ; Original far vtable/virtual method pointer
    dd @streambuf@do_sgetn$qnci ; Original far vtable/virtual method pointer
    dd @streambuf@underflow$qv ; Original far vtable/virtual method pointer
    dd @streambuf@pbackfail$qi ; Original far vtable/virtual method pointer
    dd @streambuf@do_sputn$qnxci ; Original far vtable/virtual method pointer
    dd @conbuf@overflow$qi ; Original far vtable/virtual method pointer
    dd @streambuf@seekoff$ql12ios@seek_diri ; Original far vtable/virtual method pointer
    dd @streambuf@seekpos$qli ; Original far vtable/virtual method pointer
    dd code_0bee ; Original far vtable/virtual method pointer
    dd @streambuf@doallocate$qv ; Original far vtable/virtual method pointer
    dd @conbuf@makeActive$qv ; Original far vtable/virtual method pointer
    dd @conbuf@makeInactive$qv ; Original far vtable/virtual method pointer
    dd @conbuf@swap$qv ; Original far vtable/virtual method pointer
_DATA ends
end
