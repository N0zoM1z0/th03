; Full original Japanese Borland two-index string::substr and five typed RTTI.
; Native 8086 index assertion, C++ copy and original cleanup helpers.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
extrn @string@$bctr$qnxcuiui:far
extrn @string@$bdtr$qv:far
extrn @string@assert_index$xqui:far
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

; Real native original BCC CODE1 statement/fixup order.

org 182
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_00c3

plus_1_branch_00bf:
    jmp short plus_1_branch_00c3

plus_1_branch_00c1:
    xor ax,ax

plus_1_branch_00c3:
    pop di
    pop si
    pop bp
    retf

org 162
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_00bf
    push word ptr [bp+8]
    push word ptr [bp+6]

org 135
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 105
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_0076

plus_1_branch_0072:
    jmp short plus_1_branch_0076

plus_1_branch_0074:
    xor ax,ax

plus_1_branch_0076:
    pop di
    pop si
    pop bp
    retf

substr_cleanup_b:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_00c1

org 85
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_0072
    push word ptr [bp+8]
    push word ptr [bp+6]

org 58
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 43
    dw offset _TEXT:substr_exception_frame

substr_cleanup_a:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_0074

org 31

substr_exception_state:
    dd substr_exception_header
    dw -30
    dw 0
    dw 5
    dw 0

org 17

substr_exception_frame:
    dd rtti_string_pointer
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

org 9
    dd rtti_string_outofrange
    dw 0
    dw 0

org 5

substr_exception_header:
    dd rtti_xalloc

org 0

substr_unwind:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@substr$xquiui

; Real native original BCC CODE4 statement/fixup order.

org 345
    dd @string@$bdtr$qv
    dw 5
    dw 54
    db 'string',0,0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

org 289
    dd @xmsg@$bdtr$qv
    dw 5
    dw 52
    db 'xmsg',0,0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_string:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 3
    dw 46
    dw 50
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

org 239
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_xmsg:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 3
    dw 44
    dw 48
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

org 223
    dd substr_cleanup_b
    dw 5
    dw 62
    db 'xalloc',0,0

org 173
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_xalloc:
    dw 6
    dw 3
    dw 38
    dw -1
    dw 7
    dw 46
    dw 58
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2

org 145
    dd substr_cleanup_a
    dw 5
    dw 74
    db 'string::outofrange',0,0

org 102
    dd rtti_string
    db 'string *',0

rtti_string_outofrange:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 7
    dw 58
    dw 70
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2

org 83
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_string_pointer:
    dw 4
    dw 8208
    dw 10

org 64
    call @string@$bctr$qnxcuiui
    add sp,18
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-30]

org 28
    call @string@assert_index$xqui
    mov word ptr [bp-18],6
    push word ptr [bp+16]
    push word ptr [bp+14]
    les bx,[bp+10]
    les bx,es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 14
    call ___InitExceptBlocks
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]

org 11
    mov bx,offset _TEXT:substr_exception_state

org 8
    mov ax,seg _TEXT

org 0

@string@substr$xquiui:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
_TEXTC ends
end
