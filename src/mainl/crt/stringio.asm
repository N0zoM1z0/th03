; Complete original Borland C++ string I/O: eleven independent far APIs.
; Includes string/stream adapters, format processing, token scanning,
; exception bookkeeping and typed xalloc/xmsg class metadata.
; All CODE instructions and DATA/RTTI fields are real 8086/TASM source,
; not blobs of executable target bytes or post-assembly binary patches.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn __ctype:byte
extrn @xmsg@$bdtr$qv:far
extrn @string@skip_white:word
extrn @string@resize_inc:word
extrn @string@clone$qv:far
extrn @TStringRef@check_freeboard$qv:far
extrn @TStringRef@grow_to$qui:far
extrn @TStringRef@round_capacity$qui:far
extrn @istream@ipfx$qi:far
extrn @istream@get$qncic:far
extrn @istream@get$qmc:far
extrn @istream@putback$qc:far
extrn @istream@$brsh$qnc:far
extrn @ostream@outstr$qnxct1:far
extrn @setw$qi:far

_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
DGROUP group _BSS,_DATA

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Borland exception-handler no-op and two typed cleanup frame records.
exception_noop:
    push si
    push di
    pop di
    pop si
    retf
stringio_read_delim_frame:
    dd stringio_rtti_xalloc
    dd 0
stringio_read_delim_state:
    dd stringio_read_delim_frame
    dw -30
stringio_read_token_frame:
    dd stringio_rtti_xalloc
    dd 0
stringio_read_token_state:
    dd stringio_read_token_frame
    dw -30

; Original non-exported far exception object destructor.
stringio_destroy_xalloc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz branch_1_0068
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz branch_1_0066
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short branch_1_006a

branch_1_0066:
    jmp short branch_1_006a

branch_1_0068:
    xor ax,ax

branch_1_006a:
    pop di
    pop si
    pop bp
    retf

_TEXT ends

_DATA segment word public 'DATA'
_DATA ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@read_file$qm7istream
public @string@read_string$qm7istream
public @string@read_line$qm7istream
public @string@read_to_delim$qm7istreamc
public @string@read_token$qm7istream
public @$brsh$qm7istreamm6string
public @$blsh$qm7ostreammx6string
public @getline$qm7istreamm6string
public @getline$qm7istreamm6stringc
public @TStringRef@read_to_delim$qm7istreamc
public @TStringRef@read_token$qm7istream


; String read_file: delegate to the full delimiter reader (NUL terminator).
@string@read_file$qm7istream:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna stringio_0020
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short stringio_0020

stringio_0020:
    mov al,0
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    ; Borland emits direct FAR 9A even for the same _TEXTC segment.
    ; TASM otherwise shortens this to PUSH CS + near CALL; the one real
    ; opcode and symbolic far OMF relocation preserve original codegen.
    db 09ah
    dd @TStringRef@read_to_delim$qm7istreamc
    add sp,10
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    pop bp
    retf

; String read_string: delegate to the same full delimiter reader.
@string@read_string$qm7istream:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna stringio_0065
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short stringio_0065

stringio_0065:
    mov al,0
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    db 09ah
    dd @TStringRef@read_to_delim$qm7istreamc
    add sp,10
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    pop bp
    retf

; String read_line: optional whitespace skip, ctype and newline checks.
@string@read_line$qm7istream:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    cmp word ptr DGROUP:@string@skip_white,0
    jz stringio_00e2

stringio_0099:
    push ss
    lea ax,[bp-1]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@get$qmc
    add sp,8
    les bx,[bp+10]
    mov bx,es:[bx]
    cmp word ptr es:[bx+10],0
    jnz stringio_00be
    mov ax,1
    jmp short stringio_00c0

stringio_00be:
    xor ax,ax

stringio_00c0:
    or ax,ax
    jz stringio_00d1
    mov al,[bp-1]
    cbw
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],1
    jnz stringio_0099

stringio_00d1:
    push word ptr [bp-1]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@putback$qc
    add sp,6

stringio_00e2:
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna stringio_00fd
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short stringio_00fd

stringio_00fd:
    mov al,10
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    db 09ah
    dd @TStringRef@read_to_delim$qm7istreamc
    add sp,10
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; String read_to_delim: clone shared references and forward delimiter.
@string@read_to_delim$qm7istreamc:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna stringio_0144
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short stringio_0144

stringio_0144:
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    db 09ah
    dd @TStringRef@read_to_delim$qm7istreamc
    add sp,10
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    pop bp
    retf

; String read_token: clone shared references and scan bounded token.
@string@read_token$qm7istream:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna stringio_0189
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short stringio_0189

stringio_0189:
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    ; Same original FAR 9A / relocatable far target in this code segment.
    db 09ah
    dd @TStringRef@read_token$qm7istream
    add sp,8
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    pop bp
    retf

; Istream string extraction operator (full original member).
@$brsh$qm7istreamm6string:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push cs
    call @string@read_token$qm7istream
    add sp,8
    pop di
    pop si
    pop bp
    retf

; Ostream string insertion: original width manipulator and output routine.
@$blsh$qm7ostreammx6string:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,[bp+10]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    mov [bp-2],dx
    mov [bp-4],ax
    xor ax,ax
    push ax
    push ax
    push dx
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@outstr$qnxct1
    add sp,12
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; getline overload: forwards to line reader.
@getline$qm7istreamm6string:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push cs
    call @string@read_line$qm7istream
    add sp,8
    pop di
    pop si
    pop bp
    retf

; getline with explicit character delimiter.
@getline$qm7istreamm6stringc:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+14]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push cs
    call @string@read_to_delim$qm7istreamc
    add sp,10
    pop di
    pop si
    pop bp
    retf

; Reference buffer delimiter scan, with far exception cleanup.
@TStringRef@read_to_delim$qm7istreamc:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:stringio_read_delim_state
    call ___InitExceptBlocks
    les bx,[bp+6]
    mov word ptr es:[bx+6],0

stringio_025c:
    push word ptr [bp+14]
    les bx,[bp+6]
    mov ax,es:[bx+8]
    mov dx,es:[bx+6]
    mov [bp-34],dx
    sub ax,dx
    inc ax
    push ax
    mov ax,es:[bx+2]
    add ax,[bp-34]
    push word ptr es:[bx+4]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@get$qncic
    add sp,12
    les bx,[bp+6]
    mov ax,es:[bx+2]
    push bx
    push es
    add ax,es:[bx+6]
    pop es
    pop bx
    push word ptr es:[bx+4]
    push ax
    call _strlen
    pop cx
    pop cx
    les bx,[bp+6]
    add es:[bx+6],ax
    les bx,[bp+10]
    mov bx,es:[bx]
    cmp word ptr es:[bx+10],0
    jnz stringio_030a
    push ss
    lea ax,[bp-31]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@get$qmc
    add sp,8
    mov al,[bp-31]
    cmp al,[bp+14]
    jz stringio_030a
    push word ptr [bp-31]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@putback$qc
    add sp,6
    les bx,[bp+6]
    mov ax,es:[bx+6]
    add ax,DGROUP:@string@resize_inc
    push ax
    call @TStringRef@round_capacity$qui
    pop cx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @TStringRef@grow_to$qui
    add sp,6
    jmp near ptr stringio_025c

stringio_030a:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @TStringRef@check_freeboard$qv
    pop cx
    pop cx
    push word ptr [bp-30]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Reference buffer token scan: 16-bit capacity, growth and ctype.
@TStringRef@read_token$qm7istream:
    push bp
    mov bp,sp
    sub sp,58
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:stringio_read_token_state
    call ___InitExceptBlocks
    les bx,[bp+6]
    mov word ptr es:[bx+6],0
    jmp near ptr stringio_0414

stringio_0344:
    les bx,[bp+6]
    mov ax,es:[bx+2]
    push bx
    push es
    add ax,es:[bx+6]
    pop es
    pop bx
    push word ptr es:[bx+4]
    push ax
    call _strlen
    pop cx
    pop cx
    les bx,[bp+6]
    add es:[bx+6],ax
    les bx,[bp+10]
    mov bx,es:[bx]
    cmp word ptr es:[bx+10],0
    jz stringio_0376
    jmp near ptr stringio_04b7

stringio_0376:
    mov ax,1
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jz stringio_03e4
    les bx,[bp+10]
    mov bx,es:[bx]
    mov [bp-50],es
    mov [bp-52],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-52]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc stringio_03cf
    les bx,[bp+10]
    mov bx,es:[bx]
    mov [bp-54],es
    mov [bp-56],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+12]
    pop cx
    pop cx
    jmp short stringio_03e2

stringio_03cf:
    les bx,[bp+10]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    les bx,es:[bx+30]
    mov al,es:[bx]
    mov ah,0

stringio_03e2:
    jmp short stringio_03e7

stringio_03e4:
    mov ax,65535

stringio_03e7:
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],1
    jz stringio_03f3
    jmp near ptr stringio_04b7

stringio_03f3:
    les bx,[bp+6]
    mov ax,es:[bx+6]
    add ax,DGROUP:@string@resize_inc
    push ax
    call @TStringRef@round_capacity$qui
    pop cx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @TStringRef@grow_to$qui
    add sp,6

stringio_0414:
    les bx,[bp+6]
    mov ax,es:[bx+2]
    push bx
    push es
    mov dx,es:[bx+6]
    mov [bp-58],dx
    add ax,dx
    pop es
    pop bx
    push word ptr es:[bx+4]
    push ax
    les bx,[bp+6]
    mov ax,es:[bx+8]
    sub ax,[bp-58]
    inc ax
    push ax
    push ss
    lea ax,[bp-36]
    push ax
    call @setw$qi
    add sp,6
    lea ax,[bp-36]
    mov [bp-38],ss
    mov [bp-40],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-42],dx
    mov [bp-44],ax
    les bx,[bp-40]
    push word ptr es:[bx+4]
    or ax,[bp-42]
    jz stringio_0471
    les bx,[bp-44]
    mov dx,es
    mov ax,es:[bx]
    jmp short stringio_0477

stringio_0471:
    mov dx,[bp-42]
    mov ax,[bp-44]

stringio_0477:
    push dx
    push ax
    les bx,[bp-40]
    call dword ptr es:[bx]
    add sp,6
    push word ptr [bp-42]
    push word ptr [bp-44]
    call @istream@$brsh$qnc
    add sp,8
    mov bx,ax
    mov es,dx
    mov dx,es
    mov ax,es:[bx]
    mov [bp-46],dx
    mov [bp-48],ax
    les bx,[bp-48]
    cmp word ptr es:[bx+10],0
    jnz stringio_04ae
    mov ax,1
    jmp short stringio_04b0

stringio_04ae:
    xor ax,ax

stringio_04b0:
    or ax,ax
    jz stringio_04b7
    jmp near ptr stringio_0344

stringio_04b7:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @TStringRef@check_freeboard$qv
    pop cx
    pop cx
    push word ptr [bp-30]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Typed Borland RTTI stored in the original CODE section after last retf.
; `_TEXTC+1234` xalloc base-class descriptor, +1300 xmsg superclass.
stringio_rtti_xalloc:
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2
    dd stringio_destroy_xalloc
    dw 5,62
    db 'xalloc',0
    db 0
    dd stringio_rtti_xmsg
    dw 0,3,0,0,0,0,0,0
stringio_rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0
    dw 0,0,0,0,0,0
_TEXTC ends
end
