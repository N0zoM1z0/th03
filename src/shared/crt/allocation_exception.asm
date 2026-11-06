; Shared C++ runtime: complete original storage, ABI and literal ordered fields.
; xmsg copy and destruction/unwind, full xalloc/xmsg RTTI and frame metadata.
; Real 8086 instructions and symbolic 16:16 relocations, no target CODE blob.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn @xmsg@$bctr$qmx6string:far
extrn @xmsg@$bctr$qmx4xmsg:far
extrn @xmsg@$bdtr$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @xalloc@$bctr$qmx6stringui,@xalloc@raise$qv


; Real compiler metadata + instruction blocks emitted in descending
; original offset to reproduce ordered native DOS relocation entries.

; Prebind real instruction, frame and RTTI labels before ordinary span emission.
; Every initialized byte is emitted once; metadata pointers remain symbolic.
org 457
rtti_xmsg label near
org 380
xalloc_destruct_xmsg label near
org 449
xalloc_01c1 label near
org 451
xalloc_01c3 label near
org 453
xalloc_01c5 label near
org 314
rtti_xalloc label near
org 247
xalloc_copy_xmsg label near
org 127
@xalloc@raise$qv label near
org 113
xalloc_exception_state label near
org 99
xalloc_exception_metadata label near
org 91
xalloc_exception_descriptor label near
org 0
@xalloc@$bctr$qmx6stringui label near
org 33
xalloc_0021 label near
org 63
xalloc_003f label near

; Original CODE 487..512.
org 487
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0
    dw 0,0,0,0,0,0

; Original CODE 440..486.
org 440
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short xalloc_01c5
    jmp short xalloc_01c5
    xor ax,ax
    pop di
    pop si
    pop bp
    retf
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1

; Original CODE 420..439.
org 420
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz xalloc_01c1
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 393..419.
org 393
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 360..392.
org 360
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz xalloc_01c3

; Original CODE 344..359.
org 344
    dd xalloc_destruct_xmsg
    dw 5,62
    db 'xalloc',0
    db 0

; Original CODE 286..343.
org 286
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
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2

; Original CODE 264..285.
org 264
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    les bx,[bp+10]
    mov ax,es:[bx+4]
    les bx,[bp+6]
    mov es:[bx+4],ax

; Original CODE 233..263.
org 233
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 229..232.
org 229
    mov ax,offset _TEXT:rtti_xalloc
    push ax

; Original CODE 205..228.
org 205
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-6]
    push ss
    push ax
    push cs

; Original CODE 187..204.
org 187
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    les bx,[bp-40]
    mov ax,es:[bx+4]
    mov [bp-2],ax

; Original CODE 160..186.
org 160
    mov ax,offset _TEXT:xalloc_copy_xmsg
    push ax
    xor ax,ax
    push ax
    push ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-38],dx
    mov [bp-40],ax
    push dx
    push ax
    push ss
    lea ax,[bp-6]
    push ax

; Original CODE 156..159.
org 156
    mov ax,seg _TEXT
    push ax

; Original CODE 141..155.
org 141
    call ___InitExceptBlocks
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

; Original CODE 138..140.
org 138
    mov bx,offset _TEXT:xalloc_exception_state

; Original CODE 135..137.
org 135
    mov ax,seg _TEXT

; Original CODE 125..134.
org 125
    dw offset _TEXT:xalloc_exception_metadata
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di

; Original CODE 113..124.
org 113
    dd xalloc_exception_descriptor
    dw -36,0,5,0

; Original CODE 99..112.
org 99
    dd rtti_xalloc
    dw 4,-6,0,0,0

; Original CODE 91..98.
org 91
    dd rtti_xalloc
    dd 0

; Original CODE 63..90.
org 63
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

; Original CODE 45..62.
org 45
    call @xmsg@$bctr$qmx6string
    add sp,8
    les bx,[bp+6]
    mov ax,[bp+14]
    mov es:[bx+4],ax

; Original CODE 17..44.
org 17
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz xalloc_003f
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 0..16.
org 0
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz xalloc_0021
    mov ax,6
    push ax
_TEXT ends
end
