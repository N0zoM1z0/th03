; Original Japanese Borland xalloc: complete ctor, typed exception raise,
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
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @xalloc@$bctr$qmx6stringui,@xalloc@raise$qv


; Real compiler metadata + instruction blocks emitted in descending
; original offset to reproduce ordered native DOS relocation entries.

org 457
; Full Borland base-class xmsg descriptor, imported destructor pointer.
rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0
    dw 0,0,0,0,0,0

org 380
xalloc_destruct_xmsg:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz xalloc_01c3
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz xalloc_01c1
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short xalloc_01c5

xalloc_01c1:
    jmp short xalloc_01c5

xalloc_01c3:
    xor ax,ax

xalloc_01c5:
    pop di
    pop si
    pop bp
    retf


org 348
    dw 5,62
    db 'xalloc',0
    db 0
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0


org 314
; Full Borland xalloc class RTTI including base class relation to xmsg.
rtti_xalloc:
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2
    dd xalloc_destruct_xmsg

org 247
; Non-exported original far copying helper called by raise.

xalloc_copy_xmsg:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    les bx,[bp+10]
    mov ax,es:[bx+4]
    les bx,[bp+6]
    mov es:[bx+4],ax
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


org 156
    mov ax,seg _TEXT
    push ax
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
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    les bx,[bp-40]
    mov ax,es:[bx+4]
    mov [bp-2],ax
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-6]
    push ss
    push ax
    push cs
    mov ax,offset _TEXT:rtti_xalloc
    push ax
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 127
@xalloc@raise$qv:
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:xalloc_exception_state
    call ___InitExceptBlocks
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

org 113
xalloc_exception_state:
    dd xalloc_exception_descriptor
    dw -36,0,5,0
    dw offset _TEXT:xalloc_exception_metadata


org 99
xalloc_exception_metadata:
    dd rtti_xalloc
    dw 4,-6,0,0,0

org 91
; The first two far descriptors both refer to the typed xalloc RTTI.
xalloc_exception_descriptor:
    dd rtti_xalloc
    dd 0

org 0
@xalloc@$bctr$qmx6stringui:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz xalloc_0021
    mov ax,6
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz xalloc_003f

xalloc_0021:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bctr$qmx6string
    add sp,8
    les bx,[bp+6]
    mov ax,[bp+14]
    mov es:[bx+4],ax

xalloc_003f:
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


_TEXT ends
end
