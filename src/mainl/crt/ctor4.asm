; Full original Japanese Borland string(char*, unsigned, unsigned) constructor.
; Original far C++ constructor, reference-counted substring initialization,
; exception/unwind calls, and full 16-bit compiler cleanup procedures.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn @xmsg@$bdtr$qv:far
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

org 113
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_007e

plus_1_branch_007a:
    jmp short plus_1_branch_007e

plus_1_branch_007c:
    xor ax,ax

plus_1_branch_007e:
    pop di
    pop si
    pop bp
    retf

string_constructor_cleanup_b:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_00c9

org 93
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_007a
    push word ptr [bp+8]
    push word ptr [bp+6]

org 66
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 51
    dw offset _TEXT:string_constructor_exception_state

string_constructor_cleanup_a:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_007c

org 31

string_constructor_exception_frame:
    dd string_constructor_exception_header
    dw -34
    dw 0
    dw 5
    dw 0
    dw -1
    dw 6
    dw 5
    dw 0

org 17

string_constructor_exception_state:
    dd rtti_TStringRef_pointer
    dw 8327
    dw -4
    dw 0
    dw 0
    dw 0

org 9
    dd rtti_lengtherror
    dw 0
    dw 0

org 5

string_constructor_exception_header:
    dd rtti_xalloc

org 0

string_constructor_unwind:
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
public @string@$bctr$qnxcuiui

; Real native original BCC CODE4 statement/fixup order.

org 538
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

org 518
    dd @TStringRef@$bdtr$qv
    dw 5
    dw 66
    db 'TStringRef',0,0

org 462
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

org 412
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

org 396
    dd string_constructor_cleanup_b
    dw 5
    dw 62
    db 'xalloc',0,0

org 346
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

org 318
    dd string_constructor_cleanup_a
    dw 5
    dw 74
    db 'string::lengtherror',0

org 271
    dd rtti_TStringRef
    db 'TStringRef *',0

rtti_lengtherror:
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

org 248
    call ___ExitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_TStringRef_pointer:
    dw 4
    dw 8336
    dw 10

org 227

plus_4_branch_00e3:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    push word ptr [bp-34]

org 188
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

plus_4_branch_00d3:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

org 180
    call @TStringRef@$bctr$qnxcuit1uiui
    add sp,18

org 136
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz plus_4_branch_00d3
    mov word ptr [bp-22],14
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    push word ptr [bp-40]
    mov ax,[bp+10]
    add ax,[bp-38]
    push word ptr [bp+12]
    push ax
    push dx
    push word ptr [bp-4]

org 56
    call _strlen
    pop cx
    pop cx
    mov [bp-36],ax
    mov ax,[bp+14]
    cmp ax,[bp-36]
    jnc plus_4_branch_0051
    mov dx,ss
    lea ax,[bp+14]
    jmp short plus_4_branch_0056

plus_4_branch_0051:
    mov dx,ss
    lea ax,[bp-36]

plus_4_branch_0056:
    mov bx,ax
    mov es,dx
    mov ax,es:[bx]
    mov [bp-38],ax
    mov ax,[bp-36]
    sub ax,[bp-38]
    mov [bp-42],ax
    cmp ax,[bp+16]
    jnc plus_4_branch_0075
    mov dx,ss
    lea ax,[bp-42]
    jmp short plus_4_branch_007a

plus_4_branch_0075:
    mov dx,ss
    lea ax,[bp+16]

plus_4_branch_007a:
    mov bx,ax
    mov es,dx
    mov ax,es:[bx]
    mov [bp-40],ax
    mov ax,12
    push ax

org 31
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jnz plus_4_branch_0032
    jmp near ptr plus_4_branch_00e3

plus_4_branch_0032:
    push word ptr [bp+12]
    push word ptr [bp+10]

org 14
    call ___InitExceptBlocks
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz plus_4_branch_0032
    mov ax,4
    push ax

org 11
    mov bx,offset _TEXT:string_constructor_exception_frame

org 8
    mov ax,seg _TEXT

org 0

@string@$bctr$qnxcuiui:
    push bp
    mov bp,sp
    sub sp,42
    push si
    push di
_TEXTC ends
end
