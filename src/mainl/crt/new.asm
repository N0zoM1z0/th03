; Complete original Japanese Borland C++ operator new and handler runtime.
; Far new handler, set_new_handler, operator new, throw/copy helpers,
; typed RTTI, sparse original DATA and native INIT/EXIT list entries.
; Real symbolic 8086 instructions, not a target-code byte array.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _malloc:far
extrn @xmsg@$bctr$qmx4xmsg:far
extrn @xmsg@$bdtr$qv:far
extrn @xalloc@$bctr$qmx6stringui:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
_EXIT_ segment word public 'EXITDATA'
_EXIT_ ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @xnew_handler$qv,@set_new_handler$qnqv$v,@$bnew$qui


; One original CODE LEDATA; genuine source fields are emitted
; by descending original offset, matching BCC FIXUPP/MZ chronology.

org 728
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0,0
    dw 0,0,0,0,0,0

org 681
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short new_02b6

new_02b2:
    jmp short new_02b6

new_02b4:
    xor ax,ax

new_02b6:
    pop di
    pop si
    pop bp
    retf

rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1

org 661
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz new_02b2
    push word ptr [bp+8]
    push word ptr [bp+6]

org 634
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 601
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0

new_delete_xalloc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz new_02b4

org 585
    dd new_delete_xalloc
    dw 5,62
    db 'xalloc',0,0

org 527
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0,0
    dw 0,0,0,0,0,0

rtti_xalloc:
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2

org 486
    call @xmsg@$bdtr$qv
    add sp,6
    pop di
    pop si
    retf

rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

org 482
    mov ax,offset DGROUP:___xalloc
    push ax

org 460
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push ds

org 447
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

new_static_exit:
    push si
    push di

org 436
    call @string@$bdtr$qv
    add sp,16
    push word ptr [bp-34]

org 422
    call @xalloc@$bctr$qmx6stringui
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 418
    mov ax,offset DGROUP:___xalloc
    push ax

org 404
    call @string@$bctr$qnxc
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax
    push ds

org 395
    mov ax,offset DGROUP:new_out_of_memory
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 381
    call ___InitExceptBlocks
    mov word ptr [bp-22],6
    xor ax,ax
    push ax
    push ds

org 378
    mov bx,offset _TEXT:new_exception_state

org 375
    mov ax,seg _TEXT

org 365
    dw offset _TEXT:new_exception_catch_block

new_static_init:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 339
    dd rtti_string
    dw 4,-4,0,0,0

new_exception_state:
    dw 0,0,-34,0,5,0

org 335
    dd DGROUP:___xalloc

org 329

new_exception_catch_block:
    dd rtti_xalloc
    dw 0

org 301
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

org 279
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    les bx,[bp+10]
    mov ax,es:[bx+4]
    les bx,[bp+6]
    mov es:[bx+4],ax

org 244
    or ax,word ptr DGROUP:__new_handler+2
    jnz new_00da

new_00fa:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

new_copy_xmsg:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 241
    mov ax,word ptr DGROUP:__new_handler

org 225
    call _malloc
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jnz new_00fa

org 218

new_00da:
    call dword ptr DGROUP:__new_handler

new_00de:
    push word ptr [bp+6]

org 166
    mov word ptr DGROUP:__new_handler,ax
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@$bnew$qui:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov word ptr [bp-2],0
    mov word ptr [bp-4],0
    cmp word ptr [bp+6],0
    jz new_00d2
    mov ax,[bp+6]
    jmp short new_00d5

new_00d2:
    mov ax,1

new_00d5:
    mov [bp+6],ax
    jmp short new_00de

org 162
    mov word ptr DGROUP:__new_handler+2,dx

org 147
    mov ax,word ptr DGROUP:__new_handler
    mov [bp-2],dx
    mov [bp-4],ax
    mov dx,[bp+8]
    mov ax,[bp+6]

org 143
    mov dx,word ptr DGROUP:__new_handler+2

org 121
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@set_new_handler$qnqv$v:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di

org 117
    mov ax,offset _TEXT:rtti_xalloc
    push ax

org 93
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-6]
    push ss
    push ax
    push cs

org 87
    mov ax,DGROUP:___xalloc+4
    mov [bp-2],ax

org 79
    call @xmsg@$bctr$qmx4xmsg
    add sp,8

org 70
    mov ax,offset DGROUP:___xalloc
    push ax
    push ss
    lea ax,[bp-6]
    push ax

org 61
    mov ax,offset _TEXT:new_copy_xmsg
    push ax
    xor ax,ax
    push ax
    push ax
    push ds

org 57
    mov ax,seg _TEXT
    push ax

org 42
    call ___InitExceptBlocks
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

org 39
    mov bx,offset _TEXT:new_xalloc_state

org 36
    mov ax,seg _TEXT

org 26
    dw offset _TEXT:new_xalloc_exception_metadata

@xnew_handler$qv:
    push bp
    mov bp,sp
    sub sp,36
    push si
    push di

org 0

new_xalloc_exception_metadata:
    dd rtti_xalloc
    dw 4,-6,0,0,0

new_xalloc_state:
    dw 0,0,-36,0,5,0

_TEXT ends

_DATA segment word public 'DATA'
public ___xalloc,__new_handler
; Exactly six original uninitialized DATA bytes, not filler or initialized
; CODE or a fake BSS segment.
___xalloc dw 3 dup(?)
__new_handler dd @xnew_handler$qv
new_out_of_memory db 'Out of memory',0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
; Both original INIT/EXIT retain priority 2001h and real far CODE references.
_INIT_ segment word public 'INITDATA'
    dw 2001h
    dd new_static_init
_INIT_ ends
_EXIT_ segment word public 'EXITDATA'
    dw 2001h
    dd new_static_exit
_EXIT_ ends
end
