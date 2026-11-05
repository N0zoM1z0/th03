; Complete original Borland C++ TCharMask, string::hash and hash_case.
; Original far exception metadata, uninitialized BSS mask and true static
; initializer pointer, plus typed string RTTI and real 8086 methods.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@$bdtr$qv:far
extrn @string@case_sensitive:word
extrn @to_upper$qmx6string:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Original _TEXT descending FIXUPP source-statement order.

org 39
    push ax
    db 09ah
    dd @TCharMask@$bctr$qv
    pop cx
    pop cx
    pop di
    pop si
    retf

org 36
    mov ax,offset DGROUP:hash_mask

org 31
    dw offset _TEXT:hash_exception_frame

hash_static_initializer:
    push si
    push di
    push ds

org 5
hash_exception_frame:
    dd hash_string_rtti
    dw 4
    dw -4
    dw 0
    dw 0
    dw 0

hash_exception_state:
    dw 0
    dw 0
    dw -34
    dw 0
    dw 5
    dw 0

org 0
hash_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf

_TEXT ends

_DATA segment word public 'DATA'
_DATA ends

_BSS segment word public 'BSS'
; Genuine process-global 4-byte BSS character mask, uninitialized.
hash_mask dw 2 dup(?)
_BSS ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @TCharMask@$bctr$qv
public @string@hash$xqv
public @string@hash_case$xqv

; Original _TEXTC descending FIXUPP source-statement order.

org 343
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0,0
    dw 0,0,0,0,0,0

org 293
    mov ax,DGROUP:hash_mask[bx]
    les bx,[bp-6]
    and ax,es:[bx]
    xor cx,ax

hash_branch_0131:
    mov ax,cx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

hash_string_rtti:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1

org 195
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@hash_case$xqv:
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    mov cx,es:[bx+6]
    mov ax,cx
    shr ax,1
    mov [bp-2],ax
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    mov [bp-4],dx
    mov [bp-6],ax
    jmp short hash_branch_0102

hash_branch_00f8:
    les bx,[bp-6]
    xor cx,es:[bx]
    add word ptr [bp-6],2

hash_branch_0102:
    mov ax,[bp-2]
    dec word ptr [bp-2]
    or ax,ax
    jnz hash_branch_00f8
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    and ax,1
    mov [bp-2],ax
    or ax,ax
    jz hash_branch_0131
    mov bx,[bp-2]
    add bx,bx

org 184
    call @string@$bdtr$qv
    add sp,6

hash_branch_00c0:
    push word ptr [bp-34]

org 167
    db 09ah
    dd @string@hash_case$xqv
    pop cx
    pop cx
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax

org 154
    call @to_upper$qmx6string
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax

org 128
    db 09ah
    dd @string@hash_case$xqv
    pop cx
    pop cx
    push ax
    jmp short hash_branch_00c0

hash_branch_008a:
    mov word ptr [bp-22],6
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax,[bp-4]
    push ax

org 115
    cmp word ptr DGROUP:@string@case_sensitive,0
    jz hash_branch_008a
    push word ptr [bp+8]
    push word ptr [bp+6]

org 110
    call ___InitExceptBlocks

org 107
    mov bx,offset _TEXT:hash_exception_state

org 104
    mov ax,seg _TEXT

org 20
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz hash_branch_0054

hash_branch_0024:
    xor cx,cx

hash_branch_0026:
    mov word ptr [bp-2],0

hash_branch_002b:
    cmp [bp-2],cx
    jnc hash_branch_0034
    mov al,255
    jmp short hash_branch_0036

hash_branch_0034:
    mov al,0

hash_branch_0036:
    mov dx,cx
    add dx,dx
    add dx,[bp-2]
    les bx,[bp+6]
    add bx,dx
    mov es:[bx],al
    inc word ptr [bp-2]
    cmp word ptr [bp-2],2
    jc hash_branch_002b
    inc cx
    cmp cx,2
    jc hash_branch_0026

hash_branch_0054:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@hash$xqv:
    push bp
    mov bp,sp
    sub sp,34
    push si
    push di

org 0

@TCharMask@$bctr$qv:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz hash_branch_0024
    mov ax,4
    push ax

_TEXTC ends

_INIT_ segment word public 'INITDATA'
    dw 2001h
    dd hash_static_initializer
_INIT_ ends
end
