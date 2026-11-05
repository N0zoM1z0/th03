; Original Japanese Borland C++ string substring/find family.
; Complete 3 far public methods, typed exception cleanup frames and string RTTI.
; All executable 8086 source and semantic OMF relocations; no target-CODE blobs.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn _strncmp:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
extrn @string@case_sensitive:word
extrn @string@paranoid_check:word
extrn @to_upper$qmx6string:far
extrn F_LXLSH@:far
extrn F_LMOD@:far
extrn F_LXMUL@:far
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

; Actual original Borland _TEXT exception metadata source/relocation block order.

org 61
    dw offset _TEXT:rfind_type_catch_15

org 35
rfind_type_catch_35: dd rfind_rtti_string
    dw 4,-12,0
rfind_exception_state: dw 0,0
rfind_exception_state_49: dw 0,0,-42,0,5,0

org 25
rfind_type_catch_25: dd rfind_rtti_string
    dw 4,-8,0

org 15
rfind_type_catch_15: dd rfind_rtti_string
    dw 4,-4,0

org 9
rfind_cleanup_state_9: dd rfind_cleanup_frame_5
    dw -30

org 0
rfind_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf
rfind_cleanup_frame_5: dd 0

_TEXT ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@rfind$xqmx6stringui
public @string@rfind_index$xqnxcuimui
public @string@rfind_case_index$xqnxcuimui

; Actual original Borland _TEXTC LEDATA 0..907 source/relocation block order.

org 880
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0,0
    dw 0,0,0,0,0,0

org 824
    call F_LMOD@
    mov [bp-10],dx
    mov [bp-12],ax
    dec word ptr [bp-16]
    jmp near ptr rfind_0271

rfind_0349:
    mov ax,65535

rfind_034c:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rfind_rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

org 794
    call F_LXLSH@
    mov bx,[bp-4]
    neg bx
    les si,[bp-16]
    add si,bx
    push ax
    mov al,es:[si]
    cbw
    push dx
    cwd
    pop bx
    pop cx
    add cx,ax
    adc bx,dx
    push bx
    push cx

org 767
    call F_LMOD@
    mov [bp-10],dx
    mov [bp-12],ax
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-10]
    mov ax,[bp-12]
    mov cl,5

org 742
    call F_LXMUL@
    mov bx,[bp-10]
    mov cx,[bp-12]
    add cx,64288
    adc bx,16383
    sub cx,ax
    sbb bx,dx
    push bx
    push cx

org 663
    call _strncmp
    add sp,10
    or ax,ax
    jnz rfind_02bc

rfind_02a3:
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,[bp-16]
    xor dx,dx
    sub ax,es:[bx+2]
    sbb dx,0
    sub ax,[bp-4]
    inc ax
    jmp near ptr rfind_034c

rfind_02bc:
    mov dx,[bp-14]
    mov ax,[bp-16]
    cmp dx,[bp-28]
    jnz rfind_02cc
    cmp ax,[bp-30]
    jz rfind_0349

rfind_02cc:
    mov ax,511
    mov dx,65497
    push ax
    push dx
    les bx,[bp-16]
    mov al,es:[bx]
    cbw
    cwd
    push ax
    push dx
    mov dx,[bp-22]
    mov ax,[bp-24]
    pop cx
    pop bx

org 641
    cmp word ptr DGROUP:@string@paranoid_check,0
    jz rfind_02a3
    push word ptr [bp-4]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-14]
    push word ptr [bp-16]

org 562
    call F_LMOD@
    mov [bp-10],dx
    mov [bp-12],ax
    dec word ptr [bp-16]
    inc word ptr [bp-26]

rfind_0243:
    mov ax,[bp-26]
    cmp ax,[bp-4]
    jc rfind_01d6
    les bx,[bp+6]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    add ax,[bp+14]
    dec ax
    mov [bp-14],dx
    mov [bp-16],ax
    mov ax,es:[bx+2]
    add ax,[bp-4]
    dec ax
    mov [bp-28],dx
    mov [bp-30],ax

rfind_0271:
    mov dx,[bp-10]
    mov ax,[bp-12]
    cmp dx,[bp-6]
    jnz rfind_02bc
    cmp ax,[bp-8]
    jnz rfind_02bc

org 539
    call F_LXLSH@
    les bx,[bp-16]
    push ax
    mov al,es:[bx]
    cbw
    push dx
    cwd
    pop bx
    pop cx
    add cx,ax
    adc bx,dx
    push bx
    push cx

org 509
    call F_LMOD@
    mov [bp-6],dx
    mov [bp-8],ax
    dec word ptr [bp-20]
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-10]
    mov ax,[bp-12]
    mov cl,5

org 486
    call F_LXLSH@
    les bx,[bp-20]
    push ax
    mov al,es:[bx]
    cbw
    push dx
    cwd
    pop bx
    pop cx
    add cx,ax
    adc bx,dx
    push bx
    push cx

org 442
    call F_LMOD@
    mov [bp-22],dx
    mov [bp-24],ax

rfind_01c5:
    mov ax,[bp-26]
    dec word ptr [bp-26]
    or ax,ax
    jnz rfind_01a3
    mov word ptr [bp-26],0
    jmp short rfind_0243

rfind_01d6:
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-6]
    mov ax,[bp-8]
    mov cl,5

org 435
    call F_LXLSH@
    push dx
    push ax

org 302
    call _strlen
    pop cx
    pop cx
    les bx,[bp+16]
    mov es:[bx],ax
    mov [bp-4],ax
    mov ax,[bp-2]
    cmp ax,[bp-4]
    jnc rfind_0149
    jmp near ptr rfind_0349

rfind_0149:
    cmp word ptr [bp-4],0
    jnz rfind_0154
    xor ax,ax
    jmp near ptr rfind_034c

rfind_0154:
    mov word ptr [bp-6],0
    mov word ptr [bp-8],0
    mov word ptr [bp-10],0
    mov word ptr [bp-12],0
    les bx,[bp+6]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    add ax,[bp+14]
    dec ax
    mov [bp-14],dx
    mov [bp-16],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    add ax,[bp-4]
    dec ax
    mov [bp-18],dx
    mov [bp-20],ax
    mov word ptr [bp-22],0
    mov word ptr [bp-24],1
    mov ax,[bp-4]
    dec ax
    mov [bp-26],ax
    jmp short rfind_01c5

rfind_01a3:
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-22]
    mov ax,[bp-24]
    mov cl,5

org 270
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@rfind_case_index$xqnxcuimui:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
    mov ax,[bp+14]
    mov [bp-2],ax
    push word ptr [bp+12]
    push word ptr [bp+10]

org 259
    call @string@$bdtr$qv
    add sp,18

rfind_010b:
    push word ptr [bp-42]

org 245
    call @string@$bdtr$qv
    mov ax,2
    push ax
    push ss
    lea ax,[bp-12]
    push ax

org 231
    call @string@$bdtr$qv
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 213
    db 09ah
    dd @string@rfind_case_index$xqnxcuimui

    add sp,14
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-8]
    push ax

org 200
    call @to_upper$qmx6string
    add sp,8
    lea ax,[bp-12]
    push ss
    push ax

org 170
    call @to_upper$qmx6string
    add sp,8
    les bx,[bp-8]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax,[bp-12]
    push ax

org 155
    call @string@$bctr$qnxc
    add sp,8
    push dx
    push ax
    push ss
    lea ax,[bp-8]
    push ax

org 118
    db 09ah
    dd @string@rfind_case_index$xqnxcuimui

    add sp,14
    push ax
    jmp near ptr rfind_010b

rfind_0082:
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    mov word ptr [bp-30],6
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp-4]
    push ax

org 90
    cmp word ptr DGROUP:@string@case_sensitive,0
    jz rfind_0082
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 85
    call ___InitExceptBlocks

org 82
    mov bx,offset _TEXT:rfind_exception_state_49

org 79
    mov ax,seg _TEXT

org 59
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@rfind_index$xqnxcuimui:
    push bp
    mov bp,sp
    sub sp,42
    push si
    push di

org 47
    db 09ah
    dd @string@rfind_index$xqnxcuimui

    add sp,14
    push ax
    push word ptr [bp-30]

org 14
    call ___InitExceptBlocks
    push ss
    lea ax,[bp-32]
    push ax
    push word ptr [bp+14]
    les bx,[bp+10]
    les bx,es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 11
    mov bx,offset _TEXT:rfind_cleanup_state_9

org 8
    mov ax,seg _TEXT

org 0

@string@rfind$xqmx6stringui:
    push bp
    mov bp,sp
    sub sp,32
    push si
    push di

_TEXTC ends
end
