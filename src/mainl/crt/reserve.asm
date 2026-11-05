; Full original Japanese Borland C++ reserve string method.
; Original far C++ exception cleanups, real 8086, typed xmsg/xalloc RTTI.
; Original CODE, public import ABI and literal original OMF relocation order.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
extrn @TStringRef@reserve$qui:far
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

; BCC original ordered relocations at real instruction/data boundaries

org 160
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short reserve_branch_1_00ad

reserve_branch_1_00a9:
    jmp short reserve_branch_1_00ad

reserve_branch_1_00ab:
    xor ax,ax

reserve_branch_1_00ad:
    pop di
    pop si
    pop bp
    retf

org 140
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz reserve_branch_1_00a9
    push word ptr [bp+8]
    push word ptr [bp+6]

org 113
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 83
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short reserve_branch_1_0060

reserve_branch_1_005c:
    jmp short reserve_branch_1_0060

reserve_branch_1_005e:
    xor ax,ax

reserve_branch_1_0060:
    pop di
    pop si
    pop bp
    retf

reserve_cleanup_1:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz reserve_branch_1_00ab

org 63
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz reserve_branch_1_005c
    push word ptr [bp+8]
    push word ptr [bp+6]

org 36
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 17

reserve_exception_17:
    dd reserve_exceptions
    dw -30

reserve_cleanup_0:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz reserve_branch_1_005e

org 9
    dd reserve_rtti_outofrange
    dw 0
    dw 0

org 5

reserve_exceptions:
    dd reserve_rtti_xalloc

org 0

reserve_empty_unwind:
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
public @string@reserve$qui

; BCC original ordered relocations at real instruction/data boundaries

org 228
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

org 178
    dd reserve_rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

reserve_rtti_xmsg:
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

org 162
    dd reserve_cleanup_1
    dw 5
    dw 62
    db 'xalloc',0,0

org 112
    dd reserve_rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

reserve_rtti_xalloc:
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

org 84
    dd reserve_cleanup_0
    dw 5
    dw 74
    db 'string::outofrange',0,0

org 43
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

reserve_rtti_outofrange:
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

org 32
    call @TStringRef@reserve$qui
    add sp,6
    push word ptr [bp-30]

org 14
    call ___InitExceptBlocks
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 11
    mov bx,offset _TEXT:reserve_exception_17

org 8
    mov ax,seg _TEXT

org 0

@string@reserve$qui:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di

_TEXTC ends
end
