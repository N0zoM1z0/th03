; Full original Japanese Borland string string assign and eight typed RTTI.
; Actual 8086 far C++ exception/error/constructor calls, reference-counted
; concatenation, and complete 16-bit compiler cleanup procedures.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
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

org 109
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_007a

plus_1_branch_0076:
    jmp short plus_1_branch_007a

plus_1_branch_0078:
    xor ax,ax

plus_1_branch_007a:
    pop di
    pop si
    pop bp
    retf

org 89
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_0076
    push word ptr [bp+8]
    push word ptr [bp+6]

org 62
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 47
    dw offset _TEXT:string_assign_exception_state

string_assign_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_0078

org 27

string_assign_exception_frame:
    dd string_assign_exception_header
    dw -34
    dw 0
    dw 5
    dw 0
    dw -1
    dw 6
    dw 5
    dw 0

org 13

string_assign_exception_state:
    dd rtti_TStringRef_pointer
    dw 8327
    dw -4
    dw 0
    dw 0
    dw 0

org 5

string_assign_exception_header:
    dd rtti_xalloc
    dw 0
    dw 0

org 0

string_assign_unwind:
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
public @string@assign$qmx6stringuiui

; Real native original BCC CODE4 statement/fixup order.

org 599
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

org 579
    dd @TStringRef@$bdtr$qv
    dw 5
    dw 66
    db 'TStringRef',0,0

org 523
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

org 473
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

org 457
    dd string_assign_cleanup
    dw 5
    dw 62
    db 'xalloc',0,0

org 410
    dd rtti_TStringRef
    db 'TStringRef *',0

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

org 391
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

org 352
    call @TStringRef@$bdtr$qv
    add sp,6

plus_4_branch_0168:
    les bx,[bp+10]
    mov dx,es:[bx+2]
    mov ax,es:[bx]
    les bx,[bp+6]

plus_4_branch_0175:
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-34]

org 320
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov ax,3
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 276
    call @TStringRef@$bdtr$qv
    add sp,6

plus_4_branch_011c:
    les bx,[bp+6]
    mov dx,[bp-44]
    mov ax,[bp-46]
    jmp short plus_4_branch_0175

plus_4_branch_0127:
    les bx,[bp+10]
    les bx,es:[bx]
    inc word ptr es:[bx]
    les bx,[bp+6]
    les bx,es:[bx]
    dec word ptr es:[bx]
    mov ax,es:[bx]
    or ax,ax
    jnz plus_4_branch_0168

org 244
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov ax,3
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 193
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

plus_4_branch_00d8:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-44],dx
    mov [bp-46],ax
    les bx,[bp+6]
    les bx,es:[bx]
    dec word ptr es:[bx]
    mov ax,es:[bx]
    or ax,ax
    jnz plus_4_branch_011c

org 185
    call @TStringRef@$bctr$qnxcuit1uiui
    add sp,18

org 133
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz plus_4_branch_00d8
    mov word ptr [bp-22],14
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    push word ptr [bp-40]
    les bx,[bp+10]
    les bx,es:[bx]
    mov ax,es:[bx+2]
    add ax,[bp-36]
    push word ptr es:[bx+4]
    push ax
    push dx
    push word ptr [bp-4]

org 14
    call ___InitExceptBlocks
    cmp word ptr [bp+14],0
    jnz plus_4_branch_002b
    les bx,[bp+10]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    cmp ax,[bp+16]
    ja plus_4_branch_002b
    jmp near ptr plus_4_branch_0127

plus_4_branch_002b:
    les bx,[bp+10]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    mov [bp-38],ax
    mov ax,[bp+14]
    cmp ax,[bp-38]
    jnc plus_4_branch_0047
    mov dx,ss
    lea ax,[bp+14]
    jmp short plus_4_branch_004c

plus_4_branch_0047:
    mov dx,ss
    lea ax,[bp-38]

plus_4_branch_004c:
    mov bx,ax
    mov es,dx
    mov ax,es:[bx]
    mov [bp-36],ax
    les bx,[bp+10]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    sub ax,[bp-36]
    mov [bp-42],ax
    cmp ax,[bp+16]
    jnc plus_4_branch_0072
    mov dx,ss
    lea ax,[bp-42]
    jmp short plus_4_branch_0077

plus_4_branch_0072:
    mov dx,ss
    lea ax,[bp+16]

plus_4_branch_0077:
    mov bx,ax
    mov es,dx
    mov ax,es:[bx]
    mov [bp-40],ax
    mov ax,12
    push ax

org 11
    mov bx,offset _TEXT:string_assign_exception_frame

org 8
    mov ax,seg _TEXT

org 0

@string@assign$qmx6stringuiui:
    push bp
    mov bp,sp
    sub sp,46
    push si
    push di
_TEXTC ends
end
