; Original Japanese Borland C++ string substring/find family.
; Complete 5 far public methods, typed exception cleanup frames and string RTTI.
; All executable 8086 source and semantic OMF relocations; no target-CODE blobs.
.8086
extrn @$bnew$qui:far
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

org 81
    dw offset _TEXT:find_type_catch_35

org 55
find_type_catch_55: dd find_rtti_string
    dw 4,-12,0
find_exception_state: dw 0,0
find_exception_state_69: dw 0,0,-42,0,5,0

org 45
find_type_catch_45: dd find_rtti_string
    dw 4,-8,0

org 35
find_type_catch_35: dd find_rtti_string
    dw 4,-4,0

org 29
find_cleanup_state_29: dd find_cleanup_frame_25
    dw -30

org 19
find_cleanup_state_19: dd find_cleanup_frame_15
    dw -30
find_cleanup_frame_25: dd 0

org 9
find_cleanup_state_9: dd find_cleanup_frame_5
    dw -30
find_cleanup_frame_15: dd 0

org 0
find_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf
find_cleanup_frame_5: dd 0

_TEXT ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@substring$qnxcui
public @string@substring$xqnxcui
public @string@find$xqmx6stringui
public @string@find_index$xqnxcuimui
public @string@find_case_index$xqnxcuimui

; Actual original Borland _TEXTC LEDATA 0..1023 source/relocation block order.

org 969
    call F_LMOD@
    mov [bp-10],dx
    mov [bp-12],ax
    inc word ptr [bp-16]
    inc word ptr [bp-26]

find1_03da:
    mov ax,[bp-26]
    cmp ax,[bp-4]
    jc find1_036d
    les bx,[bp+6]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    add ax,[bp+14]
    mov [bp-14],dx
    mov [bp-16],ax
    add ax,[bp-2]
    sub ax,[bp-4]
    mov [bp-28],dx

org 946
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

org 916
    call F_LMOD@
    mov [bp-6],dx
    mov [bp-8],ax
    inc word ptr [bp-20]
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-10]
    mov ax,[bp-12]
    mov cl,5

org 893
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

org 849
    call F_LMOD@
    mov [bp-22],dx
    mov [bp-24],ax

find1_035c:
    mov ax,[bp-26]
    dec word ptr [bp-26]
    or ax,ax
    jnz find1_033a
    mov word ptr [bp-26],0
    jmp short find1_03da

find1_036d:
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-6]
    mov ax,[bp-8]
    mov cl,5

org 842
    call F_LXLSH@
    push dx
    push ax

org 714
    call _strlen
    pop cx
    pop cx
    les bx,[bp+16]
    mov es:[bx],ax
    mov [bp-4],ax
    mov ax,[bp-2]
    cmp ax,[bp-4]
    jnc find1_02e5
    jmp near ptr find1_04cd

find1_02e5:
    cmp word ptr [bp-4],0
    jnz find1_02f0
    xor ax,ax
    jmp near ptr find1_04d0

find1_02f0:
    mov word ptr [bp-6],0
    mov word ptr [bp-8],0
    mov word ptr [bp-10],0
    mov word ptr [bp-12],0
    les bx,[bp+6]
    les bx,es:[bx]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    add ax,[bp+14]
    mov [bp-14],dx
    mov [bp-16],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-18],dx
    mov [bp-20],ax
    mov word ptr [bp-22],0
    mov word ptr [bp-24],1
    mov ax,[bp-4]
    dec ax
    mov [bp-26],ax
    jmp short find1_035c

find1_033a:
    mov ax,511
    mov dx,65497
    push ax
    push dx
    mov dx,[bp-22]
    mov ax,[bp-24]
    mov cl,5

org 672
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@find_case_index$xqnxcuimui:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    sub ax,[bp+14]
    mov [bp-2],ax
    push word ptr [bp+12]
    push word ptr [bp+10]

org 661
    call @string@$bdtr$qv
    add sp,18

find1_029d:
    push word ptr [bp-42]

org 647
    call @string@$bdtr$qv
    mov ax,2
    push ax
    push ss
    lea ax,[bp-12]
    push ax

org 633
    call @string@$bdtr$qv
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 615
    db 09ah
    dd @string@find_case_index$xqnxcuimui

    add sp,14
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-8]
    push ax

org 602
    call @to_upper$qmx6string
    add sp,8
    lea ax,[bp-12]
    push ss
    push ax

org 572
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

org 557
    call @string@$bctr$qnxc
    add sp,8
    push dx
    push ax
    push ss
    lea ax,[bp-8]
    push ax

org 520
    db 09ah
    dd @string@find_case_index$xqnxcuimui

    add sp,14
    push ax
    jmp near ptr find1_029d

find1_0214:
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    mov word ptr [bp-30],6
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp-4]
    push ax

org 492
    cmp word ptr DGROUP:@string@case_sensitive,0
    jz find1_0214
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 487
    call ___InitExceptBlocks

org 484
    mov bx,offset _TEXT:find_exception_state_69

org 481
    mov ax,seg _TEXT

org 461
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@find_index$xqnxcuimui:
    push bp
    mov bp,sp
    sub sp,42
    push si
    push di

org 449
    db 09ah
    dd @string@find_index$xqnxcuimui

    add sp,14
    push ax
    push word ptr [bp-30]

org 416
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

org 413
    mov bx,offset _TEXT:find_cleanup_state_29

org 410
    mov ax,seg _TEXT

org 389
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@find$xqmx6stringui:
    push bp
    mov bp,sp
    sub sp,32
    push si
    push di

org 326
    call @$bnew$qui
    pop cx
    mov [bp-44],dx
    mov [bp-46],ax

find1_0152:
    or ax,dx
    jz find1_0174
    les bx,[bp-46]
    mov dx,[bp-40]
    mov ax,[bp-42]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov ax,[bp-38]
    mov es:[bx+4],ax
    mov ax,[bp-36]
    mov es:[bx+6],ax

find1_0174:
    mov dx,[bp-44]
    mov ax,[bp-46]
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-30]

org 260
    db 09ah
    dd @string@find_index$xqnxcuimui

    add sp,14
    mov dx,ax
    cmp dx,-1
    jnz find1_0117
    xor ax,ax
    jmp short find1_011a

find1_0117:
    mov ax,[bp-32]

find1_011a:
    mov [bp-36],ax
    mov [bp-38],dx
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-40],dx
    mov [bp-42],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-44],dx
    mov [bp-46],ax
    or ax,[bp-44]
    jz find1_0142
    mov ax,[bp-46]
    jmp short find1_0152

find1_0142:
    mov ax,8
    push ax

org 211
    call _strlen
    pop cx
    pop cx
    mov [bp-34],ax
    mov ax,[bp+18]
    cmp ax,[bp-34]
    jnc find1_00ec
    mov dx,ss
    lea ax,[bp+18]
    jmp short find1_00f1

find1_00ec:
    mov dx,ss
    lea ax,[bp-34]

find1_00f1:
    mov bx,ax
    mov es,dx
    push word ptr es:[bx]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]

org 195
    call ___InitExceptBlocks
    push ss
    lea ax,[bp-32]
    push ax
    push word ptr [bp+16]
    push word ptr [bp+14]

org 192
    mov bx,offset _TEXT:find_cleanup_state_19

org 189
    mov ax,seg _TEXT

org 168
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@substring$xqnxcui:
    push bp
    mov bp,sp
    sub sp,46
    push si
    push di

org 105
    call @$bnew$qui
    pop cx
    mov [bp-42],dx
    mov [bp-44],ax

find1_0075:
    or ax,dx
    jz find1_0097
    les bx,[bp-44]
    mov dx,[bp-38]
    mov ax,[bp-40]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov ax,[bp-36]
    mov es:[bx+4],ax
    mov ax,[bp-34]
    mov es:[bx+6],ax

find1_0097:
    mov dx,[bp-42]
    mov ax,[bp-44]
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-30]

org 39
    db 09ah
    dd @string@find_index$xqnxcuimui

    add sp,14
    mov dx,ax
    cmp dx,-1
    jnz find1_003a
    xor ax,ax
    jmp short find1_003d

find1_003a:
    mov ax,[bp-32]

find1_003d:
    mov [bp-34],ax
    mov [bp-36],dx
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-38],dx
    mov [bp-40],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-42],dx
    mov [bp-44],ax
    or ax,[bp-42]
    jz find1_0065
    mov ax,[bp-44]
    jmp short find1_0075

find1_0065:
    mov ax,8
    push ax

org 14
    call ___InitExceptBlocks
    push ss
    lea ax,[bp-32]
    push ax
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]

org 11
    mov bx,offset _TEXT:find_cleanup_state_9

org 8
    mov ax,seg _TEXT

org 0

@string@substring$qnxcui:
    push bp
    mov bp,sp
    sub sp,44
    push si
    push di

; Actual original Borland _TEXTC LEDATA 1024..1295 source/relocation block order.

org 1268
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0,0
    dw 0,0,0,0,0,0

org 1212
    call F_LMOD@
    mov [bp-10],dx
    mov [bp-12],ax
    inc word ptr [bp-16]
    jmp near ptr find1_0405

find1_04cd:
    mov ax,65535

find1_04d0:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

find_rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

org 1186
    call F_LXLSH@
    les bx,[bp-16]
    add bx,[bp-4]
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

org 1159
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

org 1134
    call F_LXMUL@
    mov bx,[bp-10]
    mov cx,[bp-12]
    add cx,64288
    adc bx,16383
    sub cx,ax
    sbb bx,dx
    push bx
    push cx

org 1067
    call _strncmp
    add sp,10
    or ax,ax
    jnz find1_044c

find1_0437:
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,[bp-16]
    xor dx,dx
    sub ax,es:[bx+2]
    sbb dx,0
    jmp near ptr find1_04d0

find1_044c:
    mov ax,[bp-16]
    cmp ax,[bp-30]
    jnc find1_04cd
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

org 1045
    cmp word ptr DGROUP:@string@paranoid_check,0
    jz find1_0437
    push word ptr [bp-4]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-14]
    push word ptr [bp-16]

org 1026
    mov [bp-30],ax

find1_0405:
    mov dx,[bp-10]
    mov ax,[bp-12]
    cmp dx,[bp-6]
    jnz find1_044c
    cmp ax,[bp-8]
    jnz find1_044c

_TEXTC ends
end
