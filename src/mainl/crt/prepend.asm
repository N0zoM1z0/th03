; Full original Japanese Borland C++ prepend string method.
; Original far C++ exception cleanups, real 8086, typed xmsg/xalloc RTTI.
; Original CODE, public import ABI and literal original OMF relocation order.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strlen:far
extrn @xmsg@$bdtr$qv:far
extrn @string@clone$qv:far
extrn @TStringRef@splice$quiuinxcui:far
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

; BCC original ordered relocations at real instruction/data boundaries

org 160
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short prepend_branch_1_00ad

prepend_branch_1_00a9:
    jmp short prepend_branch_1_00ad

prepend_branch_1_00ab:
    xor ax,ax

prepend_branch_1_00ad:
    pop di
    pop si
    pop bp
    retf

org 140
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz prepend_branch_1_00a9
    push word ptr [bp+8]
    push word ptr [bp+6]

org 113
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 83
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short prepend_branch_1_0060

prepend_branch_1_005c:
    jmp short prepend_branch_1_0060

prepend_branch_1_005e:
    xor ax,ax

prepend_branch_1_0060:
    pop di
    pop si
    pop bp
    retf

prepend_cleanup_1:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz prepend_branch_1_00ab

org 63
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz prepend_branch_1_005c
    push word ptr [bp+8]
    push word ptr [bp+6]

org 36
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 17

prepend_exception_17:
    dd prepend_exception
    dw -30

prepend_cleanup_0:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz prepend_branch_1_005e

org 9
    dd prepend_rtti_lengtherror
    dw 0
    dw 0

org 5

prepend_exception:
    dd prepend_rtti_xalloc

org 0

prepend_unwind:
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
public @string@prepend$qnxcuiui

; BCC original ordered relocations at real instruction/data boundaries

org 365
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

org 315
    dd prepend_rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

prepend_rtti_xmsg:
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

org 299
    dd prepend_cleanup_1
    dw 5
    dw 62
    db 'xalloc',0,0

org 249
    dd prepend_rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

prepend_rtti_xalloc:
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

org 221
    dd prepend_cleanup_0
    dw 5
    dw 74
    db 'string::lengtherror',0

org 178
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

prepend_rtti_lengtherror:
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

org 159
    call @TStringRef@splice$quiuinxcui
    add sp,14

prepend_branch_4_00a7:
    mov dx,[bp+8]
    mov ax,[bp+6]
    push dx
    push ax
    push word ptr [bp-30]

org 63
    call _strlen
    pop cx
    pop cx
    mov [bp-32],ax
    mov ax,[bp+14]
    cmp ax,[bp-32]
    jnc prepend_branch_4_0058
    mov dx,ss
    lea ax,[bp+14]
    jmp short prepend_branch_4_005d

prepend_branch_4_0058:
    mov dx,ss
    lea ax,[bp-32]

prepend_branch_4_005d:
    mov bx,ax
    mov es,dx
    mov cx,es:[bx]
    mov ax,[bp-32]
    sub ax,cx
    mov [bp-36],ax
    cmp ax,[bp+16]
    jnc prepend_branch_4_0078
    mov dx,ss
    lea ax,[bp-36]
    jmp short prepend_branch_4_007d

prepend_branch_4_0078:
    mov dx,ss
    lea ax,[bp+16]

prepend_branch_4_007d:
    mov bx,ax
    mov es,dx
    mov ax,es:[bx]
    mov [bp-34],ax
    push ax
    mov ax,[bp+10]
    add ax,cx
    push word ptr [bp+12]
    push ax
    xor ax,ax
    push ax
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 48
    call @string@clone$qv
    pop cx
    pop cx
    jmp short prepend_branch_4_0039

prepend_branch_4_0039:
    push word ptr [bp+12]
    push word ptr [bp+10]

org 14
    call ___InitExceptBlocks
    mov ax,[bp+10]
    or ax,[bp+12]
    jnz prepend_branch_4_001e
    jmp near ptr prepend_branch_4_00a7

prepend_branch_4_001e:
    les bx,[bp+6]
    les bx,es:[bx]
    cmp word ptr es:[bx],1
    jna prepend_branch_4_0039
    push word ptr [bp+8]
    push word ptr [bp+6]

org 11
    mov bx,offset _TEXT:prepend_exception_17

org 8
    mov ax,seg _TEXT

org 0

@string@prepend$qnxcuiui:
    push bp
    mov bp,sp
    sub sp,36
    push si
    push di

_TEXTC ends
end
