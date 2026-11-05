; Full original Japanese Borland string string::remove and eight typed RTTI.
; Actual 8086 far C++ exception/error/constructor calls, reference-counted
; concatenation, and complete 16-bit compiler cleanup procedures.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bctr$qmx6string:far
extrn @xmsg@$bctr$qmx4xmsg:far
extrn @xmsg@$bdtr$qv:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
extrn @string@clone$qv:far
extrn @TStringRef@splice$quiuinxcui:far
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

org 267
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_0118

plus_1_branch_0114:
    jmp short plus_1_branch_0118

plus_1_branch_0116:
    xor ax,ax

plus_1_branch_0118:
    pop di
    pop si
    pop bp
    retf

org 247
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_0114
    push word ptr [bp+8]
    push word ptr [bp+6]

org 220
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 190
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_00cb

plus_1_branch_00c7:
    jmp short plus_1_branch_00cb

plus_1_branch_00c9:
    xor ax,ax

plus_1_branch_00cb:
    pop di
    pop si
    pop bp
    retf

string_remove_decrement_cleanup2:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_0116

org 170
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_00c7
    push word ptr [bp+8]
    push word ptr [bp+6]

org 143
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 102
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf

string_remove_decrement_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_00c9

org 94
    call @xmsg@$bctr$qmx4xmsg
    add sp,8

org 75
    dw offset _TEXT:string_remove_except_41

string_remove_ref_inc_helper:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 67
    dw offset _TEXT:string_remove_except_17
    dw 6
    dw 5
    dw 1

org 55

string_remove_except_55:
    dd string_remove_exception_header
    dw -38
    dw 0
    dw 5
    dw 0

org 41

string_remove_except_41:
    dd rtti_xmsg
    dw 256
    dw 1
    dw 0
    dw 0
    dw 0

org 27
    dd rtti_outofrange
    dw 4
    dw -8
    dw 0
    dw 0
    dw 0

org 17

string_remove_except_17:
    dd rtti_string
    dw 4
    dw -4
    dw 0

org 9
    dd rtti_outofrange
    dw 0
    dw 0

org 5

string_remove_exception_header:
    dd rtti_xalloc

org 0

string_remove_unwind:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends
_DATA segment word public 'DATA'
stremove_range_message db 'String reference out of range',0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@remove$quiui

; Real native original BCC CODE4 statement/fixup order.

org 518
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

org 490
    dd string_remove_decrement_cleanup2
    dw 5
    dw 74
    db 'string::outofrange',0,0

org 440
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_outofrange:
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

org 424
    dd string_remove_decrement_cleanup
    dw 5
    dw 62
    db 'xalloc',0,0

org 366
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

org 310
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

org 267
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

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

org 248
    call @TStringRef@splice$quiuinxcui
    add sp,14
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-38]

org 178
    call @string@clone$qv
    pop cx
    pop cx
    jmp short plus_4_branch_00bb

plus_4_branch_00bb:
    xor ax,ax
    push ax
    push ax
    push ax
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    sub ax,[bp+10]
    mov [bp-40],ax
    mov ax,[bp+12]
    cmp ax,[bp-40]
    jnc plus_4_branch_00df
    mov dx,ss
    lea ax,[bp+12]
    jmp short plus_4_branch_00e4

plus_4_branch_00df:
    mov dx,ss
    lea ax,[bp-40]

plus_4_branch_00e4:
    mov bx,ax
    mov es,dx
    push word ptr es:[bx]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 152
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26

plus_4_branch_00a0:
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna plus_4_branch_00bb
    push word ptr [bp+8]
    push word ptr [bp+6]

org 148
    mov ax,offset _TEXTC:rtti_outofrange
    push ax

org 124
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-8]
    push ss
    push ax
    push cs

org 111
    call @string@$bdtr$qv
    add sp,6
    mov word ptr [bp-26],6

org 89
    call @xmsg@$bctr$qmx6string
    add sp,8
    mov word ptr [bp-26],14
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 71
    call @string@$bctr$qnxc
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax
    push ss
    lea ax,[bp-8]
    push ax

org 62
    mov ax,offset DGROUP:stremove_range_message
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 48
    mov ax,offset _TEXT:string_remove_ref_inc_helper
    push ax
    xor ax,ax
    push ax
    push ax
    mov word ptr [bp-26],6
    push ds

org 44
    mov ax,seg _TEXT
    push ax

org 14
    call ___InitExceptBlocks
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    cmp ax,[bp+10]
    jnc plus_4_branch_00a0
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

org 11
    mov bx,offset _TEXT:string_remove_except_55

org 8
    mov ax,seg _TEXT

org 0

@string@remove$quiui:
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di
_TEXTC ends
end
