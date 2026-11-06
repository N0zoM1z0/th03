; Shared C++ runtime: complete original storage, ABI and literal ordered fields.
; raise and copy-assignment with complete exception-frame records and RTTI.
; Original Japanese MAINL CL.LIB CRT member 337, _TEXT 955 bytes.
; CODE pointers below are symbolic 16:16 OMF relocations, not raw CODE arrays.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@$bctr$qmx6string:far
extrn @string@$bdtr$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @xmsg@$bctr$qmx6string,@xmsg@$bctr$qmx4xmsg
public @xmsg@$bdtr$qv,@xmsg@raise$qv,@xmsg@$basg$qmx4xmsg



; Prebind real instruction, frame and RTTI labels before ordinary span emission.
; Every initialized byte is emitted once; metadata pointers remain symbolic.
org 897
rtti_string label near
org 878
rtti_string_pointer label near
org 822
rtti_xmsg label near
org 782
branch_030e label near
org 798
branch_031e label near
org 672
branch_02a0 label near
org 637
@xmsg@$basg$qmx4xmsg label near
org 601
xmsg_assign_frame label near
org 615
xmsg_assign_state label near
org 518
@xmsg@raise$qv label near
org 512
xmsg_raise_scope label near
org 504
xmsg_raise_frame label near
org 500
branch_01f4 label near
org 410
@xmsg@$bdtr$qv label near
org 356
branch_0164 label near
org 372
branch_0174 label near
org 286
branch_011e label near
org 239
@xmsg@$bctr$qmx4xmsg label near
org 203
xmsg_copy_frame label near
org 217
xmsg_copy_state label near
org 149
branch_0095 label near
org 165
branch_00a5 label near
org 83
branch_0053 label near
org 36
@xmsg@$bctr$qmx6string label near
org 0
xmsg_ctor_frame label near
org 14
xmsg_ctor_state label near

; Original CODE 927..954.
org 927
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0
    db 0 ; one alignment byte of the class name
    dw 0,0,0,0,0,0

; Original CODE 884..926.
org 884
    dd rtti_string
    db 'string *',0
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

; Original CODE 852..883.
org 852
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0 ; one alignment byte of the class name
    dw 0,0,0,0,0,0
    dw 4,2010h,10

; Original CODE 809..851.
org 809
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1

; Original CODE 759..808.
org 759
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-34]

; Original CODE 751..758.
org 751
    call @string@$bctr$qmx6string
    add sp,8

; Original CODE 716..750.
org 716
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_030e
    mov word ptr [bp-22],14
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push dx
    push word ptr [bp-4]

; Original CODE 704..715.
org 704
    call @string@$bdtr$qv
    add sp,6
    mov ax,4
    push ax

; Original CODE 672..703.
org 672
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

; Original CODE 651..671.
org 651
    call ___InitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    cmp dx,[bp+12]
    jnz branch_02a0
    cmp ax,[bp+10]
    jz branch_031e

; Original CODE 648..650.
org 648
    mov bx,offset _TEXT:xmsg_assign_state

; Original CODE 645..647.
org 645
    mov ax,seg _TEXT

; Original CODE 635..644.
org 635
    dw offset _TEXT:xmsg_assign_frame
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

; Original CODE 601..634.
org 601
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
    dw 0,0
    dw -34,0,5,0,-1,6,5,0

; Original CODE 587..600.
org 587
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original CODE 583..586.
org 583
    mov ax,offset _TEXT:rtti_xmsg
    push ax

; Original CODE 551..582.
org 551
    mov ax,offset _TEXT:@xmsg@$bctr$qmx4xmsg
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax,[bp-34]
    push ax
    push cs
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    lea ax,[bp-34]
    push ss
    push ax
    push cs

; Original CODE 547..550.
org 547
    mov ax,seg _TEXT
    push ax

; Original CODE 532..546.
org 532
    call ___InitExceptBlocks
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

; Original CODE 529..531.
org 529
    mov bx,offset _TEXT:xmsg_raise_scope

; Original CODE 526..528.
org 526
    mov ax,seg _TEXT

; Original CODE 512..525.
org 512
    dd xmsg_raise_frame
    dw -30
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

; Original CODE 504..511.
org 504
    dd rtti_xmsg
    dd 0

; Original CODE 493..503.
org 493
    call @$bdele$qnv
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

; Original CODE 473..492.
org 473
    call @string@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz branch_01f4
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 441..472.
org 441
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

; Original CODE 415..440.
org 415
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov ax,[bp+6]
    or ax,[bp+8]
    jz branch_01f4

; Original CODE 393..414.
org 393
    call ___ExitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
    push bp
    mov bp,sp
    push si
    push di

; Original CODE 372..392.
org 372
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    push word ptr [bp-34]

; Original CODE 333..371.
org 333
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

; Original CODE 325..332.
org 325
    call @string@$bctr$qmx6string
    add sp,8

; Original CODE 290..324.
org 290
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_0164
    mov word ptr [bp-22],14
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push dx
    push word ptr [bp-4]

; Original CODE 270..289.
org 270
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_0174
    mov ax,4
    push ax

; Original CODE 253..269.
org 253
    call ___InitExceptBlocks
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_011e
    mov ax,4
    push ax

; Original CODE 250..252.
org 250
    mov bx,offset _TEXT:xmsg_copy_state

; Original CODE 247..249.
org 247
    mov ax,seg _TEXT

; Original CODE 237..246.
org 237
    dw offset _TEXT:xmsg_copy_frame
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

; Original CODE 203..236.
org 203
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
    dw 0,0
    dw -34,0,5,0,-1,6,5,0

; Original CODE 186..202.
org 186
    call ___ExitExceptBlocks
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original CODE 165..185.
org 165
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    push word ptr [bp-34]

; Original CODE 126..164.
org 126
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax

; Original CODE 118..125.
org 118
    call @string@$bctr$qmx6string
    add sp,8

; Original CODE 87..117.
org 87
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz branch_0095
    mov word ptr [bp-22],14
    push word ptr [bp+12]
    push word ptr [bp+10]
    push dx
    push word ptr [bp-4]

; Original CODE 67..86.
org 67
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_00a5
    mov ax,4
    push ax

; Original CODE 50..66.
org 50
    call ___InitExceptBlocks
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_0053
    mov ax,4
    push ax

; Original CODE 47..49.
org 47
    mov bx,offset _TEXT:xmsg_ctor_state

; Original CODE 44..46.
org 44
    mov ax,seg _TEXT

; Original CODE 34..43.
org 34
    dw offset _TEXT:xmsg_ctor_frame
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

; Original CODE 0..33.
org 0
    dd rtti_string_pointer
    dw 2087h,-4
    dw 0,0,0
    dw 0,0
    dw -34,0,5,0,-1,6,5,0
_TEXT ends
end
