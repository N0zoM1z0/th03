; Full original Japanese Borland string operator+ and eight typed RTTI.
; Actual 8086 far C++ exception/error/constructor calls, reference-counted
; concatenation, and complete 16-bit compiler cleanup procedures.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn @xmsg@$bdtr$qv:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
extrn @TStringRef@$bctr$qnxcuit1uiui:far
extrn @TStringRef@$bdtr$qv:far
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

org 236
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_00f9

plus_1_branch_00f5:
    jmp short plus_1_branch_00f9

plus_1_branch_00f7:
    xor ax,ax

plus_1_branch_00f9:
    pop di
    pop si
    pop bp
    retf

org 216
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_00f5
    push word ptr [bp+8]
    push word ptr [bp+6]

org 189
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 159
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_00ac

plus_1_branch_00a8:
    jmp short plus_1_branch_00ac

plus_1_branch_00aa:
    xor ax,ax

plus_1_branch_00ac:
    pop di
    pop si
    pop bp
    retf

operator_plus_decrement_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_00f7

org 139
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_00a8
    push word ptr [bp+8]
    push word ptr [bp+6]

org 112
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 97
    dw offset _TEXT:operator_plus_except_55

operator_plus_copy_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_00aa

org 89
    dw offset _TEXT:operator_plus_except_41
    dw 6
    dw 5
    dw 1

org 81
    dw offset _TEXT:operator_plus_except_17
    dw 6
    dw 5
    dw 1

org 69

operator_plus_except_69:
    dd operator_plus_exception_header
    dw -38
    dw 0
    dw 5
    dw 0

org 55

operator_plus_except_55:
    dd rtti_string_pointer
    dw 180
    dw 6
    dw 0
    dw 0
    dw 0

org 41

operator_plus_except_41:
    dd rtti_TStringRef_pointer
    dw 8327
    dw -8
    dw 0
    dw 0
    dw 0

org 27
    dd rtti_string_pointer
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

org 17

operator_plus_except_17:
    dd rtti_string
    dw 4
    dw -4
    dw 0

org 9
    dd rtti_length_error
    dw 0
    dw 0

org 5

operator_plus_exception_header:
    dd rtti_xalloc

org 0

operator_plus_unwind:
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
public @$badd$qnxcmx6string

; Real native original BCC CODE4 statement/fixup order.

org 680
    dd rtti_TReference
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_TReference:
    dw 2
    dw 3
    dw 26
    dw -1
    dw 1
    dw 38
    dw 42
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    db 'TReference',0,0
    dw 0
    dw 0
    dw 0
    dw 0

org 660
    dd @TStringRef@$bdtr$qv
    dw 5
    dw 66
    db 'TStringRef',0,0

org 604
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

rtti_TStringRef:
    dw 12
    dw 3
    dw 38
    dw -1
    dw 7
    dw 50
    dw 62
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

org 554
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

org 538
    dd operator_plus_decrement_cleanup
    dw 5
    dw 62
    db 'xalloc',0,0

org 488
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

org 460
    dd operator_plus_copy_cleanup
    dw 5
    dw 74
    db 'string::lengtherror',0

org 402
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

rtti_length_error:
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

org 359
    dd rtti_string
    db 'string *',0

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

org 336
    dd rtti_TStringRef
    db 'TStringRef *',0

rtti_string_pointer:
    dw 4
    dw 8208
    dw 10

org 317
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_TStringRef_pointer:
    dw 4
    dw 8336
    dw 10

org 306
    call @string@$bdtr$qv
    add sp,6
    push word ptr [bp-38]

org 257
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0

plus_4_branch_0113:
    mov dx,[bp-52]
    mov ax,[bp-54]
    les bx,[bp-50]
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr [bp-26],22
    push dx
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 218
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-26],6

plus_4_branch_00f1:
    mov dx,[bp-6]
    mov ax,[bp-8]
    les bx,[bp-54]
    mov es:[bx+2],dx
    mov es:[bx],ax

org 210
    call @TStringRef@$bctr$qnxcuit1uiui
    add sp,18

org 162
    call _strlen
    pop cx
    pop cx
    jmp short plus_4_branch_00ad

plus_4_branch_00ab:
    xor ax,ax

plus_4_branch_00ad:
    push ax
    push word ptr [bp-40]
    push word ptr [bp-42]
    les bx,[bp-46]
    les bx,es:[bx]
    mov [bp-56],es
    mov [bp-58],bx
    push word ptr es:[bx+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp-6]
    push word ptr [bp-8]

org 124
    call @$bnew$qui
    pop cx
    mov [bp-6],dx
    mov [bp-8],ax
    or ax,dx
    jz plus_4_branch_00f1
    mov word ptr [bp-26],14
    xor ax,ax
    push ax
    mov ax,[bp-42]
    or ax,[bp-40]
    jz plus_4_branch_00ab
    push word ptr [bp-40]
    push word ptr [bp-42]

org 101
    call @$bnew$qui
    pop cx
    mov [bp-52],dx
    mov [bp-54],ax

plus_4_branch_0071:
    or ax,dx
    jnz plus_4_branch_0078
    jmp near ptr plus_4_branch_0113

plus_4_branch_0078:
    mov ax,12
    push ax

org 55
    call @string@$bctr$qnxc
    add sp,8
    mov [bp-44],dx
    mov [bp-46],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-48],dx
    mov [bp-50],ax
    mov [bp-52],dx
    mov [bp-54],ax
    or ax,[bp-52]
    jz plus_4_branch_0061
    mov ax,[bp-54]
    jmp short plus_4_branch_0071

plus_4_branch_0061:
    mov ax,4
    push ax

org 14
    call ___InitExceptBlocks
    mov word ptr [bp-26],6
    les bx,[bp+14]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    mov [bp-40],dx
    mov [bp-42],ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp-4]
    push ax

org 11
    mov bx,offset _TEXT:operator_plus_except_69

org 8
    mov ax,seg _TEXT

org 0

@$badd$qnxcmx6string:
    push bp
    mov bp,sp
    sub sp,58
    push si
    push di
_TEXTC ends
end
