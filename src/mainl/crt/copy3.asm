; Full original Japanese Borland string::copy with seven typed RTTI.
; Native 8086 reference-counted cloning and original C++ exception cleanup.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn @xmsg@$bdtr$qv:far
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

org 123
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short plus_1_branch_0088

plus_1_branch_0084:
    jmp short plus_1_branch_0088

plus_1_branch_0086:
    xor ax,ax

plus_1_branch_0088:
    pop di
    pop si
    pop bp
    retf

org 103
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz plus_1_branch_0084
    push word ptr [bp+8]
    push word ptr [bp+6]

org 76
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 61

copy_except_offset_61:
    dw offset _TEXT:copy_exception_frame

copy_reference_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz plus_1_branch_0086

org 53

copy_except_offset_53:
    dw offset _TEXT:copy_exception_state
    dw 6
    dw 5
    dw 0

org 41

copy_exception_control:
    dd copy_exception_header
    dw -34
    dw 0
    dw 5
    dw 0

org 27

copy_exception_frame:
    dd rtti_TStringRef_pointer
    dw 8327
    dw -4
    dw 0
    dw 0
    dw 0

org 13

copy_exception_state:
    dd rtti_string_pointer
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

org 5

copy_exception_header:
    dd rtti_xalloc
    dw 0
    dw 0

org 0

string_copy_unwind:
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
public @string@copy$xqv

; Real native original BCC CODE4 statement/fixup order.

org 531
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

org 511
    dd @TStringRef@$bdtr$qv
    dw 5
    dw 66
    db 'TStringRef',0,0

org 453
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

org 397
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

org 347
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

org 331
    dd copy_reference_cleanup
    dw 5
    dw 62
    db 'xalloc',0,0

org 288
    dd rtti_string
    db 'string *',0

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

org 265
    dd rtti_TStringRef
    db 'TStringRef *',0

rtti_string_pointer:
    dw 4
    dw 8208
    dw 10

org 246
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

org 211
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0

plus_4_branch_00e5:
    mov dx,[bp-40]
    mov ax,[bp-42]
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-34]

org 172
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

plus_4_branch_00c3:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp-42]
    mov es:[bx+2],dx
    mov es:[bx],ax

org 164
    call @TStringRef@$bctr$qnxcuit1uiui
    add sp,18

org 118
    call _strlen
    pop cx
    pop cx
    jmp short plus_4_branch_0081

plus_4_branch_007f:
    xor ax,ax

plus_4_branch_0081:
    push ax
    xor ax,ax
    push ax
    push ax
    les bx,[bp-38]
    les bx,es:[bx]
    mov [bp-44],es
    mov [bp-46],bx
    push word ptr es:[bx+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp-2]
    push word ptr [bp-4]

org 85
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz plus_4_branch_00c3
    mov word ptr [bp-22],14
    xor ax,ax
    push ax
    or ax,0
    jz plus_4_branch_007f
    xor ax,ax
    push ax
    push ax

org 62
    call @$bnew$qui
    pop cx
    mov [bp-40],dx
    mov [bp-42],ax

plus_4_branch_004a:
    or ax,dx
    jnz plus_4_branch_0051
    jmp near ptr plus_4_branch_00e5

plus_4_branch_0051:
    mov ax,12
    push ax

org 14
    call ___InitExceptBlocks
    mov word ptr [bp-22],6
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-36],dx
    mov [bp-38],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-40],dx
    mov [bp-42],ax
    or ax,[bp-40]
    jz plus_4_branch_003a
    mov ax,[bp-42]
    jmp short plus_4_branch_004a

plus_4_branch_003a:
    mov ax,4
    push ax

org 11
    mov bx,offset _TEXT:copy_exception_control

org 8
    mov ax,seg _TEXT

org 0

@string@copy$xqv:
    push bp
    mov bp,sp
    sub sp,46
    push si
    push di
_TEXTC ends
end
