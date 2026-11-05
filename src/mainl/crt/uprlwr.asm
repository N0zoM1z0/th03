; Complete Japanese Borland string and TSubString case conversion.
; All six far C++ methods, compiler exception state tables and two typed RTTI
; descriptors, not raw binary CODE or machine-code byte arrays.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlwr:far
extrn _strupr:far
extrn _tolower:far
extrn _toupper:far
extrn @string@$bctr$qmx6string:far
extrn @string@$bdtr$qv:far
extrn @string@copy$xqv:far
extrn @string@clone$qv:far
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

; BCC original _TEXT exception cleanup FIXUPP-record source order.

org 171

case_exception_171:
    dd case_exception_167
    dw -30

org 161

case_exception_161:
    dd case_exception_157
    dw -30

case_exception_167:
    dw 0
    dw 0

org 155
    dw offset _TEXT:case_exception_113

case_exception_157:
    dw 0
    dw 0

org 147
    dw offset _TEXT:case_exception_099
    dw 14
    dw 5
    dw 1

org 139
    dw offset _TEXT:case_exception_085
    dw 6
    dw 5
    dw 1

org 127

case_exception_127:
    dd case_exception_081
    dw -34
    dw 0
    dw 5
    dw 0

org 113

case_exception_113:
    dd case_pointer_type_rtti
    dw 180
    dw 6
    dw 0
    dw 0
    dw 0

org 99

case_exception_099:
    dd case_pointer_type_rtti
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

org 85

case_exception_085:
    dd case_string_class_rtti
    dw 4
    dw -4
    dw 0
    dw 0
    dw 0

org 79
    dw offset _TEXT:case_exception_037

case_exception_081:
    dw 0
    dw 0

org 71
    dw offset _TEXT:case_exception_023
    dw 14
    dw 5
    dw 1

org 63
    dw offset _TEXT:case_exception_009
    dw 6
    dw 5
    dw 1

org 51

case_exception_051:
    dd case_exception_005
    dw -34
    dw 0
    dw 5
    dw 0

org 37

case_exception_037:
    dd case_pointer_type_rtti
    dw 180
    dw 6
    dw 0
    dw 0
    dw 0

org 23

case_exception_023:
    dd case_pointer_type_rtti
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

org 9

case_exception_009:
    dd case_string_class_rtti
    dw 4
    dw -4
    dw 0
    dw 0
    dw 0

org 0
case_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf

case_exception_005:
    dw 0
    dw 0

_TEXT ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@to_lower$qv
public @string@to_upper$qv
public @to_lower$qmx6string
public @to_upper$qmx6string
public @TSubString@to_lower$qv
public @TSubString@to_upper$qv

; BCC original _TEXTC six methods and typed RTTI FIXUPP-record source order.

org 707
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0,0
    dw 0,0,0,0,0,0

org 664
    dd case_string_class_rtti
    db 'string *',0

case_string_class_rtti:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

org 647
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

case_pointer_type_rtti:
    dw 4,8208,10

org 619
    call _toupper
    pop cx
    les bx,[bp-34]
    mov es:[bx],al
    inc word ptr [bp-34]

case_branch_027a:
    mov ax,[bp-36]
    dec word ptr [bp-36]
    or ax,ax
    jnz case_branch_0263

case_branch_0284:
    push word ptr [bp-30]

org 563
    call @string@clone$qv
    pop cx
    pop cx
    jmp short case_branch_023c

case_branch_023c:
    les bx,[bp+6]
    les bx,es:[bx]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    les bx,[bp+6]
    add ax,es:[bx+4]
    mov [bp-32],dx
    mov [bp-34],ax
    mov ax,es:[bx+6]
    mov [bp-36],ax
    jmp short case_branch_027a

case_branch_0263:
    les bx,[bp-34]
    mov al,es:[bx]
    cbw
    push ax

org 526
    call ___InitExceptBlocks
    les bx,[bp+6]
    cmp word ptr es:[bx+4],-1
    jz case_branch_0284
    les bx,es:[bx]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna case_branch_023c
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 523
    mov bx,offset _TEXT:case_exception_171

org 520
    mov ax,seg _TEXT

org 501
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TSubString@to_upper$qv:
    push bp
    mov bp,sp
    sub sp,36
    push si
    push di

org 473
    call _tolower
    pop cx
    les bx,[bp-34]
    mov es:[bx],al
    inc word ptr [bp-34]

case_branch_01e8:
    mov ax,[bp-36]
    dec word ptr [bp-36]
    or ax,ax
    jnz case_branch_01d1

case_branch_01f2:
    push word ptr [bp-30]

org 417
    call @string@clone$qv
    pop cx
    pop cx
    jmp short case_branch_01aa

case_branch_01aa:
    les bx,[bp+6]
    les bx,es:[bx]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    les bx,[bp+6]
    add ax,es:[bx+4]
    mov [bp-32],dx
    mov [bp-34],ax
    mov ax,es:[bx+6]
    mov [bp-36],ax
    jmp short case_branch_01e8

case_branch_01d1:
    les bx,[bp-34]
    mov al,es:[bx]
    cbw
    push ax

org 380
    call ___InitExceptBlocks
    les bx,[bp+6]
    cmp word ptr es:[bx+4],-1
    jz case_branch_01f2
    les bx,es:[bx]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna case_branch_01aa
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 377
    mov bx,offset _TEXT:case_exception_161

org 374
    mov ax,seg _TEXT

org 353
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TSubString@to_lower$qv:
    push bp
    mov bp,sp
    sub sp,36
    push si
    push di

org 342
    call @string@$bdtr$qv
    add sp,6
    push word ptr [bp-34]

org 308
    call @string@$bctr$qmx6string
    add sp,8
    mov bx,ax
    mov es,dx
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr [bp-22],22
    push dx
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 275
    call @string@copy$xqv
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call @string@to_upper$qv
    add sp,12
    mov word ptr [bp-22],14
    push ss
    lea ax,[bp-4]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 254
    call ___InitExceptBlocks
    mov word ptr [bp-22],6
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp-4]
    push ax

org 251
    mov bx,offset _TEXT:case_exception_127

org 248
    mov ax,seg _TEXT

org 227
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@to_upper$qmx6string:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 216
    call @string@$bdtr$qv
    add sp,6
    push word ptr [bp-34]

org 182
    call @string@$bctr$qmx6string
    add sp,8
    mov bx,ax
    mov es,dx
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr [bp-22],22
    push dx
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 149
    call @string@copy$xqv
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call @string@to_lower$qv
    add sp,12
    mov word ptr [bp-22],14
    push ss
    lea ax,[bp-4]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 128
    call ___InitExceptBlocks
    mov word ptr [bp-22],6
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp-4]
    push ax

org 125
    mov bx,offset _TEXT:case_exception_051

org 122
    mov ax,seg _TEXT

org 103
    call _strupr
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

@to_lower$qmx6string:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 80
    call @string@clone$qv
    pop cx
    pop cx
    jmp short case_branch_0059

case_branch_0059:
    les bx,[bp+6]
    les bx,es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 46
    call _strlwr
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

@string@to_upper$qv:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna case_branch_0059
    push word ptr [bp+8]
    push word ptr [bp+6]

org 23
    call @string@clone$qv
    pop cx
    pop cx
    jmp short case_branch_0020

case_branch_0020:
    les bx,[bp+6]
    les bx,es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 0

@string@to_lower$qv:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna case_branch_0020
    push word ptr [bp+8]
    push word ptr [bp+6]

_TEXTC ends
end
